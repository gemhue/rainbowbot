import discord
import aiosqlite
from typing import Any
from discord.ext import commands
from discord import app_commands, ChannelType
from datetime import datetime, timezone
from cogs import AutoDelete, Awards, Embeds, Profiles, Purge, RSSFeeds, Tickets

class YesOrNo(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)
        self.value = None

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, emoji="👍")
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True
        self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.red, emoji="👎")
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = False
        self.stop()

class ChannelSelect(discord.ui.ChannelSelect):
    def __init__(self):
        super().__init__(
            channel_types=[ChannelType.text],
            placeholder="Select a channel...",
            min_values=1,
            max_values=1,
            row=1
        )

    async def callback(self, interaction: discord.Interaction) -> Any:
        await interaction.response.defer()
        channels: list[ChannelSelectView] = self.values
        self.view.values = [c for c in channels]

class ChannelSelectView(discord.ui.View):
    def __init__(self, *, timeout=180.0):
        super().__init__(timeout=timeout)
        self.value = None
        self.add_item(ChannelSelect())

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green, emoji="👍", row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red, emoji="👎", row=2)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = False
        self.stop()

class CogButtons(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=180)
        self.bot = bot
        self.red = discord.Colour.red()
        self.guild_cogs = {}

    @discord.ui.button(label="AutoDelete", style=discord.ButtonStyle.blurple, emoji="♻️")
    async def autodelete(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        guild = interaction.guild
        try:
            await self.bot.add_cog(AutoDelete(self.bot), override=True, guild=guild)
            if guild.id not in self.guild_cogs:
                self.guild_cogs[guild.id] = []
            coglist = self.guild_cogs[guild.id]
            if "AutoDelete" not in coglist:
                coglist.append("AutoDelete")
            button.label = "Added"
            button.style = discord.ButtonStyle.gray
            button.emoji = "✅"
            button.disabled = True
            await interaction.response.edit_message(view=self)
        except Exception as e:
            print(f"There was a problem setting up AutoDelete (Guild ID: {guild.id}). Error: {e}")
            error = discord.Embed(color=self.red, title="Error", description=f"{e}")
            await interaction.response.send_message(embed=error, delete_after=30.0)

    @discord.ui.button(label="Awards", style=discord.ButtonStyle.blurple, emoji="🏅")
    async def awards(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        guild = interaction.guild
        try:
            await self.bot.add_cog(Awards(self.bot), override=True, guild=guild)
            if guild.id not in self.guild_cogs:
                self.guild_cogs[guild.id] = []
            coglist = self.guild_cogs[guild.id]
            if "Awards" not in coglist:
                coglist.append("Awards")
            button.label = "Added"
            button.style = discord.ButtonStyle.gray
            button.emoji = "✅"
            button.disabled = True
            await interaction.response.edit_message(view=self)
        except Exception as e:
            print(f"There was a problem setting up Awards (Guild ID: {guild.id}). Error: {e}")
            error = discord.Embed(color=self.red, title="Error", description=f"{e}")
            await interaction.response.send_message(embed=error, delete_after=30.0)
    
    @discord.ui.button(label="Embeds", style=discord.ButtonStyle.blurple, emoji="📝")
    async def embeds(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        guild = interaction.guild
        try:
            await self.bot.add_cog(Embeds(self.bot), override=True, guild=guild)
            if guild.id not in self.guild_cogs:
                self.guild_cogs[guild.id] = []
            coglist = self.guild_cogs[guild.id]
            if "Embeds" not in coglist:
                coglist.append("Embeds")
            button.label = "Added"
            button.style = discord.ButtonStyle.gray
            button.emoji = "✅"
            button.disabled = True
            await interaction.response.edit_message(view=self)
        except Exception as e:
            print(f"There was a problem setting up Embeds (Guild ID: {guild.id}). Error: {e}")
            error = discord.Embed(color=self.red, title="Error", description=f"{e}")
            await interaction.response.send_message(embed=error, delete_after=30.0)

    @discord.ui.button(label="Profiles", style=discord.ButtonStyle.blurple, emoji="🪪")
    async def profiles(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        guild = interaction.guild
        try:
            await self.bot.add_cog(Profiles(self.bot), override=True, guild=guild)
            if guild.id not in self.guild_cogs:
                self.guild_cogs[guild.id] = []
            coglist = self.guild_cogs[guild.id]
            if "Profiles" not in coglist:
                coglist.append("Profiles")
            button.label = "Added"
            button.style = discord.ButtonStyle.gray
            button.emoji = "✅"
            button.disabled = True
            await interaction.response.edit_message(view=self)
        except Exception as e:
            print(f"There was a problem setting up Profiles (Guild ID: {guild.id}). Error: {e}")
            error = discord.Embed(color=self.red, title="Error", description=f"{e}")
            await interaction.response.send_message(embed=error, delete_after=30.0)

    @discord.ui.button(label="Purge", style=discord.ButtonStyle.blurple, emoji="🗑️")
    async def purge(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        guild = interaction.guild
        try:
            await self.bot.add_cog(Purge(self.bot), override=True, guild=guild)
            if guild.id not in self.guild_cogs:
                self.guild_cogs[guild.id] = []
            coglist = self.guild_cogs[guild.id]
            if "Purge" not in coglist:
                coglist.append("Purge")
            button.label = "Added"
            button.style = discord.ButtonStyle.gray
            button.emoji = "✅"
            button.disabled = True
            await interaction.response.edit_message(view=self)
        except Exception as e:
            print(f"There was a problem setting up Purge (Guild ID: {guild.id}). Error: {e}")
            error = discord.Embed(color=self.red, title="Error", description=f"{e}")
            await interaction.response.send_message(embed=error, delete_after=30.0)

    @discord.ui.button(label="RSS Feeds", style=discord.ButtonStyle.blurple, emoji="📰")
    async def rss_feeds(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        guild = interaction.guild
        try:
            await self.bot.add_cog(RSSFeeds(self.bot), override=True, guild=guild)
            if guild.id not in self.guild_cogs:
                self.guild_cogs[guild.id] = []
            coglist = self.guild_cogs[guild.id]
            if "RSS Feeds" not in coglist:
                coglist.append("RSS Feeds")
            button.label = "Added"
            button.style = discord.ButtonStyle.gray
            button.emoji = "✅"
            button.disabled = True
            await interaction.response.edit_message(view=self)
        except Exception as e:
            print(f"There was a problem setting up RSS Feeds (Guild ID: {guild.id}). Error: {e}")
            error = discord.Embed(color=self.red, title="Error", description=f"{e}")
            await interaction.response.send_message(embed=error, delete_after=30.0)

    @discord.ui.button(label="Tickets", style=discord.ButtonStyle.blurple, emoji="🎫")
    async def rss_feeds(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        guild = interaction.guild
        try:
            await self.bot.add_cog(Tickets(self.bot), override=True, guild=guild)
            if guild.id not in self.guild_cogs:
                self.guild_cogs[guild.id] = []
            coglist = self.guild_cogs[guild.id]
            if "Ticket" not in coglist:
                coglist.append("Tickets")
            button.label = "Added"
            button.style = discord.ButtonStyle.gray
            button.emoji = "✅"
            button.disabled = True
            await interaction.response.edit_message(view=self)
        except Exception as e:
            print(f"There was a problem setting up Tickets (Guild ID: {guild.id}). Error: {e}")
            error = discord.Embed(color=self.red, title="Error", description=f"{e}")
            await interaction.response.send_message(embed=error, delete_after=30.0)

    @discord.ui.button(label="Done", style=discord.ButtonStyle.green)
    async def done(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        try:
            self.stop()
        except Exception as e:
            error = discord.Embed(color=self.red, title="Error", description=f"{e}")
            await interaction.response.send_message(embed=error, delete_after=30.0)

class Start(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.blurple = discord.Colour.blurple()
        self.yellow = discord.Colour.yellow()
        self.green = discord.Colour.green()
        self.red = discord.Colour.red()

    @commands.hybrid_command(name="start")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def start(self, ctx: commands.Context):
        """(Admin Only) Start the bot by choosing desired functions.
        """
        await ctx.defer()
        guild = ctx.guild
        author = ctx.author
        timestamp = datetime.now(tz=timezone.utc)
        yes_or_no = YesOrNo()
        channel_select = ChannelSelectView()
        cog_buttons = CogButtons(bot=self.bot)
        try:
            async with aiosqlite.connect('rainbowbot.db') as db:
                await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild.id,))
                start = discord.Embed(
                    color=self.blurple,
                    title="Bot Startup",
                    description="Would you like to start by choosing channels for bot logging messages, member welcome messages, or member goodbye messages?"
                )
                response = await ctx.send(embed=start, view=yes_or_no)
                await yes_or_no.wait()

                # User wants to select logging, welcome, and/or goodbye channels
                if yes_or_no.value == True:

                    # Ask user to select a logging channel
                    ask_logging = discord.Embed(
                        color=self.blurple,
                        title="Logging Channel",
                        description="Would you like to select a channel to send logging messages?\nChoose `Cancel` to skip to the next option."
                    )
                    response = await response.edit(embed=ask_logging, view=channel_select)
                    await channel_select.wait()

                    # User selects a logging channel
                    if channel_select.value == True:
                        selected_list = [c.resolve() for c in channel_select.values]
                        selected = selected_list[0]
                        selected_id = selected.id
                        logging_channel = await guild.fetch_channel(selected_id)
                        logging_channel_id = logging_channel.id
                        await db.execute("UPDATE guilds SET logging_channel_id = ? WHERE guild_id = ?", (logging_channel_id, guild.id))

                        # Bot sends a log to the logging channel
                        log = discord.Embed(
                            color=self.blurple,
                            title="Bot Startup Log",
                            description=f"{author.mention} has just set the guild's logging channel to {logging_channel.mention}!",
                            timestamp=timestamp
                        )
                        log.set_author(name=author.display_name, icon_url=author.display_avatar)
                        await logging_channel.send(embed=log)
                    
                    # User does not select a logging channel
                    elif channel_select.value == False:
                        pass

                    # The view times out before the user selects a logging channel
                    else:
                        timed_out = discord.Embed(
                            color=self.yellow,
                            title="Timed Out",
                            description="This interaction has timed out. Please try again."
                        )
                        await response.edit(embed=timed_out, delete_after=30.0, view=None)

                    # Ask user to select a welcome channel
                    ask_welcome = discord.Embed(
                        color=self.blurple,
                        title="Welcome Channel",
                        description="Would you like to select a channel to send welcome messages?\nChoose `Cancel` to skip to the next option."
                    )
                    response = await response.edit(embed=ask_welcome, view=channel_select)
                    await channel_select.wait()

                    # User selects a welcome channel
                    if channel_select.value == True:
                        selected_list = [c.resolve() for c in channel_select.values]
                        selected = selected_list[0]
                        selected_id = selected.id
                        welcome_channel = await guild.fetch_channel(selected_id)
                        welcome_channel_id = welcome_channel.id
                        await db.execute("UPDATE guilds SET welcome_channel_id = ? WHERE guild_id = ?", (welcome_channel_id, guild.id))

                        # Bot sends a log to the logging channel
                        cur = await db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                        row = await cur.fetchone()
                        fetched_logging = row[0]
                        if fetched_logging is not None:
                            logging_channel = await guild.fetch_channel(fetched_logging)
                            log = discord.Embed(
                                color=self.blurple,
                                title="Bot Startup Log",
                                description=f"{author.mention} has just set the guild's welcome channel to {welcome_channel.mention}!",
                                timestamp=timestamp
                            )
                            log.set_author(name=author.display_name, icon_url=author.display_avatar)
                            await logging_channel.send(embed=log)
                    
                    # User does not select a welcome channel
                    elif channel_select.value == False:
                        pass

                    # The view times out before the user selects a welcome channel
                    else:
                        timed_out = discord.Embed(
                            color=self.yellow,
                            title="Timed Out",
                            description="This interaction has timed out. Please try again."
                        )
                        await response.edit(embed=timed_out, delete_after=30.0, view=None)

                    # Ask user to select a goodbye channel
                    ask_goodbye = discord.Embed(
                        color=self.blurple,
                        title="Goodbye Channel",
                        description="Would you like to select a channel to send goodbye messages?\nChoose `Cancel` to skip to the next option."
                    )
                    response = await response.edit(embed=ask_goodbye, view=channel_select)
                    await channel_select.wait()

                    # User selects a goodbye channel
                    if channel_select.value == True:
                        selected_list = [c.resolve() for c in channel_select.values]
                        selected = selected_list[0]
                        selected_id = selected.id
                        goodbye_channel = await guild.fetch_channel(selected.id)
                        goodbye_channel_id = goodbye_channel.id
                        await db.execute("UPDATE guilds SET goodbye_channel_id = ? WHERE guild_id = ?", (goodbye_channel_id, guild.id))

                        # Bot sends a log to the logging channel
                        cur = await db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                        row = await cur.fetchone()
                        fetched_logging = row[0]
                        if fetched_logging is not None:
                            logging_channel = await guild.fetch_channel(fetched_logging)
                            log = discord.Embed(
                                color=self.blurple,
                                title="Bot Startup Log",
                                description=f"{author.mention} has just set the guild's goodbye channel to {goodbye_channel.mention}!",
                                timestamp=timestamp
                            )
                            log.set_author(name=author.display_name, icon_url=author.display_avatar)
                            await logging_channel.send(embed=log)
                    
                    # User does not select a goodbye channel
                    elif channel_select.value == False:
                        pass

                    # The view times out before the user selects a goodbye channel
                    else:
                        timed_out = discord.Embed(
                            color=self.yellow,
                            title="Timed Out",
                            description="This interaction has timed out. Please try again."
                        )
                        await response.edit(embed=timed_out, delete_after=30.0, view=None)

                # The user doesn't want to select a logging, welcome, and goodbye channels
                elif yes_or_no.value == False:
                    pass

                # The view times out before the user selects yes or no
                else:
                    timed_out = discord.Embed(
                        color=self.yellow,
                        title="Timed Out",
                        description="This interaction has timed out. Please try again."
                    )
                    await response.edit(embed=timed_out, delete_after=30.0, view=None)
                
                # Ask the user to select which cogs to add to their server
                ask_cogs = discord.Embed(
                    color=self.blurple,
                    title="Bot Startup",
                    description="Choose which commands you would like to add to your server."
                )
                ask_cogs.add_field(name="AutoDelete", value="These commands allow you to set the messages in a channel to be automatically deleted on a rolling basis.", inline=False)
                ask_cogs.add_field(name="Awards", value="These commands allow you to set up an awards system in your server. The award name and emoji can be customized.", inline=False)
                ask_cogs.add_field(name="Embeds", value="These commands allow you to send and edit messages containing embeds.", inline=False)
                ask_cogs.add_field(name="Profiles", value="These commands allow you and your server members to set up member profiles that can be viewed and edited.", inline=False)
                ask_cogs.add_field(name="Purge", value="These commands allow you to easily mass-delete messages in a single channel or in multiple channels at once.", inline=False)
                ask_cogs.add_field(name="RSS Feeds", value="These commands allow you to easily assign and unassign RSS feeds to Webhooks to post new entries automatically.", inline=False)
                ask_cogs.add_field(name="Tickets", value="These commands allow you to set up a simple ticketing system for your server using threads.", inline=False)
                response = await response.edit(embed=ask_cogs, view=cog_buttons)
                await cog_buttons.wait()

                # The user has now completed bot startup for their server
                cogs = cog_buttons.guild_cogs[guild.id]
                join = ", ".join(cogs)
                done = discord.Embed(
                    color=self.blurple,
                    title="Bot Startup",
                    description=f"Bot startup is now complete!"
                )
                done.add_field(name="Commands Added", value=f"{join}")
                await response.edit(embed=done, delete_after=30.0, view=None)

                # Bot sends a log to the logging channel
                cur = await db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                row = await cur.fetchone()
                fetched_logging = row[0]
                if fetched_logging is not None:
                    logging_channel = await guild.fetch_channel(fetched_logging)
                    log = discord.Embed(
                        color=self.blurple,
                        title="Bot Startup Log",
                        description=f"{author.mention} has just added commands to {guild.name}!",
                        timestamp=timestamp
                    )
                    log.set_author(name=author.display_name, icon_url=author.display_avatar)
                    log.add_field(name="Commands Added", value=f"{join}")
                    await logging_channel.send(embed=log)

                await db.commit()
                await db.close()
        
        # Send an error message if there's an issue
        except Exception as e:
            error = discord.Embed(
                color=self.red,
                title="Error",
                description=f"There was an error running the `/start` command. Error: {e}"
            )
            await ctx.send(embed=error, delete_after=30.0)
            print(f"Start Command Error (Guild ID: {guild.id}): {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Start(bot), override=True)