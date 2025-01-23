import discord
import aiosqlite
import traceback
from discord import app_commands
from discord.ext import commands, tasks
from typing import Optional
from datetime import datetime, timezone

class YesOrNo(discord.ui.View):
    def __init__(self, *, timeout = 180, user: discord.Member):
        super().__init__(timeout=timeout)
        self.user = user
        self.value = None

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, emoji="👍", row=1)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.red, emoji="👎", row=1)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = False
            self.stop()

class Singular(discord.ui.Modal):
    def __init__(self, *, title = "Singular", timeout = 180.0, bot: commands.Bot, user: discord.Member):
        super().__init__(title=title, timeout=timeout)
        self.bot = bot
        self.user = user
        self.value = None
        self.error = None
    
    singular = discord.ui.TextInput(label="Singular", custom_id="singular_input", placeholder="Enter a cutom name (singular) for you server awards...")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.stop()

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.defer()
        self.value = False
        self.error = error
        self.stop()
        print(traceback.format_exc())
    
    async def on_timeout(self):
        self.value = False
        self.stop()

class SingularView(discord.ui.View):
    def __init__(self, *, timeout = 180, bot: commands.Bot, user: discord.Member):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.user = user
        if isinstance(bot.database, aiosqlite.Connection):
            self.db = bot.database
        self.value = None

    @discord.ui.button(label="Set Custom Award Name (Singular)", style=discord.ButtonStyle.blurple, row=1)
    async def singular(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = Singular(bot=self.bot, user=self.user)
        await interaction.response.send_modal(modal)
        await modal.wait()

        if modal.value == True:

            guild = interaction.guild
            user = interaction.user

            # Set and fetch server award name (singular)
            singular = modal.singular.value
            sing_low = singular.lower()
            await self.db.execute("UPDATE guilds SET award_singular = ? WHERE guild_id = ?", (sing_low, guild.id))
            await self.db.commit()
            cur = await self.db.execute("SELECT award_singular FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            fetched_sing_low = str(row[0])
            fetched_sing_cap = fetched_sing_low.title()
            
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
                        title="Awards Log",
                        description=f"{user.mention} has successfully set the server's custom award name (singular)!",
                        timestamp=now
                    )
                    log.add_field(name="Singular (Capitalized)", value=f"{fetched_sing_cap}")
                    log.add_field(name="Singular (Lowercase)", value=f"{fetched_sing_low}")
                    log.set_author(name=user.display_name, icon_url=user.display_avatar)
                    log.set_thumbnail(url=user.display_avatar)
                    await logging_channel.send(embed=log)
                else:
                    error = discord.Embed(
                        color=self.bot.red,
                        title="Logging Channel Not Found",
                        description=f"A logging channel with the ID {fetched_logging} was not found! Please set a new logging channel by re-running the `/start` command.",
                        timestamp=now
                    )
                    log_error = await interaction.followup.send(embed=error, wait=True)
                    await log_error.delete(delay=10.0)

        if modal.value == False:
            error = discord.Embed(
                color=self.bot.red,
                title="Error",
                description="There was a problem. Please try again later."
            )
            await interaction.message.edit(embed=error, delete_after=5.0, view=None)
        
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red, row=1)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            # Ask the user if they are sure they want to cancel
            embed = discord.Embed(
                color=self.bot.red,
                title="Cancel",
                description="Are you sure you want to cancel?")
            view = YesOrNo(user=interaction.user)
            cancel = await interaction.followup.send(wait=True, embed=embed, view=view)
            await view.wait()

            if view.value == True:
                await interaction.message.delete()
                await cancel.delete()
                self.stop()
            
            if view.value == False:
                await cancel.delete()

class Plural(discord.ui.Modal):
    def __init__(self, *, title = "Plural", timeout = 180.0, bot: commands.Bot, user: discord.Member):
        super().__init__(title=title, timeout=timeout)
        self.bot = bot
        self.user = user
        self.value = None
        self.error = None
    
    plural = discord.ui.TextInput(label="Plural", custom_id="plural_input", placeholder="Enter a cutom name (plural) for you server awards...")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.stop()

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.defer()
        self.value = False
        self.error = error
        self.stop()
        print(traceback.format_exc())
    
    async def on_timeout(self):
        self.value = False
        self.stop()

class PluralView(discord.ui.View):
    def __init__(self, *, timeout = 180, bot: commands.Bot, user: discord.Member):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.user = user
        if isinstance(bot.database, aiosqlite.Connection):
            self.db = bot.database
        self.value = None

    @discord.ui.button(label="Set Custom Award Name (Plural)", style=discord.ButtonStyle.blurple, row=1)
    async def plural(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = Plural(bot=self.bot, user=self.user)
        await interaction.response.send_modal(modal)
        await modal.wait()

        if modal.value == True:

            guild = interaction.guild
            user = interaction.user

            # Set and fetch server award name (plural)
            plural = modal.plural.value
            plur_low = plural.lower()
            await self.db.execute("UPDATE guilds SET award_plural = ? WHERE guild_id = ?", (plur_low, guild.id))
            await self.db.commit()
            cur = await self.db.execute("SELECT award_plural FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            fetched_plur_low = str(row[0])
            fetched_plur_cap = fetched_plur_low.title()
            
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
                        title="Awards Log",
                        description=f"{user.mention} has successfully set the server's custom award name (plural)!",
                        timestamp=now
                    )
                    log.add_field(name="Plural (Capitalized)", value=f"{fetched_plur_cap}")
                    log.add_field(name="Plural (Lowercase)", value=f"{fetched_plur_low}")
                    log.set_author(name=user.display_name, icon_url=user.display_avatar)
                    log.set_thumbnail(url=user.display_avatar)
                    await logging_channel.send(embed=log)
                else:
                    error = discord.Embed(
                        color=self.bot.red,
                        title="Logging Channel Not Found",
                        description=f"A logging channel with the ID {fetched_logging} was not found! Please set a new logging channel by re-running the `/start` command.",
                        timestamp=now
                    )
                    log_error = await interaction.followup.send(embed=error, wait=True)
                    await log_error.delete(delay=10.0)

        if modal.value == False:
            error = discord.Embed(
                color=self.bot.red,
                title="Error",
                description="There was a problem. Please try again later."
            )
            await interaction.message.edit(embed=error, delete_after=5.0, view=None)
        
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red, row=1)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            # Ask the user if they are sure they want to cancel
            embed = discord.Embed(
                color=self.bot.red,
                title="Cancel",
                description="Are you sure you want to cancel?")
            view = YesOrNo(user=interaction.user)
            cancel = await interaction.followup.send(wait=True, embed=embed, view=view)
            await view.wait()

            if view.value == True:
                await interaction.message.delete()
                await cancel.delete()
                self.stop()
            
            if view.value == False:
                await cancel.delete()

class Emoji(discord.ui.Modal):
    def __init__(self, *, title = "Emoji", timeout = 180.0, bot: commands.Bot, user: discord.Member):
        super().__init__(title=title, timeout=timeout)
        self.bot = bot
        self.user = user
        self.value = None
    
    emoji = discord.ui.TextInput(label="Emoji", custom_id="emoji_input", placeholder="Enter a cutom emoji for you server awards...")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.stop()

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.defer()
        self.value = False
        self.error = error
        self.stop()
        print(traceback.format_exc())
    
    async def on_timeout(self):
        self.value = False
        self.stop()

class EmojiView(discord.ui.View):
    def __init__(self, *, timeout = 180, bot: commands.Bot, user: discord.Member):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.user = user
        if isinstance(bot.database, aiosqlite.Connection):
            self.db = bot.database
        self.value = None

    @discord.ui.button(label="Set Custom Award Emoji", style=discord.ButtonStyle.blurple, row=1)
    async def emoji(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = Emoji(bot=self.bot, user=self.user)
        await interaction.response.send_modal(modal)
        await modal.wait()

        if modal.value == True:

            guild = interaction.guild
            user = interaction.user

            # Set and fetch server award emoji
            emoji = modal.emoji.value
            await self.db.execute("UPDATE guilds SET award_emoji = ? WHERE guild_id = ?", (emoji, guild.id))
            await self.db.commit()
            cur = await self.db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            fetched_emoji = row[0]
            
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
                        title="Awards Log",
                        description=f"{user.mention} has successfully set the server's custom award emoji!",
                        timestamp=now)
                    log.add_field(name="Emoji", value=f"{fetched_emoji}")
                    log.set_author(name=user.display_name, icon_url=user.display_avatar)
                    log.set_thumbnail(url=user.display_avatar)
                    await logging_channel.send(embed=log)
                else:
                    error = discord.Embed(
                        color=self.bot.red,
                        title="Logging Channel Not Found",
                        description=f"A logging channel with the ID {fetched_logging} was not found! Please set a new logging channel by re-running the `/start` command.",
                        timestamp=now
                    )
                    log_error = await interaction.followup.send(embed=error, wait=True)
                    await log_error.delete(delay=10.0)

        if modal.value == False:
            error = discord.Embed(
                color=self.bot.red,
                title="Error",
                description="There was a problem. Please try again later.")
            await interaction.message.edit(embed=error, delete_after=5.0, view=None)
        
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red, row=1)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            # Ask the user if they are sure they want to cancel
            embed = discord.Embed(
                color=self.bot.red,
                title="Cancel",
                description="Are you sure you want to cancel?")
            view = YesOrNo(user=interaction.user)
            cancel = await interaction.followup.send(wait=True, embed=embed, view=view)
            await view.wait()

            if view.value == True:
                await interaction.message.delete()
                await cancel.delete()
                self.stop()
            
            if view.value == False:
                await cancel.delete()

class Leaderboard(discord.ui.ChannelSelect):
    def __init__(self, *, user: discord.Member):
        super().__init__(
            channel_types=[discord.ChannelType.text],
            placeholder="Choose a channel...",
            min_values=1,
            max_values=1,
            row=1
        )
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if interaction.user == self.user:
            channel = self.values[0]
            self.channel = channel.resolve()

class LeaderboardView(discord.ui.View):
    def __init__(self, *, timeout = 180, bot: commands.Bot, user: discord.Member):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.user = user
        if isinstance(bot.database, aiosqlite.Connection):
            self.db = bot.database
        self.select = Leaderboard(user=self.user)
        self.add_item(self.select)

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green, row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            guild = interaction.guild
            channel = self.select.channel
            user = interaction.user

            if isinstance(channel, discord.TextChannel):

                # Set and fetch the leaderboard channel
                await self.db.execute("UPDATE guilds SET leaderboard_channel_id = ? WHERE guild_id = ?", (channel.id, guild.id))
                await self.db.commit()
                cur = await self.db.execute("SELECT leaderboard_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                row = await cur.fetchone()
                fetched_channel_id = row[0]
                fetched_channel = guild.get_channel(fetched_channel_id)

                if isinstance(fetched_channel, discord.TextChannel):
                    
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
                                title="Awards Log",
                                description=f"{user.mention} has successfully set the server's award leaderboard channel!",
                                timestamp=now
                            )
                            log.add_field(name="Channel", value=f"{fetched_channel.mention}")
                            log.set_author(name=user.display_name, icon_url=user.display_avatar)
                            log.set_thumbnail(url=user.display_avatar)
                            await logging_channel.send(embed=log)
                        else:
                            error = discord.Embed(
                                color=self.bot.red,
                                title="Logging Channel Not Found",
                                description=f"A logging channel with the ID {fetched_logging} was not found! Please set a new logging channel by re-running the `/start` command.",
                                timestamp=now
                            )
                            log_error = await interaction.followup.send(embed=error, wait=True)
                            await log_error.delete(delay=10.0)

            self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red, row=2)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            # Ask the user if they are sure they want to cancel
            embed = discord.Embed(
                color=self.bot.red,
                title="Cancel",
                description="Are you sure you want to cancel?")
            view = YesOrNo(user=interaction.user)
            cancel = await interaction.followup.send(wait=True, embed=embed, view=view)
            await view.wait()

            if view.value == True:
                await interaction.message.delete()
                await cancel.delete()
                self.stop()
            
            if view.value == False:
                await cancel.delete()

class AwardReaction(discord.ui.Select):
    def __init__(self, *, user: discord.Member):
        options = [
            discord.SelectOption(label="True"),
            discord.SelectOption(label="False")
        ]
        super().__init__(
            min_values=1,
            max_values=1,
            options=options,
            row=1
        )
        self.user = user
        self.toggle = None

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if interaction.user == self.user:
            if self.values[0] == "True":
                self.toggle = True
            elif self.values[0] == "False":
                self.toggle = False
            else:
                self.toggle = None

class AwardReactionView(discord.ui.View):
    def __init__(self, *, timeout = 180, bot: commands.Bot, user: discord.Member):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.user = user
        if isinstance(bot.database, aiosqlite.Connection):
            self.db = bot.database
        self.select = AwardReaction(user=self.user)
        self.add_item(self.select)

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green, row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            guild = interaction.guild
            user = interaction.user

            toggle = self.select.toggle
            self.toggle = None

            if toggle == True:
                await self.db.execute("UPDATE guilds SET award_react_toggle = 1 WHERE guild_id = ?", (guild.id,))
                await self.db.commit()
                self.toggle = "True"
            
            else:
                await self.db.execute("UPDATE guilds SET award_react_toggle = 0 WHERE guild_id = ?", (guild.id,))
                await self.db.commit()
                self.toggle = "False"
            
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
                        title="Awards Log",
                        description=f"{user.mention} has successfully set the server's award reaction toggle!",
                        timestamp=now
                    )
                    log.add_field(name="Toggle", value=f"{self.toggle}")
                    log.set_author(name=user.display_name, icon_url=user.display_avatar)
                    log.set_thumbnail(url=user.display_avatar)
                    await logging_channel.send(embed=log)
                else:
                    error = discord.Embed(
                        color=self.bot.red,
                        title="Logging Channel Not Found",
                        description=f"A logging channel with the ID {fetched_logging} was not found! Please set a new logging channel by re-running the `/start` command.",
                        timestamp=now
                    )
                    log_error = await interaction.followup.send(embed=error, wait=True)
                    await log_error.delete(delay=10.0)
            
            self.stop()
    
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red, row=2)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            # Ask the user if they are sure they want to cancel
            embed = discord.Embed(
                color=self.bot.red,
                title="Cancel",
                description="Are you sure you want to cancel?")
            view = YesOrNo(user=interaction.user)
            cancel = await interaction.followup.send(wait=True, embed=embed, view=view)
            await view.wait()

            if view.value == True:
                await interaction.message.delete()
                await cancel.delete()
                self.stop()
            
            if view.value == False:
                await cancel.delete()

class Awards(commands.GroupCog, group_name = "awards"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        if isinstance(bot.database, aiosqlite.Connection):
            self.db = bot.database

    async def fetch_singular(self, guild: discord.Guild):
        try:
            await self.db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild.id,))
            await self.db.commit()
            cur = await self.db.execute("SELECT award_singular FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            singular = row[0]
            if isinstance(singular, str):
                return singular
            else:
                singular = "awards"
                return singular
        except Exception:
            traceback.print_exc()
            return Exception

    async def fetch_plural(self, guild: discord.Guild):
        try:
            await self.db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild.id,))
            await self.db.commit()
            cur = await self.db.execute("SELECT award_plural FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            plural = row[0]
            if isinstance(plural, str):
                return plural
            else:
                plural = "awards"
                return plural
        except Exception:
            traceback.print_exc()
            return Exception
    
    async def fetch_emoji(self, guild: discord.Guild):
        try:
            await self.db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild.id,))
            await self.db.commit()
            cur = await self.db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            emoji = row[0]
            if isinstance(emoji, str):
                return emoji
            else:
                emoji = "🏅"
                return emoji
        except Exception:
            traceback.print_exc()
            return Exception
    
    async def fetch_leaderboard(self, guild: discord.Guild):
        try:
            await self.db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild.id,))
            await self.db.commit()
            cur = await self.db.execute("SELECT leaderboard_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            leaderboard_id = row[0]
            if isinstance(leaderboard_id, int):
                leaderboard = guild.get_channel(leaderboard_id)
                if isinstance(leaderboard, discord.TextChannel):
                    return leaderboard
            else:
                return None
        except Exception:
            traceback.print_exc()
            return Exception
    
    async def fetch_toggle(self, guild: discord.Guild):
        try:
            await self.db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild.id,))
            await self.db.commit()
            cur = await self.db.execute("SELECT award_react_toggle FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            fetched_toggle = row[0]
            if isinstance(fetched_toggle, int):
                if fetched_toggle == 1:
                    toggle = True
                    return toggle
                elif fetched_toggle == 0:
                    toggle = False
                    return toggle
                else:
                    return None
            else:
                return None
        except Exception:
            traceback.print_exc()
            return Exception

    @app_commands.command(name="setup")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup(self, interaction: discord.Interaction):
        """(Admin Only) Sets the name, emoji, leaderboard channel, and reaction toggle for the server awards.
        """
        await interaction.response.defer()
        try:
            guild = interaction.guild
            user = interaction.user

            # Create an entry for the guild if needed
            await self.db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild.id,))
            await self.db.commit()

            # Set the award name (singular)
            singular = discord.Embed(
                color=self.bot.blurple,
                title="Award Setup",
                description="Please use the button below to set the server's custom **award name (singular)**. Examples include `award`, `point`, `star`, or `like`."
            )
            singular_view = SingularView(bot=self.bot, user=user)
            response = await interaction.followup.send(embed=singular, view=singular_view, wait=True)
            await singular_view.wait()
            
            # Set the award name (plural)
            plural = discord.Embed(
                color=self.bot.blurple,
                title="Award Setup",
                description="Please use the button below to set the server's custom **award name (plural)**. For example, if you set the award name (singular) to `award`, you should set the award name (plural) to `awards`."
            )
            plural_view = PluralView(bot=self.bot, user=user)
            await response.edit(embed=plural, view=plural_view)
            await plural_view.wait()

            # Set the award emoji
            emoji = discord.Embed(
                color=self.bot.blurple,
                title="Award Setup",
                description="Please use the button below to set the server's custom **award emoji**. This emoji will represent the awards on the server's award leaderboad."
            )
            emoji_view = EmojiView(bot=self.bot, user=user)
            await response.edit(embed=emoji, view=emoji_view)
            await emoji_view.wait()

            # Set the award leaderboard channel
            leaderboard = discord.Embed(
                color=self.bot.blurple,
                title="Award Setup",
                description="Please use the dropdown below to set the server's **award leaderboard channel**. The server's award leaderboard to this channel and update the leaderboard when any changes are made to award amounts."
            )
            leaderboard_view = LeaderboardView(bot=self.bot, user=user)
            await response.edit(embed=leaderboard, view=leaderboard_view)
            await leaderboard_view.wait()

            # Set the award reaction toggle
            toggle = discord.Embed(
                color=self.bot.blurple,
                title="Award Setup",
                description="Please use the dropdown below to set the server's **award reaction toggle**. If set to `True`, members will be able to add and remove awards via emoji reactions. If set to `False`, members will only be able to add and remove awards via the slash commands `/awards add` and `/awards remove`."
            )
            toggle_view = AwardReactionView(bot=self.bot, user=user)
            await response.edit(embed=toggle, view=toggle_view)
            await toggle_view.wait()

            # Send a message that setup is complete
            done = discord.Embed(
                color=self.bot.green,
                title="Success",
                description="You have successfully set up the award system for this server!"
            )
            await response.edit(embed=done, view=None)
            await response.delete(delay=10.0)
        
        # Send a message and print a traceback on error
        except Exception as e:
            error = discord.Embed(
                color=self.bot.red,
                title="Error",
                description=f"{e}"
            )
            error = await interaction.followup.send(embed=error, wait=True)
            await error.delete(delay=10.0)
            print(traceback.format_exc())

    @app_commands.command(name="clear")
    @app_commands.checks.has_permissions(administrator=True)
    async def clear(self, interaction: discord.Interaction):
        """(Admin Only) Clears every member's awards in the server.
        """
        await interaction.response.defer(ephemeral=True)
        try:
            guild = interaction.guild
            user = interaction.user

            singular = await self.fetch_singular(guild=guild)
            if isinstance(singular, str):
                singular_title = singular.title()
            plural = await self.fetch_plural(guild=guild)
            if isinstance(plural, str):
                plural_title = plural.title()
            emoji = await self.fetch_emoji(guild=guild)
            
            members = [m for m in guild.members if not m.bot]
            for member in members:
                guild_member_id = str(guild.id) + str(member.id)
                await self.db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
                await self.db.commit()
                await self.db.execute("UPDATE awards SET amount = 0 WHERE guild_member_id = ?", (guild_member_id,))
                await self.db.commit()
            
            embed = discord.Embed(color=self.bot.green, title=f"{emoji} {plural_title} Cleared {emoji}", description=f"{guild.name} has had all its {plural} cleared!")
            response = await interaction.followup.send(ephemeral=True, embed=embed, wait=True)
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
                        title="Awards Log",
                        description=f"{user.mention} has just cleared the awards for the server.",
                        timestamp=now
                    )
                    log.set_author(name=user.display_name, icon_url=user.display_avatar)
                    log.set_thumbnail(url=user.display_avatar)
                    await logging_channel.send(embed=log)
                else:
                    error = discord.Embed(
                        color=self.bot.red,
                        title="Logging Channel Not Found",
                        description=f"A logging channel with the ID {fetched_logging} was not found! Please set a new logging channel by re-running the `/start` command.",
                        timestamp=now
                    )
                    log_error = await interaction.followup.send(embed=error, wait=True)
                    await log_error.delete(delay=10.0)

        # Send a message and print a traceback on error
        except Exception as e:
            error = discord.Embed(
                color=self.bot.red,
                title="Error",
                description=f"{e}"
            )
            error = await interaction.followup.send(embed=error, wait=True)
            await error.delete(delay=10.0)
            print(traceback.format_exc())
    
    @tasks.loop(hours=24)
    async def leaderboard(self):
        try:
            guilds = [guild for guild in self.bot.guilds]
            for guild in guilds:

                # Retreive leaderboard channel
                leaderboard_channel = await self.fetch_leaderboard(guild=guild)
                if isinstance(leaderboard_channel, discord.TextChannel):

                    # Retreive the award names and emoji
                    singular = await self.fetch_singular(guild=guild)
                    if isinstance(singular, str):
                        singular_title = singular.title()
                    plural = await self.fetch_plural(guild=guild)
                    if isinstance(plural, str):
                        plural_title = plural.title()
                    emoji = await self.fetch_emoji(guild=guild)

                    # Make a list (and dictionary) of all guild members
                    guild_member_ids = []
                    guild_member_dict = {}
                    for member in guild.members:
                        guild_member_id = str(guild.id + member.id)
                        guild_member_ids.append(guild_member_id)
                        guild_member_dict[guild_member_id] = member

                    # Figure out how many awards each guild member has
                    member_awards = {}
                    for guild_member_id in guild_member_ids:
                        cur = await self.db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
                        row = await cur.fetchone()
                        amount = row[0]
                        if isinstance(amount, int):
                            if amount > 0:
                                member_awards[guild_member_id] = amount
                    
                    # Generate and send the leaderboard to the leaderboard channel
                    if len(member_awards) > 0:
                        now = datetime.now(tz=timezone.utc)
                        embed = discord.Embed(
                            color=self.bot.blurple,
                            title=f"{emoji} {singular_title} Leaderboard {emoji}",
                            timestamp=now
                        )
                        leaderboard_dict = dict(sorted(member_awards.items(), key=lambda item: item[1], reverse=True))
                        count = 0
                        for guild_member_id, awards in leaderboard_dict.items():
                            member = guild_member_dict[guild_member_id]
                            if isinstance(member, discord.Member):
                                if awards == 1:
                                    name = singular
                                else:
                                    name = plural
                                if count == 0:
                                    embed.add_field(name="🥇 First Place", value=f"{member.mention} has {awards} {name}!")
                                elif count == 1:
                                    embed.add_field(name="🥈 Second Place", value=f"{member.mention} has {awards} {name}!")
                                elif count == 2:
                                    embed.add_field(name="🥉 Third Place", value=f"{member.mention} has {awards} {name}!")
                                elif count == 3:
                                    embed.add_field(name="Fourth Place", value=f"{member.mention} has {awards} {name}!")
                                elif count == 4:
                                    embed.add_field(name="Fifth Place", value=f"{member.mention} has {awards} {name}!")
                                elif count == 5:
                                    embed.add_field(name="Sixth Place", value=f"{member.mention} has {awards} {name}!")
                                elif count == 6:
                                    embed.add_field(name="Seventh Place", value=f"{member.mention} has {awards} {name}!")
                                elif count == 7:
                                    embed.add_field(name="Eighth Place", value=f"{member.mention} has {awards} {name}!")
                                elif count == 8:
                                    embed.add_field(name="Ninth Place", value=f"{member.mention} has {awards} {name}!")
                                elif count == 9:
                                    embed.add_field(name="Tenth Place", value=f"{member.mention} has {awards} {name}!")
                                elif count == 10:
                                    embed.add_field(name="Eleventh Place", value=f"{member.mention} has {awards} {name}!")
                                elif count == 11:
                                    embed.add_field(name="Twelfth Place", value=f"{member.mention} has {awards} {name}!")
                                elif count == 12:
                                    embed.add_field(name="Thirteenth Place", value=f"{member.mention} has {awards} {name}!")
                                elif count == 13:
                                    embed.add_field(name="Fourteenth Place", value=f"{member.mention} has {awards} {name}!")
                                elif count == 14:
                                    embed.add_field(name="Fifteenth Place", value=f"{member.mention} has {awards} {name}!")
                                elif count == 15:
                                    embed.add_field(name="Sixteenth Place", value=f"{member.mention} has {awards} {name}!")
                                elif count == 16:
                                    embed.add_field(name="Seventeenth Place", value=f"{member.mention} has {awards} {name}!")
                                elif count == 17:
                                    embed.add_field(name="Eighteenth Place", value=f"{member.mention} has {awards} {name}!")
                                elif count == 18:
                                    embed.add_field(name="Nineteenth Place", value=f"{member.mention} has {awards} {name}!")
                                elif count == 19:
                                    embed.add_field(name="Twentieth Place", value=f"{member.mention} has {awards} {name}!")
                                count += 1
                        await leaderboard_channel.send(embed=embed)

        except Exception:
            print(traceback.format_exc())

    @commands.GroupCog.listener(name="on_reaction_add")
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.Member):
        try:
            message = reaction.message
            channel = message.channel
            guild = message.guild

            # Retreive the award emoji
            emoji = await self.fetch_emoji(guild=guild)
            
            if str(reaction.emoji) == emoji:

                # Retreive the award reaction toggle
                toggle = await self.fetch_toggle(guild=guild)
                if toggle == True:

                    # Retreive the award names
                    singular = await self.fetch_singular(guild=guild)
                    if isinstance(singular, str):
                        singular_title = singular.title()
                    plural = await self.fetch_plural(guild=guild)
                    if isinstance(plural, str):
                        plural_title = plural.title()

                    member = message.author
                    guild_member_id = str(guild.id) + str(member.id)
                    await self.db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
                    await self.db.commit()

                    yesorno_view = YesOrNo(user=user)
                    yesorno = discord.Embed(color=self.bot.blurple, title=f"Add {singular_title}", description=f"Would you like to add a(n) {singular} to {member.display_name}'s current total?")
                    response = await channel.send(content=f"-# {user.mention}", embed=yesorno, view=yesorno_view)
                    await yesorno_view.wait()

                    # User wants to add an award to the member
                    if yesorno_view.value == True:

                        # Fetch the current award amount
                        cur = await self.db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
                        row = await cur.fetchone()
                        current = row[0]
                        if current is None:
                            current = 0
                        
                        # Set the new award amount
                        new = current + 1
                        await self.db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (new, guild_member_id))
                        await self.db.commit()

                        # Fetch the new award amount
                        cur = await self.db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
                        row = await cur.fetchone()
                        new = row[0]
                        if new == 1:
                            embed = discord.Embed(color=self.bot.green, title=f"{singular_title} Added", description=f"{member.mention} now has {new} {singular}! (Added by {user.mention} via an emoji reaction.)")
                        else:
                            embed = discord.Embed(color=self.bot.green, title=f"{singular_title} Added", description=f"{member.mention} now has {new} {plural}! (Added by {user.mention} via an emoji reaction.)")
                        await response.edit(embed=embed, view=None)
                        await response.delete(delay=10.0)
                    
                    # User does NOT want to add an award to the member
                    else:
                        await response.delete()

        except Exception:
            traceback.print_exc()

    @commands.GroupCog.listener(name="on_reaction_remove")
    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.Member):
        try:
            message = reaction.message
            channel = message.channel
            guild = message.guild

            # Retreive the award emoji
            emoji = await self.fetch_emoji(guild=guild)
            
            if str(reaction.emoji) == emoji:

                # Retreive the award reaction toggle
                toggle = await self.fetch_toggle(guild=guild)
                if toggle == True:

                    # Retreive the award names
                    singular = await self.fetch_singular(guild=guild)
                    if isinstance(singular, str):
                        singular_title = singular.title()
                    plural = await self.fetch_plural(guild=guild)
                    if isinstance(plural, str):
                        plural_title = plural.title()

                    member = message.author
                    guild_member_id = str(guild.id) + str(member.id)
                    await self.db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
                    await self.db.commit()

                    yesorno_view = YesOrNo(user=user)
                    yesorno = discord.Embed(color=self.bot.blurple, title=f"Remove {singular_title}", description=f"Would you like to remove a(n) {singular} from {member.display_name}'s current total?")
                    response = await channel.send(content=f"-# {user.mention}", embed=yesorno, view=yesorno_view)
                    await yesorno_view.wait()

                    # User wants to add an award to the member
                    if yesorno_view.value == True:

                        # Fetch the current award amount
                        cur = await self.db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
                        row = await cur.fetchone()
                        current = row[0]
                        if current is None:
                            current = 0
                        
                        # Set the new award amount (if the current amount is 1 or greater)
                        if current >= 1:
                            new = current - 1
                            await self.db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (new, guild_member_id))
                            await self.db.commit()

                            # Fetch the new award amount
                            cur = await self.db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
                            row = await cur.fetchone()
                            new = row[0]
                            if new == 1:
                                embed = discord.Embed(color=self.bot.green, title=f"{singular_title} Added", description=f"{member.mention} now has {new} {singular}! (Added by {user.mention} via an emoji reaction.)")
                            else:
                                embed = discord.Embed(color=self.bot.green, title=f"{singular_title} Added", description=f"{member.mention} now has {new} {plural}! (Added by {user.mention} via an emoji reaction.)")
                            await response.edit(embed=embed, view=None)
                            await response.delete(delay=10.0)
                        
                        # Send an error message
                        else:
                            embed = discord.Embed(color=self.bot.red, title="Error", description=f"{member.mention} doesn't have any rewards to remove!")
                            await response.edit(embed=embed, view=None)
                            await response.delete(delay=10.0)
                    
                    # User does NOT want to add an award to the member
                    else:
                        await response.delete()

        except Exception:
            traceback.print_exc()

    @app_commands.command(name="add")
    async def add(self, interaction: discord.Interaction, amount: Optional[int], member: Optional[discord.Member]):
        """Adds awards to the command user or another selected member.

        Parameters
        -----------
        amount : int, optional
            Choose the number of awards to add. (Default: 1)
        member : discord.Member, optional
            Choose the member to add the awards to. (Default: Self)
        """
        await interaction.response.defer()
        try:
            guild = interaction.guild
            user = interaction.user
            if not isinstance(amount, int):
                amount = 1
            if not isinstance(member, discord.Member):
                member = interaction.user
            
            # Retreive the award names and emoji
            singular = await self.fetch_singular(guild=guild)
            if isinstance(singular, str):
                singular_title = singular.title()
            plural = await self.fetch_plural(guild=guild)
            if isinstance(plural, str):
                plural_title = plural.title()
            emoji = await self.fetch_emoji(guild=guild)

            # Add the member to the database if necessary
            guild_member_id = str(guild.id) + str(member.id)
            await self.db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
            await self.db.commit()

            # Fetch and update the member's award amount
            cur = await self.db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
            row = await cur.fetchone()
            current = row[0]
            if current is None:
                await self.db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (amount, guild_member_id))
                await self.db.commit()
            else:
                new = current + amount
                await self.db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (new, guild_member_id))
                await self.db.commit()
            
            # Fetch the new award amount and send the response
            cur = await self.db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
            row = await cur.fetchone()
            new = row[0]
            if amount == 1:
                if new == 1:
                    embed = discord.Embed(color=self.bot.green, title=f"{emoji} {singular_title} Added {emoji}", description=f"{user.mention} has just given {member.mention} {amount} {singular}. {member.mention} now has {new} {singular}!")
                else:
                    embed = discord.Embed(color=self.bot.green, title=f"{emoji} {singular_title} Added {emoji}", description=f"{user.mention} has just given {member.mention} {amount} {singular}. {member.mention} now has {new} {plural}!")
            else:
                if new == 1:
                    embed = discord.Embed(color=self.bot.green, title=f"{emoji} {plural_title} Added {emoji}", description=f"{user.mention} has just given {member.mention} {amount} {plural}. {member.mention} now has {new} {singular}!")
                else:
                    embed = discord.Embed(color=self.bot.green, title=f"{emoji} {plural_title} Added {emoji}", description=f"{user.mention} has just given {member.mention} {amount} {plural}. {member.mention} now has {new} {plural}!")
            embed.set_author(name=user.display_name, icon_url=user.display_avatar)
            embed.set_thumbnail(url=member.display_avatar)
            response = await interaction.followup.send(embed=embed, wait=True)
            await response.delete(delay=10.0)

            # Send a log to the logging channel
            cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            fetched_logging = row[0]
            if fetched_logging is not None:
                logging_channel = guild.get_channel(fetched_logging)
                now = datetime.now(tz=timezone.utc)
                if isinstance(logging_channel, discord.TextChannel):
                    await logging_channel.send(embed=embed)
                else:
                    error = discord.Embed(
                        color=self.bot.red,
                        title="Logging Channel Not Found",
                        description=f"A logging channel with the ID {fetched_logging} was not found! Please set a new logging channel by re-running the `/start` command.",
                        timestamp=now
                    )
                    log_error = await interaction.followup.send(embed=error, wait=True)
                    await log_error.delete(delay=10.0)

        # Send a message and print a traceback on error
        except Exception as e:
            error = discord.Embed(
                color=self.bot.red,
                title="Error",
                description=f"{e}"
            )
            error = await interaction.followup.send(embed=error, wait=True)
            await error.delete(delay=10.0)
            print(traceback.format_exc())

    @app_commands.command(name="remove")
    async def remove(self, interaction: discord.Interaction, amount: Optional[int], member: Optional[discord.Member]):
        """Removes awards from the command user or another selected member.

        Parameters
        -----------
        amount : int, optional
            Choose the number of awards to remove. (Default: 1)
        member : discord.Member, optional
            Choose the member to remove the awards from. (Default: Self)
        """
        await interaction.response.defer()
        try:
            guild = interaction.guild
            user = interaction.user
            if not isinstance(amount, int):
                amount = 1
            if not isinstance(member, discord.Member):
                member = interaction.user
            
            # Retreive the award names and emoji
            singular = await self.fetch_singular(guild=guild)
            if isinstance(singular, str):
                singular_title = singular.title()
            plural = await self.fetch_plural(guild=guild)
            if isinstance(plural, str):
                plural_title = plural.title()
            emoji = await self.fetch_emoji(guild=guild)

            # Add the member to the database if necessary
            guild_member_id = str(guild.id) + str(member.id)
            await self.db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
            await self.db.commit()

            # Fetch and update the member's award amount and send the response
            cur = await self.db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
            row = await cur.fetchone()
            current = row[0]
            if current is None:
                current = 0
            if current == 0:
                await self.db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (current, guild_member_id))
                await self.db.commit()
                embed = discord.Embed(color=self.bot.red, title=f"Error", description=f"{member.mention} doesn't have any {plural}!")
            elif current < amount:
                embed = discord.Embed(color=self.bot.red, title=f"Error", description=f"{member.mention} doesn't have enough {plural}!")
            else:
                new = current - amount
                await self.db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (new, guild_member_id))
                await self.db.commit()
                cur = await self.db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
                row = await cur.fetchone()
                new = row[0]
                if amount == 1:
                    if new == 0:
                        embed = discord.Embed(color=self.bot.green, title=f"{emoji} {singular_title} Removed {emoji}", description=f"{member.mention} no longer has any {plural}!")
                    elif new == 1:
                        embed = discord.Embed(color=self.bot.green, title=f"{emoji} {singular_title} Removed {emoji}", description=f"{member.mention} now has {new} {singular}!")
                    else:
                        embed = discord.Embed(color=self.bot.green, title=f"{emoji} {singular_title} Removed {emoji}", description=f"{member.mention} now has {new} {plural}!")
                else:
                    if new == 0:
                        embed = discord.Embed(color=self.bot.green, title=f"{emoji} {plural_title} Removed {emoji}", description=f"{member.mention} no longer has any {plural}!")
                    elif new == 1:
                        embed = discord.Embed(color=self.bot.green, title=f"{emoji} {plural_title} Removed {emoji}", description=f"{member.mention} now has {new} {singular}!")
                    else:
                        embed = discord.Embed(color=self.bot.green, title=f"{emoji} {plural_title} Removed {emoji}", description=f"{member.mention} now has {new} {plural}!")
            embed.set_author(name=user.display_name, icon_url=user.display_avatar)
            embed.set_thumbnail(url=member.display_avatar)
            response = await interaction.followup.send(embed=embed, wait=True)
            await response.delete(delay=10.0)

            # Send a log to the logging channel
            cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            fetched_logging = row[0]
            if fetched_logging is not None:
                logging_channel = guild.get_channel(fetched_logging)
                now = datetime.now(tz=timezone.utc)
                if isinstance(logging_channel, discord.TextChannel):
                    await logging_channel.send(embed=embed)
                else:
                    error = discord.Embed(
                        color=self.bot.red,
                        title="Logging Channel Not Found",
                        description=f"A logging channel with the ID {fetched_logging} was not found! Please set a new logging channel by re-running the `/start` command.",
                        timestamp=now
                    )
                    log_error = await interaction.followup.send(embed=error, wait=True)
                    await log_error.delete(delay=10.0)

        # Send a message and print a traceback on error
        except Exception as e:
            error = discord.Embed(
                color=self.bot.red,
                title="Error",
                description=f"{e}"
            )
            error = await interaction.followup.send(embed=error, wait=True)
            await error.delete(delay=10.0)
            print(traceback.format_exc())

    @app_commands.command(name="check")
    async def check(self, interaction: discord.Interaction, member: Optional[discord.Member]):
        """Returns the number of awards that the command user or another selected user currently has.

        Parameters
        -----------
        member : discord.Member, optional
            Choose the member that you would like to check the number of awards for. (Default: Self)
        """
        await interaction.response.defer(ephemeral=True)
        try:
            guild = interaction.guild
            user = interaction.user
            if not isinstance(member, discord.Member):
                member = interaction.user
            
            # Retreive the award names and emoji
            singular = await self.fetch_singular(guild=guild)
            if isinstance(singular, str):
                singular_title = singular.title()
            plural = await self.fetch_plural(guild=guild)
            if isinstance(plural, str):
                plural_title = plural.title()
            emoji = await self.fetch_emoji(guild=guild)
            
            # Add the member to the database if necessary
            guild_member_id = str(guild.id) + str(member.id)
            await self.db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
            await self.db.commit()

            cur = await self.db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
            row = await cur.fetchone()
            amount = row[0]
            if amount is None:
                amount = 0
            if amount == 0:
                await self.db.execute("INSERT OR IGNORE INTO awards (guild_member_id, amount) VALUES (?,?)", (guild_member_id, 0))
                await self.db.commit()
                embed = discord.Embed(color=self.bot.green, title=f"{emoji} {plural_title} {emoji}", description=f"{member.mention} doesn't have any {plural}!")
            elif amount == 1:
                embed = discord.Embed(color=self.bot.green, title=f"{emoji} {plural_title} {emoji}", description=f"{member.mention} has {amount} {singular}!")
            else:
                embed = discord.Embed(color=self.bot.green, title=f"{emoji} {plural_title} {emoji}", description=f"{member.mention} has {amount} {plural}!")
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
            embed.set_thumbnail(url=member.display_avatar)
            response = await interaction.followup.send(ephemeral=True, embed=embed, wait=True)
            await response.delete(delay=10.0)
        
        # Send a message and print a traceback on error
        except Exception as e:
            error = discord.Embed(
                color=self.bot.red,
                title="Error",
                description=f"{e}"
            )
            error = await interaction.followup.send(embed=error, wait=True)
            await error.delete(delay=10.0)
            print(traceback.format_exc())

async def setup(bot: commands.Bot):
    print("Setting up Cog: awards.Awards")

async def teardown(bot: commands.Bot):
    print("Tearing down Cog: awards.Awards")