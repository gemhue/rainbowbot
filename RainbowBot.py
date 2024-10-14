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

@bot.command(name="sync", hidden=True)
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

@bot.command(name="globalsync", hidden=True)
@commands.is_owner()
async def globalsync(ctx: commands.Context):
    """(Bot Owner Only) Syncs the global command tree.
    """
    await ctx.defer(ephemeral=True)
    await bot.tree.sync(guild=None)
    embed = discord.Embed(title="Update", description=f"The bot's global command tree has been synced!")
    await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)
    await ctx.message.delete()

@bot.command(name="clear", hidden=True)
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

@bot.command(name="globalclear", hidden=True)
@commands.is_owner()
async def globalclear(ctx: commands.Context):
    """(Bot Owner Only) Clears the global command tree.
    """
    await ctx.defer(ephemeral=True)
    bot.tree.clear_commands(guild=None)
    embed = discord.Embed(title="Update", description=f"The bot's global command tree has been cleared!")
    await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)
    await ctx.message.delete()

@bot.command(name="load_cog", hidden=True)
@commands.is_owner()
async def load_cog(ctx: commands.Context, extension: str):
    """(Bot Owner Only) Loads one or all of the bot's cogs.

    Parameters
    -----------
    extension : str
        Provide the extension that you would like to load (or all).
    """
    embed = discord.Embed(title="Load Cogs")
    if extension == "all":
        try:
            await bot.load_extension('cogs.autodelete')
            embed.add_field(name="cogs.autodelete", value="Loaded successfully!")
        except Exception as e:
            print(f"Error loading cogs.autodelete: {e}")
            embed.add_field(name="cogs.autodelete", value=f"Error: {e}")
        try:
            await bot.load_extension('cogs.award')
            embed.add_field(name="cogs.award", value="Loaded successfully!")
        except Exception as e:
            print(f"Error loading cogs.award: {e}")
            embed.add_field(name="cogs.award", value=f"Error: {e}")
        try:
            await bot.load_extension('cogs.background')
            embed.add_field(name="cogs.background", value="Loaded successfully!")
        except Exception as e:
            print(f"Error loading cogs.background: {e}")
            embed.add_field(name="cogs.background", value=f"Error: {e}")
        try:
            await bot.load_extension('cogs.profile')
            embed.add_field(name="cogs.profile", value="Loaded successfully!")
        except Exception as e:
            print(f"Error loading cogs.profile: {e}")
            embed.add_field(name="cogs.profile", value=f"Error: {e}")
        try:
            await bot.load_extension('cogs.purge')
            embed.add_field(name="cogs.purge", value="Loaded successfully!")
        except Exception as e:
            print(f"Error loading cogs.purge: {e}")
            embed.add_field(name="cogs.purge", value=f"Error: {e}")
        try:
            await bot.load_extension('cogs.rss')
            embed.add_field(name="cogs.rss", value="Loaded successfully!")
        except Exception as e:
            print(f"Error loading cogs.rss: {e}")
            embed.add_field(name="cogs.rss", value=f"Error: {e}")
        try:
            await bot.load_extension('cogs.user_setup')
            embed.add_field(name="cogs.user_setup", value="Loaded successfully!")
        except Exception as e:
            print(f"Error loading cogs.user_setup: {e}")
            embed.add_field(name="cogs.user_setup", value=f"Error: {e}")
    elif extension == "autodelete":
        try:
            await bot.load_extension('cogs.autodelete')
            embed.add_field(name="cogs.autodelete", value="Loaded successfully!")
        except Exception as e:
            print(f"Error loading cogs.autodelete: {e}")
            embed.add_field(name="cogs.autodelete", value=f"Error: {e}")
    elif extension == "award":
        try:
            await bot.load_extension('cogs.award')
            embed.add_field(name="cogs.award", value="Loaded successfully!")
        except Exception as e:
            print(f"Error loading cogs.award: {e}")
            embed.add_field(name="cogs.award", value=f"Error: {e}")
    elif extension == "background":
        try:
            await bot.load_extension('cogs.background')
            embed.add_field(name="cogs.background", value="Loaded successfully!")
        except Exception as e:
            print(f"Error loading cogs.background: {e}")
            embed.add_field(name="cogs.background", value=f"Error: {e}")
    elif extension == "profile":
        try:
            await bot.load_extension('cogs.profile')
            embed.add_field(name="cogs.profile", value="Loaded successfully!")
        except Exception as e:
            print(f"Error loading cogs.profile: {e}")
            embed.add_field(name="cogs.profile", value=f"Error: {e}")
    elif extension == "purge":
        try:
            await bot.load_extension('cogs.purge')
            embed.add_field(name="cogs.purge", value="Loaded successfully!")
        except Exception as e:
            print(f"Error loading cogs.purge: {e}")
            embed.add_field(name="cogs.purge", value=f"Error: {e}")
    elif extension == "rss":
        try:
            await bot.load_extension('cogs.rss')
            embed.add_field(name="cogs.rss", value="Loaded successfully!")
        except Exception as e:
            print(f"Error loading cogs.rss: {e}")
            embed.add_field(name="cogs.rss", value=f"Error: {e}")
    elif extension == "user_setup":
        try:
            await bot.load_extension('cogs.user_setup')
            embed.add_field(name="cogs.user_setup", value="Loaded successfully!")
        except Exception as e:
            print(f"Error loading cogs.user_setup: {e}")
            embed.add_field(name="cogs.user_setup", value=f"Error: {e}")
    else:
        embed.add_field(name="Error", value="No cogs could be loaded.")
    await ctx.send(embed=embed, delete_after=30.0)
    await ctx.message.delete()

@bot.command(name="reload_cog", hidden=True)
@commands.is_owner()
async def reload_cog(ctx: commands.Context, extension: str):
    """(Bot Owner Only) Reloads one or all of the bot's cogs.

    Parameters
    -----------
    extension : str
        Provide the extension that you would like to reload (or all).
    """
    embed = discord.Embed(title="Reload Cogs")
    if extension == "all":
        try:
            await bot.reload_extension('cogs.autodelete')
            embed.add_field(name="cogs.autodelete", value="Reloaded successfully!")
        except Exception as e:
            print(f"Error reloading cogs.autodelete: {e}")
            embed.add_field(name="cogs.autodelete", value=f"Error: {e}")
        try:
            await bot.reload_extension('cogs.award')
            embed.add_field(name="cogs.award", value="Reloaded successfully!")
        except Exception as e:
            print(f"Error reloading cogs.award: {e}")
            embed.add_field(name="cogs.award", value=f"Error: {e}")
        try:
            await bot.reload_extension('cogs.background')
            embed.add_field(name="cogs.background", value="Reloaded successfully!")
        except Exception as e:
            print(f"Error reloading cogs.background: {e}")
            embed.add_field(name="cogs.background", value=f"Error: {e}")
        try:
            await bot.reload_extension('cogs.profile')
            embed.add_field(name="cogs.profile", value="Reloaded successfully!")
        except Exception as e:
            print(f"Error reloading cogs.profile: {e}")
            embed.add_field(name="cogs.profile", value=f"Error: {e}")
        try:
            await bot.reload_extension('cogs.purge')
            embed.add_field(name="cogs.purge", value="Reloaded successfully!")
        except Exception as e:
            print(f"Error reloading cogs.purge: {e}")
            embed.add_field(name="cogs.purge", value=f"Error: {e}")
        try:
            await bot.reload_extension('cogs.rss')
            embed.add_field(name="cogs.rss", value="Reloaded successfully!")
        except Exception as e:
            print(f"Error reloading cogs.rss: {e}")
            embed.add_field(name="cogs.rss", value=f"Error: {e}")
        try:
            await bot.reload_extension('cogs.user_setup')
            embed.add_field(name="cogs.user_setup", value="Reloaded successfully!")
        except Exception as e:
            print(f"Error reloading cogs.user_setup: {e}")
            embed.add_field(name="cogs.user_setup", value=f"Error: {e}")
    elif extension == "autodelete":
        try:
            await bot.reload_extension('cogs.autodelete')
            embed.add_field(name="cogs.autodelete", value="Reloaded successfully!")
        except Exception as e:
            print(f"Error reloading cogs.autodelete: {e}")
            embed.add_field(name="cogs.autodelete", value=f"Error: {e}")
    elif extension == "award":
        try:
            await bot.reload_extension('cogs.award')
            embed.add_field(name="cogs.award", value="Reloaded successfully!")
        except Exception as e:
            print(f"Error reloading cogs.award: {e}")
            embed.add_field(name="cogs.award", value=f"Error: {e}")
    elif extension == "background":
        try:
            await bot.reload_extension('cogs.background')
            embed.add_field(name="cogs.background", value="Reloaded successfully!")
        except Exception as e:
            print(f"Error reloading cogs.background: {e}")
            embed.add_field(name="cogs.background", value=f"Error: {e}")
    elif extension == "profile":
        try:
            await bot.reload_extension('cogs.profile')
            embed.add_field(name="cogs.profile", value="Reloaded successfully!")
        except Exception as e:
            print(f"Error reloading cogs.profile: {e}")
            embed.add_field(name="cogs.profile", value=f"Error: {e}")
    elif extension == "purge":
        try:
            await bot.reload_extension('cogs.purge')
            embed.add_field(name="cogs.purge", value="Reloaded successfully!")
        except Exception as e:
            print(f"Error reloading cogs.purge: {e}")
            embed.add_field(name="cogs.purge", value=f"Error: {e}")
    elif extension == "rss":
        try:
            await bot.reload_extension('cogs.rss')
            embed.add_field(name="cogs.rss", value="Reloaded successfully!")
        except Exception as e:
            print(f"Error reloading cogs.rss: {e}")
            embed.add_field(name="cogs.rss", value=f"Error: {e}")
    elif extension == "user_setup":
        try:
            await bot.reload_extension('cogs.user_setup')
            embed.add_field(name="cogs.user_setup", value="Reloaded successfully!")
        except Exception as e:
            print(f"Error reloading cogs.user_setup: {e}")
            embed.add_field(name="cogs.user_setup", value=f"Error: {e}")
    else:
        embed.add_field(name="Error", value="No cogs could be reloaded.")
    await ctx.send(embed=embed, delete_after=30.0)
    await ctx.message.delete()

@bot.command(name="add_cog", hidden=True)
@commands.is_owner()
async def add_cog(ctx: commands.Context, extension: str):
    """(Bot Owner Only) Adds one or all of the bot's cogs.

    Parameters
    -----------
    extension : str
        Provide the extension that you would like to add (or all).
    """
    embed = discord.Embed(title="Add Cogs")
    if extension == "all":
        try:
            await bot.add_cog(autodelete.Cog(bot=bot), override=True)
            embed.add_field(name="autodelete.Cog", value="Added successfully!")
        except Exception as e:
            print(f"Error adding autodelete.Cog: {e}")
            embed.add_field(name="autodelete.Cog", value=f"Error: {e}")
        try:
            await bot.add_cog(award.Cog(bot=bot), override=True)
            embed.add_field(name="award.Cog", value="Added successfully!")
        except Exception as e:
            print(f"Error adding award.Cog: {e}")
            embed.add_field(name="award.Cog", value=f"Error: {e}")
        try:
            await bot.add_cog(background.Cog(bot=bot), override=True)
            embed.add_field(name="background.Cog", value="Added successfully!")
        except Exception as e:
            print(f"Error adding background.Cog: {e}")
            embed.add_field(name="background.Cog", value=f"Error: {e}")
        try:
            await bot.add_cog(profile.Cog(bot=bot), override=True)
            embed.add_field(name="profile.Cog", value="Added successfully!")
        except Exception as e:
            print(f"Error adding profile.Cog: {e}")
            embed.add_field(name="profile.Cog", value=f"Error: {e}")
        try:
            await bot.add_cog(purge.Cog(bot=bot), override=True)
            embed.add_field(name="purge.Cog", value="Added successfully!")
        except Exception as e:
            print(f"Error adding purge.Cog: {e}")
            embed.add_field(name="purge.Cog", value=f"Error: {e}")
        try:
            await bot.add_cog(rss.CommandsCog(bot=bot), override=True)
            embed.add_field(name="rss.CommandsCog", value="Added successfully!")
        except Exception as e:
            print(f"Error adding rss.CommandsCog: {e}")
            embed.add_field(name="rss.CommandsCog", value=f"Error: {e}")
        try:
            await bot.add_cog(rss.FeedCog(bot=bot), override=True)
            embed.add_field(name="rss.FeedCog", value="Added successfully!")
        except Exception as e:
            print(f"Error adding rss.FeedCog: {e}")
            embed.add_field(name="rss.FeedCog", value=f"Error: {e}")
        try:
            await bot.add_cog(user_setup.Cog(bot=bot), override=True)
            embed.add_field(name="user_setup.Cog", value="Added successfully!")
        except Exception as e:
            print(f"Error adding user_setup.Cog: {e}")
            embed.add_field(name="user_setup.Cog", value=f"Error: {e}")
    elif extension == "autodelete":
        try:
            await bot.add_cog(autodelete.Cog(bot=bot), override=True)
            embed.add_field(name="autodelete.Cog", value="Added successfully!")
        except Exception as e:
            print(f"Error adding autodelete.Cog: {e}")
            embed.add_field(name="autodelete.Cog", value=f"Error: {e}")
    elif extension == "award":
        try:
            await bot.add_cog(award.Cog(bot=bot), override=True)
            embed.add_field(name="award.Cog", value="Added successfully!")
        except Exception as e:
            print(f"Error adding award.Cog: {e}")
            embed.add_field(name="award.Cog", value=f"Error: {e}")
    elif extension == "background":
        try:
            await bot.add_cog(background.Cog(bot=bot), override=True)
            embed.add_field(name="background.Cog", value="Added successfully!")
        except Exception as e:
            print(f"Error adding background.Cog: {e}")
            embed.add_field(name="background.Cog", value=f"Error: {e}")
    elif extension == "profile":
        try:
            await bot.add_cog(profile.Cog(bot=bot), override=True)
            embed.add_field(name="profile.Cog", value="Added successfully!")
        except Exception as e:
            print(f"Error adding profile.Cog: {e}")
            embed.add_field(name="profile.Cog", value=f"Error: {e}")
    elif extension == "purge":
        try:
            await bot.add_cog(purge.Cog(bot=bot), override=True)
            embed.add_field(name="purge.Cog", value="Added successfully!")
        except Exception as e:
            print(f"Error adding purge.Cog: {e}")
            embed.add_field(name="purge.Cog", value=f"Error: {e}")
    elif extension == "rss":
        try:
            await bot.add_cog(rss.CommandsCog(bot=bot), override=True)
            embed.add_field(name="rss.CommandsCog", value="Added successfully!")
        except Exception as e:
            print(f"Error adding rss.CommandsCog: {e}")
            embed.add_field(name="rss.CommandsCog", value=f"Error: {e}")
        try:
            await bot.add_cog(rss.FeedCog(bot=bot), override=True)
            embed.add_field(name="rss.FeedCog", value="Added successfully!")
        except Exception as e:
            print(f"Error adding rss.FeedCog: {e}")
            embed.add_field(name="rss.FeedCog", value=f"Error: {e}")
    elif extension == "user_setup":
        try:
            await bot.add_cog(user_setup.Cog(bot=bot), override=True)
            embed.add_field(name="user_setup.Cog", value="Added successfully!")
        except Exception as e:
            print(f"Error adding user_setup.Cog: {e}")
            embed.add_field(name="user_setup.Cog", value=f"Error: {e}")
    else:
        embed.add_field(name="Error", value="No cogs could be added.")
    await ctx.send(embed=embed, delete_after=30.0)
    await ctx.message.delete()

@bot.command(name="remove_cog", hidden=True)
@commands.is_owner()
async def remove_cog(ctx: commands.Context, extension: str):
    """(Bot Owner Only) Removes one or all of the bot's cogs.

    Parameters
    -----------
    extension : str
        Provide the extension that you would like to remove (or all).
    """
    embed = discord.Embed(title="Remove Cogs")
    if extension == "all":
        try:
            await bot.remove_cog(autodelete.Cog(bot=bot), override=True)
            embed.add_field(name="autodelete.Cog", value="Removed successfully!")
        except Exception as e:
            print(f"Error removing autodelete.Cog: {e}")
            embed.add_field(name="autodelete.Cog", value=f"Error: {e}")
        try:
            await bot.remove_cog(award.Cog(bot=bot), override=True)
            embed.add_field(name="award.Cog", value="Removed successfully!")
        except Exception as e:
            print(f"Error removing award.Cog: {e}")
            embed.add_field(name="award.Cog", value=f"Error: {e}")
        try:
            await bot.remove_cog(background.Cog(bot=bot), override=True)
            embed.add_field(name="background.Cog", value="Removed successfully!")
        except Exception as e:
            print(f"Error removing background.Cog: {e}")
            embed.add_field(name="background.Cog", value=f"Error: {e}")
        try:
            await bot.remove_cog(profile.Cog(bot=bot), override=True)
            embed.add_field(name="profile.Cog", value="Removed successfully!")
        except Exception as e:
            print(f"Error removing profile.Cog: {e}")
            embed.add_field(name="profile.Cog", value=f"Error: {e}")
        try:
            await bot.remove_cog(purge.Cog(bot=bot), override=True)
            embed.add_field(name="purge.Cog", value="Removed successfully!")
        except Exception as e:
            print(f"Error removing purge.Cog: {e}")
            embed.add_field(name="purge.Cog", value=f"Error: {e}")
        try:
            await bot.remove_cog(rss.CommandsCog(bot=bot), override=True)
            embed.add_field(name="rss.CommandsCog", value="Removed successfully!")
        except Exception as e:
            print(f"Error removing rss.CommandsCog: {e}")
            embed.add_field(name="rss.CommandsCog", value=f"Error: {e}")
        try:
            await bot.remove_cog(rss.FeedCog(bot=bot), override=True)
            embed.add_field(name="rss.FeedCog", value="Removed successfully!")
        except Exception as e:
            print(f"Error removing rss.FeedCog: {e}")
            embed.add_field(name="rss.FeedCog", value=f"Error: {e}")
        try:
            await bot.remove_cog(user_setup.Cog(bot=bot), override=True)
            embed.add_field(name="user_setup.Cog", value="Removed successfully!")
        except Exception as e:
            print(f"Error removing user_setup.Cog: {e}")
            embed.add_field(name="user_setup.Cog", value=f"Error: {e}")
    elif extension == "autodelete":
        try:
            await bot.remove_cog(autodelete.Cog(bot=bot), override=True)
            embed.add_field(name="autodelete.Cog", value="Removed successfully!")
        except Exception as e:
            print(f"Error removing autodelete.Cog: {e}")
            embed.add_field(name="autodelete.Cog", value=f"Error: {e}")
    elif extension == "award":
        try:
            await bot.remove_cog(award.Cog(bot=bot), override=True)
            embed.add_field(name="award.Cog", value="Removed successfully!")
        except Exception as e:
            print(f"Error removing award.Cog: {e}")
            embed.add_field(name="award.Cog", value=f"Error: {e}")
    elif extension == "background":
        try:
            await bot.remove_cog(background.Cog(bot=bot), override=True)
            embed.add_field(name="background.Cog", value="Removed successfully!")
        except Exception as e:
            print(f"Error removing background.Cog: {e}")
            embed.add_field(name="background.Cog", value=f"Error: {e}")
    elif extension == "profile":
        try:
            await bot.remove_cog(profile.Cog(bot=bot), override=True)
            embed.add_field(name="profile.Cog", value="Removed successfully!")
        except Exception as e:
            print(f"Error removing profile.Cog: {e}")
            embed.add_field(name="profile.Cog", value=f"Error: {e}")
    elif extension == "purge":
        try:
            await bot.remove_cog(purge.Cog(bot=bot), override=True)
            embed.add_field(name="purge.Cog", value="Removed successfully!")
        except Exception as e:
            print(f"Error removing purge.Cog: {e}")
            embed.add_field(name="purge.Cog", value=f"Error: {e}")
    elif extension == "rss":
        try:
            await bot.remove_cog(rss.CommandsCog(bot=bot), override=True)
            embed.add_field(name="rss.CommandsCog", value="Removed successfully!")
        except Exception as e:
            print(f"Error removing rss.CommandsCog: {e}")
            embed.add_field(name="rss.CommandsCog", value=f"Error: {e}")
        try:
            await bot.remove_cog(rss.FeedCog(bot=bot), override=True)
            embed.add_field(name="rss.FeedCog", value="Removed successfully!")
        except Exception as e:
            print(f"Error removing rss.FeedCog: {e}")
            embed.add_field(name="rss.FeedCog", value=f"Error: {e}")
    elif extension == "user_setup":
        try:
            await bot.remove_cog(user_setup.Cog(bot=bot), override=True)
            embed.add_field(name="user_setup.Cog", value="Removed successfully!")
        except Exception as e:
            print(f"Error removing user_setup.Cog: {e}")
            embed.add_field(name="user_setup.Cog", value=f"Error: {e}")
    else:
        embed.add_field(name="Error", value="No cogs could be removed.")
    await ctx.send(embed=embed, delete_after=30.0)
    await ctx.message.delete()

@bot.command(name="ping")
async def ping(ctx: commands.Context):
    """Retrieve the bot's current latency.
    """
    latency = bot.latency()
    embed = discord.Embed(color=ctx.author.accent_color, title="Pong", description=f"The bot's current latency is {latency} seconds!")
    await ctx.send(embed=embed, delete_after=30.0)
    await ctx.message.delete()

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