import discord
import aiosqlite
import aiohttp
import feedparser
from discord import ChannelType, app_commands, Webhook
from discord.ui import ChannelSelect
from discord.ext import commands, tasks
from typing import Any, Optional, Literal
from datetime import datetime, timezone, timedelta
from time import mktime
from bs4 import BeautifulSoup

bot = commands.Bot(
    command_prefix = 'rb!',
    description = "A multi-purpose Discord bot made by GitHub user gemhue.",
    intents = discord.Intents.all(),
    activity = discord.Activity(type=discord.ActivityType.listening, name="rb!help"),
    status = discord.Status.online
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
        await interaction.response.defer()
        channels: list[DropdownView] = self.values
        self.view.values = [c for c in channels]

class DropdownView(discord.ui.View):
    def __init__(self, *, timeout=180.0):
        super().__init__(timeout=timeout)
        self.value = None
        self.add_item(ChannelsSelector())

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green, row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red, row=2)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = False
        self.stop()

class BackgroundTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name="on_message")
    async def on_message(self, message: discord.Message):
        messagecont = message.content.lower()
        list1 = ['lesbian','sapphic','wlw']
        moji1 = bot.get_emoji(1274435288499884094)
        if any(x in messagecont for x in list1):
            await message.add_reaction(moji1)
        list2 = ['gay','achillean','mlm']
        moji2 = bot.get_emoji(1274435330174615624)
        if any(x in messagecont for x in list2):
            await message.add_reaction(moji2)
        list3 = ['bisexual','biromantic','bi woman','bi women','bi lady','bi ladies','bi girl','bi gal','bi man','bi men','bi guy','bi dude','bi boy','bi person','bi people']
        moji3 = bot.get_emoji(1274435359878676560)
        if any(x in messagecont for x in list3):
            await message.add_reaction(moji3)
        list4 = ['asexual','aromantic','acespec','arospec','ace spec','aro spec','ace-spec','aro-spec']
        moji4 = bot.get_emoji(1274435406804291634)
        if any(x in messagecont for x in list4):
            await message.add_reaction(moji4)
        list5 = ['transgender','transsexual','trans woman','trans women','trans lady','trans ladies','trans girl','trans gal','trans man','trans men','trans guy','trans dude','trans boy','trans person','trans people']
        moji5 = bot.get_emoji(1274435448726622208)
        if any(x in messagecont for x in list5):
            await message.add_reaction(moji5)
        list6 = ['nonbinary','non binary','non-binary','enby']
        moji6 = bot.get_emoji(1274435483912638515)
        if any(x in messagecont for x in list6):
            await message.add_reaction(moji6)
        list7 = ['transfeminine','trans feminine','trans-feminine','transfem','trans fem','trans-fem']
        moji7 = bot.get_emoji(1274435557744840820)
        if any(x in messagecont for x in list7):
            await message.add_reaction(moji7)
        list8 = ['transmasculine','trans masculine','trans-masculine','transmasc','trans masc','trans-masc']
        moji8 = bot.get_emoji(1274435528883961989)
        if any(x in messagecont for x in list8):
            await message.add_reaction(moji8)
        await bot.process_commands(message)
        
    @commands.Cog.listener(name="on_member_join")
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

    @commands.Cog.listener(name="on_member_remove")
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

    @commands.command(name="sync", hidden=True)
    @commands.is_owner()
    async def sync(self, ctx: commands.Context):
        """(Bot Owner Only) Syncs the local command tree.
        """
        await ctx.defer(ephemeral=True)
        guild = ctx.guild
        await bot.tree.sync(guild=guild)
        embed = discord.Embed(title="Update", description=f"The bot's local command tree has been synced!")
        await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)
        await ctx.message.delete()
    
    @commands.command(name="globalsync", hidden=True)
    @commands.is_owner()
    async def globalsync(self, ctx: commands.Context):
        """(Bot Owner Only) Syncs the global command tree.
        """
        await ctx.defer(ephemeral=True)
        await bot.tree.sync(guild=None)
        embed = discord.Embed(title="Update", description=f"The bot's global command tree has been synced!")
        await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)
        await ctx.message.delete()

    @commands.command(name="clear", hidden=True)
    @commands.is_owner()
    async def clear(self, ctx: commands.Context):
        """(Bot Owner Only) Clears the local command tree.
        """
        await ctx.defer(ephemeral=True)
        guild = ctx.guild
        bot.tree.clear_commands(guild=guild)
        embed = discord.Embed(title="Update", description=f"The bot's local command tree has been cleared!")
        await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)
        await ctx.message.delete()

    @commands.command(name="globalclear", hidden=True)
    @commands.is_owner()
    async def globalclear(self, ctx: commands.Context):
        """(Bot Owner Only) Clears the global command tree.
        """
        await ctx.defer(ephemeral=True)
        bot.tree.clear_commands(guild=None)
        embed = discord.Embed(title="Update", description=f"The bot's global command tree has been cleared!")
        await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)
        await ctx.message.delete()

    @commands.hybrid_group(name="setup", fallback="channels")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def setup(self, ctx: commands.Context, logging_channel: Optional[discord.TextChannel], welcome_channel: Optional[discord.TextChannel], goodbye_channel: Optional[discord.TextChannel]):
        """(Admin Only) Sets the channels for logging messages, welcome messages, and goodbye messages.

        Parameters
        -----------
        logging_channel : discord.TextChannel, optional
            Set the channel for logging messages.
        welcome_channel : discord.TextChannel, optional
            Set the channel for welcome messages.
        goodbye_channel : discord.TextChannel, optional
            Set the channel for goodbye messages.
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
                embed.add_field(name="Logging Channel", value=f"{logging.mention}", inline=False)
            if welcome_channel is not None:
                welcome_id = welcome_channel.id
                await db.execute("UPDATE guilds SET welcome_channel_id = ? WHERE guild_id = ?", (welcome_id, guild_id))
                cur = await db.execute("SELECT welcome_channel_id FROM guilds WHERE guild_id = ?", (guild_id,))
                row = await cur.fetchone()
                fetched_welcome = row[0]
                welcome = guild.get_channel(fetched_welcome)
                embed.add_field(name="Welcome Channel", value=f"{welcome.mention}", inline=False)
            if goodbye_channel is not None:
                goodbye_id = goodbye_channel.id
                await db.execute("UPDATE guilds SET goodbye_channel_id = ? WHERE guild_id = ?", (goodbye_id, guild_id))
                cur = await db.execute("SELECT goodbye_channel_id FROM guilds WHERE guild_id = ?", (guild_id,))
                row = await cur.fetchone()
                fetched_goodbye = row[0]
                goodbye = guild.get_channel(fetched_goodbye)
                embed.add_field(name="Goodbye Channel", value=f"{goodbye.mention}", inline=False)
            await db.commit()
            await db.close()
        await ctx.send(embed=embed, ephemeral=True)

    @setup.command(name="welcome_message")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def welcome_message(self, ctx: commands.Context, message: str):
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
            embed.add_field(name="Welcome Message", value=f"{fetched_message}", inline=False)
            await db.commit()
            await db.close()
        await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)

    @setup.command(name="goodbye_message")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def goodbye_message(self, ctx: commands.Context, message: str):
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
            embed.add_field(name="Goodbye Message", value=f"{fetched_message}", inline=False)
            await db.commit()
            await db.close()
        await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)

    @setup.command(name="join_roles")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def join_roles(self, ctx: commands.Context, role: discord.Role, botrole: Optional[discord.Role]):
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
            embed.add_field(name="Join Role", value=f"{role.mention}", inline=False)
            if botrole is not None:
                botrole_id = botrole.id
                await db.execute("UPDATE guilds SET bot_join_role_id = ? WHERE guild_id = ?", (botrole_id, guild_id))
                cur = await db.execute("SELECT bot_join_role_id FROM guilds WHERE guild_id = ?", (guild_id,))
                row = await cur.fetchone()
                botrole_id = row[0]
                botrole = guild.get_role(botrole_id)
                embed.add_field(name="Bot Join Role", value=f"{botrole.mention}", inline=False)
            await db.commit
            await db.close()
        ctx.send(embed=embed, delete_after=30.0, ephemeral=True)

    @setup.command(name="activity_roles")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def activity_roles(self, ctx: commands.Context, days: int, active: discord.Role, inactive: discord.Role):
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
        embed = discord.Embed(color=ctx.author.accent_color, title="Activity Roles Assigned")
        embed.add_field(name="Active Members", value=f"{len(activemembers)} members now have the {active.mention} role!", inline=False)
        embed.add_field(name="Inactive Members", value=f"{len(inactivemembers)} members now have the {inactive.mention} role!", inline=False)
        await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)

class PurgeCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(name="purge", fallback="here")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def purge(self, ctx: commands.Context):
        """(Admin Only) Purge all unpinned messages in the current channel.
        """
        await ctx.defer()
        channel = ctx.channel
        messages = [m async for m in channel.history(limit=None)]
        unpinned = [m for m in messages if not m.pinned]
        deleted = []
        while len(unpinned) > 0:
            deleted += await channel.purge(check=lambda message: message.pinned == False, oldest_first=True)
            messages = [m async for m in channel.history(limit=None)]
            unpinned = [m for m in messages if not m.pinned]
        if len(deleted) == 0:
            embed = discord.Embed(title="❌ Error ❌", description=f"{channel.mention} doesn't have any messages to purge!")
            await channel.send(embed=embed, delete_after=30.0)
        elif len(deleted) == 1:
            embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} message was just purged from {channel.mention}!')
            await channel.send(embed=embed, delete_after=30.0)
        else:
            embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} messages were just purged from {channel.mention}!')
            await channel.send(embed=embed, delete_after=30.0)
        embed = discord.Embed(title="✔️ Done ✔️", description=f'The purge is now complete!')
        await channel.send(embed=embed, delete_after=30.0)

    @purge.command(name="member")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def member(self, ctx: commands.Context, member: discord.Member):
        """(Admin Only) Purge all of a member's unpinned messages in a set list of up to 25 channels.

        Parameters
        -----------
        member : discord.Member
            Provide the member who's unpinned messages you would like to purge.
        """
        await ctx.defer()
        ctxchannel = ctx.channel
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
                    embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} message was just purged from {channel.mention}!')
                    await ctxchannel.send(embed=embed, delete_after=30.0)
                else:
                    embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} messages were just purged from {channel.mention}!')
                    await ctxchannel.send(embed=embed, delete_after=30.0)
            embed = discord.Embed(title="✔️ Done ✔️", description=f'The purge is now complete!')
            await ctxchannel.send(embed=embed, delete_after=30.0)
        elif view.value == False:
            embed = discord.Embed(title="❌ Cancelled ❌", description='This interaction has been cancelled. No messages have been purged.')
            await response.edit(embed=embed, view=None)
        else:
            embed = discord.Embed(title="⌛ Timed Out ⌛", description='This interaction has timed out. No messages have been purged.')
            await response.edit(embed=embed, view=None)

    @purge.command(name="channels")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def channels(self, ctx: commands.Context):
        """(Admin Only) Purge all unpinned messages in a set list of up to 25 channels.
        """
        await ctx.defer()
        ctxchannel = ctx.channel
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
                    embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} message was just purged from {channel.mention}!')
                    await ctxchannel.send(embed=embed, delete_after=30.0)
                else:
                    embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} messages were just purged from {channel.mention}!')
                    await ctxchannel.send(embed=embed, delete_after=30.0)
            embed = discord.Embed(title="✔️ Done ✔️", description=f'The purge is now complete!')
            await ctxchannel.send(embed=embed, delete_after=30.0)
        elif view.value == False:
            embed = discord.Embed(title="❌ Cancelled ❌", description='This interaction has been cancelled. No messages have been purged.')
            await response.edit(embed=embed, view=None)
        else:
            embed = discord.Embed(title="⌛ Timed Out ⌛", description='This interaction has timed out. No messages have been purged.')
            await response.edit(embed=embed, view=None)

    @purge.command(name="server")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def server(self, ctx: commands.Context):
        """(Admin Only) Purges all unpinned messages in a server, excluding up to 25 channels.
        """
        await ctx.defer()
        ctxchannel = ctx.channel
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
                    embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} message was just purged from {channel.mention}!')
                    await ctxchannel.send(embed=embed, delete_after=30.0)
                else:
                    embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} messages were just purged from {channel.mention}!')
                    await ctxchannel.send(embed=embed, delete_after=30.0)
            embed = discord.Embed(title="✔️ Done ✔️", description=f'The purge is now complete!')
            await ctxchannel.send(embed=embed, delete_after=30.0)
        elif view.value == False:
            embed = discord.Embed(title="❌ Cancelled ❌", description='This interaction has been cancelled. No messages have been purged.')
            await response.edit(embed=embed, view=None)
        else:
            embed = discord.Embed(title="⌛ Timed Out ⌛", description='This interaction has timed out. No messages have been purged.')
            await response.edit(embed=embed, view=None)

class AwardCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_group(name="awards", fallback="set")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def awards(self, ctx: commands.Context, name_singular: str, name_plural: str, emoji: str):
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
        embed.add_field(name="Name (Singular)", value=f"{fetched_sing_cap}", inline=False)
        embed.add_field(name="Name (Plural)", value=f"{fetched_plur_cap}", inline=False)
        embed.add_field(name="Emoji", value=f"{fetched_moji}", inline=False)
        await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)

    @awards.command(name="clear")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def clear(self, ctx: commands.Context):
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
                guild_member_id = int(str(guild_id) + str(member_id))
                await db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
                await db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (0, guild_member_id))
            await db.commit()
            await db.close()
        embed = discord.Embed(title=f"{moji} {plur_cap} Cleared {moji}", description=f"{guild.name} has had all its {plur_low} cleared!")
        await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)

    @awards.command(name="reaction_toggle")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def reaction_toggle(self, ctx: commands.Context, toggle: bool):
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
                embed = discord.Embed(title="❌ Error ❌", description=f"Your input could not be parsed. Please enter either True to toggle award reactions ON or False to toggle award reactions OFF.")
            await db.commit()
            await db.close()
        ctx.send(embed=embed, delete_after=30.0, ephemeral=True)

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
                    guild_member_id = int(str(guild_id) + str(member_id))
                    await db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
                    cur = await db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
                    row = await cur.fetchone()
                    current = row[0]
                    if current is None:
                        current = 0
                    new = current + 1
                    await db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (new, guild_member_id))
                    cur = await db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
                    row = await cur.fetchone()
                    new = row[0]
                    if new == 1:
                        embed = discord.Embed(title=f"{moji} {sing_cap} Added {moji}", description=f"{member.mention} now has {new} {sing_low}! ({sing_cap} added by {user.mention}.)")
                    else:
                        embed = discord.Embed(title=f"{moji} {sing_cap} Added {moji}", description=f"{member.mention} now has {new} {plur_low}! ({sing_cap} added by {user.mention}.)")
                    await channel.send(embed=embed, delete_after=30.0, reference=message)
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
                    guild_member_id = int(str(guild_id) + str(member_id))
                    await db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
                    cur = await db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
                    row = await cur.fetchone()
                    current = row[0]
                    if current is None:
                        current = 0
                    if current > 0:
                        new = current - 1
                        await db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (new, guild_member_id))
                        cur = await db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
                        row = await cur.fetchone()
                        new = row[0]
                        if new == 0:
                            embed = discord.Embed(title=f"{moji} {sing_cap} Removed {moji}", description=f"{member.mention} no longer has any awards! ({sing_cap} removed by {user.mention}.)")
                        elif new == 1:
                            embed = discord.Embed(title=f"{moji} {sing_cap} Removed {moji}", description=f"{member.mention} now has {new} {sing_low}! ({sing_cap} removed by {user.mention}.)")
                        else:
                            embed = discord.Embed(title=f"{moji} {sing_cap} Removed {moji}", description=f"{member.mention} now has {new} {plur_low}! ({sing_cap} removed by {user.mention}.)")
                        await channel.send(embed=embed, delete_after=30.0, reference=message)
            await db.commit()
            await db.close()

    @awards.command(name="add")
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
        guild = ctx.guild
        guild_id = guild.id
        if amount is None:
            amount = 1
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
            guild_member_id = int(str(guild_id) + str(member_id))
            await db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
            cur = await db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
            row = await cur.fetchone()
            current = row[0]
            if current is None:
                await db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (amount, guild_member_id))
            else:
                new = current + amount
                await db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (new, guild_member_id))
            cur = await db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
            row = await cur.fetchone()
            new = row[0]
            await db.commit()
            await db.close()
        if new == 1:
            embed = discord.Embed(title=f"{moji} {sing_cap} Added {moji}", description=f"{member.mention} now has {new} {sing_low}!")
        else:
            embed = discord.Embed(title=f"{moji} {plur_cap} Added {moji}", description=f"{member.mention} now has {new} {plur_low}!")
        await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)

    @awards.command(name="remove")
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
        guild = ctx.guild
        guild_id = guild.id
        if amount is None:
            amount = 1
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
            guild_member_id = int(str(guild_id) + str(member_id))
            await db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
            cur = await db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
            row = await cur.fetchone()
            current = row[0]
            if current is None:
                current = 0
            if current == 0:
                await db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (current, guild_member_id))
                embed = discord.Embed(title=f"❌ Error ❌", description=f"{member.mention} doesn't have any {plur_low}!")
            elif current < amount:
                embed = discord.Embed(title=f"❌ Error ❌", description=f"{member.mention} doesn't have enough {plur_low}!")
            else:
                new = current - amount
                await db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (new, guild_member_id))
                cur = await db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
                row = await cur.fetchone()
                new = row[0]
                if new == 0:
                    embed = discord.Embed(title=f"{moji} {plur_cap} Removed {moji}", description=f"{member.mention} no longer has any {plur_low}!")
                elif new == 1:
                    embed = discord.Embed(title=f"{moji} {plur_cap} Removed {moji}", description=f"{member.mention} now has {new} {sing_low}!")
                else:
                    embed = discord.Embed(title=f"{moji} {plur_cap} Removed {moji}", description=f"{member.mention} now has {new} {plur_low}!")
                await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)
            await db.commit()
            await db.close()

    @awards.command(name="check")
    async def check(self, ctx: commands.Context, member: Optional[discord.Member]):
        """Returns the number of awards that the user or another selected user currently has.

        Parameters
        -----------
        member : discord.Member, optional
            Choose the member that you would like to check the number of awards for. (Default: Self)
        """
        await ctx.defer(ephemeral=True)
        guild = ctx.guild
        guild_id = guild.id
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
            guild_member_id = int(str(guild_id) + str(member_id))
            await db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
            cur = await db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
            row = await cur.fetchone()
            amount = row[0]
            if amount is None:
                amount = 0
            if amount == 0:
                await db.execute("INSERT OR IGNORE INTO awards (guild_member_id, amount) VALUES (?,?)", (guild_member_id,0))
                embed = discord.Embed(title=f"{moji} Number of {plur_cap} {moji}", description=f"{member.mention} doesn't have any {plur_low}!")
            elif amount == 1:
                embed = discord.Embed(title=f"{moji} Number of {plur_cap} {moji}", description=f"{member.mention} has {amount} {sing_low}!")
            else:
                embed = discord.Embed(title=f"{moji} Number of {plur_cap} {moji}", description=f"{member.mention} has {amount} {plur_low}!")
            await db.commit()
            await db.close()
        await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)

    @awards.command(name="leaderboard")
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
                guild_member_id = int(str(guild_id) + str(member_id))
                await db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
                cur = await db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
                row = await cur.fetchone()
                amount = row[0]
                if amount is None:
                    await db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (awards, guild_member_id))
                elif amount > 0:
                    member_awards[member_id] = amount
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
    
    @commands.hybrid_group(name="profile", fallback="set")
    async def profile(self, ctx: commands.Context, name: Optional[str], age: Optional[str], location: Optional[str], pronouns: Optional[str], gender: Optional[str], sexuality: Optional[str], relationship_status: Optional[str], family_status: Optional[str], biography: Optional[str]):
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
        await ctx.send(embed=embed, delete_after=60.0, ephemeral=True)

    @profile.command(name="name")
    async def name(self, ctx: commands.Context, name: str):
        """Run this command to set or update your profile name.

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
            embed = discord.Embed(color=member.accent_color, title="❌ Error ❌", description="There was an error! Try again later.")
        await ctx.send(embed=embed, delete_after=60.0, ephemeral=True)

    @profile.command(name="age")
    async def age(self, ctx: commands.Context, age: str):
        """Run this command to set or update your profile age.

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
            embed = discord.Embed(color=member.accent_color, title="❌ Error ❌", description="There was an error! Try again later.")
        await ctx.send(embed=embed, delete_after=60.0, ephemeral=True)

    @profile.command(name="location")
    async def location(self, ctx: commands.Context, location: str):
        """Run this command to set or update your profile location.

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
            embed = discord.Embed(color=member.accent_color, title="❌ Error ❌", description="There was an error! Try again later.")
        await ctx.send(embed=embed, delete_after=60.0, ephemeral=True)

    @profile.command(name="pronouns")
    async def pronouns(self, ctx: commands.Context, pronouns: str):
        """Run this command to set or update your profile pronouns.

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
            embed = discord.Embed(color=member.accent_color, title="❌ Error ❌", description="There was an error! Try again later.")
        await ctx.send(embed=embed, delete_after=60.0, ephemeral=True)

    @profile.command(name="gender")
    async def gender(self, ctx: commands.Context, gender: str):
        """Run this command to set or update your profile gender.

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
            embed = discord.Embed(color=member.accent_color, title="❌ Error ❌", description="There was an error! Try again later.")
        await ctx.send(embed=embed, delete_after=60.0, ephemeral=True)

    @profile.command(name="sexuality")
    async def sexuality(self, ctx: commands.Context, sexuality: str):
        """Run this command to set or update your profile sexuality.

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
            embed = discord.Embed(color=member.accent_color, title="❌ Error ❌", description="There was an error! Try again later.")
        await ctx.send(embed=embed, delete_after=60.0, ephemeral=True)

    @profile.command(name="relationship")
    async def relationship(self, ctx: commands.Context, relationship_status: str):
        """Run this command to set or update your profile relationship status.

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
            embed = discord.Embed(color=member.accent_color, title="❌ Error ❌", description="There was an error! Try again later.")
        await ctx.send(embed=embed, delete_after=60.0, ephemeral=True)

    @profile.command(name="family")
    async def family(self, ctx: commands.Context, family_status: str):
        """Run this command to set or update your profile family planning status.

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
            embed = discord.Embed(color=member.accent_color, title="❌ Error ❌", description="There was an error! Try again later.")
        await ctx.send(embed=embed, delete_after=60.0, ephemeral=True)

    @profile.command(name="biography")
    async def biography(self, ctx: commands.Context, biography: str):
        """Run this command to set or update your profile biography.

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
            embed = discord.Embed(color=member.accent_color, title="❌ Error ❌", description="There was an error! Try again later.")
        await ctx.send(embed=embed, delete_after=60.0, ephemeral=True)

    @profile.command(name="get")
    async def get(self, ctx: commands.Context, member: Optional[discord.Member]):
        """Run this command to retrieve a member's profile.

        Parameters
        -----------
        member : str, optional
            Provide the member whose profile you would like to retrieve.
        """
        await ctx.defer(ephemeral=True)
        guild = ctx.guild
        if member is None:
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
        await ctx.send(embed=embed, delete_after=60.0, ephemeral=True)

class RSSCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(name="rss", fallback="webhook_setup")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def rss(self, ctx: commands.Context, webhook_url: str, webhook_name: str, webhook_avatar_url: str):
        """(Admin Only) Run this command to set a Webhook. All fields are required.

        Parameters
        -----------
        webhook_url : str
            Provide the URL for the webhook.
        webhook_name : str
            Provide the name of the webhook.
        webhook_avatar_url : str
            Provide the image URL for the webhook's avatar.
        """
        await ctx.defer(ephemeral=True)
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
        embed = discord.Embed(title="Webhook Set")
        embed.add_field(name="Webhook URL", value=f"{webhook_url}", inline=False)
        embed.add_field(name="Webhook Name", value=f"{name}", inline=False)
        embed.add_field(name="Webhook Avatar URL", value=f"{avatar_url}", inline=False)
        await ctx.send(embed=embed, delete_after=60.0, ephemeral=True)

    @rss.command(name="webhook_check")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def webhook_check(self, ctx: commands.Context, webhook_url: str):
        """(Admin Only) Run this command to check what RSS feeds are set to the webhook.

        Parameters
        -----------
        webhook_url : str
            Provide the URL for the webhook.
        """
        await ctx.defer(ephemeral=True)
        embed = discord.Embed(title="Webhook", description=f"**Webhook URL**: {webhook_url}")
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO webhooks (url) VALUES (?)", (webhook_url,))
            cur = await db.execute("SELECT name FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            name = row[0]
            cur = await db.execute("SELECT avatar_url FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            avatar_url = row[0]
            if name is not None and avatar_url is not None:
                embed.set_author(name=name,icon_url=avatar_url)
            cur = await db.execute("SELECT rss_url_1 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                embed.add_field(name="Position One", value=f"**RSS URL**: {fetched_rss_url}", inline=False)
            else:
                embed.add_field(name="Position One", value="Empty", inline=False)
            cur = await db.execute("SELECT rss_url_2 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                embed.add_field(name="Position Two", value=f"**RSS URL**: {fetched_rss_url}", inline=False)
            else:
                embed.add_field(name="Position Two", value="Empty", inline=False)
            cur = await db.execute("SELECT rss_url_3 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                embed.add_field(name="Position Three", value=f"**RSS URL**: {fetched_rss_url}", inline=False)
            else:
                embed.add_field(name="Position Three", value="Empty", inline=False)
            cur = await db.execute("SELECT rss_url_4 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                embed.add_field(name="Position Four", value=f"**RSS URL**: {fetched_rss_url}", inline=False)
            else:
                embed.add_field(name="Position Four", value="Empty", inline=False)
            cur = await db.execute("SELECT rss_url_5 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                embed.add_field(name="Position Five", value=f"**RSS URL**: {fetched_rss_url}", inline=False)
            else:
                embed.add_field(name="Position Five", value="Empty", inline=False)
            cur = await db.execute("SELECT rss_url_6 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                embed.add_field(name="Position Six", value=f"**RSS URL**: {fetched_rss_url}", inline=False)
            else:
                embed.add_field(name="Position Six", value="Empty", inline=False)
            cur = await db.execute("SELECT rss_url_7 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                embed.add_field(name="Position Seven", value=f"**RSS URL**: {fetched_rss_url}", inline=False)
            else:
                embed.add_field(name="Position Seven", value="Empty", inline=False)
            cur = await db.execute("SELECT rss_url_8 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                embed.add_field(name="Position Eight", value=f"**RSS URL**: {fetched_rss_url}", inline=False)
            else:
                embed.add_field(name="Position Eight", value="Empty", inline=False)
            cur = await db.execute("SELECT rss_url_9 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                embed.add_field(name="Position Nine", value=f"**RSS URL**: {fetched_rss_url}", inline=False)
            else:
                embed.add_field(name="Position Nine", value="Empty", inline=False)
            cur = await db.execute("SELECT rss_url_10 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                embed.add_field(name="Position Ten", value=f"**RSS URL**: {fetched_rss_url}", inline=False)
            else:
                embed.add_field(name="Position Ten", value="Empty", inline=False)
            await db.commit()
            await db.close()
        await ctx.send(embed=embed, delete_after=60.0, ephemeral=True)

    @rss.command(name="webhook_clear")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def webhook_clear(self, ctx: commands.Context, webhook_url: str):
        """(Admin Only) Run this command to clear all RSS feeds set to the webhook.

        Parameters
        -----------
        webhook_url : str
            Provide the URL for the webhook.
        """
        await ctx.defer(ephemeral=True)
        embed = discord.Embed(title="Webhook Cleared", description=f"**Webhook URL**: {webhook_url}")
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR REPLACE INTO webhooks (url) VALUES (?)", (webhook_url,))
            cur = await db.execute("SELECT name FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            name = row[0]
            cur = await db.execute("SELECT avatar_url FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            avatar_url = row[0]
            if name is not None and avatar_url is not None:
                embed.set_author(name=name,icon_url=avatar_url)
            cur = await db.execute("SELECT rss_url_1 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is None:
                embed.add_field(name="Position One", value="Cleared!", inline=False)
            else:
                embed.add_field(name="Position One Error", value=f"{fetched_rss_url}", inline=False)
            cur = await db.execute("SELECT rss_url_2 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is None:
                embed.add_field(name="Position Two", value="Cleared!", inline=False)
            else:
                embed.add_field(name="Position Two Error", value=f"{fetched_rss_url}", inline=False)
            cur = await db.execute("SELECT rss_url_3 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is None:
                embed.add_field(name="Position Three", value="Cleared!", inline=False)
            else:
                embed.add_field(name="Position Three Error", value=f"{fetched_rss_url}", inline=False)
            cur = await db.execute("SELECT rss_url_4 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is None:
                embed.add_field(name="Position Four", value="Cleared!", inline=False)
            else:
                embed.add_field(name="Position Four Error", value=f"{fetched_rss_url}", inline=False)
            cur = await db.execute("SELECT rss_url_5 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is None:
                embed.add_field(name="Position Five", value="Cleared", inline=False)
            else:
                embed.add_field(name="Position Five Error", value=f"{fetched_rss_url}", inline=False)
            cur = await db.execute("SELECT rss_url_6 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is None:
                embed.add_field(name="Position Six", value="Cleared!", inline=False)
            else:
                embed.add_field(name="Position Six Error", value=f"{fetched_rss_url}", inline=False)
            cur = await db.execute("SELECT rss_url_7 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is None:
                embed.add_field(name="Position Seven", value="Cleared!", inline=False)
            else:
                embed.add_field(name="Position Seven Error", value=f"{fetched_rss_url}", inline=False)
            cur = await db.execute("SELECT rss_url_8 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is None:
                embed.add_field(name="Position Eight", value="Cleared!", inline=False)
            else:
                embed.add_field(name="Position Eight Error", value=f"{fetched_rss_url}", inline=False)
            cur = await db.execute("SELECT rss_url_9 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is None:
                embed.add_field(name="Position Nine", value="Cleared!", inline=False)
            else:
                embed.add_field(name="Position Nine Error", value=f"{fetched_rss_url}", inline=False)
            cur = await db.execute("SELECT rss_url_10 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is None:
                embed.add_field(name="Position Ten", value="Cleared!", inline=False)
            else:
                embed.add_field(name="Position Ten Error", value=f"{fetched_rss_url}", inline=False)
            await db.commit()
            await db.close()
        await ctx.send(embed=embed, delete_after=60.0, ephemeral=True)

    @rss.command(name="feed_setup")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def feed_setup(self, ctx: commands.Context, webhook_url: str, rss_feed_url: str):
        """(Admin Only) Run this command to set an RSS Feed. All fields are required.

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
        embed = discord.Embed(title="RSS Feed Setup")
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO webhooks (url) VALUES (?)", (webhook_url,))
            cur = await db.execute("SELECT name FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            name = row[0]
            cur = await db.execute("SELECT avatar_url FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            avatar_url = row[0]
            if name is not None and avatar_url is not None:
                embed.set_author(name = name, icon_url = avatar_url)
            cur = await db.execute("SELECT rss_url_1 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is None:
                await db.execute("UPDATE webhooks SET rss_url_1 = ? WHERE url = ?", (rss_feed_url, webhook_url))
                embed.add_field(name="✔️ Success ✔️", value="The RSS feed has been set to the webhook at **position one**!")
                embed.add_field(name="Webhook URL", value=f"{webhook_url}", inline=False)
                embed.add_field(name="RSS Feed URL", value=f"{rss_feed_url}", inline=False)
            else:
                cur = await db.execute("SELECT rss_url_2 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is None:
                    await db.execute("UPDATE webhooks SET rss_url_2 = ? WHERE url = ?", (rss_feed_url, webhook_url))
                    embed.add_field(name="✔️ Success ✔️", value="The RSS feed has been set to the webhook at **position two**!")
                    embed.add_field(name="Webhook URL", value=f"{webhook_url}", inline=False)
                    embed.add_field(name="RSS Feed URL", value=f"{rss_feed_url}", inline=False)
                else:
                    cur = await db.execute("SELECT rss_url_3 FROM webhooks WHERE url = ?", (webhook_url,))
                    row = await cur.fetchone()
                    fetched_rss_url = row[0]
                    if fetched_rss_url is None:
                        await db.execute("UPDATE webhooks SET rss_url_3 = ? WHERE url = ?", (rss_feed_url, webhook_url))
                        embed.add_field(name="✔️ Success ✔️", value="The RSS feed has been set to the webhook at **position three**!")
                        embed.add_field(name="Webhook URL", value=f"{webhook_url}", inline=False)
                        embed.add_field(name="RSS Feed URL", value=f"{rss_feed_url}", inline=False)
                    else:
                        cur = await db.execute("SELECT rss_url_4 FROM webhooks WHERE url = ?", (webhook_url,))
                        row = await cur.fetchone()
                        fetched_rss_url = row[0]
                        if fetched_rss_url is None:
                            await db.execute("UPDATE webhooks SET rss_url_4 = ? WHERE url = ?", (rss_feed_url, webhook_url))
                            embed.add_field(name="✔️ Success ✔️", value="The RSS feed has been set to the webhook at **position four**!")
                            embed.add_field(name="Webhook URL", value=f"{webhook_url}", inline=False)
                            embed.add_field(name="RSS Feed URL", value=f"{rss_feed_url}", inline=False)
                        else:
                            cur = await db.execute("SELECT rss_url_5 FROM webhooks WHERE url = ?", (webhook_url,))
                            row = await cur.fetchone()
                            fetched_rss_url = row[0]
                            if fetched_rss_url is None:
                                await db.execute("UPDATE webhooks SET rss_url_5 = ? WHERE url = ?", (rss_feed_url, webhook_url))
                                embed.add_field(name="✔️ Success ✔️", value="The RSS feed has been set to the webhook at **position five**!")
                                embed.add_field(name="Webhook URL", value=f"{webhook_url}", inline=False)
                                embed.add_field(name="RSS Feed URL", value=f"{rss_feed_url}", inline=False)
                            else:
                                cur = await db.execute("SELECT rss_url_6 FROM webhooks WHERE url = ?", (webhook_url,))
                                row = await cur.fetchone()
                                fetched_rss_url = row[0]
                                if fetched_rss_url is None:
                                    await db.execute("UPDATE webhooks SET rss_url_6 = ? WHERE url = ?", (rss_feed_url, webhook_url))
                                    embed.add_field(name="✔️ Success ✔️", value="The RSS feed has been set to the webhook at **position six**!")
                                    embed.add_field(name="Webhook URL", value=f"{webhook_url}", inline=False)
                                    embed.add_field(name="RSS Feed URL", value=f"{rss_feed_url}", inline=False)
                                else:
                                    cur = await db.execute("SELECT rss_url_7 FROM webhooks WHERE url = ?", (webhook_url,))
                                    row = await cur.fetchone()
                                    fetched_rss_url = row[0]
                                    if fetched_rss_url is None:
                                        await db.execute("UPDATE webhooks SET rss_url_7 = ? WHERE url = ?", (rss_feed_url, webhook_url))
                                        embed.add_field(name="✔️ Success ✔️", value="The RSS feed has been set to the webhook at **position seven**!")
                                        embed.add_field(name="Webhook URL", value=f"{webhook_url}", inline=False)
                                        embed.add_field(name="RSS Feed URL", value=f"{rss_feed_url}", inline=False)
                                    else:
                                        cur = await db.execute("SELECT rss_url_8 FROM webhooks WHERE url = ?", (webhook_url,))
                                        row = await cur.fetchone()
                                        fetched_rss_url = row[0]
                                        if fetched_rss_url is None:
                                            await db.execute("UPDATE webhooks SET rss_url_8 = ? WHERE url = ?", (rss_feed_url, webhook_url))
                                            embed.add_field(name="✔️ Success ✔️", value="The RSS feed has been set to the webhook at **position eight**!")
                                            embed.add_field(name="Webhook URL", value=f"{webhook_url}", inline=False)
                                            embed.add_field(name="RSS Feed URL", value=f"{rss_feed_url}", inline=False)
                                        else:
                                            cur = await db.execute("SELECT rss_url_9 FROM webhooks WHERE url = ?", (webhook_url,))
                                            row = await cur.fetchone()
                                            fetched_rss_url = row[0]
                                            if fetched_rss_url is None:
                                                await db.execute("UPDATE webhooks SET rss_url_9 = ? WHERE url = ?", (rss_feed_url, webhook_url))
                                                embed.add_field(name="✔️ Success ✔️", value="The RSS feed has been set to the webhook at **position nine**!")
                                                embed.add_field(name="Webhook URL", value=f"{webhook_url}", inline=False)
                                                embed.add_field(name="RSS Feed URL", value=f"{rss_feed_url}", inline=False)
                                            else:
                                                cur = await db.execute("SELECT rss_url_10 FROM webhooks WHERE url = ?", (webhook_url,))
                                                row = await cur.fetchone()
                                                fetched_rss_url = row[0]
                                                if fetched_rss_url is None:
                                                    await db.execute("UPDATE webhooks SET rss_url_10 = ? WHERE url = ?", (rss_feed_url, webhook_url))
                                                    embed.add_field(name="✔️ Success ✔️", value="The RSS feed has been set to the webhook at **position ten**!")
                                                    embed.add_field(name="Webhook URL", value=f"{webhook_url}", inline=False)
                                                    embed.add_field(name="RSS Feed URL", value=f"{rss_feed_url}", inline=False)
                                                else:
                                                    embed.add_field(name="❌ Error ❌", value="This webhook is already associated with 10 RSS feeds. Please use `/rss feed_clear` or `/rss webhook_clear` to remove one or all RSS feeds from this webhook.")
            await db.commit()
            await db.close()
        await ctx.send(embed=embed, delete_after=60.0, ephemeral=True)

    @rss.command(name="feed_clear")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def feed_clear(self, ctx: commands.Context, webhook_url: str, rss_feed_position: Literal[1,2,3,4,5,6,7,8,9,10]):
        """(Admin Only) Run this command to clear one RSS feed from a webhook.

        Parameters
        -----------
        webhook_url : str
            Provide the URL for the webhook.
        rss_feed_position : int
            Provide the position (1-10) for the RSS feed you want to clear. Check position with /checkwebhook.
        """
        await ctx.defer(ephemeral=True)
        embed = discord.Embed(title="Webhook Update", description=f"**Webhook URL**: {webhook_url}")
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR REPLACE INTO webhooks (url) VALUES (?)", (webhook_url,))
            cur = await db.execute("SELECT name FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            name = row[0]
            cur = await db.execute("SELECT avatar_url FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            avatar_url = row[0]
            if name is not None and avatar_url is not None:
                embed.set_author(name=name,icon_url=avatar_url)
            if rss_feed_position == 1:
                await db.execute("INSERT OR REPLACE INTO webhooks (rss_url_1) VALUES (NULL) WHERE url = ?", (webhook_url,))
                cur = await db.execute("SELECT rss_url_1 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is None:
                    embed.add_field(name="✔️ Success ✔️", value=f"Position one cleared!", inline=False)
                else:
                    embed.add_field(name="❌ Error ❌", value=f"Position one **not** cleared!", inline=False)
            elif rss_feed_position == 2:
                await db.execute("INSERT OR REPLACE INTO webhooks (rss_url_2) VALUES (NULL) WHERE url = ?", (webhook_url,))
                cur = await db.execute("SELECT rss_url_2 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is None:
                    embed.add_field(name="✔️ Success ✔️", value=f"Position two cleared!", inline=False)
                else:
                    embed.add_field(name="❌ Error ❌", value=f"Position two **not** cleared!", inline=False)
            elif rss_feed_position == 3:
                await db.execute("INSERT OR REPLACE INTO webhooks (rss_url_3) VALUES (NULL) WHERE url = ?", (webhook_url,))
                cur = await db.execute("SELECT rss_url_3 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is None:
                    embed.add_field(name="✔️ Success ✔️", value=f"Position three cleared!", inline=False)
                else:
                    embed.add_field(name="❌ Error ❌", value=f"Position three **not** cleared!", inline=False)
            elif rss_feed_position == 4:
                await db.execute("INSERT OR REPLACE INTO webhooks (rss_url_4) VALUES (NULL) WHERE url = ?", (webhook_url,))
                cur = await db.execute("SELECT rss_url_4 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is None:
                    embed.add_field(name="✔️ Success ✔️", value=f"Position four cleared!", inline=False)
                else:
                    embed.add_field(name="❌ Error ❌", value=f"Position four **not** cleared!", inline=False)
            elif rss_feed_position == 5:
                await db.execute("INSERT OR REPLACE INTO webhooks (rss_url_5) VALUES (NULL) WHERE url = ?", (webhook_url,))
                cur = await db.execute("SELECT rss_url_5 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is None:
                    embed.add_field(name="✔️ Success ✔️", value=f"Position five cleared!", inline=False)
                else:
                    embed.add_field(name="❌ Error ❌", value=f"Position five **not** cleared!", inline=False)
            elif rss_feed_position == 6:
                await db.execute("INSERT OR REPLACE INTO webhooks (rss_url_6) VALUES (NULL) WHERE url = ?", (webhook_url,))
                cur = await db.execute("SELECT rss_url_6 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is None:
                    embed.add_field(name="✔️ Success ✔️", value=f"Position six cleared!", inline=False)
                else:
                    embed.add_field(name="❌ Error ❌", value=f"Position six **not** cleared!", inline=False)
            elif rss_feed_position == 7:
                await db.execute("INSERT OR REPLACE INTO webhooks (rss_url_7) VALUES (NULL) WHERE url = ?", (webhook_url,))
                cur = await db.execute("SELECT rss_url_7 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is None:
                    embed.add_field(name="✔️ Success ✔️", value=f"Position seven cleared!", inline=False)
                else:
                    embed.add_field(name="❌ Error ❌", value=f"Position seven **not** cleared!", inline=False)
            elif rss_feed_position == 8:
                await db.execute("INSERT OR REPLACE INTO webhooks (rss_url_8) VALUES (NULL) WHERE url = ?", (webhook_url,))
                cur = await db.execute("SELECT rss_url_8 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is None:
                    embed.add_field(name="✔️ Success ✔️", value=f"Position eight cleared!", inline=False)
                else:
                    embed.add_field(name="❌ Error ❌", value=f"Position eight **not** cleared!", inline=False)
            elif rss_feed_position == 9:
                await db.execute("INSERT OR REPLACE INTO webhooks (rss_url_9) VALUES (NULL) WHERE url = ?", (webhook_url,))
                cur = await db.execute("SELECT rss_url_9 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is None:
                    embed.add_field(name="✔️ Success ✔️", value=f"Position nine cleared!", inline=False)
                else:
                    embed.add_field(name="❌ Error ❌", value=f"Position nine **not** cleared!", inline=False)
            elif rss_feed_position == 10:
                await db.execute("INSERT OR REPLACE INTO webhooks (rss_url_10) VALUES (NULL) WHERE url = ?", (webhook_url,))
                cur = await db.execute("SELECT rss_url_10 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is None:
                    embed.add_field(name="✔️ Success ✔️", value=f"Position ten cleared!", inline=False)
                else:
                    embed.add_field(name="❌ Error ❌", value=f"Position ten **not** cleared!", inline=False)
            else:
                embed = discord.Embed(title="❌ Error ❌", description="You must enter a number from 1 to 10 as the RSS feed position. Check which position on the Webhook the RSS feed is stored at by using `/checkwebhook`.")
            await db.commit()
            await db.close()
        await ctx.send(embed=embed, delete_after=60.0, ephemeral=True)

class RSSFeeds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.postrss.start()
    
    def cog_unload(self):
        self.postrss.cancel()
    
    async def getwebhooks(self):
        urls = []
        async with aiosqlite.connect('rainbowbot.db') as db:
            async with db.execute("SELECT url FROM webhooks") as cur:
                async for row in cur:
                    url = str(row[0])
                    if "https://discord.com/api/webhooks/" in url:
                        urls.append(url)
        return urls
    
    async def getfeeds(self, webhook_url):
        allfeeds = {}
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO webhooks (url) VALUES (?)", (webhook_url,))
            feed1 = {}
            cur = await db.execute("SELECT rss_url_1 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                feed1["url"] = fetched_rss_url
                cur = await db.execute("SELECT rss_last_sent_1 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_last_sent = row[0]
                if fetched_last_sent is not None:
                    feed1["last sent"] = fetched_last_sent
                allfeeds["feed1"] = feed1
            feed2 = {}
            cur = await db.execute("SELECT rss_url_2 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                feed2["url"] = fetched_rss_url
                cur = await db.execute("SELECT rss_last_sent_2 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_last_sent = row[0]
                if fetched_last_sent is not None:
                    feed2["last sent"] = fetched_last_sent
                allfeeds["feed2"] = feed2
            feed3 = {}
            cur = await db.execute("SELECT rss_url_3 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                feed3["url"] = fetched_rss_url
                cur = await db.execute("SELECT rss_last_sent_3 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_last_sent = row[0]
                if fetched_last_sent is not None:
                    feed3["last sent"] = fetched_last_sent
                allfeeds["feed3"] = feed3
            feed4 = {}
            cur = await db.execute("SELECT rss_url_4 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                feed4["url"] = fetched_rss_url
                cur = await db.execute("SELECT rss_last_sent_4 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_last_sent = row[0]
                if fetched_last_sent is not None:
                    feed4["last sent"] = fetched_last_sent
                allfeeds["feed4"] = feed4
            feed5 = {}
            cur = await db.execute("SELECT rss_url_5 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                feed5["url"] = fetched_rss_url
                cur = await db.execute("SELECT rss_last_sent_5 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_last_sent = row[0]
                if fetched_last_sent is not None:
                    feed5["last sent"] = fetched_last_sent
                allfeeds["feed5"] = feed5
            feed6 = {}
            cur = await db.execute("SELECT rss_url_6 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                feed6["url"] = fetched_rss_url
                cur = await db.execute("SELECT rss_last_sent_6 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_last_sent = row[0]
                if fetched_last_sent is not None:
                    feed6["last sent"] = fetched_last_sent
                allfeeds["feed6"] = feed6
            feed7 = {}
            cur = await db.execute("SELECT rss_url_7 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                feed7["url"] = fetched_rss_url
                cur = await db.execute("SELECT rss_last_sent_7 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_last_sent = row[0]
                if fetched_last_sent is not None:
                    feed7["last sent"] = fetched_last_sent
                allfeeds["feed7"] = feed7
            feed8 = {}
            cur = await db.execute("SELECT rss_url_8 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                feed8["url"] = fetched_rss_url
                cur = await db.execute("SELECT rss_last_sent_8 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_last_sent = row[0]
                if fetched_last_sent is not None:
                    feed8["last sent"] = fetched_last_sent
                allfeeds["feed8"] = feed8
            feed9 = {}
            cur = await db.execute("SELECT rss_url_9 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                feed9["url"] = fetched_rss_url
                cur = await db.execute("SELECT rss_last_sent_9 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_last_sent = row[0]
                if fetched_last_sent is not None:
                    feed9["last sent"] = fetched_last_sent
                allfeeds["feed9"] = feed9
            feed10 = {}
            cur = await db.execute("SELECT rss_url_10 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                feed10["url"] = fetched_rss_url
                cur = await db.execute("SELECT rss_last_sent_10 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_last_sent = row[0]
                if fetched_last_sent is not None:
                    feed10["last sent"] = fetched_last_sent
                allfeeds["feed10"] = feed10
        return allfeeds

    async def parsefeed(self, webhook_url, feed_url):
        feedparser.USER_AGENT = "RainbowBot/1.0 +https://rainbowbot.carrd.co/#"
        feed = feedparser.parse(feed_url)
        entries = feed.entries
        embeds = {}
        for entry in entries:
            color = discord.Colour.blurple()
            title = entry.title[:256]
            print(f"Title: {title}")
            link = entry.link
            print(f"Link: {link}")
            async with aiohttp.ClientSession() as session:
                partialwebhook = Webhook.from_url(url=webhook_url, session=session)
                webhook = await partialwebhook.fetch()
                channel = webhook.channel
                embeds = [message.embeds async for message in channel.history(limit=100)]
                for embedlist in embeds:
                    for embed in embedlist:
                        if embed.url != link:
                            soup = BeautifulSoup(entry.summary, "html.parser")
                            parsedsoup = soup.get_text()
                            summary = parsedsoup[:256] + "..."
                            print(f"Summary: {summary}")
                            time = datetime.fromtimestamp(mktime(entry.published_parsed))
                            print(f"Timestamp: {time}")
                            embed = discord.Embed(colour=color, title=title, url=link, description=summary, timestamp=time)
                            embed.set_thumbnail(url=link)
                            author = entry.author[:256]
                            print(f"Author: {author}")
                            author_url = entry.href
                            print(f"Author URL: {author_url}")
                            embed.set_author(name=author, url=author_url)
                            print(embed)
                            embeds.append(embed)
        return embeds

    @tasks.loop(minutes=5.0)
    async def postrss(self):
        urls = await self.getwebhooks()
        async with aiosqlite.connect('rainbowbot.db') as db:
            for url in urls:
                feeds = await self.getfeeds(url)
                if len(feeds) > 0:
                    for feed in feeds.items():
                        feed_url = feed[1]['url']
                        embeds = await self.parsefeed(url, feed_url)
                        for embed in embeds:
                            async with aiohttp.ClientSession() as session:
                                webhook = Webhook.from_url(url=url, session=session)
                                await webhook.send(embed=embed)
                else:
                    return
            await db.commit()
            await db.close()

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
        await db.execute("""CREATE TABLE IF NOT EXISTS awards(
                         guild_member_id INTEGER PRIMARY KEY,
                         amount INTEGER DEFAULT NULL)""")
        await db.execute("""CREATE TABLE IF NOT EXISTS members(
                         member_id INTEGER PRIMARY KEY,
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
                         rss_url_1 TEXT DEFAULT NULL,
                         rss_url_2 TEXT DEFAULT NULL,
                         rss_url_3 TEXT DEFAULT NULL,
                         rss_url_4 TEXT DEFAULT NULL,
                         rss_url_5 TEXT DEFAULT NULL,
                         rss_url_6 TEXT DEFAULT NULL,
                         rss_url_7 TEXT DEFAULT NULL,
                         rss_url_8 TEXT DEFAULT NULL,
                         rss_url_9 TEXT DEFAULT NULL,
                         rss_url_10 TEXT DEFAULT NULL)""")
        await db.commit()
        await db.close()
    await bot.add_cog(BackgroundTasks(bot), override=True)
    await bot.add_cog(SetupCommands(bot), override=True)
    await bot.add_cog(PurgeCommands(bot), override=True)
    await bot.add_cog(AwardCommands(bot), override=True)
    await bot.add_cog(ProfileCommands(bot), override=True)
    await bot.add_cog(RSSCommands(bot), override=True)
    await bot.add_cog(RSSFeeds(bot), override=True)

@bot.event
async def on_ready():
    await setup(bot)
    print(f'Logged in as {bot.user}! (ID: {bot.user.id})')

token = 'token'
bot.run(token)