import discord
import traceback
import os

from discord.ext import commands
from discord import app_commands, Colour
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

class YesOrNo(discord.ui.View):
    def __init__(self, *, timeout = 180, bot: commands.Bot, user: discord.Member):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.user = user
        self.value = None
        self.method = None

    @discord.ui.button(label="Yes, Delete Recent Messages", style=discord.ButtonStyle.green, emoji="👍", row=0)
    async def recent(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.method = "Recent"
            self.stop()
    
    @discord.ui.button(label="Yes, Delete All Messages", style=discord.ButtonStyle.blurple, emoji="👍", row=0)
    async def all(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.method = "All"
            self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.red, emoji="👎", row=0)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = False
            self.stop()

class ChannelSelect(discord.ui.ChannelSelect):
    def __init__(self, *, user: discord.Member):
        super().__init__(
            channel_types=[discord.ChannelType.text],
            placeholder="Select up to 25 channels...",
            min_values=1,
            max_values=25,
            row=0
        )
        self.user = user
        self.channels = []

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.channels = list(self.values)

class ChannelSelectView(discord.ui.View):
    def __init__(self, *, timeout=180.0, bot: commands.Bot, user: discord.Member):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.user = user
        self.value = None
        self.channels = None
        self.select = ChannelSelect(user=self.user)
        self.add_item(self.select)

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green, row=1)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.channels = self.select.channels
            self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red, row=1)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = False
            self.stop()

# Group cog for all purge commands
class Purge(commands.GroupCog, group_name="purge"):
    """Group cog containing the bot's purge commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    async def purge_channel(channel: discord.TextChannel, *, recent_only: bool = False) -> int:
        """
        Delete unpinned messages from a text channel.

        If recent_only is True, only messages from the last two weeks are removed.
        Otherwise, the method continues until all unpinned messages are removed.

        Discord only permits bulk deletion for messages younger than 14 days.
        Older messages are therefore deleted individually.
        """
        deleted_total = 0

        cutoff = None
        if recent_only:
            cutoff = datetime.now(tz=timezone.utc) - timedelta(weeks=2)

        while True:
            messages = []

            async for message in channel.history(limit=100, oldest_first=False):
                if message.pinned:
                    continue

                if cutoff is not None and message.created_at < cutoff:
                    # History is newest-first, so once we reach the cutoff,
                    # there are no newer eligible messages left to inspect.
                    break

                messages.append(message)

            if not messages:
                break

            # Bulk deletion is only valid for messages younger than 14 days.
            now = datetime.now(tz=timezone.utc)
            bulk_messages = [
                message for message in messages
                if (now - message.created_at).total_seconds() < 14 * 24 * 60 * 60
            ]
            old_messages = [
                message for message in messages
                if message not in bulk_messages
            ]

            if bulk_messages:
                await channel.delete_messages(bulk_messages)
                deleted_total += len(bulk_messages)

            for message in old_messages:
                try:
                    await message.delete()
                    deleted_total += 1
                except discord.NotFound:
                    # The message was already deleted; don't fail the entire purge.
                    pass

            # For a recent-only purge, once we have reached the cutoff the next
            # history scan will return no eligible messages.
            if recent_only and cutoff is not None:
                # Continue scanning in case the batch contained pinned/old
                # messages mixed with eligible messages.
                continue

        return deleted_total

    @staticmethod
    async def safe_edit_response(response, embed):
        """Edit an interaction response, falling back to fetching it if needed."""
        try:
            await response.edit(embed=embed, view=None)
        except (discord.NotFound, discord.HTTPException):
            # Webhook messages can occasionally become stale.
            if isinstance(response, discord.WebhookMessage):
                try:
                    fetched_response = await response.channel.fetch_message(response.id)
                    await fetched_response.edit(embed=embed, view=None)
                except (discord.NotFound, discord.HTTPException):
                    pass

    @staticmethod
    async def finish_response(response):
        """Delete the progress/confirmation response after completion."""
        try:
            await response.delete(delay=10.0)
        except (discord.NotFound, discord.HTTPException):
            pass

    async def run_purge(self, interaction, response, channels, user, method):
        """Run the common purge workflow for one or more channels."""
        wait = discord.Embed(
            color=Colour.blurple(),
            title="Purge in Progress",
            description=(
                "Please wait while the purge is in progress. "
                "This message will be edited when the purge is complete."
            )
        )
        wait.add_field(name="Currently Purging", value="None", inline=False)
        await self.safe_edit_response(response, wait)

        recent_only = method == "Recent"

        for channel in channels:
            wait.set_field_at(
                index=0,
                name="Currently Purging",
                value=f"{channel.mention}",
                inline=False
            )
            await self.safe_edit_response(response, wait)

            deleted = await self.purge_channel(
                channel,
                recent_only=recent_only
            )

            purged_message = discord.Embed(
                color=Colour.blurple(),
                title="Messages Purged",
                description=(
                    f"{user.mention} has just purged {deleted} messages "
                    f"from {channel.mention} using the purge command!"
                )
            )
            await channel.send(embed=purged_message, delete_after=300.0)

        success = discord.Embed(
            color=Colour.green(),
            title="Success",
            description="The purge is now complete!"
        )
        await self.safe_edit_response(response, success)
        await self.finish_response(response)

    @app_commands.command(name="here")
    @app_commands.checks.has_permissions(administrator=True)
    async def here(self, interaction: discord.Interaction):
        """(Admin Only) Purge all unpinned messages in the current channel."""
        response = None

        await interaction.response.defer()

        try:
            user = interaction.user
            channel = interaction.channel

            if not isinstance(channel, discord.TextChannel):
                raise RuntimeError("This command can only be used in a text channel.")

            yesorno = YesOrNo(bot=self.bot, user=user)

            embed = discord.Embed(
                color=Colour.blurple(),
                title="Confirm Purge",
                description=(
                    "Are you **sure** you want to purge all unpinned messages "
                    "in the current channel?"
                )
            )
            embed.add_field(
                name="Delete Recent Messages",
                value="This option will delete all messages posted within the last 2 weeks.",
                inline=False
            )
            embed.add_field(
                name="Delete All Messages",
                value="This option will delete all unpinned messages, including messages older than 2 weeks.",
                inline=False
            )
            embed.add_field(
                name="No",
                value="Cancels the interaction.",
                inline=False
            )

            response = await interaction.followup.send(
                embed=embed,
                view=yesorno,
                wait=True
            )
            await response.pin()
            await yesorno.wait()

            if yesorno.value is True:
                await self.run_purge(
                    interaction,
                    response,
                    [channel],
                    user,
                    yesorno.method
                )
            elif yesorno.value is False:
                cancelled = discord.Embed(
                    color=Colour.red(),
                    title="Cancelled",
                    description="This interaction has been cancelled. No messages have been purged."
                )
                await self.safe_edit_response(response, cancelled)
                await self.finish_response(response)
            else:
                timed_out = discord.Embed(
                    color=Colour.yellow(),
                    title="Timed Out",
                    description="This interaction has timed out. No messages have been purged."
                )
                await self.safe_edit_response(response, timed_out)
                await self.finish_response(response)

        except Exception as e:
            print(traceback.format_exc())

            if response is not None:
                try:
                    await response.delete()
                except (discord.NotFound, discord.HTTPException):
                    pass

            error = discord.Embed(
                color=Colour.red(),
                title="Error",
                description=f"{e}"
            )
            await interaction.channel.send(embed=error, delete_after=10.0)

    @app_commands.command(name="channels")
    @app_commands.checks.has_permissions(administrator=True)
    async def channels(self, interaction: discord.Interaction):
        """(Admin Only) Purge all unpinned messages in a set list of up to 25 channels."""
        response = None

        await interaction.response.defer()

        try:
            user = interaction.user

            csv = ChannelSelectView(bot=self.bot, user=user)

            embed = discord.Embed(
                color=Colour.blurple(),
                title="Purge Channels",
                description="Which channel(s) would you like to purge all unpinned messages from?"
            )

            response = await interaction.followup.send(
                embed=embed,
                view=csv,
                wait=True
            )
            await response.pin()
            await csv.wait()

            if csv.value is True:
                selected_channels = [
                    c for c in csv.channels
                    if isinstance(c, discord.TextChannel)
                ]

                if not selected_channels:
                    raise RuntimeError("No valid text channels were selected.")

                channels_str = ", ".join(c.mention for c in selected_channels)

                yon = YesOrNo(bot=self.bot, user=user)

                embed = discord.Embed(
                    color=Colour.blurple(),
                    title="Confirm Purge",
                    description=(
                        "Please review the list of selected channels below and confirm "
                        "that you would like to continue with the purge of all unpinned "
                        f"messages from the following channels:\n\n{channels_str}"
                    )
                )
                embed.add_field(
                    name="Delete Recent Messages",
                    value="This option will delete all messages posted within the last 2 weeks.",
                    inline=False
                )
                embed.add_field(
                    name="Delete All Messages",
                    value="This option will delete all unpinned messages, including messages older than 2 weeks.",
                    inline=False
                )
                embed.add_field(
                    name="No",
                    value="Cancels the interaction.",
                    inline=False
                )

                await response.edit(embed=embed, view=yon)
                await yon.wait()

                if yon.value is True:
                    await self.run_purge(
                        interaction,
                        response,
                        selected_channels,
                        user,
                        yon.method
                    )
                elif yon.value is False:
                    cancelled = discord.Embed(
                        color=Colour.red(),
                        title="Cancelled",
                        description="This interaction has been cancelled. No messages have been purged."
                    )
                    await self.safe_edit_response(response, cancelled)
                    await self.finish_response(response)
                else:
                    timed_out = discord.Embed(
                        color=Colour.yellow(),
                        title="Timed Out",
                        description="This interaction has timed out. No messages have been purged."
                    )
                    await self.safe_edit_response(response, timed_out)
                    await self.finish_response(response)

            elif csv.value is False:
                cancelled = discord.Embed(
                    color=Colour.red(),
                    title="Cancelled",
                    description="This interaction has been cancelled. No messages have been purged."
                )
                await self.safe_edit_response(response, cancelled)
                await self.finish_response(response)

            else:
                timed_out = discord.Embed(
                    color=Colour.yellow(),
                    title="Timed Out",
                    description="This interaction has timed out. No messages have been purged."
                )
                await self.safe_edit_response(response, timed_out)
                await self.finish_response(response)

        except Exception as e:
            print(traceback.format_exc())

            if response is not None:
                try:
                    await response.delete()
                except (discord.NotFound, discord.HTTPException):
                    pass

            error = discord.Embed(
                color=Colour.red(),
                title="Error",
                description=f"{e}"
            )
            await interaction.channel.send(embed=error, delete_after=10.0)

    @app_commands.command(name="server")
    @app_commands.checks.has_permissions(administrator=True)
    async def server(self, interaction: discord.Interaction):
        """(Admin Only) Purges all unpinned messages in a server, excluding up to 25 channels."""
        response = None

        await interaction.response.defer()

        try:
            user = interaction.user
            guild = interaction.guild

            if guild is None or not isinstance(user, discord.Member):
                raise RuntimeError("This command can only be used inside a server.")

            csv = ChannelSelectView(bot=self.bot, user=user)

            embed = discord.Embed(
                color=Colour.blurple(),
                title="Purge Server",
                description=(
                    "Which channel(s) would you like to **exclude** from the purge "
                    "of all unpinned messages in the server?"
                )
            )

            response = await interaction.followup.send(
                embed=embed,
                view=csv,
                wait=True
            )
            await response.pin()
            await csv.wait()

            if csv.value is True:
                excluded_channels = {
                    c.id
                    for c in csv.channels
                    if isinstance(c, discord.TextChannel)
                }

                all_channels = [
                    c for c in guild.text_channels
                    if c.id not in excluded_channels
                ]

                if not all_channels:
                    raise RuntimeError("There are no text channels available to purge.")

                excluded_str = ", ".join(
                    c.mention for c in csv.channels
                    if isinstance(c, discord.TextChannel)
                )
                if not excluded_str:
                    excluded_str = "None"

                yon = YesOrNo(bot=self.bot, user=user)

                embed = discord.Embed(
                    color=Colour.blurple(),
                    title="Confirm Purge",
                    description=(
                        "Please review the list of selected channels below and confirm "
                        "that you would like to continue with the purge of all unpinned "
                        "messages in the server **except** from the following channels:\n\n"
                        f"{excluded_str}"
                    )
                )
                embed.add_field(
                    name="Channels to Purge",
                    value=f"{len(all_channels)} text channel(s)",
                    inline=False
                )
                embed.add_field(
                    name="Delete Recent Messages",
                    value="This option will delete all messages posted within the last 2 weeks.",
                    inline=False
                )
                embed.add_field(
                    name="Delete All Messages",
                    value="This option will delete all unpinned messages, including messages older than 2 weeks.",
                    inline=False
                )
                embed.add_field(
                    name="No",
                    value="Cancels the interaction.",
                    inline=False
                )

                await response.edit(embed=embed, view=yon)
                await yon.wait()

                if yon.value is True:
                    await self.run_purge(
                        interaction,
                        response,
                        all_channels,
                        user,
                        yon.method
                    )
                elif yon.value is False:
                    cancelled = discord.Embed(
                        color=Colour.red(),
                        title="Cancelled",
                        description="This interaction has been cancelled. No messages have been purged."
                    )
                    await self.safe_edit_response(response, cancelled)
                    await self.finish_response(response)
                else:
                    timed_out = discord.Embed(
                        color=Colour.yellow(),
                        title="Timed Out",
                        description="This interaction has timed out. No messages have been purged."
                    )
                    await self.safe_edit_response(response, timed_out)
                    await self.finish_response(response)

            elif csv.value is False:
                cancelled = discord.Embed(
                    color=Colour.red(),
                    title="Cancelled",
                    description="This interaction has been cancelled. No messages have been purged."
                )
                await self.safe_edit_response(response, cancelled)
                await self.finish_response(response)

            else:
                timed_out = discord.Embed(
                    color=Colour.yellow(),
                    title="Timed Out",
                    description="This interaction has timed out. No messages have been purged."
                )
                await self.safe_edit_response(response, timed_out)
                await self.finish_response(response)

        except Exception as e:
            print(traceback.format_exc())

            if response is not None:
                try:
                    await response.delete()
                except (discord.NotFound, discord.HTTPException):
                    pass

            error = discord.Embed(
                color=Colour.red(),
                title="Error",
                description=f"{e}"
            )
            await interaction.channel.send(embed=error, delete_after=10.0)


class RainbowBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="rb!",
            description = "A Discord bot made by GitHub user gemhue.",
            intents = discord.Intents.default(),
            status = discord.Status.online
        )
    
    async def setup_hook(self):
        # Clear the global command tree
        try:
            self.tree.clear_commands(guild=None)
            print("Global Command Tree: Cleared")
        except Exception as e:
            print(f"There was an error clearing the global command tree: {e}")
            print(traceback.format_exc())
        # Add cog(s) to the bot
        try:
            purge_cog = self.get_cog("Purge")
            if purge_cog is None:
                await self.add_cog(Purge(self))
                print("Cog: Purge has been added.")
            else:
                print("Cog: Purge has been found.")
        except Exception as e:
            print(f"There was an error adding the cog(s): {e}")
            print(traceback.format_exc())
        # Sync the global command tree
        try:
            await self.tree.sync(guild=None)
            print("Global Command Tree: Synced")
        except Exception as e:
            print(f"There was an error syncing the global command tree: {e}")
            print(traceback.format_exc())

bot = RainbowBot()

@bot.event
async def on_ready(bot=bot):
    if bot.user is not None:
        print(f'Logged in as {bot.user}! (ID: {bot.user.id})')

load_dotenv()
token = os.getenv("token")
if token is not None:
    bot.run(token)
else:
    print("No token found! Check the .env file.")