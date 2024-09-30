import discord
import aiosqlite
import requests
import feedparser
from discord import ChannelType, app_commands
from discord.ui import ChannelSelect
from discord.ext import commands
from typing import Any, Optional
from datetime import datetime, timezone, timedelta

bot = commands.Bot(
    command_prefix='rb!',
    description="A multi-purpose Discord bot made by GitHub user gemhue.",
    intents=discord.Intents.all()
)

class ChannelsSelector(ChannelSelect):
    def __init__(self):
        super().__init__(
            channel_types=[ChannelType.text],
            placeholder="Select channels... (Limit: 25)",
            min_values=1,
            max_values=25,
            row=1
        )

    async def callback(self, interaction: discord.Interaction) -> Any:
        channels: list[DropdownView] = self.values
        self.view.values = [c for c in channels]

class DropdownView(discord.ui.View):
    def __init__(self, *, timeout=180.0):
        super().__init__(timeout=timeout)
        self.value = None
        self.add_item(ChannelsSelector())

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green, row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red, row=2)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        self.stop()

class BackgroundTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name="emoji_reactions")
    async def on_message(self, message: discord.Message):
        message = message.content.lower()
        list1 = ['lesbian','sapphic','wlw']
        moji1 = bot.get_emoji(1274435288499884094)
        if any(x in message for x in list1):
            await message.add_reaction(moji1)
        list2 = ['gay','achillean','mlm']
        moji2 = bot.get_emoji(1274435330174615624)
        if any(x in message for x in list2):
            await message.add_reaction(moji2)
        list3 = ['bisexual','biromantic','bi woman','bi women','bi lady','bi ladies','bi girl','bi gal','bi man','bi men','bi guy','bi dude','bi boy','bi person','bi people']
        moji3 = bot.get_emoji(1274435359878676560)
        if any(x in message for x in list3):
            await message.add_reaction(moji3)
        list4 = ['asexual','aromantic','acespec','arospec','ace spec','aro spec','ace-spec','aro-spec']
        moji4 = bot.get_emoji(1274435406804291634)
        if any(x in message for x in list4):
            await message.add_reaction(moji4)
        list5 = ['transgender','transsexual','trans woman','trans women','trans lady','trans ladies','trans girl','trans gal','trans man','trans men','trans guy','trans dude','trans boy','trans person','trans people']
        moji5 = bot.get_emoji(1274435448726622208)
        if any(x in message for x in list5):
            await message.add_reaction(moji5)
        list6 = ['nonbinary','non binary','non-binary','enby']
        moji6 = bot.get_emoji(1274435483912638515)
        if any(x in message for x in list6):
            await message.add_reaction(moji6)
        list7 = ['transfeminine','trans feminine','trans-feminine','transfem','trans fem','trans-fem']
        moji7 = bot.get_emoji(1274435557744840820)
        if any(x in message for x in list7):
            await message.add_reaction(moji7)
        list8 = ['transmasculine','trans masculine','trans-masculine','transmasc','trans masc','trans-masc']
        moji8 = bot.get_emoji(1274435528883961989)
        if any(x in message for x in list8):
            await message.add_reaction(moji8)
        await bot.process_commands(message)
        
    @commands.Cog.listener(name="member_join")
    async def on_member_join(self, member: discord.Member):
        guild = member.guild
        guild_id = guild.id
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            cur = await db.execute("SELECT welcome_channel_id FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            channel_id = row[0]
            cur = await db.execute("SELECT welcome_message FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            message = row[0]
            cur = await db.execute("SELECT join_role_id FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            role_id = row[0]
            cur = await db.execute("SELECT bot_join_role_id FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            botrole_id = row[0]
            await db.commit()
            await db.close()
        if channel_id is not None:
            channel = guild.get_channel(channel_id)
            if message is not None:
                embed = discord.Embed(color=member.accent_color, description=message, timestamp=datetime.now())
                content = f"-# {member.mention}"
                await channel.send(content=content, embed=embed)
            else:
                description = f"Welcome to {guild.name}, {member.mention}!"
                embed = discord.Embed(color=member.accent_color, description=description, timestamp=datetime.now())
                content = f"-# {member.mention}"
                await channel.send(content=content, embed=embed)
        if role_id is not None and not member.bot:
            role = guild.get_role(role_id)
            await member.add_roles(role)
        if botrole_id is not None and member.bot:
            botrole = guild.get_role(botrole_id)
            await member.add_roles(botrole)

    @commands.Cog.listener(name="member_remove")
    async def on_member_remove(self, member: discord.Member):
        guild = member.guild
        guild_id = guild.id
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            cur = await db.execute("SELECT goodbye_channel_id FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            channel_id = row[0]
            cur = await db.execute("SELECT goodbye_message FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            message = row[0]
            await db.commit()
            await db.close()
        if channel_id is not None:
            channel = guild.get_channel(channel_id)
            if message is not None:
                embed = discord.Embed(color=member.accent_color, description=message, timestamp=datetime.now())
                await channel.send(embed=embed)
            else:
                description = f"{member.mention} has just left {guild.name}!"
                embed = discord.Embed(color=member.accent_color, description=description, timestamp=datetime.now())
                await channel.send(embed=embed)

class SetupCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sync")
    @commands.is_owner()
    async def sync(self, ctx: commands.Context):
        """(Bot Owner Only) Syncs the local command tree.
        """
        await ctx.defer()
        guild = ctx.guild
        await bot.tree.sync(guild=guild)
        embed = discord.Embed(title="Update", description=f"The bot's local command tree has been synced!")
        await ctx.send(embed=embed)
    
    @commands.command(name="globalsync")
    @commands.is_owner()
    async def globalsync(self, ctx: commands.Context):
        """(Bot Owner Only) Syncs the global command tree.
        """
        await ctx.defer()
        await bot.tree.sync(guild=None)
        embed = discord.Embed(title="Update", description=f"The bot's global command tree has been synced!")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="setchannels")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def setchannels(self, ctx: commands.Context, logging_channel: Optional[discord.TextChannel], welcome_channel: Optional[discord.TextChannel], goodbye_channel: Optional[discord.TextChannel]):
        """(Admin Only) Sets the channels for logging messages, welcome messages, and goodbye messages.

        Parameters
        -----------
        logging_channel : discord.TextChannel, optional
            Set the channels for logging messages.
        welcome_channel : discord.TextChannel, optional
            Set the channels for welcome messages.
        goodbye_channel : discord.TextChannel, optional
            Set the channels for goodbye messages.
        """
        guild = ctx.guild
        guild_id = guild.id
        embed = discord.Embed(color=ctx.author.accent_color, title="Channels Set")
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            if logging_channel is not None:
                logging_id = logging_channel.id
                await db.execute("UPDATE guilds SET logging_channel_id = ? WHERE guild_id = ?", (logging_id, guild_id))
                cur = await db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild_id,))
                row = await cur.fetchone()
                fetched_logging = row[0]
                logging = guild.get_channel(fetched_logging)
                embed.add_field(name="Logging Channel", value=f"{logging.mention}")
            if welcome_channel is not None:
                welcome_id = welcome_channel.id
                await db.execute("UPDATE guilds SET welcome_channel_id = ? WHERE guild_id = ?", (welcome_id, guild_id))
                cur = await db.execute("SELECT welcome_channel_id FROM guilds WHERE guild_id = ?", (guild_id,))
                row = await cur.fetchone()
                fetched_welcome = row[0]
                welcome = guild.get_channel(fetched_welcome)
                embed.add_field(name="Welcome Channel", value=f"{welcome.mention}")
            if goodbye_channel is not None:
                goodbye_id = goodbye_channel.id
                await db.execute("UPDATE guilds SET goodbye_channel_id = ? WHERE guild_id = ?", (goodbye_id, guild_id))
                cur = await db.execute("SELECT goodbye_channel_id FROM guilds WHERE guild_id = ?", (guild_id,))
                row = await cur.fetchone()
                fetched_goodbye = row[0]
                goodbye = guild.get_channel(fetched_goodbye)
                embed.add_field(name="Goodbye Channel", value=f"{goodbye.mention}")
            await db.commit()
            await db.close()
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="setwelcome")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def setwelcome(self, ctx: commands.Context, message: str):
        """(Admin Only) Sets the welcome message for members who join the server.

        Parameters
        -----------
        message : str
            Set the welcome message for members who join the server.
        """
        ctx.defer(ephemeral=True)
        guild = ctx.guild
        guild_id = guild.id
        embed = discord.Embed(color=ctx.author.accent_color, title="Message Set")
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            await db.execute("UPDATE guilds SET welcome_message = ? WHERE guild_id = ?", (message, guild_id))
            cur = await db.execute("SELECT welcome_message FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            fetched_message = row[0]
            embed.add_field(name="Welcome Message", value=f"{fetched_message}")
            await db.commit()
            await db.close()
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="setgoodbye")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def setgoodbye(self, ctx: commands.Context, message: str):
        """(Admin Only) Sets the goodbye message for members who leave the server.

        Parameters
        -----------
        message : str
            Set the goodbye message for members who leave the server.
        """
        ctx.defer(ephemeral=True)
        guild = ctx.guild
        guild_id = guild.id
        embed = discord.Embed(color=ctx.author.accent_color, title="Message Set")
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            await db.execute("UPDATE guilds SET goodbye_message = ? WHERE guild_id = ?", (message, guild_id))
            cur = await db.execute("SELECT goodbye_message FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            fetched_message = row[0]
            embed.add_field(name="Goodbye Message", value=f"{fetched_message}")
            await db.commit()
            await db.close()
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="setjoinroles")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def setjoinroles(self, ctx: commands.Context, role: discord.Role, botrole: Optional[discord.Role]):
        """(Admin Only) Sets the roles to give to new members who join the server.

        Parameters
        -----------
        role : discord.Role
            Choose the role that you would like to give to new members on join.
        botrole : discord.Role, optional
            Choose the role that you would like to give to new bots on join.
        """
        ctx.defer(ephemeral=True)
        guild = ctx.guild
        guild_id = guild.id
        embed = discord.Embed(color=ctx.author.accent_color, title="Roles Set")
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            role_id = role.id
            await db.execute("UPDATE guilds SET join_role_id = ? WHERE guild_id = ?", (role_id, guild_id))
            cur = await db.execute("SELECT join_role_id FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            role_id = row[0]
            role = guild.get_role(role_id)
            embed.add_field(name="Join Role", value=f"{role.mention}")
            if botrole is not None:
                botrole_id = botrole.id
                await db.execute("UPDATE guilds SET bot_join_role_id = ? WHERE guild_id = ?", (botrole_id, guild_id))
                cur = await db.execute("SELECT bot_join_role_id FROM guilds WHERE guild_id = ?", (guild_id,))
                row = await cur.fetchone()
                botrole_id = row[0]
                botrole = guild.get_role(botrole_id)
                embed.add_field(name="Bot Join Role", value=f"{botrole.mention}")
            await db.commit
            await db.close()
        ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="activityroles")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def activityroles(self, ctx: commands.Context, days: int, active: discord.Role, inactive: discord.Role):
        """(Admin Only) Assigns an active role to active members and an inactive role to inactive members.

        Parameters
        -----------
        days : int
            Set the number of days a member must be inactive before getting the inactive role.
        inactive : discord.Role
            Choose the role that you would like to give to inactive members.
        active : discord.Role
            Choose the role that you would like to give to active members.
        """
        await ctx.defer(ephemeral=True)
        guild = ctx.guild
        channels = guild.text_channels
        members = [m for m in guild.members if not m.bot]
        today =  datetime.now(timezone.utc)
        setdays = timedelta(days=days)
        daysago = today-setdays
        newmembers = [m for m in members if m.joined_at < daysago]
        activemembers = []
        inactivemembers = []
        for channel in channels:
            async for message in channel.history(after=daysago):
                if message.author in members and message.author not in activemembers:
                    activemembers.append(message.author)
        for member in members:
            if member not in newmembers and member not in activemembers:
                inactivemembers.append(member)
            if member in newmembers and member not in activemembers:
                activemembers.append(member)
        for member in activemembers:
            if active not in member.roles:
                await member.add_roles(active)
            if inactive in member.roles:
                await member.remove_roles(inactive)
        for member in inactivemembers:
            if inactive not in member.roles:
                await member.add_roles(inactive)
            if active in member.roles:
                await member.remove_roles(active)
        await ctx.send(f"{len(activemembers)} members now have the {active.mention} role!\n{len(inactivemembers)} members now have the {inactive.mention} role!")

class PurgeCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="purgemember")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def purgemember(self, ctx: commands.Context, member: discord.Member):
        """(Admin Only) Purge all of a member's unpinned messages in a set list of up to 25 channels.

        Parameters
        -----------
        member : discord.Member
            Provide the member who's unpinned messages you would like to purge.
        """
        await ctx.defer()
        view = DropdownView()
        embed = discord.Embed(title="🗑️ Purge Member 🗑️", description=f"Which channel(s) would you like to purge {member.mention}'s unpinned messages from?")
        response = await ctx.send(embed=embed, view=view)
        await view.wait()
        if view.value == True:
            selected = [c.resolve() for c in view.values]
            mentions = [c.mention for c in selected]
            selectedlist = ", ".join(mentions)
            embed = discord.Embed(title="📋 Selected Channels 📋", description=f'{selectedlist}')
            await response.edit(embed=embed, view=None)
            for channel in selected:
                messages = [m async for m in channel.history(limit=None)]
                unpinned = [m for m in messages if not m.pinned]
                deleted = []
                while len(unpinned) > 0:
                    deleted += await channel.purge(check=lambda message: message.author == member and message.pinned == False, oldest_first=True)
                    messages = [m async for m in channel.history(limit=None)]
                    unpinned = [m for m in messages if not m.pinned]
                if len(deleted) == 1:
                    embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} message was just removed from {channel.mention}!')
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} messages were just removed from {channel.mention}!')
                    await ctx.send(embed=embed)
            embed = discord.Embed(title="✔️ Done ✔️", description=f'The purge is now complete!')
            await ctx.send(embed=embed)
        elif view.value == False:
            embed = discord.Embed(title="❌ Cancelled ❌", description='This interaction has been cancelled. No messages have been purged.')
            await response.edit(embed=embed, view=None)
        else:
            embed = discord.Embed(title="⌛ Timed Out ⌛", description='This interaction has timed out. No messages have been purged.')
            await response.edit(embed=embed, view=None)

    @commands.hybrid_command(name="purgechannels")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def purgechannels(self, ctx: commands.Context):
        """(Admin Only) Purge all unpinned messages in a set list of up to 25 channels."""
        await ctx.defer()
        view = DropdownView()
        embed = discord.Embed(title="🗑️ Purge Channels 🗑️", description="Which channel(s) would you like to purge all unpinned messages from?")
        response = await ctx.send(embed=embed, view=view)
        await view.wait()
        if view.value == True:
            selected = [c.resolve() for c in view.values]
            mentions = [c.mention for c in selected]
            selectedlist = ", ".join(mentions)
            embed = discord.Embed(title="📋 Selected Channels 📋", description=f'{selectedlist}')
            await response.edit(embed=embed, view=None)
            for channel in selected:
                messages = [m async for m in channel.history(limit=None)]
                unpinned = [m for m in messages if not m.pinned]
                deleted = []
                while len(unpinned) > 0:
                    deleted += await channel.purge(check=lambda message: message.pinned == False, oldest_first=True)
                    messages = [m async for m in channel.history(limit=None)]
                    unpinned = [m for m in messages if not m.pinned]
                if len(deleted) == 1:
                    embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} message was just removed from {channel.mention}!')
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} messages were just removed from {channel.mention}!')
                    await ctx.send(embed=embed)
            embed = discord.Embed(title="✔️ Done ✔️", description=f'The purge is now complete!')
            await ctx.send(embed=embed)
        elif view.value == False:
            embed = discord.Embed(title="❌ Cancelled ❌", description='This interaction has been cancelled. No messages have been purged.')
            await response.edit(embed=embed, view=None)
        else:
            embed = discord.Embed(title="⌛ Timed Out ⌛", description='This interaction has timed out. No messages have been purged.')
            await response.edit(embed=embed, view=None)

    @commands.hybrid_command(name="purgeserver")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def purgeserver(self, ctx: commands.Context):
        """(Admin Only) Purges all unpinned messages in a server, excluding up to 25 channels."""
        await ctx.defer()
        view = DropdownView()
        embed = discord.Embed(title="🗑️ Purge Server 🗑️", description="Which channels would you like to **exclude** from the purge of all unpinned messages?")
        response = await ctx.send(embed=embed, view=view)
        await view.wait()
        if view.value == True:
            excluded = [c for c in view.values]
            mentions = [c.mention for c in excluded]
            excludedlist = ", ".join(mentions)
            embed = discord.Embed(title="📋 Excluded Channels 📋", description=f'{excludedlist}')
            await response.edit(embed=embed, view=None)
            selected = [c for c in ctx.guild.text_channels if c not in excluded]
            for channel in selected:
                messages = [m async for m in channel.history(limit=None)]
                unpinned = [m for m in messages if not m.pinned]
                deleted = []
                while len(unpinned) > 0:
                    deleted += await channel.purge(check=lambda message: message.pinned == False, oldest_first=True)
                    messages = [m async for m in channel.history(limit=None)]
                    unpinned = [m for m in messages if not m.pinned]
                if len(deleted) == 1:
                    embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} message was just removed from {channel.mention}!')
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} messages were just removed from {channel.mention}!')
                    await ctx.send(embed=embed)
            embed = discord.Embed(title="✔️ Done ✔️", description=f'The purge is now complete!')
            await ctx.send(embed=embed)
        elif view.value == False:
            embed = discord.Embed(title="❌ Cancelled ❌", description='This interaction has been cancelled. No messages have been purged.')
            await response.edit(embed=embed, view=None)
        else:
            embed = discord.Embed(title="⌛ Timed Out ⌛", description='This interaction has timed out. No messages have been purged.')
            await response.edit(embed=embed, view=None)

class AwardCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="setawards")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def setawards(self, ctx: commands.Context, name_singular: str, name_plural: str, emoji: str):
        """(Admin Only) Sets the name and emoji for the server awards.

        Parameters
        -----------
        name_singular : str
            Provide the singular form of the award name. (Default: Award)
        name_plural : str
            Provide the plural form of the award name. (Default: Awards)
        emoji : str
            Choose the emoji you would like to represent the award. (Default: 🏅)
        """
        await ctx.defer(ephemeral=True)
        guild = ctx.guild
        guild_id = guild.id
        sing_low = name_singular.lower()
        plur_low = name_plural.lower()
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            await db.execute("UPDATE guilds SET award_singular = ? WHERE guild_id = ?", (sing_low, guild_id))
            cur = await db.execute("SELECT award_singular FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            fetched_sing_low = str(row[0])
            fetched_sing_cap = fetched_sing_low.title()
            await db.execute("UPDATE guilds SET award_plural = ? WHERE guild_id = ?", (plur_low, guild_id))
            cur = await db.execute("SELECT award_plural FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            fetched_plur_low = str(row[0])
            fetched_plur_cap = fetched_plur_low.title()
            await db.execute("UPDATE guilds SET award_emoji = ? WHERE guild_id = ?", (emoji, guild_id))
            cur = await db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            fetched_moji = str(row[0])
            await db.commit()
            await db.close()
        embed = discord.Embed(title="Custom Awards Set")
        embed.add_field(name="Name (Singular)", value=f"{fetched_sing_cap}")
        embed.add_field(name="Name (Plural)", value=f"{fetched_plur_cap}")
        embed.add_field(name="Emoji", value=f"{fetched_moji}")
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="clearawards")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def clearawards(self, ctx: commands.Context):
        """(Admin Only) Clears all of the awards in the server.
        """
        await ctx.defer(ephemeral=True)
        guild = ctx.guild
        guild_id = guild.id
        member_ids = [member.id for member in guild.members if not member.bot]
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            cur = await db.execute("SELECT award_plural FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            plur_low = row[0]
            if plur_low is None:
                plur_low = "awards"
            plur_cap = plur_low.title()
            cur = await db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            moji = row[0]
            if moji is None:
                moji = "🏅"
            for member_id in member_ids:
                await db.execute("UPDATE members SET awards = ? WHERE member_id = ?", (0, member_id))
            await db.commit()
            await db.close()
        embed = discord.Embed(title=f"{moji} {plur_cap} Cleared {moji}", description=f"{guild.name} has had all its {plur_low} cleared!")
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="awardreactiontoggle")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def awardreactiontoggle(self, ctx: commands.Context, toggle: bool):
        """(Admin Only) Toggles the ability for users to add or remove awards with reactions.

        Parameters
        -----------
        toggle : bool
            Set to True to toggle award reactions on. Set to False to toggle award reactions off.
        """
        ctx.defer(ephemeral=True)
        guild = ctx.guild
        guild_id = guild.id
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            if toggle == True:
                toggle = 1
                await db.execute("UPDATE guilds SET award_reaction_toggle = ? WHERE guild_id = ?", (toggle, guild_id))
                cur = await db.execute(("SELECT award_reaction_toggle FROM guilds WHERE guild_id = ?", (guild_id,)))
                row = await cur.fetchone()
                fetched_toggle = row[0]
                embed = discord.Embed(title="Update", description=f"The toggle for award reactions has been set to **True** AKA {fetched_toggle}. Reacting and un-reacting to posts with the award emoji **will** now add and remove awards.")
            elif toggle == False:
                toggle = 0
                await db.execute("UPDATE guilds SET award_reaction_toggle = ? WHERE guild_id = ?", (toggle, guild_id))
                cur = await db.execute(("SELECT award_reaction_toggle FROM guilds WHERE guild_id = ?", (guild_id,)))
                row = await cur.fetchone()
                fetched_toggle = row[0]
                embed = discord.Embed(title="Update", description=f"The toggle for award reactions has been set to **False** AKA {fetched_toggle}. Reacting and un-reacting to posts with the award emoji **will not** add and remove awards.")
            else:
                embed = discord.Embed(title="Error", description=f"Your input could not be parsed. Please enter either True to toggle award reactions ON or False to toggle award reactions OFF.")
            await db.commit()
            await db.close()
        ctx.send(embed=embed, ephemeral=True)

    @commands.Cog.listener(name="reactionadd")
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.Member):
        message = reaction.message
        channel = message.channel
        guild = message.guild
        guild_id = guild.id
        member = message.author
        member_id = member.id
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            cur = await db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            moji = row[0]
            if moji is None:
                moji = "🏅"
            if str(reaction.emoji) == moji:
                cur = await db.execute("SELECT award_react_toggle FROM guilds WHERE guild_id = ?", (guild_id,))
                row = await cur.fetchone()
                toggle = row[0]
                if toggle == 1:
                    cur = await db.execute("SELECT award_singular FROM guilds WHERE guild_id = ?", (guild_id,))
                    row = await cur.fetchone()
                    sing_low = row[0]
                    if sing_low is None:
                        sing_low = "award"
                    sing_cap = sing_low.title()
                    cur = await db.execute("SELECT award_plural FROM guilds WHERE guild_id = ?", (guild_id,))
                    row = await cur.fetchone()
                    plur_low = row[0]
                    if plur_low is None:
                        plur_low = "awards"
                    await db.execute("INSERT OR IGNORE INTO members (member_id) VALUES (?)", (member_id,))
                    cur = await db.execute("SELECT awards FROM members WHERE member_id = ?", (member_id,))
                    row = await cur.fetchone()
                    awards = row[0]
                    if awards is None:
                        awards = 0
                    awards += 1
                    await db.execute("UPDATE members SET awards = ? WHERE member_id = ?", (awards, member_id))
                    cur = await db.execute("SELECT awards FROM members WHERE member_id = ?", (member_id,))
                    row = await cur.fetchone()
                    awards = row[0]
                    if awards == 1:
                        embed = discord.Embed(title=f"{moji} {sing_cap} Added {moji}", description=f"{member.mention} now has {awards} {sing_low}! ({sing_cap} added by {user.mention}.)")
                    else:
                        embed = discord.Embed(title=f"{moji} {sing_cap} Added {moji}", description=f"{member.mention} now has {awards} {plur_low}! ({sing_cap} added by {user.mention}.)")
                    await channel.send(embed=embed, reference=message)
            await db.commit()
            await db.close()

    @commands.Cog.listener(name="reactionremove")
    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.Member):
        message = reaction.message
        channel = message.channel
        guild = message.guild
        guild_id = guild.id
        member = message.author
        member_id = member.id
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            cur = await db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            moji = row[0]
            if moji is None:
                moji = "🏅"
            if str(reaction.emoji) == moji:
                cur = await db.execute("SELECT award_react_toggle FROM guilds WHERE guild_id = ?", (guild_id,))
                row = await cur.fetchone()
                toggle = row[0]
                if toggle == 1:
                    cur = await db.execute("SELECT award_singular FROM guilds WHERE guild_id = ?", (guild_id,))
                    row = await cur.fetchone()
                    sing_low = row[0]
                    if sing_low is None:
                        sing_low = "award"
                    sing_cap = sing_low.title()
                    cur = await db.execute("SELECT award_plural FROM guilds WHERE guild_id = ?", (guild_id,))
                    row = await cur.fetchone()
                    plur_low = row[0]
                    if plur_low is None:
                        plur_low = "awards"
                    await db.execute("INSERT OR IGNORE INTO members (member_id) VALUES (?)", (member_id,))
                    cur = await db.execute("SELECT awards FROM members WHERE member_id = ?", (member_id,))
                    row = await cur.fetchone()
                    awards = row[0]
                    if awards is None:
                        awards = 0
                    if awards > 0:
                        awards -= 1
                        await db.execute("UPDATE members SET awards = ? WHERE member_id = ?", (awards, member_id))
                        cur = await db.execute("SELECT awards FROM members WHERE member_id = ?", (member_id,))
                        row = await cur.fetchone()
                        awards = row[0]
                        if awards == 0:
                            embed = discord.Embed(title=f"{moji} {sing_cap} Removed {moji}", description=f"{member.mention} no longer has any awards! ({sing_cap} removed by {user.mention}.)")
                        elif awards == 1:
                            embed = discord.Embed(title=f"{moji} {sing_cap} Removed {moji}", description=f"{member.mention} now has {awards} {sing_low}! ({sing_cap} removed by {user.mention}.)")
                        else:
                            embed = discord.Embed(title=f"{moji} {sing_cap} Removed {moji}", description=f"{member.mention} now has {awards} {plur_low}! ({sing_cap} removed by {user.mention}.)")
                        await channel.send(embed=embed, reference=message)
            await db.commit()
            await db.close()

    @commands.hybrid_command(name="addawards")
    async def addawards(self, ctx: commands.Context, amount: Optional[int], member: Optional[discord.Member]):
        """Adds awards to the command user or another selected member.

        Parameters
        -----------
        amount : int, optional
            Choose the number of awards to add. (Default: 1)
        member : discord.Member, optional
            Choose the member to add the awards to. (Default: Self)
        """
        await ctx.defer(ephemeral=True)
        guild = ctx.guild
        guild_id = guild.id
        amount = amount
        if amount is None:
            amount = 1
        member = member
        if member is None:
            member = ctx.author
        member_id = member.id
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            cur = await db.execute("SELECT award_singular FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            sing_low = row[0]
            if sing_low is None:
                sing_low = "award"
            sing_cap = sing_low.title()
            cur = await db.execute("SELECT award_plural FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            plur_low = row[0]
            if plur_low is None:
                plur_low = "awards"
            plur_cap = plur_low.title()
            cur = await db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            moji = row[0]
            if moji is None:
                moji = "🏅"
            await db.execute("INSERT OR IGNORE INTO members (member_id) VALUES (?)", (member_id,))
            cur = await db.execute("SELECT awards FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            awards = row[0]
            if awards is None:
                await db.execute("UPDATE members SET awards = ? WHERE member_id = ?", (amount, member_id))
            else:
                awards += amount
                await db.execute("UPDATE members SET awards = ? WHERE member_id = ?", (amount, member_id))
            cur = await db.execute("SELECT awards FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            awards = row[0]
            await db.commit()
            await db.close()
        if awards == 1:
            embed = discord.Embed(title=f"{moji} {sing_cap} Added {moji}", description=f"{member.mention} now has {awards} {sing_low}!")
        else:
            embed = discord.Embed(title=f"{moji} {plur_cap} Added {moji}", description=f"{member.mention} now has {awards} {plur_low}!")
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="removeawards")
    async def removeawards(self, ctx: commands.Context, amount: Optional[int], member: Optional[discord.Member]):
        """Removes awards from the command user or another selected member.

        Parameters
        -----------
        amount : int, optional
            Choose the number of awards to remove. (Default: 1)
        member : discord.Member, optional
            Choose the member to remove the awards from. (Default: Self)
        """
        await ctx.defer(ephemeral=True)
        guild = ctx.guild
        guild_id = guild.id
        amount = amount
        if amount is None:
            amount = 1
        member = member
        if member is None:
            member = ctx.author
        member_id = member.id
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            cur = await db.execute("SELECT award_singular FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            sing_low = row[0]
            if sing_low is None:
                sing_low = "award"
            cur = await db.execute("SELECT award_plural FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            plur_low = row[0]
            if plur_low is None:
                plur_low = "awards"
            plur_cap = plur_low.title()
            cur = await db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            moji = row[0]
            if moji is None:
                moji = "🏅"
            await db.execute("INSERT OR IGNORE INTO members (member_id) VALUES (?)", (member_id,))
            cur = await db.execute("SELECT awards FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            awards = row[0]
            if awards is None:
                awards = 0
            if awards == 0:
                await db.execute("UPDATE members SET awards = ? WHERE member_id = ?", (awards, member_id))
                embed = discord.Embed(title=f"Error", description=f"{member.mention} doesn't have any {plur_low}!")
            elif awards < amount:
                embed = discord.Embed(title=f"Error", description=f"{member.mention} doesn't have enough {plur_low}!")
            else:
                awards -= amount
                await db.execute("UPDATE members SET awards = ? WHERE member_id = ?", (awards, member_id))
                cur = await db.execute("SELECT awards FROM members WHERE member_id = ?", (member_id,))
                row = await cur.fetchone()
                awards = row[0]
                if awards == 0:
                    embed = discord.Embed(title=f"{moji} {plur_cap} Removed {moji}", description=f"{member.mention} no longer has any {plur_low}!")
                elif awards == 1:
                    embed = discord.Embed(title=f"{moji} {plur_cap} Removed {moji}", description=f"{member.mention} now has {awards} {sing_low}!")
                else:
                    embed = discord.Embed(title=f"{moji} {plur_cap} Removed {moji}", description=f"{member.mention} now has {awards} {plur_low}!")
                await ctx.send(embed=embed, ephemeral=True)
            await db.commit()
            await db.close()
        

    @commands.hybrid_command(name="checkawards")
    async def checkawards(self, ctx: commands.Context, member: Optional[discord.Member]):
        """Returns the number of awards that the user or another selected user currently has.

        Parameters
        -----------
        member : discord.Member, optional
            Choose the member that you would like to check the number of awards for. (Default: Self)
        """
        await ctx.defer(ephemeral=True)
        guild = ctx.guild
        guild_id = guild.id
        member = member
        if member is None:
            member = ctx.author
        member_id = member.id
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            cur = await db.execute("SELECT award_singular FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            sing_low = row[0]
            if sing_low is None:
                sing_low = "award"
            cur = await db.execute("SELECT award_plural FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            plur_low = row[0]
            if plur_low is None:
                plur_low = "awards"
            plur_cap = plur_low.title()
            cur = await db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            moji = row[0]
            if moji is None:
                moji = "🏅"
            await db.execute("INSERT OR IGNORE INTO members (member_id) VALUES (?)", (member_id,))
            cur = await db.execute("SELECT awards FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            awards = row[0]
            if awards is None:
                awards = 0
            if awards == 0:
                await db.execute("INSERT OR IGNORE INTO members (member_id, awards) VALUES (?,?)", (member_id, 0))
                embed = discord.Embed(title=f"{moji} Number of {plur_cap} {moji}", description=f"{member.mention} doesn't have any {plur_low}!")
            elif awards == 1:
                embed = discord.Embed(title=f"{moji} Number of {plur_cap} {moji}", description=f"{member.mention} has {awards} {sing_low}!")
            else:
                embed = discord.Embed(title=f"{moji} Number of {plur_cap} {moji}", description=f"{member.mention} has {awards} {plur_low}!")
            await db.commit()
            await db.close()
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="leaderboard")
    async def leaderboard(self, ctx: commands.Context):
        """Returns the current award leaderboard for the server."""
        await ctx.defer()
        guild = ctx.guild
        guild_id = guild.id
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            cur = await db.execute("SELECT award_singular FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            sing_low = row[0]
            if sing_low is None:
                sing_low = "award"
            sing_cap = sing_low.title()
            cur = await db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            moji = row[0]
            if moji is None:
                moji = "🏅"
            member_awards = {}
            member_ids = [member.id for member in guild.members if not member.bot]
            for member_id in member_ids:
                await db.execute("INSERT OR IGNORE INTO members (member_id) VALUES (?)", (member_id,))
                cur = await db.execute("SELECT awards FROM members WHERE member_id = ?", (member_id,))
                row = await cur.fetchone()
                awards = row[0]
                if awards is None:
                    await db.execute("UPDATE members SET awards = ? WHERE member_id = ?", (awards, member_id))
                elif awards > 0:
                    member_awards[member_id] = awards
            await db.commit()
            await db.close()
        desc = []
        for member, awards in dict(sorted(member_awards.items(), key=lambda item: item[1])):
            awards = awards * moji
            desc.append(f"<@{member}>:\n{awards}")
        description = "\n\n".join(x for x in desc)
        embed = discord.Embed(title=f"{moji} {sing_cap} Leaderboard {moji}", description=description)
        await ctx.send(embed=embed)

class ProfileCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="setprofile")
    async def setprofile(self, ctx: commands.Context, name: Optional[str], age: Optional[str], location: Optional[str], pronouns: Optional[str], gender: Optional[str], sexuality: Optional[str], relationship_status: Optional[str], family_status: Optional[str], biography: Optional[str]):
        """Run this command to set up your member profile. Note that all fields are optional.

        Parameters
        -----------
        name : str, optional
            Provide your name or nickname.
        age : str, optional
            Provide your age or age range.
        location : str, optional
            Provide your continent, country, state, or city of residence.
        pronouns : str, optional
            Provide your pronouns (ex. she/her, he/him, they/them, etc).
        gender : str, optional
            Provide your gender identity label (ex. woman, man, nonbinary, etc).
        sexuality : str, optional
            Provide your sexuality label (ex. lesbian, gay, bisexual, etc).
        relationship_status : str, optional
            Provide your relationship status (ex. single, married, etc).
        family_status : str, optional
            Provide your your family planning status (ex. TTC, expecting, parenting, etc).
        biography : str, optional
            Provide a brief biography (ex. family, hobbies, interests, work, etc).
        """
        await ctx.defer(ephemeral=True)
        guild = ctx.guild
        member = ctx.author
        member_id = int(member.id)
        joined = discord.utils.format_dt(member.joined_at, style="D")
        joinedago = discord.utils.format_dt(member.joined_at, style="R")
        embed = discord.Embed(color=member.accent_color, title=f"{member.name}'s Member Profile", description=f"Member of {guild.name} since {joined} ({joinedago}).")
        if member.avatar is not None:
            embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar}")
        else:
            embed.set_author(name=f"{member.name}")
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO members (member_id) VALUES (?)", (member_id,))
            if name is not None:
                await db.execute("UPDATE members SET name = ? WHERE member_id = ?", (name, member_id))
            cur = await db.execute("SELECT name FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_name = row[0]
            if fetched_name is not None:
                embed.add_field(name="🏷️ Name", value=f"{fetched_name}", inline=True)
            if age is not None:
                await db.execute("UPDATE members SET age = ? WHERE member_id = ?", (age, member_id))
            cur = await db.execute("SELECT age FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_age = row[0]
            if fetched_age is not None:
                embed.add_field(name="🏷️ Age", value=f"{fetched_age}", inline=True)
            if location is not None:
                await db.execute("UPDATE members SET location = ? WHERE member_id = ?", (location, member_id))
            cur = await db.execute("SELECT location FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_location = row[0]
            if fetched_location is not None:
                embed.add_field(name="🏷️ Location", value=f"{fetched_location}", inline=True)
            if pronouns is not None:
                await db.execute("UPDATE members SET pronouns = ? WHERE member_id = ?", (pronouns, member_id))
            cur = await db.execute("SELECT pronouns FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_pronouns = row[0]
            if fetched_pronouns is not None:
                embed.add_field(name="🏷️ Pronouns", value=f"{fetched_pronouns}", inline=True)
            if gender is not None:
                await db.execute("UPDATE members SET gender = ? WHERE member_id = ?", (gender, member_id))
            cur = await db.execute("SELECT gender FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_gender = row[0]
            if fetched_gender is not None:
                embed.add_field(name="🏷️ Gender", value=f"{fetched_gender}", inline=True)
            if sexuality is not None:
                await db.execute("UPDATE members SET sexuality = ? WHERE member_id = ?", (sexuality, member_id))
            cur = await db.execute("SELECT sexuality FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_sexuality = row[0]
            if fetched_sexuality is not None:
                embed.add_field(name="🏷️ Sexuality", value=f"{fetched_sexuality}", inline=True)
            if relationship_status is not None:
                await db.execute("UPDATE members SET relationship_status = ? WHERE member_id = ?", (relationship_status, member_id))
            cur = await db.execute("SELECT relationship_status FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_relationship_status = row[0]
            if fetched_relationship_status is not None:
                embed.add_field(name="📝 Relationship Status", value=f"{fetched_relationship_status}", inline=True)
            if family_status is not None:
                await db.execute("UPDATE members SET family_status = ? WHERE member_id = ?", (family_status, member_id))
            cur = await db.execute("SELECT family_status FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_family_status = row[0]
            if fetched_family_status is not None:
                embed.add_field(name="📝 Family Planning Status", value=f"{fetched_family_status}", inline=True)
            if biography is not None:
                await db.execute("UPDATE members SET biography = ? WHERE member_id = ?", (biography, member_id))
            cur = await db.execute("SELECT biography FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_biography = row[0]
            if fetched_biography is not None:
                embed.add_field(name="📝 Biography", value=f"{fetched_biography}", inline=False)
            await db.commit()
            await db.close()
        roles = [r.mention for r in member.roles]
        roles = ", ".join(roles)
        embed.add_field(name="📝 Roles", value=f"{roles}", inline=False)
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="setprofilename")
    async def setprofilename(self, ctx: commands.Context, name: str):
        """Run this command to set your profile name.

        Parameters
        -----------
        name : str
            Provide your name or nickname.
        """
        await ctx.defer(ephemeral=True)
        member = ctx.author
        member_id = int(ctx.author.id)
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO members (member_id) VALUES (?)", (member_id,))
            await db.execute("UPDATE members SET name = ? WHERE member_id = ?", (name, member_id))
            cur = await db.execute("SELECT name FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_name = row[0]
            await db.commit()
            await db.close()
        if fetched_name is not None:
            embed = discord.Embed(color=member.accent_color, title="✔️ Success ✔️", description=f"Your profile name is now set to: {fetched_name}")
        else:
            embed = discord.Embed(color=member.accent_color, title="Error", description="There was an error! Try again later.")
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="setprofileage")
    async def setprofileage(self, ctx: commands.Context, age: str):
        """Run this command to set your profile age.

        Parameters
        -----------
        age : str
            Provide your age or age range.
        """
        await ctx.defer(ephemeral=True)
        member = ctx.author
        member_id = int(ctx.author.id)
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO members (member_id) VALUES (?)", (member_id,))
            await db.execute("UPDATE members SET age = ? WHERE member_id = ?", (age, member_id))
            cur = await db.execute("SELECT age FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_age = row[0]
            await db.commit()
            await db.close()
        if fetched_age is not None:
            embed = discord.Embed(color=member.accent_color, title="✔️ Success ✔️", description=f"Your profile age is now set to: {fetched_age}")
        else:
            embed = discord.Embed(color=member.accent_color, title="Error", description="There was an error! Try again later.")
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="setprofilelocation")
    async def setprofilelocation(self, ctx: commands.Context, location: str):
        """Run this command to set your profile location.

        Parameters
        -----------
        location : str
            Provide your continent, country, state, or city of residence.
        """
        await ctx.defer(ephemeral=True)
        member = ctx.author
        member_id = int(ctx.author.id)
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO members (member_id) VALUES (?)", (member_id,))
            await db.execute("UPDATE members SET location = ? WHERE member_id = ?", (location, member_id))
            cur = await db.execute("SELECT location FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_location = row[0]
            await db.commit()
            await db.close()
        if fetched_location is not None:
            embed = discord.Embed(color=member.accent_color, title="✔️ Success ✔️", description=f"Your profile location is now set to: {fetched_location}")
        else:
            embed = discord.Embed(color=member.accent_color, title="Error", description="There was an error! Try again later.")
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="setprofilepronouns")
    async def setprofilepronouns(self, ctx: commands.Context, pronouns: str):
        """Run this command to set your profile pronouns.

        Parameters
        -----------
        pronouns : str
            Provide your pronouns (ex. she/her, he/him, they/them, etc).
        """
        await ctx.defer(ephemeral=True)
        member = ctx.author
        member_id = int(ctx.author.id)
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO members (member_id) VALUES (?)", (member_id,))
            await db.execute("UPDATE members SET pronouns = ? WHERE member_id = ?", (pronouns, member_id))
            cur = await db.execute("SELECT pronouns FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_pronouns = row[0]
            await db.commit()
            await db.close()
        if fetched_pronouns is not None:
            embed = discord.Embed(color=member.accent_color, title="✔️ Success ✔️", description=f"Your profile pronouns are now set to: {fetched_pronouns}")
        else:
            embed = discord.Embed(color=member.accent_color, title="Error", description="There was an error! Try again later.")
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="setprofilegender")
    async def setprofilegender(self, ctx: commands.Context, gender: str):
        """Run this command to set your profile gender.

        Parameters
        -----------
        gender : str
            Provide your gender identity label (ex. woman, man, nonbinary, etc).
        """
        await ctx.defer(ephemeral=True)
        member = ctx.author
        member_id = int(ctx.author.id)
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO members (member_id) VALUES (?)", (member_id,))
            await db.execute("UPDATE members SET gender = ? WHERE member_id = ?", (gender, member_id))
            cur = await db.execute("SELECT gender FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_gender = row[0]
            await db.commit()
            await db.close()
        if fetched_gender is not None:
            embed = discord.Embed(color=member.accent_color, title="✔️ Success ✔️", description=f"Your profile gender is now set to: {fetched_gender}")
        else:
            embed = discord.Embed(color=member.accent_color, title="Error", description="There was an error! Try again later.")
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="setprofilesexuality")
    async def setprofilesexuality(self, ctx: commands.Context, sexuality: str):
        """Run this command to set your profile sexuality.

        Parameters
        -----------
        sexuality : str
            Provide your sexuality label (ex. lesbian, gay, bisexual, etc).
        """
        await ctx.defer(ephemeral=True)
        member = ctx.author
        member_id = int(ctx.author.id)
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO members (member_id) VALUES (?)", (member_id,))
            await db.execute("UPDATE members SET sexuality = ? WHERE member_id = ?", (sexuality, member_id))
            cur = await db.execute("SELECT sexuality FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_sexuality = row[0]
            await db.commit()
            await db.close()
        if fetched_sexuality is not None:
            embed = discord.Embed(color=member.accent_color, title="✔️ Success ✔️", description=f"Your profile sexuality is now set to: {fetched_sexuality}")
        else:
            embed = discord.Embed(color=member.accent_color, title="Error", description="There was an error! Try again later.")
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="setprofilerelationship")
    async def setprofilerelationship(self, ctx: commands.Context, relationship_status: str):
        """Run this command to set your profile relationship status.

        Parameters
        -----------
        relationship_status : str
            Provide your relationship status (ex. single, married, etc).
        """
        await ctx.defer(ephemeral=True)
        member = ctx.author
        member_id = int(ctx.author.id)
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO members (member_id) VALUES (?)", (member_id,))
            await db.execute("UPDATE members SET relationship_status = ? WHERE member_id = ?", (relationship_status, member_id))
            cur = await db.execute("SELECT relationship_status FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_relationship_status = row[0]
            await db.commit()
            await db.close()
        if fetched_relationship_status is not None:
            embed = discord.Embed(color=member.accent_color, title="✔️ Success ✔️", description=f"Your profile relationship status is now set to: {fetched_relationship_status}")
        else:
            embed = discord.Embed(color=member.accent_color, title="Error", description="There was an error! Try again later.")
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="setprofilefamily")
    async def setprofilefamily(self, ctx: commands.Context, family_status: str):
        """Run this command to set your profile family planning status.

        Parameters
        -----------
        family_status : str
            Provide your your family planning status (ex. TTC, expecting, parenting, etc).
        """
        await ctx.defer(ephemeral=True)
        member = ctx.author
        member_id = int(ctx.author.id)
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO members (member_id) VALUES (?)", (member_id,))
            await db.execute("UPDATE members SET family_status = ? WHERE member_id = ?", (family_status, member_id))
            cur = await db.execute("SELECT family_status FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_family_status = row[0]
            await db.commit()
            await db.close()
        if fetched_family_status is not None:
            embed = discord.Embed(color=member.accent_color, title="✔️ Success ✔️", description=f"Your profile family planning status is now set to: {fetched_family_status}")
        else:
            embed = discord.Embed(color=member.accent_color, title="Error", description="There was an error! Try again later.")
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="setprofilebiography")
    async def setprofilebiography(self, ctx: commands.Context, biography: str):
        """Run this command to set your profile biography.

        Parameters
        -----------
        biography : str
            Provide a brief biography (ex. family, hobbies, interests, work, etc).
        """
        await ctx.defer(ephemeral=True)
        member = ctx.author
        member_id = int(ctx.author.id)
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO members (member_id) VALUES (?)", (member_id,))
            await db.execute("UPDATE members SET biography = ? WHERE member_id = ?", (biography, member_id))
            cur = await db.execute("SELECT biography FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_biography = row[0]
            await db.commit()
            await db.close()
        if fetched_biography is not None:
            embed = discord.Embed(color=member.accent_color, title="✔️ Success ✔️", description=f"Your profile biography is now set to: {fetched_biography}")
        else:
            embed = discord.Embed(color=member.accent_color, title="Error", description="There was an error! Try again later.")
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="getprofile")
    async def getprofile(self, ctx: commands.Context, member: discord.Member):
        """Run this command to retrieve a member's profile.

        Parameters
        -----------
        member : str
            Provide the member whose profile you would like to retrieve.
        """
        await ctx.defer(ephemeral=True)
        guild = ctx.guild
        member_id = int(member.id)
        joined = discord.utils.format_dt(member.joined_at, style="D")
        joinedago = discord.utils.format_dt(member.joined_at, style="R")
        embed = discord.Embed(color=member.accent_color, title=f"{member.name}'s Member Profile", description=f"Member of {guild.name} since {joined} ({joinedago}).")
        if member.avatar is not None:
            embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar}")
        else:
            embed.set_author(name=f"{member.name}")
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO members (member_id) VALUES (?)", (member_id,))
            cur = await db.execute("SELECT name FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_name = row[0]
            if fetched_name is not None:
                embed.add_field(name="🏷️ Name", value=f"{fetched_name}", inline=True)
            cur = await db.execute("SELECT age FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_age = row[0]
            if fetched_age is not None:
                embed.add_field(name="🏷️ Age", value=f"{fetched_age}", inline=True)
            cur = await db.execute("SELECT location FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_location = row[0]
            if fetched_location is not None:
                embed.add_field(name="🏷️ Location", value=f"{fetched_location}", inline=True)
            cur = await db.execute("SELECT pronouns FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_pronouns = row[0]
            if fetched_pronouns is not None:
                embed.add_field(name="🏷️ Pronouns", value=f"{fetched_pronouns}", inline=True)
            cur = await db.execute("SELECT gender FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_gender = row[0]
            if fetched_gender is not None:
                embed.add_field(name="🏷️ Gender", value=f"{fetched_gender}", inline=True)
            cur = await db.execute("SELECT sexuality FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_sexuality = row[0]
            if fetched_sexuality is not None:
                embed.add_field(name="🏷️ Sexuality", value=f"{fetched_sexuality}", inline=True)
            cur = await db.execute("SELECT relationship_status FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_relationship_status = row[0]
            if fetched_relationship_status is not None:
                embed.add_field(name="📝 Relationship Status", value=f"{fetched_relationship_status}", inline=True)
            cur = await db.execute("SELECT family_status FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_family_status = row[0]
            if fetched_family_status is not None:
                embed.add_field(name="📝 Family Planning Status", value=f"{fetched_family_status}", inline=True)
            cur = await db.execute("SELECT biography FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_biography = row[0]
            if fetched_biography is not None:
                embed.add_field(name="📝 Biography", value=f"{fetched_biography}", inline=False)
            await db.commit()
            await db.close()
        roles = [r.mention for r in member.roles]
        roles = ", ".join(roles)
        embed.add_field(name="📝 Roles", value=f"{roles}", inline=False)
        await ctx.send(embed=embed, ephemeral=True)

class RSSCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="createrssfeed")
    async def setwebhook(self, ctx: commands.Context, webhook_url: str, webhook_name: str, webhook_avatar_url: str):
        """Run this command to set a Webhook. All fields are required.

        Parameters
        -----------
        webhook_url : str
            Provide the URL for the webhook.
        webhook_name : str
            Provide the name of the webhook.
        webhook_avatar_url : str
            Provide the image URL for the webhook's avatar.
        """
        guild = ctx.guild
        member = ctx.author
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO webhooks (url) VALUES (?)", (webhook_url,))
            await db.execute("UPDATE webhooks SET name = ? WHERE url = ?", (webhook_name, webhook_url))
            cur = await db.execute("SELECT name FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            name = row[0]
            await db.execute("UPDATE webhooks SET avatar_url = ? WHERE url = ?", (webhook_avatar_url, webhook_url))
            cur = await db.execute("SELECT avatar_url FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            avatar_url = row[0]
            await db.commit()
            await db.close()

    @commands.hybrid_command(name="createrssfeed")
    async def setrssfeed(self, ctx: commands.Context, webhook_url: str, rss_channel: discord.TextChannel, rss_feed_url: str):
        """Run this command to set an RSS Feed. All fields are required.

        Parameters
        -----------
        webhook_url : str
            Provide the URL for the webhook. You can set the webhook's name and avatar using the /setwebhook command.
        rss_channel : discord.TextChannel
            Select the channel where you would like the RSS feed to post.
        rss_feed_url : str
            Provide the URL for the RSS feed.
        """
        await ctx.defer(ephemeral=True)
        guild = ctx.guild
        member = ctx.author
        rss_channel_id = rss_channel.id
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO webhooks (url) VALUES (?)", (webhook_url,))
            cur = await db.execute("SELECT rss_channel_id_1 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            name1 = row[0]
            if name1 is None:
                await db.execute("UPDATE webhooks SET rss_channel_id_1 = ? WHERE url = ?", (rss_channel_id, webhook_url))
                cur = await db.execute("SELECT rss_channel_id_1 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_name = row[0]
                await db.execute("UPDATE webhooks SET rss_url_1 = ? WHERE url = ?", (rss_feed_url, webhook_url))
                cur = await db.execute("SELECT rss_url_1 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_avatar_url = row[0]
            else:
                cur = await db.execute("SELECT rss_channel_id_2 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                name2 = row[0]
                if name2 is None:
                    await db.execute("UPDATE webhooks SET rss_channel_id_2 = ? WHERE url = ?", (rss_channel_id, webhook_url))
                    cur = await db.execute("SELECT rss_channel_id_2 FROM webhooks WHERE url = ?", (webhook_url,))
                    row = await cur.fetchone()
                    fetched_name = row[0]
                    await db.execute("UPDATE webhooks SET rss_url_2 = ? WHERE url = ?", (rss_feed_url, webhook_url))
                    cur = await db.execute("SELECT rss_url_2 FROM webhooks WHERE url = ?", (webhook_url,))
                    row = await cur.fetchone()
                    fetched_avatar_url = row[0]
                else:
                    cur = await db.execute("SELECT rss_channel_id_3 FROM webhooks WHERE url = ?", (webhook_url,))
                    row = await cur.fetchone()
                    name3 = row[0]
                    if name3 is None:
                        await db.execute("UPDATE webhooks SET rss_channel_id_3 = ? WHERE url = ?", (rss_channel_id, webhook_url))
                        cur = await db.execute("SELECT rss_channel_id_3 FROM webhooks WHERE url = ?", (webhook_url,))
                        row = await cur.fetchone()
                        fetched_name = row[0]
                        await db.execute("UPDATE webhooks SET rss_url_3 = ? WHERE url = ?", (rss_feed_url, webhook_url))
                        cur = await db.execute("SELECT rss_url_3 FROM webhooks WHERE url = ?", (webhook_url,))
                        row = await cur.fetchone()
                        fetched_avatar_url = row[0]
                    else:
                        cur = await db.execute("SELECT rss_channel_id_4 FROM webhooks WHERE url = ?", (webhook_url,))
                        row = await cur.fetchone()
                        name4 = row[0]
                        if name4 is None:
                            await db.execute("UPDATE webhooks SET rss_channel_id_4 = ? WHERE url = ?", (rss_channel_id, webhook_url))
                            cur = await db.execute("SELECT rss_channel_id_4 FROM webhooks WHERE url = ?", (webhook_url,))
                            row = await cur.fetchone()
                            fetched_name = row[0]
                            await db.execute("UPDATE webhooks SET rss_url_4 = ? WHERE url = ?", (rss_feed_url, webhook_url))
                            cur = await db.execute("SELECT rss_url_4 FROM webhooks WHERE url = ?", (webhook_url,))
                            row = await cur.fetchone()
                            fetched_avatar_url = row[0]
                        else:
                            cur = await db.execute("SELECT rss_channel_id_5 FROM webhooks WHERE url = ?", (webhook_url,))
                            row = await cur.fetchone()
                            name5 = row[0]
                            if name5 is None:
                                await db.execute("UPDATE webhooks SET rss_channel_id_5 = ? WHERE url = ?", (rss_channel_id, webhook_url))
                                cur = await db.execute("SELECT rss_channel_id_5 FROM webhooks WHERE url = ?", (webhook_url,))
                                row = await cur.fetchone()
                                fetched_name = row[0]
                                await db.execute("UPDATE webhooks SET rss_url_5 = ? WHERE url = ?", (rss_feed_url, webhook_url))
                                cur = await db.execute("SELECT rss_url_5 FROM webhooks WHERE url = ?", (webhook_url,))
                                row = await cur.fetchone()
                                fetched_avatar_url = row[0]
                            else:
                                cur = await db.execute("SELECT rss_channel_id_6 FROM webhooks WHERE url = ?", (webhook_url,))
                                row = await cur.fetchone()
                                name6 = row[0]
                                if name6 is None:
                                    await db.execute("UPDATE webhooks SET rss_channel_id_6 = ? WHERE url = ?", (rss_channel_id, webhook_url))
                                    cur = await db.execute("SELECT rss_channel_id_6 FROM webhooks WHERE url = ?", (webhook_url,))
                                    row = await cur.fetchone()
                                    fetched_name = row[0]
                                    await db.execute("UPDATE webhooks SET rss_url_6 = ? WHERE url = ?", (rss_feed_url, webhook_url))
                                    cur = await db.execute("SELECT rss_url_6 FROM webhooks WHERE url = ?", (webhook_url,))
                                    row = await cur.fetchone()
                                    fetched_avatar_url = row[0]
                                else:
                                    cur = await db.execute("SELECT rss_channel_id_7 FROM webhooks WHERE url = ?", (webhook_url,))
                                    row = await cur.fetchone()
                                    name7 = row[0]
                                    if name7 is None:
                                        await db.execute("UPDATE webhooks SET rss_channel_id_7 = ? WHERE url = ?", (rss_channel_id, webhook_url))
                                        cur = await db.execute("SELECT rss_channel_id_7 FROM webhooks WHERE url = ?", (webhook_url,))
                                        row = await cur.fetchone()
                                        fetched_name = row[0]
                                        await db.execute("UPDATE webhooks SET rss_url_7 = ? WHERE url = ?", (rss_feed_url, webhook_url))
                                        cur = await db.execute("SELECT rss_url_7 FROM webhooks WHERE url = ?", (webhook_url,))
                                        row = await cur.fetchone()
                                        fetched_avatar_url = row[0]
                                    else:
                                        cur = await db.execute("SELECT rss_channel_id_8 FROM webhooks WHERE url = ?", (webhook_url,))
                                        row = await cur.fetchone()
                                        name8 = row[0]
                                        if name8 is None:
                                            await db.execute("UPDATE webhooks SET rss_channel_id_8 = ? WHERE url = ?", (rss_channel_id, webhook_url))
                                            cur = await db.execute("SELECT rss_channel_id_8 FROM webhooks WHERE url = ?", (webhook_url,))
                                            row = await cur.fetchone()
                                            fetched_name = row[0]
                                            await db.execute("UPDATE webhooks SET rss_url_8 = ? WHERE url = ?", (rss_feed_url, webhook_url))
                                            cur = await db.execute("SELECT rss_url_8 FROM webhooks WHERE url = ?", (webhook_url,))
                                            row = await cur.fetchone()
                                            fetched_avatar_url = row[0]
                                        else:
                                            cur = await db.execute("SELECT rss_channel_id_9 FROM webhooks WHERE url = ?", (webhook_url,))
                                            row = await cur.fetchone()
                                            name9 = row[0]
                                            if name9 is None:
                                                await db.execute("UPDATE webhooks SET rss_channel_id_9 = ? WHERE url = ?", (rss_channel_id, webhook_url))
                                                cur = await db.execute("SELECT rss_channel_id_9 FROM webhooks WHERE url = ?", (webhook_url,))
                                                row = await cur.fetchone()
                                                fetched_name = row[0]
                                                await db.execute("UPDATE webhooks SET rss_url_9 = ? WHERE url = ?", (rss_feed_url, webhook_url))
                                                cur = await db.execute("SELECT rss_url_9 FROM webhooks WHERE url = ?", (webhook_url,))
                                                row = await cur.fetchone()
                                                fetched_avatar_url = row[0]
                                            else:
                                                cur = await db.execute("SELECT rss_channel_id_10 FROM webhooks WHERE url = ?", (webhook_url,))
                                                row = await cur.fetchone()
                                                name10 = row[0]
                                                if name10 is None:
                                                    await db.execute("UPDATE webhooks SET rss_channel_id_10 = ? WHERE url = ?", (rss_channel_id, webhook_url))
                                                    cur = await db.execute("SELECT rss_channel_id_10 FROM webhooks WHERE url = ?", (webhook_url,))
                                                    row = await cur.fetchone()
                                                    fetched_name = row[0]
                                                    await db.execute("UPDATE webhooks SET rss_url_10 = ? WHERE url = ?", (rss_feed_url, webhook_url))
                                                    cur = await db.execute("SELECT rss_url_10 FROM webhooks WHERE url = ?", (webhook_url,))
                                                    row = await cur.fetchone()
                                                    fetched_avatar_url = row[0]
                                                else:
                                                    embed = discord.Embed(title="Error", description="This webhook is already associated with 10 RSS feeds. You will need to remove ")
            await db.commit()
            await db.close()
        await ctx.send(embed=embed, ephemeral=True)

async def setup(bot):
    async with aiosqlite.connect('rainbowbot.db') as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS guilds(
                         guild_id INTEGER PRIMARY KEY,
                         logging_channel_id INTEGER DEFAULT NULL,
                         welcome_channel_id INTEGER DEFAULT NULL,
                         welcome_message TEXT DEFAULT NULL,
                         goodbye_channel_id INTEGER DEFAULT NULL,
                         goodbye_message TEXT DEFAULT NULL,
                         join_role_id INTEGER DEFAULT NULL,
                         bot_join_role_id INTEGER DEFAULT NULL,
                         award_singular TEXT DEFAULT NULL,
                         award_plural TEXT DEFAULT NULL,
                         award_emoji TEXT DEFAULT NULL,
                         award_react_toggle INTEGER DEFAULT 0)""")
        await db.execute("""CREATE TABLE IF NOT EXISTS members(
                         member_id INTEGER PRIMARY KEY,
                         awards INTEGER DEFAULT NULL,
                         name TEXT DEFAULT NULL,
                         age TEXT DEFAULT NULL,
                         location TEXT DEFAULT NULL,
                         pronouns TEXT DEFAULT NULL,
                         gender TEXT DEFAULT NULL,
                         sexuality TEXT DEFAULT NULL,
                         relationship_status TEXT DEFAULT NULL,
                         family_status TEXT DEFAULT NULL,
                         biography TEXT DEFAULT NULL)""")
        await db.execute("""CREATE TABLE IF NOT EXISTS webhooks(
                         url TEXT PRIMARY KEY,
                         name TEXT DEFAULT NULL,
                         avatar_url TEXT DEFAULT NULL,
                         rss_channel_id_1
                         rss_url_1
                         rss_channel_id_2
                         rss_url_2
                         rss_channel_id_3
                         rss_url_3
                         rss_channel_id_4
                         rss_url_4
                         rss_channel_id_5
                         rss_url_5
                         rss_channel_id_6
                         rss_url_6
                         rss_channel_id_7
                         rss_url_7
                         rss_channel_id_8
                         rss_url_8
                         rss_channel_id_9
                         rss_url_9
                         rss_channel_id_10
                         rss_url_10)""")
        await db.commit()
        await db.close()
    await bot.add_cog(BackgroundTasks(bot), override=True)
    await bot.add_cog(SetupCommands(bot), override=True)
    await bot.add_cog(PurgeCommands(bot), override=True)
    await bot.add_cog(AwardCommands(bot), override=True)
    await bot.add_cog(ProfileCommands(bot), override=True)
    await bot.add_cog(RSSCommands(bot), override=True)

@bot.event
async def on_ready():
    await setup(bot)
    print(f'Logged in as {bot.user}! (ID: {bot.user.id})')

bot.run('token')