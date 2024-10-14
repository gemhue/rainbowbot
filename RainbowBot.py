import discord
import aiosqlite
from discord.ext import commands
from typing import Literal
from cogs import autodelete, award, background, profile, purge, rss, user_setup

bot = commands.Bot(
    command_prefix = 'rb!',
    description = "A multi-purpose Discord bot made by GitHub user gemhue.",
    intents = discord.Intents.all(),
    activity = discord.Activity(type=discord.ActivityType.listening, name="rb!help"),
    status = discord.Status.online
)

@commands.command(name="sync", hidden=True)
@commands.is_owner()
async def sync(ctx: commands.Context):
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
async def globalsync(ctx: commands.Context):
    """(Bot Owner Only) Syncs the global command tree.
    """
    await ctx.defer(ephemeral=True)
    await bot.tree.sync(guild=None)
    embed = discord.Embed(title="Update", description=f"The bot's global command tree has been synced!")
    await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)
    await ctx.message.delete()

@commands.command(name="clear", hidden=True)
@commands.is_owner()
async def clear(ctx: commands.Context):
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
async def globalclear(ctx: commands.Context):
    """(Bot Owner Only) Clears the global command tree.
    """
    await ctx.defer(ephemeral=True)
    bot.tree.clear_commands(guild=None)
    embed = discord.Embed(title="Update", description=f"The bot's global command tree has been cleared!")
    await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)
    await ctx.message.delete()

@commands.command(name="load_cog", hidden=True)
@commands.is_owner()
async def load_cog(ctx: commands.Context, extension: Literal["all","autodelete","award","background","profile","purge","rss","user_setup"]):
    """(Bot Owner Only) Loads one or all of the bot's cogs.

    Parameters
    -----------
    extension : str
        Provide the extension that you would like to load.
    """
    if extension == "all":
        await bot.load_extension(autodelete.Cog(bot=bot))
        await bot.load_extension(award.Cog(bot=bot))
        await bot.load_extension(background.Cog(bot=bot))
        await bot.load_extension(profile.Cog(bot=bot))
        await bot.load_extension(purge.Cog(bot=bot))
        await bot.load_extension(rss.CommandsCog(bot=bot))
        await bot.load_extension(rss.FeedCog(bot=bot))
        await bot.load_extension(user_setup.Cog(bot=bot))
        embed = discord.Embed(title="Update", description=f"The bot's cogs were successfully loaded!")
        await ctx.send(embed=embed, delete_after=30.0)
    elif extension == "autodelete":
        await bot.load_extension(autodelete.Cog(bot=bot))
        embed = discord.Embed(title="Update", description=f"The bot's cog \`{extension}\` was successfully loaded!")
        await ctx.send(embed=embed, delete_after=30.0)
    elif extension == "award":
        await bot.load_extension(award.Cog(bot=bot))
        embed = discord.Embed(title="Update", description=f"The bot's cog \`{extension}\` was successfully loaded!")
        await ctx.send(embed=embed, delete_after=30.0)
    elif extension == "background":
        await bot.load_extension(background.Cog(bot=bot))
        embed = discord.Embed(title="Update", description=f"The bot's cog \`{extension}\` was successfully loaded!")
        await ctx.send(embed=embed, delete_after=30.0)
    elif extension == "profile":
        await bot.load_extension(profile.Cog(bot=bot))
        embed = discord.Embed(title="Update", description=f"The bot's cog \`{extension}\` was successfully loaded!")
        await ctx.send(embed=embed, delete_after=30.0)
    elif extension == "purge":
        await bot.load_extension(purge.Cog(bot=bot))
        embed = discord.Embed(title="Update", description=f"The bot's cog \`{extension}\` was successfully loaded!")
        await ctx.send(embed=embed, delete_after=30.0)
    elif extension == "rss":
        await bot.load_extension(rss.CommandsCog(bot=bot))
        await bot.load_extension(rss.FeedCog(bot=bot))
        embed = discord.Embed(title="Update", description=f"The bot's cog \`{extension}\` was successfully loaded!")
        await ctx.send(embed=embed, delete_after=30.0)
    elif extension == "user_setup":
        await bot.load_extension(user_setup.Cog(bot=bot))
        embed = discord.Embed(title="Update", description=f"The bot's cog \`{extension}\` was successfully loaded!")
        await ctx.send(embed=embed, delete_after=30.0)
    else:
        embed = discord.Embed(title="Error", description=f"No cog was found with the name \`{extension}\`.")
        await ctx.send(embed=embed, delete_after=30.0)

@commands.command(name="reload_cog", hidden=True)
@commands.is_owner()
async def reload_cog(ctx: commands.Context, extension: Literal["all","autodelete","award","background","profile","purge","rss","user_setup"]):
    """(Bot Owner Only) Reloads one or all of the bot's cogs.

    Parameters
    -----------
    extension : str
        Provide the extension that you would like to reload.
    """
    if extension == "all":
        await bot.reload_extension(autodelete.Cog(bot=bot))
        await bot.reload_extension(award.Cog(bot=bot))
        await bot.reload_extension(background.Cog(bot=bot))
        await bot.reload_extension(profile.Cog(bot=bot))
        await bot.reload_extension(purge.Cog(bot=bot))
        await bot.reload_extension(rss.CommandsCog(bot=bot))
        await bot.reload_extension(rss.FeedCog(bot=bot))
        await bot.reload_extension(user_setup.Cog(bot=bot))
        embed = discord.Embed(title="Update", description=f"The bot's cogs were successfully reloaded!")
        await ctx.send(embed=embed, delete_after=30.0)
    elif extension == "autodelete":
        await bot.reload_extension(autodelete.Cog(bot=bot))
        embed = discord.Embed(title="Update", description=f"The bot's cog \`{extension}\` was successfully reloaded!")
        await ctx.send(embed=embed, delete_after=30.0)
    elif extension == "award":
        await bot.reload_extension(award.Cog(bot=bot))
        embed = discord.Embed(title="Update", description=f"The bot's cog \`{extension}\` was successfully reloaded!")
        await ctx.send(embed=embed, delete_after=30.0)
    elif extension == "background":
        await bot.reload_extension(background.Cog(bot=bot))
        embed = discord.Embed(title="Update", description=f"The bot's cog \`{extension}\` was successfully reloaded!")
        await ctx.send(embed=embed, delete_after=30.0)
    elif extension == "profile":
        await bot.reload_extension(profile.Cog(bot=bot))
        embed = discord.Embed(title="Update", description=f"The bot's cog \`{extension}\` was successfully reloaded!")
        await ctx.send(embed=embed, delete_after=30.0)
    elif extension == "purge":
        await bot.reload_extension(purge.Cog(bot=bot))
        embed = discord.Embed(title="Update", description=f"The bot's cog \`{extension}\` was successfully reloaded!")
        await ctx.send(embed=embed, delete_after=30.0)
    elif extension == "rss":
        await bot.reload_extension(rss.CommandsCog(bot=bot))
        await bot.reload_extension(rss.FeedCog(bot=bot))
        embed = discord.Embed(title="Update", description=f"The bot's cog \`{extension}\` was successfully reloaded!")
        await ctx.send(embed=embed, delete_after=30.0)
    elif extension == "user_setup":
        await bot.reload_extension(user_setup.Cog(bot=bot))
        embed = discord.Embed(title="Update", description=f"The bot's cog \`{extension}\` was successfully reloaded!")
        await ctx.send(embed=embed, delete_after=30.0)
    else:
        embed = discord.Embed(title="Error", description=f"No cog was found with the name \`{extension}\`.")
        await ctx.send(embed=embed, delete_after=30.0)

@commands.command(name="ping")
async def ping(ctx: commands.Context):
    """Retrieve the bot's current latency.
    """
    latency = bot.latency()
    embed = discord.Embed(color=ctx.author.accent_color, title="Pong", description=f"The bot's current latency is {latency} seconds!")
    await ctx.send(embed=embed, delete_after=30.0)

async def setup(bot: commands.Bot):
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
    await bot.add_cog(autodelete.Cog(bot=bot), override=True)
    await bot.add_cog(award.Cog(bot=bot), override=True)
    await bot.add_cog(background.Cog(bot=bot), override=True)
    await bot.add_cog(profile.Cog(bot=bot), override=True)
    await bot.add_cog(purge.Cog(bot=bot), override=True)
    await bot.add_cog(rss.CommandsCog(bot=bot), override=True)
    await bot.add_cog(rss.FeedCog(bot=bot), override=True)
    await bot.add_cog(user_setup.Cog(bot=bot), override=True)

@bot.event
async def on_ready():
    await setup(bot)
    print(f'Logged in as {bot.user}! (ID: {bot.user.id})')

token = 'token'
bot.run(token)