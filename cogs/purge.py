import discord
import aiosqlite
import traceback
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timezone, timedelta

class YesOrNo(discord.ui.View):
    def __init__(self, *, timeout = 180, bot: commands.Bot, user: discord.Member):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.user = user
        self.value = None
        self.method = None

    @discord.ui.button(label="Yes (Delete Recent Messages)", style=discord.ButtonStyle.green, emoji="👍", row=0)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.method = "Recent"
            self.stop()
    
    @discord.ui.button(label="Yes (Delete All Messages)", style=discord.ButtonStyle.blurple, emoji="👍", row=0)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
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
    
    async def on_timeout(self):
        self.value = None
    
    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.defer(ephemeral=True)
        if interaction.user == self.user:
            self.value = False
            self.stop()

            embed = discord.Embed(
                color=self.bot.red,
                title="Error", description=f"{error}"
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            print(traceback.format_exc())

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
            self.channels = [c.resolve() for c in self.values]

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

    async def on_timeout(self):
        self.value = None
        self.stop()
    
    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.defer(ephemeral=True)
        if interaction.user == self.user:
            self.value = False
            self.stop()

            embed = discord.Embed(
                color=self.bot.red,
                title="Error", description=f"{error}"
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            print(traceback.format_exc())

# Group cog for all purge commands
class Purge(commands.GroupCog, group_name = "purge"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        if isinstance(bot.database, aiosqlite.Connection):
            self.db = bot.database

    # /purge here
    @app_commands.command(name="here")
    @app_commands.checks.has_permissions(administrator=True)
    async def here(self, interaction: discord.Interaction):
        """(Admin Only) Purge all unpinned messages in the current channel.
        """
        await interaction.response.defer()
        try:
            user = interaction.user
            guild = interaction.guild
            channel = interaction.channel

            yesorno = YesOrNo(bot=self.bot, user=user)
            embed = discord.Embed(
                color=self.bot.blurple,
                title="Confirm Purge",
                description="Are you **sure** you want to purge all unpinned messages in the current channel?"
            )
            embed.add_field(name="Delete Recent Messages", value="This option will delete all messages posted within the last 2 weeks.", inline=False)
            embed.add_field(name="Delete All Messages", value="This option will delete all messages (this can take a very long time).", inline=False)
            embed.add_field(name="No", value="Cancels the interaction.", inline=False)
            response = await interaction.followup.send(embed=embed, view=yesorno, wait=True)
            await response.pin()
            await yesorno.wait()

            if yesorno.value == True:

                wait = discord.Embed(
                    color=self.bot.blurple,
                    title="Purge in Progress",
                    description="Please wait while the purge is in progress. This message will be edited when the purge is complete."
                )
                wait.add_field(name="Currently Purging", value=f"{channel.mention}", inline=False)
                await response.edit(embed=wait, view=None)

                if yesorno.method == "Recent":
                    time = datetime.now(tz=timezone.utc) - timedelta(weeks=2.0)
                    deleted = await channel.purge(limit=1000, check=lambda m: m.pinned == False, after=time, oldest_first=True, bulk=True)
                elif yesorno.method == "All":
                    deleted = await channel.purge(limit=1000, check=lambda m: m.pinned == False, oldest_first=True, bulk=True)

                success = discord.Embed(color=self.bot.green, title="Success", description=f'The purge is now complete!')
                await response.edit(embed=success, view=None)
                await response.delete(delay=10.0)
                                        
                # Send a log to the logging channel
                cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                row = await cur.fetchone()
                fetched_logging = row[0]
                if fetched_logging is not None:
                    logging_channel = guild.get_channel(fetched_logging)
                    now = datetime.now(tz=timezone.utc)
                    if isinstance(logging_channel, discord.TextChannel):
                        purge_log = discord.Embed(
                            color=self.bot.green,
                            title="Purge Log",
                            description=f"{user.mention} has just deleted {len(deleted)} messages from {channel.mention} via the `/purge here` command.",
                            timestamp=now
                        )
                        await logging_channel.send(embed=purge_log)
                    
                    # Sends an error message if the logging channel was not found
                    else:
                        error = discord.Embed(
                            color=self.bot.red,
                            title="Logging Channel Not Found",
                            description=f"A logging channel with the ID {fetched_logging} was not found! Please set a new logging channel by re-running the `/start` command.",
                            timestamp=now
                        )
                        await channel.send(embed=error, delete_after=10.0)
            
            # Sends a message that the interaction was cancelled
            else:
                if isinstance(response, discord.WebhookMessage):
                    await response.delete()
                cancelled = discord.Embed(
                    color=self.bot.red,
                    title="Cancelled",
                    description='This interaction has been cancelled. No messages have been purged.'
                )
                await channel.send(embed=cancelled, delete_after=10.0)

        # Send an error message if there is an issue
        except Exception as e:
            print(traceback.format_exc())
            if isinstance(response, discord.WebhookMessage):
                await response.delete()
            error = discord.Embed(
                color=self.bot.red,
                title="Error",
                description=f"{e}"
            )
            await interaction.channel.send(embed=error, delete_after=10.0)

    # /purge self
    @app_commands.command(name="self")
    async def self(self, interaction: discord.Interaction):
        """Purge all of your own unpinned messages in a set list of up to 25 channels.
        """
        await interaction.response.defer()
        try:
            member = interaction.user
            guild = interaction.guild
            channel = interaction.channel

            csv = ChannelSelectView(bot=self.bot, user=member)
            embed = discord.Embed(
                color=self.bot.blurple,
                title="Purge Self",
                description=f"Which channel(s) would you like to purge your own unpinned messages from?"
            )
            response = await interaction.followup.send(embed=embed, view=csv, wait=True)
            await response.pin()
            await csv.wait()
            
            if csv.value == True:

                channels = [c.mention for c in csv.channels]
                channels_str = ", ".join(channels)
                yon = YesOrNo(bot=self.bot, user=member)
                embed = discord.Embed(
                    color=self.bot.blurple,
                    title="Confirm Purge",
                    description=f"Please review the list of selected channels below and confirm that you would like to continue with the purge of your own unpinned messages from the following channels:\n\n{channels_str}"
                )
                embed.add_field(name="Delete Recent Messages", value="This option will delete all messages posted within the last 2 weeks.", inline=False)
                embed.add_field(name="Delete All Messages", value="This option will delete all messages (this can take a very long time).", inline=False)
                embed.add_field(name="No", value="Cancels the interaction.", inline=False)
                await response.edit(embed=embed, view=yon)
                await yon.wait()

                if yon.value == True:

                    wait = discord.Embed(
                        color=self.bot.blurple,
                        title="Purge in Progress",
                        description="Please wait while the purge is in progress. This message will be edited when the purge is complete."
                    )
                    wait.add_field(name="Currently Purging", value="None", inline=False)
                    await response.edit(embed=wait, view=None)
                    time = datetime.now(tz=timezone.utc) - timedelta(weeks=2.0)
                    for channel in csv.channels:
                        wait.set_field_at(index=0, name="Currently Purging", value=f"{channel.mention}", inline=False)
                        await response.edit(embed=wait, view=None)

                        if yon.method == "Recent":
                            time = datetime.now(tz=timezone.utc) - timedelta(weeks=2.0)
                            deleted = await channel.purge(limit=1000, check=lambda m: m.pinned == False and m.author == member, after=time, oldest_first=True, bulk=True)
                        elif yon.method == "All":
                            deleted = await channel.purge(limit=1000, check=lambda m: m.pinned == False and m.author == member, oldest_first=True, bulk=True)
                        
                        # Send logs to the logging channel as the channels are purged
                        cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                        row = await cur.fetchone()
                        fetched_logging = row[0]
                        if fetched_logging is not None:
                            logging_channel = guild.get_channel(fetched_logging)
                            now = datetime.now(tz=timezone.utc)
                            if isinstance(logging_channel, discord.TextChannel):
                                purge_log = discord.Embed(
                                    color=self.bot.green,
                                    title="Purge Log",
                                    description=f"{member.mention} has just deleted {len(deleted)} messages from {channel.mention} via the `/purge self` command."
                                )
                                await logging_channel.send(embed=purge_log)
                    
                    success = discord.Embed(color=self.bot.green, title="Success", description=f'The purge is now complete!')
                    await response.edit(embed=success, view=None)
                    await response.delete(delay=10.0)

                    # Send a log to the logging channel
                    cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                    row = await cur.fetchone()
                    fetched_logging = row[0]
                    if fetched_logging is not None:
                        logging_channel = guild.get_channel(fetched_logging)
                        now = datetime.now(tz=timezone.utc)
                        if isinstance(logging_channel, discord.TextChannel):
                            log = discord.Embed(
                                color=self.bot.blurple,
                                title="Purge Log",
                                description=f"{member.mention} has just purged all of their own unpinned messages from the following channels: {channels_str}.",
                                timestamp=now
                            )
                            log.set_author(name=member.display_name, icon_url=member.display_avatar)
                            log.set_thumbnail(url=member.display_avatar)
                            await logging_channel.send(embed=log)
                        
                        # Sends an error message if the logging channel was not found
                        else:
                            error = discord.Embed(
                                color=self.bot.red,
                                title="Logging Channel Not Found",
                                description=f"A logging channel with the ID {fetched_logging} was not found! Please set a new logging channel by re-running the `/start` command.",
                                timestamp=now
                            )
                            await channel.send(embed=error, delete_after=10.0)

                elif yon.value == False:
                    cancelled = discord.Embed(color=self.bot.red, title="Cancelled", description='This interaction has been cancelled. No messages have been purged.')
                    await response.edit(embed=cancelled, view=None)
                    await response.delete(delay=10.0)

                else:
                    timed_out = discord.Embed(color=self.bot.yellow, title="Timed Out", description='This interaction has timed out. No messages have been purged.')
                    await response.edit(embed=timed_out, view=None)
                    await response.delete(delay=10.0)

            elif csv.value == False:
                cancelled = discord.Embed(color=self.bot.red, title="Cancelled", description='This interaction has been cancelled. No messages have been purged.')
                await response.edit(embed=cancelled, view=None)
                await response.delete(delay=10.0)

            else:
                timed_out = discord.Embed(color=self.bot.yellow, title="Timed Out", description='This interaction has timed out. No messages have been purged.')
                await response.edit(embed=timed_out, view=None)
                await response.delete(delay=10.0)

        # Send an error message if there is an issue
        except Exception as e:
            print(traceback.format_exc())
            if isinstance(response, discord.WebhookMessage):
                await response.delete()
            error = discord.Embed(
                color=self.bot.red,
                title="Error",
                description=f"{e}"
            )
            await interaction.channel.send(embed=error, delete_after=10.0)

    # /purge member
    @app_commands.command(name="member")
    @app_commands.checks.has_permissions(administrator=True)
    async def member(self, interaction: discord.Interaction, member: discord.Member):
        """(Admin Only) Purge a member's unpinned messages in a set list of up to 25 channels.

        Parameters
        -----------
        member : discord.Member
            Choose the member to whose messages you would like to purge.
        """
        await interaction.response.defer()
        try:
            user = interaction.user
            guild = interaction.guild
            channel = interaction.channel

            csv = ChannelSelectView(bot=self.bot, user=user)
            embed = discord.Embed(
                color=self.bot.blurple,
                title="Purge Member",
                description=f"Which channel(s) would you like to purge {member.mention}'s unpinned messages from?"
            )
            response = await interaction.followup.send(embed=embed, view=csv, wait=True)
            await response.pin()
            await csv.wait()
            
            if csv.value == True:

                channels = [c.mention for c in csv.channels]
                channels_str = ", ".join(channels)
                yon = YesOrNo(bot=self.bot, user=user)
                embed = discord.Embed(
                    color=self.bot.blurple,
                    title="Confirm Purge",
                    description=f"Please review the list of selected channels below and confirm that you would like to continue with the purge of {member.mention}'s unpinned messages from the following channels:\n\n{channels_str}"
                )
                embed.add_field(name="Delete Recent Messages", value="This option will delete all messages posted within the last 2 weeks.", inline=False)
                embed.add_field(name="Delete All Messages", value="This option will delete all messages (this can take a very long time).", inline=False)
                embed.add_field(name="No", value="Cancels the interaction.", inline=False)
                await response.edit(embed=embed, view=yon)
                await yon.wait()

                if yon.value == True:

                    wait = discord.Embed(
                        color=self.bot.blurple,
                        title="Purge in Progress",
                        description="Please wait while the purge is in progress. This message will be edited when the purge is complete."
                    )
                    wait.add_field(name="Currently Purging", value="None", inline=False)
                    await response.edit(embed=wait, view=None)
                    time = datetime.now(tz=timezone.utc) - timedelta(weeks=2.0)
                    for channel in csv.channels:
                        wait.set_field_at(index=0, name="Currently Purging", value=f"{channel.mention}", inline=False)
                        await response.edit(embed=wait, view=None)

                        if yon.method == "Recent":
                            time = datetime.now(tz=timezone.utc) - timedelta(weeks=2.0)
                            deleted = await channel.purge(limit=1000, check=lambda m: m.pinned == False and m.author == member, after=time, oldest_first=True, bulk=True)
                        elif yon.method == "All":
                            deleted = await channel.purge(limit=1000, check=lambda m: m.pinned == False and m.author == member, oldest_first=True, bulk=True)
                        
                        # Send logs to the logging channel as the channels are purged
                        cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                        row = await cur.fetchone()
                        fetched_logging = row[0]
                        if fetched_logging is not None:
                            logging_channel = guild.get_channel(fetched_logging)
                            now = datetime.now(tz=timezone.utc)
                            if isinstance(logging_channel, discord.TextChannel):
                                purge_log = discord.Embed(
                                    color=self.bot.green,
                                    title="Purge Log",
                                    description=f"{user.mention} has just deleted {len(deleted)} messages from {channel.mention} via the `/purge member` command."
                                )
                                await logging_channel.send(embed=purge_log)
                    
                    success = discord.Embed(color=self.bot.green, title="Success", description=f'The purge is now complete!')
                    await response.edit(embed=success, view=None)
                    await response.delete(delay=10.0)

                    # Send a log to the logging channel
                    cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                    row = await cur.fetchone()
                    fetched_logging = row[0]
                    if fetched_logging is not None:
                        logging_channel = guild.get_channel(fetched_logging)
                        now = datetime.now(tz=timezone.utc)
                        if isinstance(logging_channel, discord.TextChannel):
                            log = discord.Embed(
                                color=self.bot.blurple,
                                title="Purge Log",
                                description=f"{user.mention} has just purged all of {member.mention}'s unpinned messages from the following channels: {channels_str}.",
                                timestamp=now
                            )
                            log.set_author(name=user.display_name, icon_url=user.display_avatar)
                            log.set_thumbnail(url=member.display_avatar)
                            await logging_channel.send(embed=log)
                        
                        # Sends an error message if the logging channel was not found
                        else:
                            error = discord.Embed(
                                color=self.bot.red,
                                title="Logging Channel Not Found",
                                description=f"A logging channel with the ID {fetched_logging} was not found! Please set a new logging channel by re-running the `/start` command.",
                                timestamp=now
                            )
                            await channel.send(embed=error, delete_after=10.0)

                elif yon.value == False:
                    cancelled = discord.Embed(color=self.bot.red, title="Cancelled", description='This interaction has been cancelled. No messages have been purged.')
                    await response.edit(embed=cancelled, view=None)
                    await response.delete(delay=10.0)

                else:
                    timed_out = discord.Embed(color=self.bot.yellow, title="Timed Out", description='This interaction has timed out. No messages have been purged.')
                    await response.edit(embed=timed_out, view=None)
                    await response.delete(delay=10.0)

            elif csv.value == False:
                cancelled = discord.Embed(color=self.bot.red, title="Cancelled", description='This interaction has been cancelled. No messages have been purged.')
                await response.edit(embed=cancelled, view=None)
                await response.delete(delay=10.0)

            else:
                timed_out = discord.Embed(color=self.bot.yellow, title="Timed Out", description='This interaction has timed out. No messages have been purged.')
                await response.edit(embed=timed_out, view=None)
                await response.delete(delay=10.0)

        # Send an error message if there is an issue
        except Exception as e:
            print(traceback.format_exc())
            if isinstance(response, discord.WebhookMessage):
                await response.delete()
            error = discord.Embed(
                color=self.bot.red,
                title="Error",
                description=f"{e}"
            )
            await interaction.channel.send(embed=error, delete_after=10.0)

    # /purge channels
    @app_commands.command(name="channels")
    @app_commands.checks.has_permissions(administrator=True)
    async def channels(self, interaction: discord.Interaction):
        """(Admin Only) Purge all unpinned messages in a set list of up to 25 channels.
        """
        await interaction.response.defer()
        try:
            user = interaction.user
            guild = interaction.guild
            channel = interaction.channel

            csv = ChannelSelectView(bot=self.bot, user=user)
            embed = discord.Embed(
                color=self.bot.blurple,
                title="Purge Channels",
                description=f"Which channel(s) would you like to purge all unpinned messages from?"
            )
            response = await interaction.followup.send(embed=embed, view=csv, wait=True)
            await response.pin()
            await csv.wait()
            
            if csv.value == True:

                channels = [c.mention for c in csv.channels]
                channels_str = ", ".join(channels)
                yon = YesOrNo(bot=self.bot, user=user)
                embed = discord.Embed(
                    color=self.bot.blurple,
                    title="Confirm Purge",
                    description=f"Please review the list of selected channels below and confirm that you would like to continue with the purge of all unpinned messages from the following channels:\n\n{channels_str}"
                )
                embed.add_field(name="Delete Recent Messages", value="This option will delete all messages posted within the last 2 weeks.", inline=False)
                embed.add_field(name="Delete All Messages", value="This option will delete all messages (this can take a very long time).", inline=False)
                embed.add_field(name="No", value="Cancels the interaction.", inline=False)
                await response.edit(embed=embed, view=yon)
                await yon.wait()

                if yon.value == True:

                    wait = discord.Embed(
                        color=self.bot.blurple,
                        title="Purge in Progress",
                        description="Please wait while the purge is in progress. This message will be edited when the purge is complete."
                    )
                    wait.add_field(name="Currently Purging", value="None", inline=False)
                    await response.edit(embed=wait, view=None)
                    time = datetime.now(tz=timezone.utc) - timedelta(weeks=2.0)
                    for channel in csv.channels:
                        wait.set_field_at(index=0, name="Currently Purging", value=f"{channel.mention}", inline=False)
                        await response.edit(embed=wait, view=None)

                        if yon.method == "Recent":
                            time = datetime.now(tz=timezone.utc) - timedelta(weeks=2.0)
                            deleted = await channel.purge(limit=1000, check=lambda m: m.pinned == False, after=time, oldest_first=True, bulk=True)
                        elif yon.method == "All":
                            deleted = await channel.purge(limit=1000, check=lambda m: m.pinned == False, oldest_first=True, bulk=True)

                        # Send logs to the logging channel as the channels are purged
                        cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                        row = await cur.fetchone()
                        fetched_logging = row[0]
                        if fetched_logging is not None:
                            logging_channel = guild.get_channel(fetched_logging)
                            now = datetime.now(tz=timezone.utc)
                            if isinstance(logging_channel, discord.TextChannel):
                                purge_log = discord.Embed(
                                    color=self.bot.green,
                                    title="Purge Log",
                                    description=f"{user.mention} has just deleted {len(deleted)} messages from {channel.mention} via the `/purge channels` command."
                                )
                                await logging_channel.send(embed=purge_log)
                    
                    success = discord.Embed(color=self.bot.green, title="Success", description=f'The purge is now complete!')
                    await response.edit(embed=success, view=None)
                    await response.delete(delay=10.0)

                    # Send a log to the logging channel
                    cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                    row = await cur.fetchone()
                    fetched_logging = row[0]
                    if fetched_logging is not None:
                        logging_channel = guild.get_channel(fetched_logging)
                        now = datetime.now(tz=timezone.utc)
                        if isinstance(logging_channel, discord.TextChannel):
                            log = discord.Embed(
                                color=self.bot.blurple,
                                title="Purge Log",
                                description=f"{user.mention} has just purged all unpinned messages from the following channels: {channels_str}.",
                                timestamp=now
                            )
                            log.set_author(name=user.display_name, icon_url=user.display_avatar)
                            log.set_thumbnail(url=user.display_avatar)
                            await logging_channel.send(embed=log)
                        
                        # Sends an error message if the logging channel was not found
                        else:
                            error = discord.Embed(
                                color=self.bot.red,
                                title="Logging Channel Not Found",
                                description=f"A logging channel with the ID {fetched_logging} was not found! Please set a new logging channel by re-running the `/start` command.",
                                timestamp=now
                            )
                            await channel.send(embed=error, delete_after=10.0)

                elif yon.value == False:
                    cancelled = discord.Embed(color=self.bot.red, title="Cancelled", description='This interaction has been cancelled. No messages have been purged.')
                    await response.edit(embed=cancelled, view=None)
                    await response.delete(delay=10.0)

                else:
                    timed_out = discord.Embed(color=self.bot.yellow, title="Timed Out", description='This interaction has timed out. No messages have been purged.')
                    await response.edit(embed=timed_out, view=None)
                    await response.delete(delay=10.0)

            elif csv.value == False:
                cancelled = discord.Embed(color=self.bot.red, title="Cancelled", description='This interaction has been cancelled. No messages have been purged.')
                await response.edit(embed=cancelled, view=None)
                await response.delete(delay=10.0)

            else:
                timed_out = discord.Embed(color=self.bot.yellow, title="Timed Out", description='This interaction has timed out. No messages have been purged.')
                await response.edit(embed=timed_out, view=None)
                await response.delete(delay=10.0)

        # Send an error message if there is an issue
        except Exception as e:
            print(traceback.format_exc())
            if isinstance(response, discord.WebhookMessage):
                await response.delete()
            error = discord.Embed(
                color=self.bot.red,
                title="Error",
                description=f"{e}"
            )
            await interaction.channel.send(embed=error, delete_after=10.0)

    # /purge server
    @app_commands.command(name="server")
    @app_commands.checks.has_permissions(administrator=True)
    async def server(self, interaction: discord.Interaction):
        """(Admin Only) Purges all unpinned messages in a server, excluding up to 25 channels.
        """
        await interaction.response.defer()
        try:
            user = interaction.user
            guild = interaction.guild
            channel = interaction.channel

            csv = ChannelSelectView(bot=self.bot, user=user)
            embed = discord.Embed(
                color=self.bot.blurple,
                title="Purge Server",
                description=f"Which channel(s) would you like to **exclude** from the purge of all unpinned messages in the server?"
            )
            response = await interaction.followup.send(embed=embed, view=csv, wait=True)
            await response.pin()
            await csv.wait()
            
            if csv.value == True:

                channels = [c.mention for c in csv.channels]
                channels_str = ", ".join(channels)
                yon = YesOrNo(bot=self.bot, user=user)
                embed = discord.Embed(
                    color=self.bot.blurple,
                    title="Confirm Purge",
                    description=f"Please review the list of selected channels below and confirm that you would like to continue with the purge of all unpinned messages in the server **except** from the following channels:\n\n{channels_str}"
                )
                embed.add_field(name="Delete Recent Messages", value="This option will delete all messages posted within the last 2 weeks.", inline=False)
                embed.add_field(name="Delete All Messages", value="This option will delete all messages (this can take a very long time).", inline=False)
                embed.add_field(name="No", value="Cancels the interaction.", inline=False)
                await response.edit(embed=embed, view=yon)
                await yon.wait()

                if yon.value == True:

                    wait = discord.Embed(
                        color=self.bot.blurple,
                        title="Purge in Progress",
                        description="Please wait while the purge is in progress. This message will be edited when the purge is complete."
                    )
                    wait.add_field(name="Currently Purging", value="None", inline=False)
                    await response.edit(embed=wait, view=None)
                    time = datetime.now(tz=timezone.utc) - timedelta(weeks=2.0)
                    purge_channels = [c for c in guild.text_channels if c not in csv.channels]
                    for channel in purge_channels:
                        wait.set_field_at(index=0, name="Currently Purging", value=f"{channel.mention}", inline=False)
                        await response.edit(embed=wait, view=None)

                        if yon.method == "Recent":
                            time = datetime.now(tz=timezone.utc) - timedelta(weeks=2.0)
                            deleted = await channel.purge(limit=1000, check=lambda m: m.pinned == False, after=time, oldest_first=True, bulk=True)
                        elif yon.method == "All":
                            deleted = await channel.purge(limit=1000, check=lambda m: m.pinned == False, oldest_first=True, bulk=True)

                        # Send logs to the logging channel as the channels are purged
                        cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                        row = await cur.fetchone()
                        fetched_logging = row[0]
                        if fetched_logging is not None:
                            logging_channel = guild.get_channel(fetched_logging)
                            now = datetime.now(tz=timezone.utc)
                            if isinstance(logging_channel, discord.TextChannel):
                                purge_log = discord.Embed(
                                    color=self.bot.green,
                                    title="Purge Log",
                                    description=f"{user.mention} has just deleted {len(deleted)} messages from {channel.mention} via the `/purge server` command."
                                )
                                await logging_channel.send(embed=purge_log)
                    
                    success = discord.Embed(color=self.bot.green, title="Success", description=f'The purge is now complete!')
                    await response.edit(embed=success, view=None)
                    await response.delete(delay=10.0)

                    # Send a log to the logging channel
                    cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                    row = await cur.fetchone()
                    fetched_logging = row[0]
                    if fetched_logging is not None:
                        logging_channel = guild.get_channel(fetched_logging)
                        now = datetime.now(tz=timezone.utc)
                        if isinstance(logging_channel, discord.TextChannel):
                            log = discord.Embed(
                                color=self.bot.blurple,
                                title="Purge Log",
                                description=f"{user.mention} has just purged all unpinned messages **except** from the following channels: {channels_str}.",
                                timestamp=now
                            )
                            log.set_author(name=user.display_name, icon_url=user.display_avatar)
                            log.set_thumbnail(url=user.display_avatar)
                            await logging_channel.send(embed=log)
                        
                        # Sends an error message if the logging channel was not found
                        else:
                            error = discord.Embed(
                                color=self.bot.red,
                                title="Logging Channel Not Found",
                                description=f"A logging channel with the ID {fetched_logging} was not found! Please set a new logging channel by re-running the `/start` command.",
                                timestamp=now
                            )
                            await channel.send(embed=error, delete_after=10.0)

                elif yon.value == False:
                    cancelled = discord.Embed(color=self.bot.red, title="Cancelled", description='This interaction has been cancelled. No messages have been purged.')
                    await response.edit(embed=cancelled, view=None)
                    await response.delete(delay=10.0)

                else:
                    timed_out = discord.Embed(color=self.bot.yellow, title="Timed Out", description='This interaction has timed out. No messages have been purged.')
                    await response.edit(embed=timed_out, view=None)
                    await response.delete(delay=10.0)

            elif csv.value == False:
                cancelled = discord.Embed(color=self.bot.red, title="Cancelled", description='This interaction has been cancelled. No messages have been purged.')
                await response.edit(embed=cancelled, view=None)
                await response.delete(delay=10.0)

            else:
                timed_out = discord.Embed(color=self.bot.yellow, title="Timed Out", description='This interaction has timed out. No messages have been purged.')
                await response.edit(embed=timed_out, view=None)
                await response.delete(delay=10.0)

        # Send an error message if there is an issue
        except Exception as e:
            print(traceback.format_exc())
            if isinstance(response, discord.WebhookMessage):
                await response.delete()
            error = discord.Embed(
                color=self.bot.red,
                title="Error",
                description=f"{e}"
            )
            await interaction.channel.send(embed=error, delete_after=10.0)

async def setup(bot: commands.Bot):
    print("Setting up Cog: purge.Purge")

async def teardown(bot: commands.Bot):
    print("Tearing down Cog: purge.Purge")