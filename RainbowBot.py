import discord
import aiosqlite
import os
from discord.ext import commands
from datetime import datetime, timezone

bot = commands.Bot(
    command_prefix = commands.when_mentioned_or("rb!"),
    description = "A multi-purpose Discord bot made by GitHub user gemhue.",
    intents = discord.Intents.all(),
    activity = discord.Activity(type=discord.ActivityType.listening, name="rb!help"),
    status = discord.Status.online
)

blurple = discord.Colour.blurple()
green = discord.Colour.green()
red = discord.Colour.red()

@bot.command(name="sync", aliases=["synctree"], hidden=True)
@commands.is_owner()
async def sync(ctx: commands.Context, where: str):
    """(Bot Owner Only) Syncs the local command tree.
    """
    await ctx.defer(ephemeral=True)
    guild = ctx.guild
    now = datetime.now(tz=timezone.utc)
    if where == "here" or where == "local":
        await bot.tree.sync(guild=guild)
        embed = discord.Embed(color=green, title="Success", description=f"The bot's local command tree has been synced!", timestamp=now)
    elif where == "all" or where == "global":
        await bot.tree.sync(guild=None)
        embed = discord.Embed(color=green, title="Success", description=f"The bot's global command tree has been synced!", timestamp=now)
    else:
        embed = discord.Embed(color=red, title="Error", description=f"The bot's command tree has not been synced! Please specify if you would like to sync \`here\` or \`global\`.", timestamp=now)
    await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)
    await ctx.message.delete()
    async with aiosqlite.connect('rainbowbot.db') as db:
        cur = await db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
        row = await cur.fetchone()
        fetched_logging = row[0]
        if fetched_logging is not None:
            logging = bot.get_channel(fetched_logging)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
            await logging.send(embed=embed)
        await db.commit()
        await db.close()

@bot.command(name="clear", aliases=["cleartree"], hidden=True)
@commands.is_owner()
async def clear(ctx: commands.Context, where: str):
    """(Bot Owner Only) Clears the local command tree.
    """
    await ctx.defer(ephemeral=True)
    guild = ctx.guild
    now = datetime.now(tz=timezone.utc)
    if where == "here" or where == "local":
        bot.tree.clear_commands(guild=guild)
        embed = discord.Embed(color=green, title="Success", description=f"The bot's local command tree has been cleared!", timestamp=now)
    elif where == "all" or where == "global":
        bot.tree.clear_commands(guild=None)
        embed = discord.Embed(color=green, title="Success", description=f"The bot's global command tree has been cleared!", timestamp=now)
    else:
        embed = discord.Embed(color=red, title="Error", description=f"The bot's command tree has not been cleared! Please specify if you would like to clear \`here\` or \`global\`.", timestamp=now)
    await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)
    await ctx.message.delete()
    async with aiosqlite.connect('rainbowbot.db') as db:
        cur = await db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
        row = await cur.fetchone()
        fetched_logging = row[0]
        if fetched_logging is not None:
            logging = bot.get_channel(fetched_logging)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
            await logging.send(embed=embed)
        await db.commit()
        await db.close()

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
            cogs.append(f"{file}.{file}")
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

@bot.command(name="get_cogs", aliases=["get_cog","getcogs","getcog"], hidden=True)
@commands.is_owner()
async def get_cogs(ctx: commands.Context):
    """(Bot Owner Only) Returns all of the bot's cogs.
    """
    await ctx.defer(ephemeral=True)
    now = datetime.now(tz=timezone.utc)
    embed = discord.Embed(color=blurple, title="Cogs", timestamp=now)
    for cog in await allcogs(x="names"):
        embed.add_field(name=cog, value="Retreived successfully!")
    await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)
    await ctx.message.delete()
    async with aiosqlite.connect('rainbowbot.db') as db:
        cur = await db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
        row = await cur.fetchone()
        fetched_logging = row[0]
        if fetched_logging is not None:
            logging = bot.get_channel(fetched_logging)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
            await logging.send(embed=embed)
        await db.commit()
        await db.close()

@bot.command(name="load_cogs", aliases=["load_cog","loadcogs","loadcog"], hidden=True)
@commands.is_owner()
async def load_cogs(ctx: commands.Context, extension: str):
    """(Bot Owner Only) Loads one or all of the bot's cogs.

    Parameters
    -----------
    extension : str
        Provide the extension that you would like to load (or all).
    """
    await ctx.defer(ephemeral=True)
    now = datetime.now(tz=timezone.utc)
    embed = discord.Embed(color=blurple, title="Load Cogs", timestamp=now)
    lower = extension.lower()
    if lower == "all":
        for cog in await allcogs(x="cogs"):
            try:
                await bot.load_extension(cog)
                embed.add_field(name=cog, value="Loaded successfully!")
            except Exception as e:
                embed.add_field(name=cog, value=f"Error: {e}")
    elif lower in await allcogs(x="names_lower") and lower != "all":
        for cog in await allcogs(x="cogs"):
            cogstr = str(cog)
            coglow = cogstr.lower()
            lowcog = f"cog.{lower}"
            if coglow == lowcog:
                try:
                    await bot.load_extension(cog)
                    embed.add_field(name=cog, value="Loaded successfully!")
                except Exception as e:
                    embed.add_field(name=cog, value=f"Error: {e}")
    else:
        embed.add_field(name="Error", value="No cogs could be loaded.")
    await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)
    await ctx.message.delete()
    async with aiosqlite.connect('rainbowbot.db') as db:
        cur = await db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
        row = await cur.fetchone()
        fetched_logging = row[0]
        if fetched_logging is not None:
            logging = bot.get_channel(fetched_logging)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
            await logging.send(embed=embed)
        await db.commit()
        await db.close()

@bot.command(name="reload_cogs", aliases=["reload_cog","reloadcogs","reloadcog"], hidden=True)
@commands.is_owner()
async def reload_cogs(ctx: commands.Context, extension: str):
    """(Bot Owner Only) Reloads one or all of the bot's cogs.

    Parameters
    -----------
    extension : str
        Provide the extension that you would like to reload (or all).
    """
    await ctx.defer(ephemeral=True)
    now = datetime.now(tz=timezone.utc)
    embed = discord.Embed(color=blurple, title="Reload Cogs", timestamp=now)
    lower = extension.lower()
    if lower == "all":
        for cog in await allcogs(x="cogs"):
            try:
                await bot.reload_extension(cog)
                embed.add_field(name=cog, value="Reloaded successfully!")
            except Exception as e:
                embed.add_field(name=cog, value=f"Error: {e}")
    elif lower in await allcogs(x="names_lower") and lower != "all":
        for cog in await allcogs(x="cogs"):
            cogstr = str(cog)
            coglow = cogstr.lower()
            lowcog = f"cog.{lower}"
            if coglow == lowcog:
                try:
                    await bot.reload_extension(cog)
                    embed.add_field(name=cog, value="Reloaded successfully!")
                except Exception as e:
                    embed.add_field(name=cog, value=f"Error: {e}")
    else:
        embed.add_field(name="Error", value="No cogs could be reloaded.")
    await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)
    await ctx.message.delete()
    async with aiosqlite.connect('rainbowbot.db') as db:
        cur = await db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
        row = await cur.fetchone()
        fetched_logging = row[0]
        if fetched_logging is not None:
            logging = bot.get_channel(fetched_logging)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
            await logging.send(embed=embed)
        await db.commit()
        await db.close()

@bot.command(name="ping", aliases=["latency"])
async def ping(ctx: commands.Context):
    """Retrieve the bot's current latency.
    """
    await ctx.defer(ephemeral=True)
    embed = discord.Embed(color=blurple, title="Pong", description=f"The bot's current latency is {bot.latency} seconds!")
    await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)
    await ctx.message.delete()

async def setup():
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
                         active_role_id INTEGER DEFAULT NULL,
                         inactive_role_id INTEGER DEFAULT NULL,
                         inactive_days INTEGER DEFAULT NULL,
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

@bot.event
async def on_ready():
    await setup()
    print(f'Logged in as {bot.user}! (ID: {bot.user.id})')

token = 'token'
bot.run(token)
