import discord
import traceback
import asyncio
from discord.ext import commands
from discord import app_commands, ChannelType
from datetime import datetime, timezone
from cogs import AutoDelete, Awards, Embeds, Profiles, Purge, RSSFeeds, Tickets

class YesOrNo(discord.ui.View):
    def __init__(self, *, timeout = 180, user: discord.Member):
        super().__init__(timeout=timeout)
        self.user = user
        self.value = None

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, emoji="👍")
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.red, emoji="👎")
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = False
            self.stop()

class ChannelSelect(discord.ui.ChannelSelect):
    def __init__(self, *, user: discord.Member):
        super().__init__(
            channel_types=[ChannelType.text],
            placeholder="Select a channel...",
            min_values=1,
            max_values=1,
            row=1
        )
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.view.channel = self.values[0]

class ChannelSelectView(discord.ui.View):
    def __init__(self, *, timeout=180.0, user: discord.Member):
        super().__init__(timeout=timeout)
        self.user = user
        self.value = None
        self.add_item(ChannelSelect(user=self.user))

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green, row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red, row=2)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = False
            self.stop()

class RoleSelect(discord.ui.RoleSelect):
    def __init__(self, *, user: discord.Member):
        super().__init__(
            placeholder="Select a role...",
            min_values=1,
            max_values=1,
            row=1
        )
        self.user = user
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.view.role = self.values[0]

class RoleSelectView(discord.ui.View):
    def __init__(self, *, timeout=180.0, user: discord.Member):
        super().__init__(timeout=timeout)
        self.user = user
        self.value = None
        self.add_item(RoleSelect(user=self.user))

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green, row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red, row=2)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = False
            self.stop()

class InactiveMonths(discord.ui.Select):
    def __init__(self, *, user: discord.Member):
        options = [
            discord.SelectOption(label="One Month", value="1"),
            discord.SelectOption(label="Two Months", value="2"),
            discord.SelectOption(label="Three Months", value="3"),
            discord.SelectOption(label="Four Months", value="4"),
            discord.SelectOption(label="Five Months", value="5"),
            discord.SelectOption(label="Six Months", value="6"),
            discord.SelectOption(label="Seven Months", value="7"),
            discord.SelectOption(label="Eight Months", value="8"),
            discord.SelectOption(label="Nine Months", value="9"),
            discord.SelectOption(label="Ten Months", value="10"),
            discord.SelectOption(label="Eleven Months", value="11"),
            discord.SelectOption(label="Twelve Months", value="12"),
        ]
        super().__init__(
            placeholder="Select a number...",
            min_values=1,
            max_values=1,
            options=options,
            row=1
        )
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.view.months = self.values[0]

class InactiveMonthsView(discord.ui.View):
    def __init__(self, *, timeout=180.0, user: discord.Member):
        super().__init__(timeout=timeout)
        self.user = user
        self.value = None
        self.add_item(InactiveMonths(user=self.user))

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green, row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red, row=2)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = False
            self.stop()

class CogButtons(discord.ui.View):
    def __init__(self, *, timeout = 180, bot: commands.Bot, user: discord.Member):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.user = user
        self.value = False
        self.guild_cogs = {}

    @discord.ui.button(label="AutoDelete", style=discord.ButtonStyle.blurple, emoji="♻️")
    async def autodelete(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message
        guild = interaction.guild
        try:
            if interaction.user == self.user:
                await self.bot.add_cog(AutoDelete.AutoDelete(bot=self.bot), override=True, guild=guild)
                if guild.id not in self.guild_cogs:
                    self.guild_cogs[guild.id] = []
                coglist = self.guild_cogs[guild.id]
                if "AutoDelete" not in coglist:
                    coglist.append("AutoDelete")
                button.label = "Added"
                button.style = discord.ButtonStyle.gray
                button.emoji = "✅"
                button.disabled = True
                await interaction.followup.edit_message(message_id=message.id, view=self)
        except Exception as e:
            print(f"There was a problem setting up AutoDelete (Guild ID: {guild.id}). Error: {e}")
            print(traceback.format_exc())
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.edit_message(message_id=message.id, embed=error, view=None)

    @discord.ui.button(label="Awards", style=discord.ButtonStyle.blurple, emoji="🏅")
    async def awards(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message
        guild = interaction.guild
        try:
            if interaction.user == self.user:
                await self.bot.add_cog(Awards.Awards(bot=self.bot), override=True, guild=guild)
                if guild.id not in self.guild_cogs:
                    self.guild_cogs[guild.id] = []
                coglist = self.guild_cogs[guild.id]
                if "Awards" not in coglist:
                    coglist.append("Awards")
                button.label = "Added"
                button.style = discord.ButtonStyle.gray
                button.emoji = "✅"
                button.disabled = True
                await interaction.followup.edit_message(message_id=message.id, view=self)
        except Exception as e:
            print(f"There was a problem setting up Awards (Guild ID: {guild.id}). Error: {e}")
            print(traceback.format_exc())
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.edit_message(message_id=message.id, embed=error, view=None)
    
    @discord.ui.button(label="Embeds", style=discord.ButtonStyle.blurple, emoji="📝")
    async def embeds(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message
        guild = interaction.guild
        try:
            if interaction.user == self.user:
                await self.bot.add_cog(Embeds.Embeds(bot=self.bot), override=True, guild=guild)
                if guild.id not in self.guild_cogs:
                    self.guild_cogs[guild.id] = []
                coglist = self.guild_cogs[guild.id]
                if "Embeds" not in coglist:
                    coglist.append("Embeds")
                button.label = "Added"
                button.style = discord.ButtonStyle.gray
                button.emoji = "✅"
                button.disabled = True
                await interaction.followup.edit_message(message_id=message.id, view=self)
        except Exception as e:
            print(f"There was a problem setting up Embeds (Guild ID: {guild.id}). Error: {e}")
            print(traceback.format_exc())
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.edit_message(message_id=message.id, embed=error, view=None)

    @discord.ui.button(label="Profiles", style=discord.ButtonStyle.blurple, emoji="🪪")
    async def profiles(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message
        guild = interaction.guild
        try:
            if interaction.user == self.user:
                await self.bot.add_cog(Profiles.Profiles(bot=self.bot), override=True, guild=guild)
                if guild.id not in self.guild_cogs:
                    self.guild_cogs[guild.id] = []
                coglist = self.guild_cogs[guild.id]
                if "Profiles" not in coglist:
                    coglist.append("Profiles")
                button.label = "Added"
                button.style = discord.ButtonStyle.gray
                button.emoji = "✅"
                button.disabled = True
                await interaction.followup.edit_message(message_id=message.id, view=self)
        except Exception as e:
            print(f"There was a problem setting up Profiles (Guild ID: {guild.id}). Error: {e}")
            print(traceback.format_exc())
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.edit_message(message_id=message.id, embed=error, view=None)

    @discord.ui.button(label="Purge", style=discord.ButtonStyle.blurple, emoji="🗑️")
    async def purge(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message
        guild = interaction.guild
        try:
            if interaction.user == self.user:
                await self.bot.add_cog(Purge.Purge(bot=self.bot), override=True, guild=guild)
                if guild.id not in self.guild_cogs:
                    self.guild_cogs[guild.id] = []
                coglist = self.guild_cogs[guild.id]
                if "Purge" not in coglist:
                    coglist.append("Purge")
                button.label = "Added"
                button.style = discord.ButtonStyle.gray
                button.emoji = "✅"
                button.disabled = True
                await interaction.followup.edit_message(message_id=message.id, view=self)
        except Exception as e:
            print(f"There was a problem setting up Purge (Guild ID: {guild.id}). Error: {e}")
            print(traceback.format_exc())
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.edit_message(message_id=message.id, embed=error, view=None)

    @discord.ui.button(label="RSS Feeds", style=discord.ButtonStyle.blurple, emoji="📰")
    async def rss_feeds(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message
        guild = interaction.guild
        try:
            if interaction.user == self.user:
                await self.bot.add_cog(RSSFeeds.RSSFeeds(bot=self.bot), override=True, guild=guild)
                if guild.id not in self.guild_cogs:
                    self.guild_cogs[guild.id] = []
                coglist = self.guild_cogs[guild.id]
                if "RSS Feeds" not in coglist:
                    coglist.append("RSS Feeds")
                button.label = "Added"
                button.style = discord.ButtonStyle.gray
                button.emoji = "✅"
                button.disabled = True
                await interaction.followup.edit_message(message_id=message.id, view=self)
        except Exception as e:
            print(f"There was a problem setting up RSS Feeds (Guild ID: {guild.id}). Error: {e}")
            print(traceback.format_exc())
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.edit_message(message_id=message.id, embed=error, view=None)

    @discord.ui.button(label="Tickets", style=discord.ButtonStyle.blurple, emoji="🎫")
    async def rss_feeds(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message
        guild = interaction.guild
        try:
            if interaction.user == self.user:
                await self.bot.add_cog(Tickets.Tickets(bot=self.bot), override=True, guild=guild)
                if guild.id not in self.guild_cogs:
                    self.guild_cogs[guild.id] = []
                coglist = self.guild_cogs[guild.id]
                if "Ticket" not in coglist:
                    coglist.append("Tickets")
                button.label = "Added"
                button.style = discord.ButtonStyle.gray
                button.emoji = "✅"
                button.disabled = True
                await interaction.followup.edit_message(message_id=message.id, view=self)
        except Exception as e:
            print(f"There was a problem setting up Tickets (Guild ID: {guild.id}). Error: {e}")
            print(traceback.format_exc())
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.edit_message(message_id=message.id, embed=error, view=None)

    @discord.ui.button(label="Done", style=discord.ButtonStyle.green)
    async def done(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message
        try:
            if interaction.user == self.user:
                self.value = True
                self.stop()
        except Exception as e:
            print(traceback.format_exc())
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.edit_message(message_id=message.id, embed=error, view=None)

class RemoveButtons(discord.ui.View):
    def __init__(self, *, timeout = 180, bot: commands.Bot, user: discord.Member):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.user = user
        self.value = False
        self.guild_cogs = {}

    @discord.ui.button(label="AutoDelete", style=discord.ButtonStyle.blurple, emoji="♻️")
    async def autodelete(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message
        guild = interaction.guild
        try:
            if interaction.user == self.user:
                await self.bot.remove_cog(AutoDelete.AutoDelete(bot=self.bot), guild=guild)
                if guild.id not in self.guild_cogs:
                    self.guild_cogs[guild.id] = []
                coglist = self.guild_cogs[guild.id]
                if "AutoDelete" not in coglist:
                    coglist.append("AutoDelete")
                button.label = "Removed"
                button.style = discord.ButtonStyle.gray
                button.emoji = "✅"
                button.disabled = True
                await interaction.followup.edit_message(message_id=message.id, view=self)
        except Exception as e:
            print(f"There was a problem removing AutoDelete (Guild ID: {guild.id}). Error: {e}")
            print(traceback.format_exc())
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.edit_message(message_id=message.id, embed=error, view=None)

    @discord.ui.button(label="Awards", style=discord.ButtonStyle.blurple, emoji="🏅")
    async def awards(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message
        guild = interaction.guild
        try:
            if interaction.user == self.user:
                await self.bot.remove_cog(Awards.Awards(bot=self.bot), guild=guild)
                if guild.id not in self.guild_cogs:
                    self.guild_cogs[guild.id] = []
                coglist = self.guild_cogs[guild.id]
                if "Awards" not in coglist:
                    coglist.append("Awards")
                button.label = "Removed"
                button.style = discord.ButtonStyle.gray
                button.emoji = "✅"
                button.disabled = True
                await interaction.followup.edit_message(message_id=message.id, view=self)
        except Exception as e:
            print(f"There was a problem removing Awards (Guild ID: {guild.id}). Error: {e}")
            print(traceback.format_exc())
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.edit_message(message_id=message.id, embed=error, view=None)
    
    @discord.ui.button(label="Embeds", style=discord.ButtonStyle.blurple, emoji="📝")
    async def embeds(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message
        guild = interaction.guild
        try:
            if interaction.user == self.user:
                await self.bot.remove_cog(Embeds.Embeds(bot=self.bot), guild=guild)
                if guild.id not in self.guild_cogs:
                    self.guild_cogs[guild.id] = []
                coglist = self.guild_cogs[guild.id]
                if "Embeds" not in coglist:
                    coglist.append("Embeds")
                button.label = "Removed"
                button.style = discord.ButtonStyle.gray
                button.emoji = "✅"
                button.disabled = True
                await interaction.followup.edit_message(message_id=message.id, view=self)
        except Exception as e:
            print(f"There was a problem removing Embeds (Guild ID: {guild.id}). Error: {e}")
            print(traceback.format_exc())
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.edit_message(message_id=message.id, embed=error, view=None)

    @discord.ui.button(label="Profiles", style=discord.ButtonStyle.blurple, emoji="🪪")
    async def profiles(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message
        guild = interaction.guild
        try:
            if interaction.user == self.user:
                await self.bot.remove_cog(Profiles.Profiles(bot=self.bot), guild=guild)
                if guild.id not in self.guild_cogs:
                    self.guild_cogs[guild.id] = []
                coglist = self.guild_cogs[guild.id]
                if "Profiles" not in coglist:
                    coglist.append("Profiles")
                button.label = "Removed"
                button.style = discord.ButtonStyle.gray
                button.emoji = "✅"
                button.disabled = True
                await interaction.followup.edit_message(message_id=message.id, view=self)
        except Exception as e:
            print(f"There was a problem removing Profiles (Guild ID: {guild.id}). Error: {e}")
            print(traceback.format_exc())
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.edit_message(message_id=message.id, embed=error, view=None)

    @discord.ui.button(label="Purge", style=discord.ButtonStyle.blurple, emoji="🗑️")
    async def purge(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message
        guild = interaction.guild
        try:
            if interaction.user == self.user:
                await self.bot.remove_cog(Purge.Purge(bot=self.bot), guild=guild)
                if guild.id not in self.guild_cogs:
                    self.guild_cogs[guild.id] = []
                coglist = self.guild_cogs[guild.id]
                if "Purge" not in coglist:
                    coglist.append("Purge")
                button.label = "Removed"
                button.style = discord.ButtonStyle.gray
                button.emoji = "✅"
                button.disabled = True
                await interaction.followup.edit_message(message_id=message.id, view=self)
        except Exception as e:
            print(f"There was a problem removing Purge (Guild ID: {guild.id}). Error: {e}")
            print(traceback.format_exc())
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.edit_message(message_id=message.id, embed=error, view=None)

    @discord.ui.button(label="RSS Feeds", style=discord.ButtonStyle.blurple, emoji="📰")
    async def rss_feeds(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message
        guild = interaction.guild
        try:
            if interaction.user == self.user:
                await self.bot.remove_cog(RSSFeeds.RSSFeeds(bot=self.bot), guild=guild)
                if guild.id not in self.guild_cogs:
                    self.guild_cogs[guild.id] = []
                coglist = self.guild_cogs[guild.id]
                if "RSS Feeds" not in coglist:
                    coglist.append("RSS Feeds")
                button.label = "Removed"
                button.style = discord.ButtonStyle.gray
                button.emoji = "✅"
                button.disabled = True
                await interaction.followup.edit_message(message_id=message.id, view=self)
        except Exception as e:
            print(f"There was a problem removing RSS Feeds (Guild ID: {guild.id}). Error: {e}")
            print(traceback.format_exc())
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.edit_message(message_id=message.id, embed=error, view=None)

    @discord.ui.button(label="Tickets", style=discord.ButtonStyle.blurple, emoji="🎫")
    async def rss_feeds(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message
        guild = interaction.guild
        try:
            if interaction.user == self.user:
                await self.bot.remove_cog(Tickets.Tickets(bot=self.bot), guild=guild)
                if guild.id not in self.guild_cogs:
                    self.guild_cogs[guild.id] = []
                coglist = self.guild_cogs[guild.id]
                if "Ticket" not in coglist:
                    coglist.append("Tickets")
                button.label = "Removed"
                button.style = discord.ButtonStyle.gray
                button.emoji = "✅"
                button.disabled = True
                await interaction.followup.edit_message(message_id=message.id, view=self)
        except Exception as e:
            print(f"There was a problem removing Tickets (Guild ID: {guild.id}). Error: {e}")
            print(traceback.format_exc())
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.edit_message(message_id=message.id, embed=error, view=None)

    @discord.ui.button(label="Done", style=discord.ButtonStyle.green)
    async def done(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message
        try:
            if interaction.user == self.user:
                self.value = True
                self.stop()
        except Exception as e:
            print(traceback.format_exc())
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.edit_message(message_id=message.id, embed=error, view=None)

class Start(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.database

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
        try:
            
            # Add guild to database if needed
            await self.db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild.id,))
            await self.db.commit()

            # Ask user to select default channels
            start = discord.Embed(
                color=self.bot.blurple,
                title="Bot Startup",
                description="Would you like to start by choosing channels for bot logging messages, member welcome messages, or member goodbye messages?"
            )
            channels_yn = YesOrNo(user=author)
            response = await ctx.send(content=None, embed=start, view=channels_yn)
            await channels_yn.wait()

            # User wants to select logging, welcome, and/or goodbye channels
            if channels_yn.value == True:

                # Ask user to select a logging channel
                ask_logging = discord.Embed(
                    color=self.bot.blurple,
                    title="Logging Channel",
                    description="Would you like to select a channel to send logging messages?\nChoose `Cancel` to skip to the next option."
                )
                logging_select = ChannelSelectView(user=author)
                response = await response.edit(content=None, embed=ask_logging, view=logging_select)
                await logging_select.wait()

                # User selects a logging channel
                if logging_select.value == True:
                    logging_channel = logging_select.channel
                    response = await response.edit(content=f"The logging channel has been set to {logging_channel.mention}.", embed=None, view=None)
                    await self.db.execute("UPDATE guilds SET logging_channel_id = ? WHERE guild_id = ?", (logging_channel.id, guild.id))
                    await self.db.commit()
                    await asyncio.sleep(3.0)

                    # Bot sends a log to the logging channel
                    cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                    row = await cur.fetchone()
                    fetched_logging = row[0]
                    if fetched_logging is not None:
                        logging_channel = await guild.fetch_channel(fetched_logging)
                        log = discord.Embed(
                            color=self.bot.blurple,
                            title="Bot Startup Log",
                            description=f"{author.mention} has just set the server's logging channel to {logging_channel.mention}!",
                            timestamp=timestamp
                        )
                        log.set_author(name=author.display_name, icon_url=author.display_avatar)
                        await logging_channel.send(content=None, embed=log)

                # Ask user to select a welcome channel
                ask_welcome = discord.Embed(
                    color=self.bot.blurple,
                    title="Welcome Channel",
                    description="Would you like to select a channel to send welcome messages?\nChoose `Cancel` to skip to the next option."
                )
                welcome_select = ChannelSelectView(user=author)
                response = await response.edit(content=None, embed=ask_welcome, view=welcome_select)
                await welcome_select.wait()

                # User selects a welcome channel
                if welcome_select.value == True:
                    welcome_channel = welcome_select.channel
                    response = await response.edit(content=f"The welcome channel has been set to {welcome_channel.mention}.", embed=None, view=None)
                    await self.db.execute("UPDATE guilds SET welcome_channel_id = ? WHERE guild_id = ?", (welcome_channel.id, guild.id))
                    await self.db.commit()
                    await asyncio.sleep(3.0)

                    # Bot sends a log to the logging channel
                    cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                    row = await cur.fetchone()
                    fetched_logging = row[0]
                    if fetched_logging is not None:
                        logging_channel = await guild.fetch_channel(fetched_logging)
                        log = discord.Embed(
                            color=self.bot.blurple,
                            title="Bot Startup Log",
                            description=f"{author.mention} has just set the server's welcome channel to {welcome_channel.mention}!",
                            timestamp=timestamp
                        )
                        log.set_author(name=author.display_name, icon_url=author.display_avatar)
                        await logging_channel.send(content=None, embed=log)
                    
                # Ask user to select a goodbye channel
                ask_goodbye = discord.Embed(
                    color=self.bot.blurple,
                    title="Goodbye Channel",
                    description="Would you like to select a channel to send goodbye messages?\nChoose `Cancel` to skip to the next option."
                )
                goodbye_select = ChannelSelectView(user=author)
                response = await response.edit(content=None, embed=ask_goodbye, view=goodbye_select)
                await goodbye_select.wait()

                # User selects a goodbye channel
                if goodbye_select.value == True:
                    goodbye_channel = goodbye_select.channel
                    response = await response.edit(content=f"The goodbye channel has been set to {goodbye_channel.mention}.", embed=None, view=None)
                    await self.db.execute("UPDATE guilds SET goodbye_channel_id = ? WHERE guild_id = ?", (goodbye_channel.id, guild.id))
                    await self.db.commit()
                    await asyncio.sleep(3.0)

                    # Bot sends a log to the logging channel
                    cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                    row = await cur.fetchone()
                    fetched_logging = row[0]
                    if fetched_logging is not None:
                        logging_channel = await guild.fetch_channel(fetched_logging)
                        log = discord.Embed(
                            color=self.bot.blurple,
                            title="Bot Startup Log",
                            description=f"{author.mention} has just set the server's goodbye channel to {goodbye_channel.mention}!",
                            timestamp=timestamp
                        )
                        log.set_author(name=author.display_name, icon_url=author.display_avatar)
                        await logging_channel.send(content=None, embed=log)
            
            # Ask the user to select join roles
            start = discord.Embed(
                color=self.bot.blurple,
                title="Bot Startup",
                description="Would you like to choose join roles?"
            )
            join_yn = YesOrNo(user=author)
            response = await response.edit(content=None, embed=start, view=join_yn)
            await join_yn.wait()

            # User wants to select join roles
            if join_yn.value == True:

                # Ask user to select a join role
                ask_join_role = discord.Embed(
                    color=self.bot.blurple,
                    title="Join Role",
                    description="Would you like to select a role to give members on join?\nChoose `Cancel` to skip to the next option."
                )
                join_select = RoleSelectView(user=author)
                response = await response.edit(content=None, embed=ask_join_role, view=join_select)
                await join_select.wait()

                # User selects a join role
                if join_select.value == True:
                    join_role = join_select.role
                    response = await response.edit(content=f"The join role was set to {join_role.mention}.", embed=None, view=None)
                    await self.db.execute("UPDATE guilds SET join_role_id = ? WHERE guild_id = ?", (join_role.id, guild.id))
                    await self.db.commit()
                    await asyncio.sleep(3.0)

                    # Bot sends a log to the logging channel
                    cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                    row = await cur.fetchone()
                    fetched_logging = row[0]
                    if fetched_logging is not None:
                        logging_channel = await guild.fetch_channel(fetched_logging)
                        log = discord.Embed(
                            color=self.bot.blurple,
                            title="Bot Startup Log",
                            description=f"{author.mention} has just set the server's join role to {join_role.mention}!",
                            timestamp=timestamp
                        )
                        log.set_author(name=author.display_name, icon_url=author.display_avatar)
                        await logging_channel.send(content=None, embed=log)

                # Ask user to select a bot role
                ask_bot_role = discord.Embed(
                    color=self.bot.blurple,
                    title="Bot Role",
                    description="Would you like to select a role to give bots on join?\nChoose `Cancel` to skip to the next option."
                )
                bot_select = RoleSelectView(user=author)
                response = await response.edit(content=None, embed=ask_bot_role, view=bot_select)
                await bot_select.wait()

                # User selects a bot role
                if bot_select.value == True:
                    bot_role = bot_select.role
                    response = await response.edit(content=f"The bot role was set to {bot_role.mention}.", embed=None, view=None)
                    await self.db.execute("UPDATE guilds SET bot_role_id = ? WHERE guild_id = ?", (bot_role.id, guild.id))
                    await self.db.commit()
                    await asyncio.sleep(3.0)

                    # Bot sends a log to the logging channel
                    cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                    row = await cur.fetchone()
                    fetched_logging = row[0]
                    if fetched_logging is not None:
                        logging_channel = await guild.fetch_channel(fetched_logging)
                        log = discord.Embed(
                            color=self.bot.blurple,
                            title="Bot Startup Log",
                            description=f"{author.mention} has just set the server's bot role to {bot_role.mention}!",
                            timestamp=timestamp
                        )
                        log.set_author(name=author.display_name, icon_url=author.display_avatar)
                        await logging_channel.send(content=None, embed=log)
            
            # Ask the user to select activity roles
            start = discord.Embed(
                color=self.bot.blurple,
                title="Bot Startup",
                description="Would you like to choose activity roles?"
            )
            activity_yn = YesOrNo(user=author)
            response = await response.edit(content=None, embed=start, view=activity_yn)
            await activity_yn.wait()

            # User wants to select activity roles
            if activity_yn.value == True:

                # Ask user to select an active role
                ask_active_role = discord.Embed(
                    color=self.bot.blurple,
                    title="Active Role",
                    description="Would you like to select a role to give active members?\nChoose `Cancel` to skip to the next option."
                )
                active_select = RoleSelectView(user=author)
                response = await response.edit(content=None, embed=ask_active_role, view=active_select)
                await active_select.wait()

                # User selects an active role
                if active_select.value == True:
                    active_role = active_select.role
                    response = await response.edit(content=f"The active role was set to {active_role.mention}.", embed=None, view=None)
                    await self.db.execute("UPDATE guilds SET active_role_id = ? WHERE guild_id = ?", (active_role.id, guild.id))
                    await self.db.commit()
                    await asyncio.sleep(3.0)

                    # Bot sends a log to the logging channel
                    cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                    row = await cur.fetchone()
                    fetched_logging = row[0]
                    if fetched_logging is not None:
                        logging_channel = await guild.fetch_channel(fetched_logging)
                        log = discord.Embed(
                            color=self.bot.blurple,
                            title="Bot Startup Log",
                            description=f"{author.mention} has just set the server's active member role to {active_role.mention}!",
                            timestamp=timestamp
                        )
                        log.set_author(name=author.display_name, icon_url=author.display_avatar)
                        await logging_channel.send(content=None, embed=log)

                # Ask user to select an inactive role
                ask_inactive_role = discord.Embed(
                    color=self.bot.blurple,
                    title="Inactive Role",
                    description="Would you like to select a role to give to inactive members?\nChoose `Cancel` to skip to the next option."
                )
                inactive_select = RoleSelectView(user=author)
                response = await response.edit(content=None, embed=ask_inactive_role, view=inactive_select)
                await inactive_select.wait()

                # User selects an inactive role
                if inactive_select.value == True:
                    inactive_role = inactive_select.role
                    response = await response.edit(content=f"The inactive role was set to {inactive_role.mention}.", embed=None, view=None)
                    await self.db.execute("UPDATE guilds SET inactive_role_id = ? WHERE guild_id = ?", (inactive_role.id, guild.id))
                    await self.db.commit()
                    await asyncio.sleep(3.0)

                    # Bot sends a log to the logging channel
                    cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                    row = await cur.fetchone()
                    fetched_logging = row[0]
                    if fetched_logging is not None:
                        logging_channel = await guild.fetch_channel(fetched_logging)
                        log = discord.Embed(
                            color=self.bot.blurple,
                            title="Bot Startup Log",
                            description=f"{author.mention} has just set the server's inactive role to {inactive_role.mention}!",
                            timestamp=timestamp
                        )
                        log.set_author(name=author.display_name, icon_url=author.display_avatar)
                        await logging_channel.send(content=None, embed=log)

                # Ask user to provide inactive months
                ask_inactive_months = discord.Embed(
                    color=self.bot.blurple,
                    title="Inactive Months",
                    description="How many months should a member be inactive before recieving the inactive role?\nChoose `Cancel` to skip to the next option."
                )
                months_select = InactiveMonthsView(user=author)
                response = await response.edit(content=None, embed=ask_inactive_months, view=months_select)
                await months_select.wait()

                # User selects an inactive months
                if months_select.value == True:
                    inactive_months = int(months_select.months)
                    response = await response.edit(content=f"The inactive month amount was set to {str(inactive_months)}.", embed=None, view=None)
                    await self.db.execute("UPDATE guilds SET inactive_months = ? WHERE guild_id = ?", (inactive_months, guild.id))
                    await self.db.commit()
                    await asyncio.sleep(3.0)

                    # Bot sends a log to the logging channel
                    cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                    row = await cur.fetchone()
                    fetched_logging = row[0]
                    if fetched_logging is not None:
                        logging_channel = await guild.fetch_channel(fetched_logging)
                        log = discord.Embed(
                            color=self.bot.blurple,
                            title="Bot Startup Log",
                            description=f"{author.mention} has just set the server's inactive month amount to {str(inactive_months)}!",
                            timestamp=timestamp
                        )
                        log.set_author(name=author.display_name, icon_url=author.display_avatar)
                        await logging_channel.send(content=None, embed=log)
            
            # Ask the user to select which cogs to add to their server
            ask_cogs = discord.Embed(
                color=self.bot.blurple,
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
            cog_buttons = CogButtons(bot=self.bot, user=author)
            response = await response.edit(content=None, embed=ask_cogs, view=cog_buttons)
            await cog_buttons.wait()

            if cog_buttons.value == True:

                # The user has now completed bot startup for their server
                await self.bot.tree.sync(guild=guild)
                cogs = cog_buttons.guild_cogs[guild.id]
                join = ", ".join(cogs)
                done = discord.Embed(
                    color=self.bot.blurple,
                    title="Bot Startup",
                    description=f"Bot startup is now complete!"
                )
                done.add_field(name="Commands Added", value=f"{join}")
                response = await response.edit(content=None, embed=done, view=None)

                # Bot sends a log to the logging channel
                cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                row = await cur.fetchone()
                fetched_logging = row[0]
                if fetched_logging is not None:
                    logging_channel = await guild.fetch_channel(fetched_logging)
                    log = discord.Embed(
                        color=self.bot.blurple,
                        title="Bot Startup Log",
                        description=f"{author.mention} has just added commands to {guild.name}!",
                        timestamp=timestamp
                    )
                    log.set_author(name=author.display_name, icon_url=author.display_avatar)
                    log.add_field(name="Commands Added", value=f"{join}")
                    await logging_channel.send(content=None, embed=log)

        # Send an error message if there's an issue
        except Exception as e:
            print(f"Start Command Error (Guild ID: {guild.id}): {e}")
            print(traceback.format_exc())
            error = discord.Embed(
                color=self.bot.red,
                title="Error",
                description=f"There was an error running the `/start` or `rb!start` command. Error: {e}"
            )
            response = await response.edit(content=None, embed=error, view=None)

    @commands.hybrid_command(name="add_commands")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def add_commands(self, ctx: commands.Context):
        """(Admin Only) Add desired commands to the server.
        """
        await ctx.defer()
        guild = ctx.guild
        author = ctx.author
        timestamp = datetime.now(tz=timezone.utc)
        response = None
        try:
            
            # Add the guild to the database if needed
            await self.db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild.id,))
            await self.db.commit()
            
            ask_cogs = discord.Embed(
                color=self.bot.blurple,
                title="Add Commands",
                description="Choose which commands you would like to add to your server."
            )
            ask_cogs.add_field(name="AutoDelete", value="These commands allow you to set the messages in a channel to be automatically deleted on a rolling basis.", inline=False)
            ask_cogs.add_field(name="Awards", value="These commands allow you to set up an awards system in your server. The award name and emoji can be customized.", inline=False)
            ask_cogs.add_field(name="Embeds", value="These commands allow you to send and edit messages containing embeds.", inline=False)
            ask_cogs.add_field(name="Profiles", value="These commands allow you and your server members to set up member profiles that can be viewed and edited.", inline=False)
            ask_cogs.add_field(name="Purge", value="These commands allow you to easily mass-delete messages in a single channel or in multiple channels at once.", inline=False)
            ask_cogs.add_field(name="RSS Feeds", value="These commands allow you to easily assign and unassign RSS feeds to Webhooks to post new entries automatically.", inline=False)
            ask_cogs.add_field(name="Tickets", value="These commands allow you to set up a simple ticketing system for your server using threads.", inline=False)
            cog_buttons = CogButtons(bot=self.bot, user=author)
            response = await ctx.send(embed=ask_cogs, view=cog_buttons)
            await cog_buttons.wait()

            if cog_buttons.value == True:

                await self.bot.tree.sync(guild=guild)
                cogs = cog_buttons.guild_cogs[guild.id]
                join = ", ".join(cogs)
                done = discord.Embed(
                    color=self.bot.green,
                    title="Success",
                    description=f"{author.mention} has successfully added commands to the server!"
                )
                done.add_field(name="Commands Added", value=f"{join}")
                response = await response.edit(embed=done, view=None)

                cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                row = await cur.fetchone()
                fetched_logging = row[0]
                if fetched_logging is not None:
                    logging_channel = await guild.fetch_channel(fetched_logging)
                    log = discord.Embed(
                        color=self.bot.red,
                        title="Add Commands",
                        description=f"{author.mention} has just added commands to {guild.name}!",
                        timestamp=timestamp
                    )
                    log.set_author(name=author.display_name, icon_url=author.display_avatar)
                    log.add_field(name="Commands Added", value=f"{join}")
                    await logging_channel.send(embed=log)
                
        except Exception as e:
            print(f"Start Command Error (Guild ID: {guild.id}): {e}")
            print(traceback.format_exc())
            error = discord.Embed(
                color=self.bot.red,
                title="Error",
                description=f"There was an error running the `/add_commands` or `rb!add_commands` command. Error: {e}"
            )
            if response is not None:
                await response.edit(embed=error, view=None)
            else:
                await ctx.send(embed=error, view=None)

    @commands.hybrid_command(name="remove_commands")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def remove_commands(self, ctx: commands.Context):
        """(Admin Only) Remove unwanted commands from the server.
        """
        await ctx.defer()
        guild = ctx.guild
        author = ctx.author
        timestamp = datetime.now(tz=timezone.utc)
        response = None
        try:

            # Add the bot to the database if needed
            await self.db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild.id,))
            await self.db.commit()
            
            ask_cogs = discord.Embed(
                color=self.bot.blurple,
                title="Remove Commands",
                description="Choose which commands you would like to remove from your server."
            )
            ask_cogs.add_field(name="AutoDelete", value="These commands allow you to set the messages in a channel to be automatically deleted on a rolling basis.", inline=False)
            ask_cogs.add_field(name="Awards", value="These commands allow you to set up an awards system in your server. The award name and emoji can be customized.", inline=False)
            ask_cogs.add_field(name="Embeds", value="These commands allow you to send and edit messages containing embeds.", inline=False)
            ask_cogs.add_field(name="Profiles", value="These commands allow you and your server members to set up member profiles that can be viewed and edited.", inline=False)
            ask_cogs.add_field(name="Purge", value="These commands allow you to easily mass-delete messages in a single channel or in multiple channels at once.", inline=False)
            ask_cogs.add_field(name="RSS Feeds", value="These commands allow you to easily assign and unassign RSS feeds to Webhooks to post new entries automatically.", inline=False)
            ask_cogs.add_field(name="Tickets", value="These commands allow you to set up a simple ticketing system for your server using threads.", inline=False)
            cog_buttons = RemoveButtons(bot=self.bot, user=author)
            response = await ctx.send(embed=ask_cogs, view=cog_buttons)
            await cog_buttons.wait()

            if cog_buttons.value == True:

                await self.bot.tree.sync(guild=guild)
                cogs = cog_buttons.guild_cogs[guild.id]
                join = ", ".join(cogs)
                done = discord.Embed(
                    color=self.bot.green,
                    title="Success",
                    description=f"{author.mention} has successfully removed commands from the server!"
                )
                done.add_field(name="Commands Removed", value=f"{join}")
                response = await response.edit(embed=done, view=None)

                cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                row = await cur.fetchone()
                fetched_logging = row[0]
                if fetched_logging is not None:
                    logging_channel = await guild.fetch_channel(fetched_logging)
                    log = discord.Embed(
                        color=self.bot.red,
                        title="Remove Commands",
                        description=f"{author.mention} has just removed commands from {guild.name}!",
                        timestamp=timestamp
                    )
                    log.set_author(name=author.display_name, icon_url=author.display_avatar)
                    log.add_field(name="Commands Removed", value=f"{join}")
                    await logging_channel.send(embed=log)
                
        except Exception as e:
            print(f"Start Command Error (Guild ID: {guild.id}): {e}")
            print(traceback.format_exc())
            error = discord.Embed(
                color=self.bot.red,
                title="Error",
                description=f"There was an error running the `/remove_commands` or `rb!remove_commands` command. Error: {e}"
            )
            if response is not None:
                await response.edit(embed=error, view=None)
            else:
                await ctx.send(embed=error, view=None)

async def setup(bot: commands.Bot):
    await bot.add_cog(Start(bot=bot), override=True)

async def teardown(bot: commands.Bot):
    await bot.remove_cog("Start")