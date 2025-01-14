import discord
import aiosqlite
import logging
import traceback
import os
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, timezone
from RainbowBotHelp import RainbowBotHelp

load_dotenv()
token = os.getenv("token")

class RainbowBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = commands.when_mentioned_or("rb!"),
            help_command = RainbowBotHelp(),
            description = "A multi-purpose Discord bot made by GitHub user gemhue.",
            intents = discord.Intents.all(),
            activity = discord.Activity(type=discord.ActivityType.listening, name="rb!help"),
            status = discord.Status.online
        )
        self.blurple = discord.Colour.blurple()
        self.green = discord.Colour.green()
        self.yellow = discord.Colour.yellow()
        self.red = discord.Colour.red()
    
    async def setup_hook(self):
        # Connect to database
        try:
            self.database = await aiosqlite.connect("rainbowbot.db")
            print("Connected to Database: rainbowbot.db")
        except Exception:
            print("There was an error connecting to the database.")
        # Clear the global command tree
        try:
            self.tree.clear_commands(guild=None)
            print("Global Command Tree: Cleared")
        except Exception:
            print("There was an error clearing the global command tree.")
        # Load all extensions
        try:
            cogs = []
            for cog in await allcogs(x="cogs"):
                await self.load_extension(cog)
                cogs.append(cog)
            list = ", ".join(cogs)
            print(f"Extensions Loaded: {list}")
        except Exception:
            print("There was an error loading the extensions.")
        # Sync the global command tree
        try:
            await self.tree.sync(guild=None)
            print("Global Command Tree: Synced")
        except Exception:
            print("There was an error syncing the global command tree.")

bot = RainbowBot()
handler = logging.FileHandler(filename="rainbowbot.log", encoding="utf-8", mode="w")

@bot.command(name="sync", hidden=True)
@commands.is_owner()
async def sync(ctx: commands.Context, where: str):
    """(Bot Owner Only) Syncs the bot's command tree either locally or globally.
    """
    await ctx.defer()
    guild = ctx.guild
    if where == "here" or where == "local":
        await bot.tree.sync(guild=guild)
        embed = discord.Embed(color=bot.green, title="Success", description=f"The bot's local command tree has been **synced**!")
    elif where == "all" or where == "global":
        await bot.tree.sync(guild=None)
        embed = discord.Embed(color=bot.green, title="Success", description=f"The bot's global command tree has been **synced**!")
    else:
        embed = discord.Embed(color=bot.red, title="Error", description=f"The bot's command tree has not been synced! Please specify if you would like to sync `here` or `all`.")
    await ctx.send(embed=embed, delete_after=10.0)
    await ctx.message.delete()

    # Send a log to the logging channel
    cur = await bot.database.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
    row = await cur.fetchone()
    fetched_logging = row[0]
    if fetched_logging is not None:
        logging_channel = ctx.guild.get_channel(fetched_logging)
        now = datetime.now(tz=timezone.utc)
        if logging_channel is None:
            log = discord.Embed(
                color=bot.red,
                title="Logging Channel Not Found",
                description=f"A logging channel with the ID {fetched_logging} was not found! Please set a new logging channel by re-running the `/start` command.",
                timestamp=now
            )
            await ctx.send(embed=log, delete_after=10.0)
        else:
            log = discord.Embed(
                color=bot.blurple,
                title="Command Tree Synced",
                timestamp=now
            )
            if where == "here" or where == "local":
                log.add_field(name="Local Tree", value=f"{ctx.author.mention} has just **synced** the bot's local command tree.")
            if where == "all" or where == "global":
                log.add_field(name="Global Tree", value=f"{ctx.author.mention} has just **synced** the bot's global command tree.")
            log.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
            log.set_thumbnail(url=ctx.author.display_avatar)
            await logging_channel.send(embed=log)

@bot.command(name="clear", hidden=True)
@commands.is_owner()
async def clear(ctx: commands.Context, where: str):
    """(Bot Owner Only) Clears the bot's command tree either locally or globally.
    """
    await ctx.defer()
    guild = ctx.guild
    if where == "here" or where == "local":
        bot.tree.clear_commands(guild=guild)
        embed = discord.Embed(color=bot.green, title="Success", description=f"The bot's local command tree has been **cleared**!")
    elif where == "all" or where == "global":
        bot.tree.clear_commands(guild=None)
        embed = discord.Embed(color=bot.green, title="Success", description=f"The bot's global command tree has been **cleared**!")
    else:
        embed = discord.Embed(color=bot.red, title="Error", description=f"The bot's command tree has not been cleared! Please specify if you would like to clear `here` or `all`.")
    await ctx.send(embed=embed, delete_after=10.0)
    await ctx.message.delete()
    
    # Send a log to the logging channel
    cur = await bot.database.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
    row = await cur.fetchone()
    fetched_logging = row[0]
    if fetched_logging is not None:
        logging_channel = ctx.guild.get_channel(fetched_logging)
        now = datetime.now(tz=timezone.utc)
        if logging_channel is None:
            log = discord.Embed(
                color=bot.red,
                title="Logging Channel Not Found",
                description=f"A logging channel with the ID {fetched_logging} was not found! Please set a new logging channel by re-running the `/start` command.",
                timestamp=now
            )
            await ctx.send(embed=log, delete_after=10.0)
        else:
            log = discord.Embed(
                color=bot.blurple,
                title="Command Tree Cleared",
                timestamp=now
            )
            if where == "here" or where == "local":
                log.add_field(name="Local Tree", value=f"{ctx.author.mention} has just **cleared** the bot's local command tree.")
            if where == "all" or where == "global":
                log.add_field(name="Global Tree", value=f"{ctx.author.mention} has just **cleared** the bot's global command tree.")
            log.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
            log.set_thumbnail(url=ctx.author.display_avatar)
            await logging_channel.send(embed=log)

async def allcogs(x):
    files = []
    cogs = []
    cogsdict = {}
    folder = "./cogs"
    for file in os.listdir(folder):
        if file.endswith(".py"):
            files.append(file[:-3])
    for file in files:
        if x == "cogs":
            cogs.append(f"cogs.{file}")
        elif x == "modules":
            title = file.title()
            cogs.append(f"{file}.{title}")
        elif x == "names":
            cogs.append(file)
        elif x == "names_lower":
            name = file.lower()
            cogs.append(name)
        elif x == "names_dict":
            lower = file.lower()
            cogsdict[lower] = file
    if len(cogs) > 0:
        return cogs
    elif len(cogsdict) > 0:
        return cogsdict
    else:
        return None

@bot.command(name="get", hidden=True)
@commands.is_owner()
async def get(ctx: commands.Context):
    """(Bot Owner Only) Returns a list of all of the bot's cogs.
    """
    await ctx.defer()
    now = datetime.now(tz=timezone.utc)
    embed = discord.Embed(color=bot.blurple, title="Cogs", timestamp=now)
    for cog in await allcogs(x="names"):
        embed.add_field(name=cog, value="Retreived successfully!")
    await ctx.send(embed=embed, delete_after=10.0)
    await ctx.message.delete()

    # Send a log to the logging channel
    cur = await bot.database.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
    row = await cur.fetchone()
    fetched_logging = row[0]
    if fetched_logging is not None:
        logging_channel = ctx.guild.get_channel(fetched_logging)
        if logging_channel is None:
            log = discord.Embed(
                color=bot.red,
                title="Logging Channel Not Found",
                description=f"A logging channel with the ID {fetched_logging} was not found! Please set a new logging channel by re-running the `/start` command.",
                timestamp=now
            )
            await ctx.send(embed=log, delete_after=10.0)
        else:
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
            embed.set_thumbnail(url=ctx.author.display_avatar)
            await logging_channel.send(embed=embed)

@bot.command(name="load", hidden=True)
@commands.is_owner()
async def load(ctx: commands.Context, extension: str):
    """(Bot Owner Only) Loads one or all of the bot's cogs.

    Parameters
    -----------
    extension : str
        Provide the extension that you would like to load (or all).
    """
    await ctx.defer()
    now = datetime.now(tz=timezone.utc)
    embed = discord.Embed(color=bot.blurple, title="Load Cogs", timestamp=now)
    lower = extension.lower()
    if lower == "all":
        for cog in await allcogs(x="cogs"):
            try:
                await bot.load_extension(cog)
                embed.add_field(name=cog, value="Loaded successfully!")
            except Exception as e:
                embed.add_field(name=cog, value=f"Error: {e}")
                print(traceback.format_exc())
    elif lower in await allcogs(x="names_lower"):
        for cog in await allcogs(x="cogs"):
            if cog.lower() == f"cogs.{lower}":
                try:
                    await bot.load_extension(cog)
                    embed.add_field(name=cog, value="Loaded successfully!")
                except Exception as e:
                    embed.add_field(name=cog, value=f"Error: {e}")
                    print(traceback.format_exc())
    else:
        embed.add_field(name="Error", value="No cogs could be loaded.")
    await ctx.send(embed=embed, delete_after=10.0)
    await ctx.message.delete()
    
    # Send a log to the logging channel
    cur = await bot.database.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
    row = await cur.fetchone()
    fetched_logging = row[0]
    if fetched_logging is not None:
        logging_channel = ctx.guild.get_channel(fetched_logging)
        if logging_channel is None:
            log = discord.Embed(
                color=bot.red,
                title="Logging Channel Not Found",
                description=f"A logging channel with the ID {fetched_logging} was not found! Please set a new logging channel by re-running the `/start` command.",
                timestamp=now
            )
            await ctx.send(embed=log, delete_after=10.0)
        else:
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
            embed.set_thumbnail(url=ctx.author.display_avatar)
            await logging_channel.send(embed=embed)

@bot.command(name="unload", hidden=True)
@commands.is_owner()
async def unload(ctx: commands.Context, extension: str):
    """(Bot Owner Only) Unloads one or all of the bot's cogs.

    Parameters
    -----------
    extension : str
        Provide the extension that you would like to unload (or all).
    """
    await ctx.defer()
    now = datetime.now(tz=timezone.utc)
    embed = discord.Embed(color=bot.blurple, title="Unload Cogs", timestamp=now)
    lower = extension.lower()
    if lower == "all":
        for cog in await allcogs(x="cogs"):
            try:
                await bot.unload_extension(cog)
                embed.add_field(name=cog, value="Unloaded successfully!")
            except Exception as e:
                embed.add_field(name=cog, value=f"Error: {e}")
                print(traceback.format_exc())
    elif lower in await allcogs(x="names_lower"):
        for cog in await allcogs(x="cogs"):
            if cog.lower() == f"cogs.{lower}":
                try:
                    await bot.unload_extension(cog)
                    embed.add_field(name=cog, value="Unloaded successfully!")
                except Exception as e:
                    embed.add_field(name=cog, value=f"Error: {e}")
                    print(traceback.format_exc())
    else:
        embed.add_field(name="Error", value="No cogs could be unloaded.")
    await ctx.send(embed=embed, delete_after=10.0)
    await ctx.message.delete()
    
    # Send a log to the logging channel
    cur = await bot.database.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
    row = await cur.fetchone()
    fetched_logging = row[0]
    if fetched_logging is not None:
        logging_channel = ctx.guild.get_channel(fetched_logging)
        if logging_channel is None:
            log = discord.Embed(
                color=bot.red,
                title="Logging Channel Not Found",
                description=f"A logging channel with the ID {fetched_logging} was not found! Please set a new logging channel by re-running the `/start` command.",
                timestamp=now
            )
            await ctx.send(embed=log, delete_after=10.0)
        else:
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
            embed.set_thumbnail(url=ctx.author.display_avatar)
            await logging_channel.send(embed=embed)

@bot.command(name="reload", hidden=True)
@commands.is_owner()
async def reload(ctx: commands.Context, extension: str):
    """(Bot Owner Only) Reloads one or all of the bot's cogs.

    Parameters
    -----------
    extension : str
        Provide the extension that you would like to reload (or all).
    """
    await ctx.defer()
    now = datetime.now(tz=timezone.utc)
    embed = discord.Embed(color=bot.blurple, title="Reload Cogs", timestamp=now)
    lower = extension.lower()
    if lower == "all":
        for cog in await allcogs(x="cogs"):
            try:
                await bot.reload_extension(cog)
                embed.add_field(name=cog, value="Reloaded successfully!")
            except Exception as e:
                embed.add_field(name=cog, value=f"Error: {e}")
                print(traceback.format_exc())
    elif lower in await allcogs(x="names_lower"):
        for cog in await allcogs(x="cogs"):
            if cog.lower() == f"cogs.{lower}":
                try:
                    await bot.reload_extension(cog)
                    embed.add_field(name=cog, value="Reloaded successfully!")
                except Exception as e:
                    embed.add_field(name=cog, value=f"Error: {e}")
                    print(traceback.format_exc())
    else:
        embed.add_field(name="Error", value="No cogs could be reloaded.")
    await ctx.send(embed=embed, delete_after=10.0)
    await ctx.message.delete()
    
    # Send a log to the logging channel
    cur = await bot.database.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
    row = await cur.fetchone()
    fetched_logging = row[0]
    if fetched_logging is not None:
        logging_channel = ctx.guild.get_channel(fetched_logging)
        if logging_channel is None:
            log = discord.Embed(
                color=bot.red,
                title="Logging Channel Not Found",
                description=f"A logging channel with the ID {fetched_logging} was not found! Please set a new logging channel by re-running the `/start` command.",
                timestamp=now
            )
            await ctx.send(embed=log, delete_after=10.0)
        else:
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
            embed.set_thumbnail(url=ctx.author.display_avatar)
            await logging_channel.send(embed=embed) 

@bot.command(name="ping")
async def ping(ctx: commands.Context):
    """Retrieve the bot's current latency.
    """
    await ctx.defer()
    try:
        now = datetime.now(tz=timezone.utc)
        latency = bot.latency*1000
        embed = discord.Embed(color=bot.blurple, title="Pong", description=f"The bot's current latency is {latency} seconds!", timestamp=now)
    except Exception as e:
        embed = discord.Embed(color=bot.red, title="Error", description=f"{e}")
        print(traceback.format_exc())
    await ctx.send(embed=embed, delete_after=10.0)
    await ctx.message.delete()

    # Send a log to the logging channel
    cur = await bot.database.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
    row = await cur.fetchone()
    fetched_logging = row[0]
    if fetched_logging is not None:
        logging_channel = ctx.guild.get_channel(fetched_logging)
        if logging_channel is None:
            log = discord.Embed(
                color=bot.red,
                title="Logging Channel Not Found",
                description=f"A logging channel with the ID {fetched_logging} was not found! Please set a new logging channel by re-running the `/start` command.",
                timestamp=now
            )
            await ctx.send(embed=log, delete_after=10.0)
        else:
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
            embed.set_thumbnail(url=ctx.author.display_avatar)
            await logging_channel.send(embed=embed)

@bot.event
async def on_ready(bot=bot):
    print(f'Logged in as {bot.user}! (ID: {bot.user.id})')

bot.run(token, log_handler=handler, log_level=logging.DEBUG)