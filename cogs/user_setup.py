import discord
from discord import app_commands
from discord.ext import commands
import aiosqlite
from typing import Optional
from datetime import datetime, timedelta, timezone

bot = commands.Bot(
    command_prefix = 'rb!',
    description = "A multi-purpose Discord bot made by GitHub user gemhue.",
    intents = discord.Intents.all(),
    activity = discord.Activity(type=discord.ActivityType.listening, name="rb!help"),
    status = discord.Status.online
)

class Cog(commands.Cog):
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