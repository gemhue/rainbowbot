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

    @discord.ui.button(label="Set Custom Award Name (Singular)", style=discord.ButtonStyle.blurple)
    async def singular(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Singular(bot=self.bot, user=self.user))

class Singular(discord.ui.Modal):
    def __init__(self, *, title = "Singular", timeout = None, bot: commands.Bot, user: discord.Member):
        super().__init__(title=title, timeout=timeout)
        self.bot = bot
        self.user = user
        self.db = bot.database
    
    singular = discord.ui.TextInput(label="Singular", custom_id="singular_input", placeholder="Enter a cutom name (singular) for you server awards...")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if interaction.user == self.user:
            guild = interaction.guild

            singular = self.singular.value
            sing_low = singular.lower()
            await self.db.execute("UPDATE guilds SET award_singular = ? WHERE guild_id = ?", (sing_low, guild.id))
            await self.db.commit()
            cur = await self.db.execute("SELECT award_singular FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            fetched_sing_low = str(row[0])
            fetched_sing_cap = fetched_sing_low.title()

            now = datetime.now(tz=timezone.utc)
            submitted = discord.Embed(color=self.bot.green, title="Success", description=f"{interaction.user.mention} has successfully set the server's custom award name (singular)!", timestamp=now)
            submitted.add_field(name="Singular (Capitalized)", value=f"{fetched_sing_cap}")
            submitted.add_field(name="Singular (Lowercase)", value=f"{fetched_sing_low}")
            submitted.set_author(name=f"{interaction.user.display_name}", icon_url=f"{interaction.user.display_avatar}")
            await interaction.followup.send(embed=submitted, ephemeral=True)
            await self.stop()

            cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            fetched_logging = row[0]
            if fetched_logging is not None:
                logging = self.bot.get_channel(fetched_logging)
                await logging.send(embed=submitted)

class PluralView(discord.ui.View):
    def __init__(self, *, timeout = 180, bot: commands.Bot, user: discord.Member):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.user = user
        self.db = bot.database

    @discord.ui.button(label="Set Custom Award Name (Plural)", style=discord.ButtonStyle.blurple)
    async def singular(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Plural(bot=self.bot, user=self.user))

class Plural(discord.ui.Modal):
    def __init__(self, *, title = "Plural", timeout = None, bot: commands.Bot, user: discord.Member):
        super().__init__(title=title, timeout=timeout)
        self.bot = bot
        self.user = user
        self.db = bot.database
    
    plural = discord.ui.TextInput(label="Plural", custom_id="plural_input", placeholder="Enter a cutom name (plural) for you server awards...")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if interaction.user == self.user:
            guild = interaction.guild

            plural = self.plural.value
            plur_low = plural.lower()
            await self.db.execute("UPDATE guilds SET award_plural = ? WHERE guild_id = ?", (plur_low, guild.id))
            await self.db.commit()
            cur = await self.db.execute("SELECT award_plural FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            fetched_plur_low = str(row[0])
            fetched_plur_cap = fetched_plur_low.title()

            now = datetime.now(tz=timezone.utc)
            submitted = discord.Embed(color=self.bot.green, title="Success", description=f"{interaction.user.mention} has successfully set the server's custom award name (plural)!", timestamp=now)
            submitted.add_field(name="Plural (Capitalized)", value=f"{fetched_plur_cap}")
            submitted.add_field(name="Plural (Lowercase)", value=f"{fetched_plur_low}")
            submitted.set_author(name=f"{interaction.user.display_name}", icon_url=f"{interaction.user.display_avatar}")
            await interaction.followup.send(embed=submitted, ephemeral=True)
            await self.stop()

            cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            fetched_logging = row[0]
            if fetched_logging is not None:
                logging = self.bot.get_channel(fetched_logging)
                await logging.send(embed=submitted)

class EmojiView(discord.ui.View):
    def __init__(self, *, timeout = 180, bot: commands.Bot, user: discord.Member):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.user = user
        self.db = bot.database

    @discord.ui.button(label="Set Custom Award Emoji", style=discord.ButtonStyle.blurple)
    async def singular(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Emoji(bot=self.bot, user=self.user))

class Emoji(discord.ui.Modal):
    def __init__(self, *, title = "Emoji", timeout = None, bot: commands.Bot, user: discord.Member):
        super().__init__(title=title, timeout=timeout)
        self.bot = bot
        self.user = user
        self.db = bot.database
    
    emoji = discord.ui.TextInput(label="Emoji", custom_id="emoji_input", placeholder="Enter a cutom emoji for you server awards...")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if interaction.user == self.user:
            guild = interaction.guild

            emoji = self.emoji.value
            await self.db.execute("UPDATE guilds SET award_emoji = ? WHERE guild_id = ?", (emoji, guild.id))
            await self.db.commit()
            cur = await self.db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            fetched_emoji = row[0]

            now = datetime.now(tz=timezone.utc)
            submitted = discord.Embed(color=self.bot.green, title="Success", description=f"{interaction.user.mention} has successfully set the server's custom award emoji!", timestamp=now)
            submitted.add_field(name="Emoji", value=f"{fetched_emoji}")
            submitted.set_author(name=f"{interaction.user.display_name}", icon_url=f"{interaction.user.display_avatar}")
            await interaction.followup.send(embed=submitted, ephemeral=True)
            await self.stop()

            cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            fetched_logging = row[0]
            if fetched_logging is not None:
                logging = self.bot.get_channel(fetched_logging)
                await logging.send(embed=submitted)

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
            fetched_channel = self.bot.get_channel(fetched_channel_id)

            now = datetime.now(tz=timezone.utc)
            submitted = discord.Embed(color=self.bot.green, title="Success", description=f"{interaction.user.mention} has successfully set the server's award leaderboard channel!", timestamp=now)
            submitted.add_field(name="Channel", value=f"{fetched_channel.mention}")
            submitted.set_author(name=f"{interaction.user.display_name}", icon_url=f"{interaction.user.display_avatar}")
            await interaction.followup.send(embed=submitted, ephemeral=True)
            await self.stop()

            cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            fetched_logging = row[0]
            if fetched_logging is not None:
                logging = self.bot.get_channel(fetched_logging)
                await logging.send(embed=submitted)

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

                now = datetime.now(tz=timezone.utc)
                submitted = discord.Embed(color=self.bot.green, title="Success", description=f"{interaction.user.mention} has successfully set the server's award reaction toggle!", timestamp=now)
                submitted.add_field(name="Toggle", value=f"True")
                submitted.set_author(name=f"{interaction.user.display_name}", icon_url=f"{interaction.user.display_avatar}")
                await interaction.followup.send(embed=submitted, ephemeral=True)
                await self.stop()
            
            if toggle == "False":
                await self.db.execute("UPDATE guilds SET award_reaction_toggle = 0 WHERE guild_id = ?", (guild.id,))
                await self.db.commit()

                now = datetime.now(tz=timezone.utc)
                submitted = discord.Embed(color=self.bot.green, title="Success", description=f"{interaction.user.mention} has successfully set the server's award reaction toggle!", timestamp=now)
                submitted.add_field(name="Toggle", value=f"False")
                submitted.set_author(name=f"{interaction.user.display_name}", icon_url=f"{interaction.user.display_avatar}")
                await interaction.followup.send(embed=submitted, ephemeral=True)
                await self.stop()

            cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            fetched_logging = row[0]
            if fetched_logging is not None:
                logging = self.bot.get_channel(fetched_logging)
                await logging.send(embed=submitted)

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

class Awards(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.database

    @app_commands.command(name="setup")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup(self, interaction: discord.Interaction):
        """(Admin Only) Sets the name, emoji, and leaderboard channel for the server awards.
        """
        await interaction.response.defer(ephemeral=True)
        try:

            guild = interaction.guild
            await self.db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild.id,))
            await self.db.commit()

            embed = discord.Embed(color=self.bot.blurple, title="Award Setup", description="Please use the button below to set the server's custom **award name (singular)**. Examples include `award`, `point`, `star`, or `like`.")
            singular_view = SingularView(bot=self.bot, user=interaction.user)
            response = await interaction.followup.send(wait=True, embed=embed, view=singular_view)
            await singular_view.wait()

            embed = discord.Embed(color=self.bot.blurple, title="Award Setup", description="Please use the button below to set the server's custom **award name (plural)**. For example, if you set the award name (singular) to `award`, you should set the award name (plural) to `awards`.")
            plural_view = PluralView(bot=self.bot, user=interaction.user)
            response = await response.edit(embed=embed, view=plural_view)
            await plural_view.wait()

            embed = discord.Embed(color=self.bot.blurple, title="Award Setup", description="Please use the button below to set the server's custom **award emoji**. This emoji will represent the awards on the server's award leaderboad.")
            emoji_view = EmojiView(bot=self.bot, user=interaction.user)
            response = await response.edit(embed=embed, view=emoji_view)
            await emoji_view.wait()

            embed = discord.Embed(color=self.bot.blurple, title="Award Setup", description="Please use the dropdown below to set the server's **award leaderboard channel**. This bot will post the server's award leaderboard to this channel and update the leaderboard when any changes are made to award amounts.")
            leaderboard_view = LeaderboardView(bot=self.bot, user=interaction.user)
            response = await response.edit(embed=embed, view=leaderboard_view)
            await leaderboard_view.wait()

            embed = discord.Embed(color=self.bot.blurple, title="Award Setup", description="Please use the dropdown below to set the server's **award reaction toggle**. If set to `True`, members will be able to add and remove awards via emoji reactions. If set to `False`, members will only be able to add and remove awards via slash commands.")
            toggle_view = AwardReactionView(bot=self.bot, user=interaction.user)
            response = await response.edit(embed=embed, view=toggle_view)
            await toggle_view.wait()
        
        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, ephemeral=True)
            print(traceback.format_exc())

    @app_commands.command(name="clear")
    @app_commands.checks.has_permissions(administrator=True)
    async def clear(self, ctx: commands.Context):
        """(Admin Only) Clears every member's awards in the server.
        """
        await ctx.defer(ephemeral=True)
        try:

            guild = ctx.guild
            guild_id = guild.id
            await self.db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            await self.db.commit()

            cur = await self.db.execute("SELECT award_plural FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            plur_low = row[0]
            if plur_low is None:
                plur_low = "awards"
            
            cur = await self.db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            moji = row[0]
            if moji is None:
                moji = "🏅"
            
            member_ids = [member.id for member in guild.members if not member.bot]
            for member_id in member_ids:
                guild_member_id = str(guild_id) + str(member_id)
                await self.db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
                await self.db.commit()
                await self.db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (0, guild_member_id))
                await self.db.commit()
            
            embed = discord.Embed(color=self.bot.green, title=f"Success", description=f"{guild.name} has had all its {plur_low} cleared! {moji}")
            await ctx.send(embed=embed, ephemeral=True)

            cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
            row = await cur.fetchone()
            fetched_logging = row[0]
            if fetched_logging is not None:
                logging = self.bot.get_channel(fetched_logging)
                now = datetime.now(tz=timezone.utc)
                log = discord.Embed(color=self.bot.blurple, title="Awards Log", description=f"{ctx.author.mention} has just cleared the awards for the server.", timestamp=now)
                log.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
                await logging.send(embed=log)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await ctx.send(embed=error, ephemeral=True)
            print(traceback.format_exc())

    @commands.Cog.listener(name="on_reaction_add")
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.Member):
        try:
            message = reaction.message
            channel = message.channel
            guild = message.guild
            guild_id = guild.id
            member = message.author
            member_id = member.id
            await self.db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            await self.db.commit()
            cur = await self.db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            moji = row[0]
            if moji is None:
                moji = "🏅"
            if str(reaction.emoji) == moji:
                users = [user async for user in reaction.users()]
                if len(users) == 1:
                    cur = await self.db.execute("SELECT award_react_toggle FROM guilds WHERE guild_id = ?", (guild_id,))
                    row = await cur.fetchone()
                    toggle = row[0]
                    if toggle == 1:
                        cur = await self.db.execute("SELECT award_singular FROM guilds WHERE guild_id = ?", (guild_id,))
                        row = await cur.fetchone()
                        sing_low = row[0]
                        if sing_low is None:
                            sing_low = "award"
                        sing_cap = sing_low.title()
                        cur = await self.db.execute("SELECT award_plural FROM guilds WHERE guild_id = ?", (guild_id,))
                        row = await cur.fetchone()
                        plur_low = row[0]
                        if plur_low is None:
                            plur_low = "awards"
                        guild_member_id = str(guild_id) + str(member_id)
                        await self.db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
                        await self.db.commit()
                        cur = await self.db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
                        row = await cur.fetchone()
                        current = row[0]
                        if current is None:
                            current = 0
                        new = current + 1
                        await self.db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (new, guild_member_id))
                        await self.db.commit()
                        cur = await self.db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
                        row = await cur.fetchone()
                        new = row[0]
                        if new == 1:
                            embed = discord.Embed(color=self.bot.green, title=f"{sing_cap} Added", description=f"{member.mention} now has {new} {sing_low}! ({sing_cap} added by {user.mention}.)")
                        else:
                            embed = discord.Embed(color=self.bot.green, title=f"{sing_cap} Added", description=f"{member.mention} now has {new} {plur_low}! ({sing_cap} added by {user.mention}.)")
                        await channel.send(embed=embed, reference=message)
        except Exception:
            traceback.print_exc()

    @commands.Cog.listener(name="on_reaction_remove")
    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.Member):
        try:
            message = reaction.message
            channel = message.channel
            guild = message.guild
            guild_id = guild.id
            member = message.author
            member_id = member.id
            await self.db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            await self.db.commit()
            cur = await self.db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            moji = row[0]
            if moji is None:
                moji = "🏅"
            if str(reaction.emoji) == moji:
                users = [user async for user in reaction.users()]
                if len(users) == 1:
                    cur = await self.db.execute("SELECT award_react_toggle FROM guilds WHERE guild_id = ?", (guild_id,))
                    row = await cur.fetchone()
                    toggle = row[0]
                    if toggle == 1:
                        cur = await self.db.execute("SELECT award_singular FROM guilds WHERE guild_id = ?", (guild_id,))
                        row = await cur.fetchone()
                        sing_low = row[0]
                        if sing_low is None:
                            sing_low = "award"
                        sing_cap = sing_low.title()
                        cur = await self.db.execute("SELECT award_plural FROM guilds WHERE guild_id = ?", (guild_id,))
                        row = await cur.fetchone()
                        plur_low = row[0]
                        if plur_low is None:
                            plur_low = "awards"
                        guild_member_id = str(guild_id) + str(member_id)
                        await self.db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
                        await self.db.commit()
                        cur = await self.db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
                        row = await cur.fetchone()
                        current = row[0]
                        if current is None:
                            current = 0
                        if current > 0:
                            new = current - 1
                            await self.db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (new, guild_member_id))
                            await self.db.commit()
                            cur = await self.db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
                            row = await cur.fetchone()
                            new = row[0]
                            if new == 0:
                                embed = discord.Embed(color=self.bot.red, title=f"{sing_cap} Removed", description=f"{member.mention} no longer has any awards! ({sing_cap} removed by {user.mention}.)")
                            elif new == 1:
                                embed = discord.Embed(color=self.bot.red, title=f"{sing_cap} Removed", description=f"{member.mention} now has {new} {sing_low}! ({sing_cap} removed by {user.mention}.)")
                            else:
                                embed = discord.Embed(color=self.bot.red, title=f"{sing_cap} Removed", description=f"{member.mention} now has {new} {plur_low}! ({sing_cap} removed by {user.mention}.)")
                            await channel.send(embed=embed, reference=message)
        except Exception:
            traceback.print_exc()

    @app_commands.command(name="add")
    async def add(self, ctx: commands.Context, amount: Optional[int], member: Optional[discord.Member]):
        """Adds awards to the command user or another selected member.

        Parameters
        -----------
        amount : int, optional
            Choose the number of awards to add. (Default: 1)
        member : discord.Member, optional
            Choose the member to add the awards to. (Default: Self)
        """
        await ctx.defer(ephemeral=True)
        try:

            guild_id = ctx.guild.id
            if amount is None:
                amount = 1
            if member is None:
                member = ctx.author
            member_id = member.id

            await self.db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            await self.db.commit()
            
            cur = await self.db.execute("SELECT award_singular FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            sing_low = row[0]
            if sing_low is None:
                sing_low = "award"
            sing_cap = sing_low.title()

            cur = await self.db.execute("SELECT award_plural FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            plur_low = row[0]
            if plur_low is None:
                plur_low = "awards"
            plur_cap = plur_low.title()

            cur = await self.db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            moji = row[0]
            if moji is None:
                moji = "🏅"

            guild_member_id = str(guild_id) + str(member_id)
            await self.db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
            await self.db.commit()

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
            
            cur = await self.db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
            row = await cur.fetchone()
            new = row[0]
            if new == 1:
                embed = discord.Embed(color=self.bot.green, title=f"{sing_cap} Added", description=f"{member.mention} now has {new} {sing_low}!")
            else:
                embed = discord.Embed(color=self.bot.green, title=f"{plur_cap} Added", description=f"{member.mention} now has {new} {plur_low}!")
        
        except Exception as e:
            embed = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            print(traceback.format_exc())
        
        await ctx.send(embed=embed, ephemeral=True)
        

    @app_commands.command(name="remove")
    async def remove(self, ctx: commands.Context, amount: Optional[int], member: Optional[discord.Member]):
        """Removes awards from the command user or another selected member.

        Parameters
        -----------
        amount : int, optional
            Choose the number of awards to remove. (Default: 1)
        member : discord.Member, optional
            Choose the member to remove the awards from. (Default: Self)
        """
        await ctx.defer(ephemeral=True)
        try:

            guild_id = ctx.guild.id
            if amount is None:
                amount = 1
            if member is None:
                member = ctx.author
            member_id = member.id

            await self.db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            await self.db.commit()

            cur = await self.db.execute("SELECT award_singular FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            sing_low = row[0]
            if sing_low is None:
                sing_low = "award"
            
            cur = await self.db.execute("SELECT award_plural FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            plur_low = row[0]
            if plur_low is None:
                plur_low = "awards"
            plur_cap = plur_low.title()

            cur = await self.db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            moji = row[0]
            if moji is None:
                moji = "🏅"
            
            guild_member_id = str(guild_id) + str(member_id)
            await self.db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
            await self.db.commit()

            cur = await self.db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
            row = await cur.fetchone()
            current = row[0]
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
                new = row[0]
                if new == 0:
                    embed = discord.Embed(color=self.bot.green, title=f"{plur_cap} Removed", description=f"{member.mention} no longer has any {plur_low}!")
                elif new == 1:
                    embed = discord.Embed(color=self.bot.green, title=f"{plur_cap} Removed", description=f"{member.mention} now has {new} {sing_low}!")
                else:
                    embed = discord.Embed(color=self.bot.green, title=f"{plur_cap} Removed", description=f"{member.mention} now has {new} {plur_low}!")
        
        except Exception as e:
            embed = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            print(traceback.format_exc())
        
        await ctx.send(embed=embed, ephemeral=True)

    @app_commands.command(name="check")
    async def check(self, ctx: commands.Context, member: Optional[discord.Member]):
        """Returns the number of awards that the command user or another selected user currently has.

        Parameters
        -----------
        member : discord.Member, optional
            Choose the member that you would like to check the number of awards for. (Default: Self)
        """
        await ctx.defer(ephemeral=True)
        try:

            guild_id = ctx.guild.id
            if member is None:
                member = ctx.author
            member_id = member.id

            await self.db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            await self.db.commit()

            cur = await self.db.execute("SELECT award_singular FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            sing_low = row[0]
            if sing_low is None:
                sing_low = "award"
            sing_cap = sing_low.title()

            cur = await self.db.execute("SELECT award_plural FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            plur_low = row[0]
            if plur_low is None:
                plur_low = "awards"
            
            cur = await self.db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            moji = row[0]
            if moji is None:
                moji = "🏅"
            
            guild_member_id = str(guild_id) + str(member_id)
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
                embed = discord.Embed(color=self.bot.green, title=f"{sing_cap} Check", description=f"{member.mention} doesn't have any {plur_low}!")
            elif amount == 1:
                embed = discord.Embed(color=self.bot.green, title=f"{sing_cap} Check", description=f"{member.mention} has {amount} {sing_low}!")
            else:
                embed = discord.Embed(color=self.bot.green, title=f"{sing_cap} Check", description=f"{member.mention} has {amount} {plur_low}!")
        
        except Exception as e:
            embed = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            print(traceback.format_exc())
        
        await ctx.send(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    print("Setting up Cog: Awards.Awards")

async def teardown(bot: commands.Bot):
    print("Tearing down Cog: Awards.Awards")