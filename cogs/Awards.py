import discord
import traceback
from discord import app_commands, ChannelType
from discord.ext import commands
from typing import Optional
from datetime import datetime, timezone

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

class SingularView(discord.ui.View):
    def __init__(self, *, timeout = 180, bot: commands.Bot, user: discord.Member):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.user = user
        self.db = bot.database
        self.value = None

    @discord.ui.button(label="Set Custom Award Name (Singular)", style=discord.ButtonStyle.blurple)
    async def singular(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = Singular(bot=self.bot, user=self.user)
        await interaction.response.send_modal(modal)
        await modal.wait()

        if modal.value == True:

            guild = interaction.guild

            singular = modal.singular.value
            sing_low = singular.lower()
            await self.db.execute("UPDATE guilds SET award_singular = ? WHERE guild_id = ?", (sing_low, guild.id))
            await self.db.commit()
            cur = await self.db.execute("SELECT award_singular FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            fetched_sing_low = str(row[0])
            fetched_sing_cap = fetched_sing_low.title()

            cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (interaction.guild.id,))
            row = await cur.fetchone()
            fetched_logging = row[0]
            if fetched_logging is not None:
                logging = guild.get_channel(fetched_logging)
                if logging is not None:
                    now = datetime.now(tz=timezone.utc)
                    log = discord.Embed(color=self.bot.blurple, title="Awards Log", description=f"{interaction.user.mention} has successfully set the server's custom award name (singular)!", timestamp=now)
                    log.add_field(name="Singular (Capitalized)", value=f"{fetched_sing_cap}")
                    log.add_field(name="Singular (Lowercase)", value=f"{fetched_sing_low}")
                    log.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
                    log.set_thumbnail(url=interaction.user.display_avatar)
                    await logging.send(embed=log)

        if modal.value == False:
            
            error = discord.Embed(color=self.bot.red, title="Error", description="There was a problem. Please try again later.")
            await interaction.message.edit(embed=error, delete_after=10.0, view=None)
        
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red, row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            embed = discord.Embed(color=self.bot.red, title="Cancel", description="Are you sure you want to cancel?")
            view = YesOrNo(user=interaction.user)
            cancel = await interaction.followup.send(wait=True, embed=embed, view=view)
            await view.wait()

            if view.value == True:
                await interaction.message.delete()
                await cancel.delete()
                self.stop()
            
            if view.value == False:
                await cancel.delete()

class Singular(discord.ui.Modal):
    def __init__(self, *, title = "Singular", timeout = 180.0, bot: commands.Bot, user: discord.Member):
        super().__init__(title=title, timeout=timeout)
        self.bot = bot
        self.user = user
        self.db = bot.database
        self.value = None
    
    singular = discord.ui.TextInput(label="Singular", custom_id="singular_input", placeholder="Enter a cutom name (singular) for you server awards...")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.stop()

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = False
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
        self.db = bot.database
        self.value = None

    @discord.ui.button(label="Set Custom Award Name (Plural)", style=discord.ButtonStyle.blurple)
    async def plural(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = Plural(bot=self.bot, user=self.user)
        await interaction.response.send_modal(modal)
        await modal.wait()

        if modal.value == True:

            guild = interaction.guild

            plural = modal.plural.value
            plur_low = plural.lower()
            await self.db.execute("UPDATE guilds SET award_plural = ? WHERE guild_id = ?", (plur_low, guild.id))
            await self.db.commit()
            cur = await self.db.execute("SELECT award_plural FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            fetched_plur_low = str(row[0])
            fetched_plur_cap = fetched_plur_low.title()

            cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (interaction.guild.id,))
            row = await cur.fetchone()
            fetched_logging = row[0]
            if fetched_logging is not None:
                logging = guild.get_channel(fetched_logging)
                if logging is not None:
                    now = datetime.now(tz=timezone.utc)
                    log = discord.Embed(color=self.bot.blurple, title="Awards Log", description=f"{interaction.user.mention} has successfully set the server's custom award name (plural)!", timestamp=now)
                    log.add_field(name="Singular (Capitalized)", value=f"{fetched_plur_cap}")
                    log.add_field(name="Singular (Lowercase)", value=f"{fetched_plur_low}")
                    log.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
                    log.set_thumbnail(url=interaction.user.display_avatar)
                    await logging.send(embed=log)

        if modal.value == False:
            
            error = discord.Embed(color=self.bot.red, title="Error", description="There was a problem. Please try again later.")
            await interaction.message.edit(embed=error, delete_after=10.0, view=None)
        
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red, row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            embed = discord.Embed(color=self.bot.red, title="Cancel", description="Are you sure you want to cancel?")
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
        self.db = bot.database
        self.value = None
    
    plural = discord.ui.TextInput(label="Plural", custom_id="plural_input", placeholder="Enter a cutom name (plural) for you server awards...")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.stop()

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = False
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
        self.db = bot.database
        self.value = None

    @discord.ui.button(label="Set Custom Award Emoji", style=discord.ButtonStyle.blurple)
    async def emoji(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = Emoji(bot=self.bot, user=self.user)
        await interaction.response.send_modal(modal)
        await modal.wait()

        if modal.value == True:

            guild = interaction.guild

            emoji = modal.emoji.value
            await self.db.execute("UPDATE guilds SET award_emoji = ? WHERE guild_id = ?", (emoji, guild.id))
            await self.db.commit()
            cur = await self.db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            fetched_emoji = row[0]

            cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (interaction.guild.id,))
            row = await cur.fetchone()
            fetched_logging = row[0]
            if fetched_logging is not None:
                logging = guild.get_channel(fetched_logging)
                if logging is not None:
                    now = datetime.now(tz=timezone.utc)
                    log = discord.Embed(color=self.bot.blurple, title="Awards Log", description=f"{interaction.user.mention} has successfully set the server's custom award emoji!", timestamp=now)
                    log.add_field(name="Emoji", value=f"{fetched_emoji}")
                    log.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
                    log.set_thumbnail(url=interaction.user.display_avatar)
                    await logging.send(embed=log)

        if modal.value == False:
            
            error = discord.Embed(color=self.bot.red, title="Error", description="There was a problem. Please try again later.")
            await interaction.message.edit(embed=error, delete_after=10.0, view=None)
        
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red, row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            embed = discord.Embed(color=self.bot.red, title="Cancel", description="Are you sure you want to cancel?")
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
        self.db = bot.database
        self.value = None
    
    emoji = discord.ui.TextInput(label="Emoji", custom_id="emoji_input", placeholder="Enter a cutom emoji for you server awards...")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.stop()

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = False
            self.stop()
        print(traceback.format_exc())
    
    async def on_timeout(self):
        self.value = False
        self.stop()

class LeaderboardView(discord.ui.View):
    def __init__(self, *, timeout = 180, bot: commands.Bot, user: discord.Member):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.user = user
        self.db = bot.database
        self.view = Leaderboard(user=self.user)
        self.add_item(self.view)

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green, row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            guild = interaction.guild

            channel = self.view.channel
            await self.db.execute("UPDATE guilds SET leaderboard_channel_id = ? WHERE guild_id = ?", (channel.id, guild.id))
            await self.db.commit()
            cur = await self.db.execute("SELECT leaderboard_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            fetched_channel_id = row[0]
            fetched_channel = guild.get_channel(fetched_channel_id)

            cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (interaction.guild.id,))
            row = await cur.fetchone()
            fetched_logging = row[0]
            if fetched_logging is not None:
                logging = guild.get_channel(fetched_logging)
                if logging is not None:
                    now = datetime.now(tz=timezone.utc)
                    log = discord.Embed(color=self.bot.blurple, title="Awards Log", description=f"{interaction.user.mention} has successfully set the server's award leaderboard channel!", timestamp=now)
                    log.add_field(name="Channel", value=f"{fetched_channel.mention}")
                    log.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
                    log.set_thumbnail(url=interaction.user.display_avatar)
                    await logging.send(embed=log)

        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red, row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            embed = discord.Embed(color=self.bot.red, title="Cancel", description="Are you sure you want to cancel?")
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
            channel_types=[ChannelType.text],
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

class AwardReactionView(discord.ui.View):
    def __init__(self, *, timeout = 180, bot: commands.Bot, user: discord.Member):
        super().__init__(timeout=timeout)
        self.value = None
        self.bot = bot
        self.user = user
        self.db = bot.database
        self.view = AwardReaction(user=self.user)
        self.add_item(self.view)

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green, row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            guild = interaction.guild

            toggle = self.view.toggle

            if toggle == "True":
                await self.db.execute("UPDATE guilds SET award_reaction_toggle = 1 WHERE guild_id = ?", (guild.id,))
                await self.db.commit()

                cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (interaction.guild.id,))
                row = await cur.fetchone()
                fetched_logging = row[0]
                if fetched_logging is not None:
                    logging = guild.get_channel(fetched_logging)
                    if logging is not None:
                        now = datetime.now(tz=timezone.utc)
                        log = discord.Embed(color=self.bot.blurple, title="Awards Log", description=f"{interaction.user.mention} has successfully set the server's award reaction toggle!", timestamp=now)
                        log.add_field(name="Toggle", value=f"True")
                        log.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
                        log.set_thumbnail(url=interaction.user.display_avatar)
                        await logging.send(embed=log)

                self.stop()
            
            elif toggle == "False":
                await self.db.execute("UPDATE guilds SET award_reaction_toggle = 0 WHERE guild_id = ?", (guild.id,))
                await self.db.commit()

                cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (interaction.guild.id,))
                row = await cur.fetchone()
                fetched_logging = row[0]
                if fetched_logging is not None:
                    logging = guild.get_channel(fetched_logging)
                    if logging is not None:
                        now = datetime.now(tz=timezone.utc)
                        log = discord.Embed(color=self.bot.blurple, title="Awards Log", description=f"{interaction.user.mention} has successfully set the server's award reaction toggle!", timestamp=now)
                        log.add_field(name="Toggle", value=f"False")
                        log.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
                        log.set_thumbnail(url=interaction.user.display_avatar)
                        await logging.send(embed=log)

                self.stop()
            
            else:
                error = discord.Embed(color=self.bot.red, title="Error", description=f"Please choose an option from the dropdown before confirming!")
                error_msg = await interaction.followup.send(embed=error, wait=True)
                await error_msg.delete(delay=10.0)
    
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red, row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            embed = discord.Embed(color=self.bot.red, title="Cancel", description="Are you sure you want to cancel?")
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

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.toggle = self.values[0]

class Awards(commands.GroupCog, group_name = "awards"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.database

    @app_commands.command(name="setup")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup(self, interaction: discord.Interaction):
        """(Admin Only) Sets the name, emoji, and leaderboard channel for the server awards.
        """
        await interaction.response.defer()
        try:

            guild = interaction.guild
            await self.db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild.id,))
            await self.db.commit()

            embed = discord.Embed(color=self.bot.blurple, title="Award Setup", description="Please use the button below to set the server's custom **award name (singular)**. Examples include `award`, `point`, `star`, or `like`.")
            response = await interaction.followup.send(wait=True, embed=embed)
            singular_view = SingularView(bot=self.bot, user=interaction.user)
            await response.edit(view=singular_view)
            await singular_view.wait()
            
            embed = discord.Embed(color=self.bot.blurple, title="Award Setup", description="Please use the button below to set the server's custom **award name (plural)**. For example, if you set the award name (singular) to `award`, you should set the award name (plural) to `awards`.")
            plural_view = PluralView(bot=self.bot, user=interaction.user)
            await response.edit(embed=embed, view=plural_view)
            await plural_view.wait()

            embed = discord.Embed(color=self.bot.blurple, title="Award Setup", description="Please use the button below to set the server's custom **award emoji**. This emoji will represent the awards on the server's award leaderboad.")
            emoji_view = EmojiView(bot=self.bot, user=interaction.user)
            await response.edit(embed=embed, view=emoji_view)
            await emoji_view.wait()

            embed = discord.Embed(color=self.bot.blurple, title="Award Setup", description="Please use the dropdown below to set the server's **award leaderboard channel**. This bot will post the server's award leaderboard to this channel and update the leaderboard when any changes are made to award amounts.")
            leaderboard_view = LeaderboardView(bot=self.bot, user=interaction.user)
            await response.edit(embed=embed, view=leaderboard_view)
            await leaderboard_view.wait()

            embed = discord.Embed(color=self.bot.blurple, title="Award Setup", description="Please use the dropdown below to set the server's **award reaction toggle**. If set to `True`, members will be able to add and remove awards via emoji reactions. If set to `False`, members will only be able to add and remove awards via slash commands.")
            toggle_view = AwardReactionView(bot=self.bot, user=interaction.user)
            await response.edit(embed=embed, view=toggle_view)
            await toggle_view.wait()

            done = discord.Embed(color=self.bot.green, title="Success", description="You have successfully set up the award system for this server!")
            await response.edit(embed=done, view=None)
            await response.delete(delay=10.0)
        
        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            if response is not None:
                await response.edit(embed=error, view=None)
            else:
                response = await interaction.followup.send(wait=True, embed=error)
            await response.delete(delay=10.0)
            print(traceback.format_exc())

    @app_commands.command(name="clear")
    @app_commands.checks.has_permissions(administrator=True)
    async def clear(self, interaction: discord.Interaction):
        """(Admin Only) Clears every member's awards in the server.
        """
        await interaction.response.defer(ephemeral=True)
        try:

            guild = interaction.guild
            await self.db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild.id,))
            await self.db.commit()

            cur = await self.db.execute("SELECT award_plural FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            plur_low = row[0]
            if plur_low is None:
                plur_low = "awards"
            
            cur = await self.db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            moji = row[0]
            if moji is None:
                moji = "🏅"
            
            members = [m for m in guild.members if not m.bot]
            for member in members:
                guild_member_id = str(guild.id) + str(member.id)
                await self.db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
                await self.db.commit()
                await self.db.execute("UPDATE awards SET amount = 0 WHERE guild_member_id = ?", (guild_member_id,))
                await self.db.commit()
            
            embed = discord.Embed(color=self.bot.green, title=f"Success", description=f"{guild.name} has had all its {plur_low} cleared! {moji}")
            response = await interaction.followup.send(ephemeral=True, embed=embed, wait=True)

            cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            fetched_logging = row[0]
            if fetched_logging is not None:
                logging = guild.get_channel(fetched_logging)
                if logging is not None:
                    logging = guild.get_channel(fetched_logging)
                    now = datetime.now(tz=timezone.utc)
                    log = discord.Embed(color=self.bot.blurple, title="Awards Log", description=f"{interaction.user.mention} has just cleared the awards for the server.", timestamp=now)
                    log.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
                    log.set_thumbnail(url=interaction.user.display_avatar)
                    await logging.send(embed=log)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            if response is not None:
                await response.edit(embed=error, view=None)
            else:
                response = await interaction.followup.send(ephemeral=True, embed=error, wait=True)
            await response.delete(delay=10.0)
            print(traceback.format_exc())

    @commands.GroupCog.listener(name="on_reaction_add")
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.Member):
        try:
            message = reaction.message
            channel = message.channel
            guild = message.guild

            await self.db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild.id,))
            await self.db.commit()

            cur = await self.db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            moji = row[0]
            if moji is None:
                moji = "🏅"
            
            if str(reaction.emoji) == moji:

                cur = await self.db.execute("SELECT award_react_toggle FROM guilds WHERE guild_id = ?", (guild.id,))
                row = await cur.fetchone()
                toggle = row[0]

                if toggle == 1:

                    cur = await self.db.execute("SELECT award_singular FROM guilds WHERE guild_id = ?", (guild.id,))
                    row = await cur.fetchone()
                    sing_low = row[0]
                    if sing_low is None:
                        sing_low = "award"
                    sing_cap = sing_low.title()

                    cur = await self.db.execute("SELECT award_plural FROM guilds WHERE guild_id = ?", (guild.id,))
                    row = await cur.fetchone()
                    plur_low = row[0]
                    if plur_low is None:
                        plur_low = "awards"
                    #plur_cap = plur_low.title()

                    member = message.author
                    guild_member_id = str(guild.id) + str(member.id)
                    await self.db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
                    await self.db.commit()

                    cur = await self.db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
                    row = await cur.fetchone()
                    current = int(row[0])
                    if current is None:
                        current = 0
                    
                    new = current + 1
                    await self.db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (new, guild_member_id))
                    await self.db.commit()

                    cur = await self.db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
                    row = await cur.fetchone()
                    new = int(row[0])
                    if new == 1:
                        embed = discord.Embed(color=self.bot.green, title=f"{sing_cap} Added", description=f"{member.mention} now has {new} {sing_low}! ({sing_cap} added by {user.mention} via an emoji reaction.)")
                    else:
                        embed = discord.Embed(color=self.bot.green, title=f"{sing_cap} Added", description=f"{member.mention} now has {new} {plur_low}! ({sing_cap} added by {user.mention} via an emoji reaction.)")
                    
                    await channel.send(embed=embed, delete_after=30.0, reference=message)

        except Exception:
            traceback.print_exc()

    @commands.GroupCog.listener(name="on_reaction_remove")
    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.Member):
        try:
            message = reaction.message
            channel = message.channel
            guild = message.guild

            await self.db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild.id,))
            await self.db.commit()

            cur = await self.db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            moji = row[0]
            if moji is None:
                moji = "🏅"
            
            if str(reaction.emoji) == moji:

                cur = await self.db.execute("SELECT award_react_toggle FROM guilds WHERE guild_id = ?", (guild.id,))
                row = await cur.fetchone()
                toggle = row[0]
                
                if toggle == 1:

                    cur = await self.db.execute("SELECT award_singular FROM guilds WHERE guild_id = ?", (guild.id,))
                    row = await cur.fetchone()
                    sing_low = row[0]
                    if sing_low is None:
                        sing_low = "award"
                    sing_cap = sing_low.title()

                    cur = await self.db.execute("SELECT award_plural FROM guilds WHERE guild_id = ?", (guild.id,))
                    row = await cur.fetchone()
                    plur_low = row[0]
                    if plur_low is None:
                        plur_low = "awards"
                    #plur_cap = plur_low.title()

                    member = message.author
                    guild_member_id = str(guild.id) + str(member.id)
                    await self.db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
                    await self.db.commit()

                    cur = await self.db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
                    row = await cur.fetchone()
                    current = int(row[0])
                    if current is None:
                        current = 0
                    
                    new = current - 1
                    await self.db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (new, guild_member_id))
                    await self.db.commit()

                    cur = await self.db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
                    row = await cur.fetchone()
                    new = int(row[0])
                    if new == 0:
                        embed = discord.Embed(color=self.bot.red, title=f"{sing_cap} Removed", description=f"{member.mention} no longer has any awards! ({sing_cap} removed by {user.mention}.)")
                    elif new == 1:
                        embed = discord.Embed(color=self.bot.red, title=f"{sing_cap} Removed", description=f"{member.mention} now has {new} {sing_low}! ({sing_cap} removed by {user.mention}.)")
                    else:
                        embed = discord.Embed(color=self.bot.red, title=f"{sing_cap} Removed", description=f"{member.mention} now has {new} {plur_low}! ({sing_cap} removed by {user.mention}.)")
                    await channel.send(embed=embed, delete_after=30.0, reference=message)

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
        await interaction.response.defer(ephemeral=True)
        try:

            guild = interaction.guild
            if amount is None:
                amount = 1
            if member is None:
                member = interaction.user

            await self.db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild.id,))
            await self.db.commit()
            
            cur = await self.db.execute("SELECT award_singular FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            sing_low = row[0]
            if sing_low is None:
                sing_low = "award"
            sing_cap = sing_low.title()

            cur = await self.db.execute("SELECT award_plural FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            plur_low = row[0]
            if plur_low is None:
                plur_low = "awards"
            plur_cap = plur_low.title()

            cur = await self.db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            moji = row[0]
            if moji is None:
                moji = "🏅"

            guild_member_id = str(guild.id) + str(member.id)
            await self.db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
            await self.db.commit()

            cur = await self.db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
            row = await cur.fetchone()
            current = int(row[0])
            if current is None:
                await self.db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (amount, guild_member_id))
                await self.db.commit()
            else:
                new = current + amount
                await self.db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (new, guild_member_id))
                await self.db.commit()
            
            cur = await self.db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
            row = await cur.fetchone()
            new = int(row[0])
            if amount == 1:
                if new == 1:
                    embed = discord.Embed(color=self.bot.green, title=f"{sing_cap} Added", description=f"{interaction.user.mention} has just given {member.mention} {amount} {sing_low}. {member.mention} now has {new} {sing_low}!")
                else:
                    embed = discord.Embed(color=self.bot.green, title=f"{sing_cap} Added", description=f"{interaction.user.mention} has just given {member.mention} {amount} {sing_low}. {member.mention} now has {new} {plur_low}!")
            else:
                if new == 1:
                    embed = discord.Embed(color=self.bot.green, title=f"{plur_cap} Added", description=f"{interaction.user.mention} has just given {member.mention} {amount} {plur_low}. {member.mention} now has {new} {sing_low}!")
                else:
                    embed = discord.Embed(color=self.bot.green, title=f"{plur_cap} Added", description=f"{interaction.user.mention} has just given {member.mention} {amount} {plur_low}. {member.mention} now has {new} {plur_low}!")
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
            embed.set_thumbnail(url=member.display_avatar)
            response = await interaction.followup.send(ephemeral=True, embed=embed, wait=True)
            await response.delete(delay=10.0)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            error = await interaction.followup.send(ephemeral=True, embed=error, wait=True)
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
        await interaction.response.defer(ephemeral=True)
        try:

            guild = interaction.guild
            if amount is None:
                amount = 1
            if member is None:
                member = interaction.user

            await self.db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild.id,))
            await self.db.commit()

            cur = await self.db.execute("SELECT award_singular FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            sing_low = row[0]
            if sing_low is None:
                sing_low = "award"
            sing_cap = sing_low.title()
            
            cur = await self.db.execute("SELECT award_plural FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            plur_low = row[0]
            if plur_low is None:
                plur_low = "awards"
            plur_cap = plur_low.title()

            cur = await self.db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            moji = row[0]
            if moji is None:
                moji = "🏅"
            
            guild_member_id = str(guild.id) + str(member.id)
            await self.db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
            await self.db.commit()

            cur = await self.db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
            row = await cur.fetchone()
            current = int(row[0])
            if current is None:
                current = 0
            if current == 0:
                await self.db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (current, guild_member_id))
                await self.db.commit()
                embed = discord.Embed(color=self.bot.red, title=f"Error", description=f"{member.mention} doesn't have any {plur_low}!")
            elif current < amount:
                embed = discord.Embed(color=self.bot.red, title=f"Error", description=f"{member.mention} doesn't have enough {plur_low}!")
            else:
                new = current - amount
                await self.db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (new, guild_member_id))
                await self.db.commit()
                cur = await self.db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
                row = await cur.fetchone()
                new = int(row[0])
                if amount == 1:
                    if new == 0:
                        embed = discord.Embed(color=self.bot.green, title=f"{sing_cap} Removed", description=f"{member.mention} no longer has any {plur_low}!")
                    elif new == 1:
                        embed = discord.Embed(color=self.bot.green, title=f"{sing_cap} Removed", description=f"{member.mention} now has {new} {sing_low}!")
                    else:
                        embed = discord.Embed(color=self.bot.green, title=f"{sing_cap} Removed", description=f"{member.mention} now has {new} {plur_low}!")
                else:
                    if new == 0:
                        embed = discord.Embed(color=self.bot.green, title=f"{plur_cap} Removed", description=f"{member.mention} no longer has any {plur_low}!")
                    elif new == 1:
                        embed = discord.Embed(color=self.bot.green, title=f"{plur_cap} Removed", description=f"{member.mention} now has {new} {sing_low}!")
                    else:
                        embed = discord.Embed(color=self.bot.green, title=f"{plur_cap} Removed", description=f"{member.mention} now has {new} {plur_low}!")
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
            embed.set_thumbnail(url=member.display_avatar)
            response = await interaction.followup.send(ephemeral=True, embed=embed, wait=True)
            await response.delete(delay=10.0)
        
        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            error = await interaction.followup.send(ephemeral=True, embed=error, wait=True)
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
            if member is None:
                member = interaction.user

            await self.db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild.id,))
            await self.db.commit()

            cur = await self.db.execute("SELECT award_singular FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            sing_low = row[0]
            if sing_low is None:
                sing_low = "award"
            #sing_cap = sing_low.title()

            cur = await self.db.execute("SELECT award_plural FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            plur_low = row[0]
            if plur_low is None:
                plur_low = "awards"
            plur_cap = plur_low.title()
            
            cur = await self.db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            moji = row[0]
            if moji is None:
                moji = "🏅"
            
            guild_member_id = str(guild.id) + str(member.id)
            await self.db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
            await self.db.commit()

            cur = await self.db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
            row = await cur.fetchone()
            amount = row[0]
            if amount is None:
                amount = 0
            if amount == 0:
                await self.db.execute("INSERT OR IGNORE INTO awards (guild_member_id, amount) VALUES (?,?)", (guild_member_id,0))
                await self.db.commit()
                embed = discord.Embed(color=self.bot.green, title=f"{plur_cap}", description=f"{member.mention} doesn't have any {plur_low}!")
            elif amount == 1:
                embed = discord.Embed(color=self.bot.green, title=f"{plur_cap}", description=f"{member.mention} has {amount} {sing_low}!")
            else:
                embed = discord.Embed(color=self.bot.green, title=f"{plur_cap}", description=f"{member.mention} has {amount} {plur_low}!")
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
            embed.set_thumbnail(url=member.display_avatar)
            response = await interaction.followup.send(ephemeral=True, embed=embed, wait=True)
            await response.delete(delay=10.0)
        
        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            error = await interaction.followup.send(ephemeral=True, embed=error, wait=True)
            await error.delete(delay=10.0)
            print(traceback.format_exc())

async def setup(bot: commands.Bot):
    print("Setting up Cog: Awards.Awards")

async def teardown(bot: commands.Bot):
    print("Tearing down Cog: Awards.Awards")