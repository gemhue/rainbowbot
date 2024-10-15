import discord
import aiosqlite
from discord.ext import commands
from cogs import AutoDelete, Awards, BackgroundTasks, Profiles, Purge, RSSFeeds, UserSetup

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
            await bot.load_extension('cogs.AutoDelete')
            embed.add_field(name="cogs.AutoDelete", value="Loaded successfully!")
        except Exception as e:
            print(f"Error loading cogs.AutoDelete: {e}")
            embed.add_field(name="cogs.AutoDelete", value=f"Error: {e}")
        try:
            await bot.load_extension('cogs.Awards')
            embed.add_field(name="cogs.Awards", value="Loaded successfully!")
        except Exception as e:
            print(f"Error loading cogs.Awards: {e}")
            embed.add_field(name="cogs.Awards", value=f"Error: {e}")
        try:
            await bot.load_extension('cogs.BackgroundTasks')
            embed.add_field(name="cogs.BackgroundTasks", value="Loaded successfully!")
        except Exception as e:
            print(f"Error loading cogs.BackgroundTasks: {e}")
            embed.add_field(name="cogs.BackgroundTasks", value=f"Error: {e}")
        try:
            await bot.load_extension('cogs.Profiles')
            embed.add_field(name="cogs.Profiles", value="Loaded successfully!")
        except Exception as e:
            print(f"Error loading cogs.Profiles: {e}")
            embed.add_field(name="cogs.Profiles", value=f"Error: {e}")
        try:
            await bot.load_extension('cogs.Purge')
            embed.add_field(name="cogs.Purge", value="Loaded successfully!")
        except Exception as e:
            print(f"Error loading cogs.Purge: {e}")
            embed.add_field(name="cogs.Purge", value=f"Error: {e}")
        try:
            await bot.load_extension('cogs.RSSFeeds')
            embed.add_field(name="cogs.RSSFeeds", value="Loaded successfully!")
        except Exception as e:
            print(f"Error loading cogs.RSSFeeds: {e}")
            embed.add_field(name="cogs.RSSFeeds", value=f"Error: {e}")
        try:
            await bot.load_extension('cogs.UserSetup')
            embed.add_field(name="cogs.UserSetup", value="Loaded successfully!")
        except Exception as e:
            print(f"Error loading cogs.UserSetup: {e}")
            embed.add_field(name="cogs.UserSetup", value=f"Error: {e}")
    elif extension == "autodelete":
        try:
            await bot.load_extension('cogs.AutoDelete')
            embed.add_field(name="cogs.AutoDelete", value="Loaded successfully!")
        except Exception as e:
            print(f"Error loading cogs.AutoDelete: {e}")
            embed.add_field(name="cogs.AutoDelete", value=f"Error: {e}")
    elif extension == "award":
        try:
            await bot.load_extension('cogs.Awards')
            embed.add_field(name="cogs.Awards", value="Loaded successfully!")
        except Exception as e:
            print(f"Error loading cogs.Awards: {e}")
            embed.add_field(name="cogs.Awards", value=f"Error: {e}")
    elif extension == "background":
        try:
            await bot.load_extension('cogs.BackgroundTasks')
            embed.add_field(name="cogs.BackgroundTasks", value="Loaded successfully!")
        except Exception as e:
            print(f"Error loading cogs.BackgroundTasks: {e}")
            embed.add_field(name="cogs.BackgroundTasks", value=f"Error: {e}")
    elif extension == "profile":
        try:
            await bot.load_extension('cogs.Profiles')
            embed.add_field(name="cogs.Profiles", value="Loaded successfully!")
        except Exception as e:
            print(f"Error loading cogs.Profiles: {e}")
            embed.add_field(name="cogs.Profiles", value=f"Error: {e}")
    elif extension == "purge":
        try:
            await bot.load_extension('cogs.Purge')
            embed.add_field(name="cogs.Purge", value="Loaded successfully!")
        except Exception as e:
            print(f"Error loading cogs.Purge: {e}")
            embed.add_field(name="cogs.Purge", value=f"Error: {e}")
    elif extension == "rss":
        try:
            await bot.load_extension('cogs.RSSFeeds')
            embed.add_field(name="cogs.RSSFeeds", value="Loaded successfully!")
        except Exception as e:
            print(f"Error loading cogs.RSSFeeds: {e}")
            embed.add_field(name="cogs.RSSFeeds", value=f"Error: {e}")
    elif extension == "user_setup":
        try:
            await bot.load_extension('cogs.UserSetup')
            embed.add_field(name="cogs.UserSetup", value="Loaded successfully!")
        except Exception as e:
            print(f"Error loading cogs.UserSetup: {e}")
            embed.add_field(name="cogs.UserSetup", value=f"Error: {e}")
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
            await bot.reload_extension('cogs.AutoDelete')
            embed.add_field(name="cogs.AutoDelete", value="Reloaded successfully!")
        except Exception as e:
            print(f"Error reloading cogs.AutoDelete: {e}")
            embed.add_field(name="cogs.AutoDelete", value=f"Error: {e}")
        try:
            await bot.reload_extension('cogs.Awards')
            embed.add_field(name="cogs.Awards", value="Reloaded successfully!")
        except Exception as e:
            print(f"Error reloading cogs.Awards: {e}")
            embed.add_field(name="cogs.Awards", value=f"Error: {e}")
        try:
            await bot.reload_extension('cogs.BackgroundTasks')
            embed.add_field(name="cogs.BackgroundTasks", value="Reloaded successfully!")
        except Exception as e:
            print(f"Error reloading cogs.BackgroundTasks: {e}")
            embed.add_field(name="cogs.BackgroundTasks", value=f"Error: {e}")
        try:
            await bot.reload_extension('cogs.Profiles')
            embed.add_field(name="cogs.Profiles", value="Reloaded successfully!")
        except Exception as e:
            print(f"Error reloading cogs.Profiles: {e}")
            embed.add_field(name="cogs.Profiles", value=f"Error: {e}")
        try:
            await bot.reload_extension('cogs.Purge')
            embed.add_field(name="cogs.Purge", value="Reloaded successfully!")
        except Exception as e:
            print(f"Error reloading cogs.Purge: {e}")
            embed.add_field(name="cogs.Purge", value=f"Error: {e}")
        try:
            await bot.reload_extension('cogs.RSSFeeds')
            embed.add_field(name="cogs.RSSFeeds", value="Reloaded successfully!")
        except Exception as e:
            print(f"Error reloading cogs.RSSFeeds: {e}")
            embed.add_field(name="cogs.RSSFeeds", value=f"Error: {e}")
        try:
            await bot.reload_extension('cogs.UserSetup')
            embed.add_field(name="cogs.UserSetup", value="Reloaded successfully!")
        except Exception as e:
            print(f"Error reloading cogs.UserSetup: {e}")
            embed.add_field(name="cogs.UserSetup", value=f"Error: {e}")
    elif extension == "autodelete":
        try:
            await bot.reload_extension('cogs.AutoDelete')
            embed.add_field(name="cogs.AutoDelete", value="Reloaded successfully!")
        except Exception as e:
            print(f"Error reloading cogs.AutoDelete: {e}")
            embed.add_field(name="cogs.AutoDelete", value=f"Error: {e}")
    elif extension == "award":
        try:
            await bot.reload_extension('cogs.Awards')
            embed.add_field(name="cogs.Awards", value="Reloaded successfully!")
        except Exception as e:
            print(f"Error reloading cogs.Awards: {e}")
            embed.add_field(name="cogs.Awards", value=f"Error: {e}")
    elif extension == "background":
        try:
            await bot.reload_extension('cogs.BackgroundTasks')
            embed.add_field(name="cogs.BackgroundTasks", value="Reloaded successfully!")
        except Exception as e:
            print(f"Error reloading cogs.BackgroundTasks: {e}")
            embed.add_field(name="cogs.BackgroundTasks", value=f"Error: {e}")
    elif extension == "profile":
        try:
            await bot.reload_extension('cogs.Profiles')
            embed.add_field(name="cogs.Profiles", value="Reloaded successfully!")
        except Exception as e:
            print(f"Error reloading cogs.Profiles: {e}")
            embed.add_field(name="cogs.Profiles", value=f"Error: {e}")
    elif extension == "purge":
        try:
            await bot.reload_extension('cogs.Purge')
            embed.add_field(name="cogs.Purge", value="Reloaded successfully!")
        except Exception as e:
            print(f"Error reloading cogs.Purge: {e}")
            embed.add_field(name="cogs.Purge", value=f"Error: {e}")
    elif extension == "rss":
        try:
            await bot.reload_extension('cogs.RSSFeeds')
            embed.add_field(name="cogs.RSSFeeds", value="Reloaded successfully!")
        except Exception as e:
            print(f"Error reloading cogs.RSSFeeds: {e}")
            embed.add_field(name="cogs.RSSFeeds", value=f"Error: {e}")
    elif extension == "user_setup":
        try:
            await bot.reload_extension('cogs.UserSetup')
            embed.add_field(name="cogs.UserSetup", value="Reloaded successfully!")
        except Exception as e:
            print(f"Error reloading cogs.UserSetup: {e}")
            embed.add_field(name="cogs.UserSetup", value=f"Error: {e}")
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
            await bot.add_cog(AutoDelete.AutoDelete(bot=bot), override=True)
            embed.add_field(name="AutoDelete.AutoDelete", value="Added successfully!")
        except Exception as e:
            print(f"Error adding AutoDelete.AutoDelete: {e}")
            embed.add_field(name="AutoDelete.AutoDelete", value=f"Error: {e}")
        try:
            await bot.add_cog(Awards.Awards(bot=bot), override=True)
            embed.add_field(name="Awards.Awards", value="Added successfully!")
        except Exception as e:
            print(f"Error adding Awards.Awards: {e}")
            embed.add_field(name="Awards.Awards", value=f"Error: {e}")
        try:
            await bot.add_cog(BackgroundTasks.BackgroundTasks(bot=bot), override=True)
            embed.add_field(name="BackgroundTasks.BackgroundTasks", value="Added successfully!")
        except Exception as e:
            print(f"Error adding BackgroundTasks.BackgroundTasks: {e}")
            embed.add_field(name="BackgroundTasks.BackgroundTasks", value=f"Error: {e}")
        try:
            await bot.add_cog(Profiles.Profiles(bot=bot), override=True)
            embed.add_field(name="Profiles.Profiles", value="Added successfully!")
        except Exception as e:
            print(f"Error adding Profiles.Profiles: {e}")
            embed.add_field(name="Profiles.Profiles", value=f"Error: {e}")
        try:
            await bot.add_cog(Purge.Purge(bot=bot), override=True)
            embed.add_field(name="Purge.Purge", value="Added successfully!")
        except Exception as e:
            print(f"Error adding Purge.Purge: {e}")
            embed.add_field(name="Purge.Purge", value=f"Error: {e}")
        try:
            await bot.add_cog(RSSFeeds.RSSFeeds(bot=bot), override=True)
            embed.add_field(name="RSSFeeds.RSSFeeds", value="Added successfully!")
        except Exception as e:
            print(f"Error adding RSSFeeds.RSSFeeds: {e}")
            embed.add_field(name="RSSFeeds.RSSFeeds", value=f"Error: {e}")
        try:
            await bot.add_cog(UserSetup.UserSetup(bot=bot), override=True)
            embed.add_field(name="UserSetup.UserSetup", value="Added successfully!")
        except Exception as e:
            print(f"Error adding UserSetup.UserSetup: {e}")
            embed.add_field(name="UserSetup.UserSetup", value=f"Error: {e}")
    elif extension == "autodelete":
        try:
            await bot.add_cog(AutoDelete.AutoDelete(bot=bot), override=True)
            embed.add_field(name="AutoDelete.AutoDelete", value="Added successfully!")
        except Exception as e:
            print(f"Error adding AutoDelete.AutoDelete: {e}")
            embed.add_field(name="AutoDelete.AutoDelete", value=f"Error: {e}")
    elif extension == "award":
        try:
            await bot.add_cog(Awards.Awards(bot=bot), override=True)
            embed.add_field(name="Awards.Awards", value="Added successfully!")
        except Exception as e:
            print(f"Error adding Awards.Awards: {e}")
            embed.add_field(name="Awards.Awards", value=f"Error: {e}")
    elif extension == "background":
        try:
            await bot.add_cog(BackgroundTasks.BackgroundTasks(bot=bot), override=True)
            embed.add_field(name="BackgroundTasks.BackgroundTasks", value="Added successfully!")
        except Exception as e:
            print(f"Error adding BackgroundTasks.BackgroundTasks: {e}")
            embed.add_field(name="BackgroundTasks.BackgroundTasks", value=f"Error: {e}")
    elif extension == "profile":
        try:
            await bot.add_cog(Profiles.Profiles(bot=bot), override=True)
            embed.add_field(name="Profiles.Profiles", value="Added successfully!")
        except Exception as e:
            print(f"Error adding Profiles.Profiles: {e}")
            embed.add_field(name="Profiles.Profiles", value=f"Error: {e}")
    elif extension == "purge":
        try:
            await bot.add_cog(Purge.Purge(bot=bot), override=True)
            embed.add_field(name="Purge.Purge", value="Added successfully!")
        except Exception as e:
            print(f"Error adding Purge.Purge: {e}")
            embed.add_field(name="Purge.Purge", value=f"Error: {e}")
    elif extension == "rss":
        try:
            await bot.add_cog(RSSFeeds.RSSFeeds(bot=bot), override=True)
            embed.add_field(name="RSSFeeds.RSSFeeds", value="Added successfully!")
        except Exception as e:
            print(f"Error adding RSSFeeds.RSSFeeds: {e}")
            embed.add_field(name="RSSFeeds.RSSFeeds", value=f"Error: {e}")
    elif extension == "user_setup":
        try:
            await bot.add_cog(UserSetup.UserSetup(bot=bot), override=True)
            embed.add_field(name="UserSetup.UserSetup", value="Added successfully!")
        except Exception as e:
            print(f"Error adding UserSetup.UserSetup: {e}")
            embed.add_field(name="UserSetup.UserSetup", value=f"Error: {e}")
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
            await bot.remove_cog(AutoDelete.AutoDelete(bot=bot))
            embed.add_field(name="AutoDelete.AutoDelete", value="Removed successfully!")
        except Exception as e:
            print(f"Error removing AutoDelete.AutoDelete: {e}")
            embed.add_field(name="AutoDelete.AutoDelete", value=f"Error: {e}")
        try:
            await bot.remove_cog(Awards.Awards(bot=bot))
            embed.add_field(name="Awards.Awards", value="Removed successfully!")
        except Exception as e:
            print(f"Error removing Awards.Awards: {e}")
            embed.add_field(name="Awards.Awards", value=f"Error: {e}")
        try:
            await bot.remove_cog(BackgroundTasks.BackgroundTasks(bot=bot))
            embed.add_field(name="BackgroundTasks.BackgroundTasks", value="Removed successfully!")
        except Exception as e:
            print(f"Error removing BackgroundTasks.BackgroundTasks: {e}")
            embed.add_field(name="BackgroundTasks.BackgroundTasks", value=f"Error: {e}")
        try:
            await bot.remove_cog(Profiles.Profiles(bot=bot))
            embed.add_field(name="Profiles.Profiles", value="Removed successfully!")
        except Exception as e:
            print(f"Error removing Profiles.Profiles: {e}")
            embed.add_field(name="Profiles.Profiles", value=f"Error: {e}")
        try:
            await bot.remove_cog(Purge.Purge(bot=bot))
            embed.add_field(name="Purge.Purge", value="Removed successfully!")
        except Exception as e:
            print(f"Error removing Purge.Purge: {e}")
            embed.add_field(name="Purge.Purge", value=f"Error: {e}")
        try:
            await bot.remove_cog(RSSFeeds.RSSFeeds(bot=bot))
            embed.add_field(name="RSSFeeds.RSSFeeds", value="Removed successfully!")
        except Exception as e:
            print(f"Error removing RSSFeeds.RSSFeeds: {e}")
            embed.add_field(name="RSSFeeds.RSSFeeds", value=f"Error: {e}")
        try:
            await bot.remove_cog(UserSetup.UserSetup(bot=bot))
            embed.add_field(name="UserSetup.UserSetup", value="Removed successfully!")
        except Exception as e:
            print(f"Error removing UserSetup.UserSetup: {e}")
            embed.add_field(name="UserSetup.UserSetup", value=f"Error: {e}")
    elif extension == "autodelete":
        try:
            await bot.remove_cog(AutoDelete.AutoDelete(bot=bot))
            embed.add_field(name="AutoDelete.AutoDelete", value="Removed successfully!")
        except Exception as e:
            print(f"Error removing AutoDelete.AutoDelete: {e}")
            embed.add_field(name="AutoDelete.AutoDelete", value=f"Error: {e}")
    elif extension == "award":
        try:
            await bot.remove_cog(Awards.Awards(bot=bot))
            embed.add_field(name="Awards.Awards", value="Removed successfully!")
        except Exception as e:
            print(f"Error removing Awards.Awards: {e}")
            embed.add_field(name="Awards.Awards", value=f"Error: {e}")
    elif extension == "background":
        try:
            await bot.remove_cog(BackgroundTasks.BackgroundTasks(bot=bot))
            embed.add_field(name="BackgroundTasks.BackgroundTasks", value="Removed successfully!")
        except Exception as e:
            print(f"Error removing BackgroundTasks.BackgroundTasks: {e}")
            embed.add_field(name="BackgroundTasks.BackgroundTasks", value=f"Error: {e}")
    elif extension == "profile":
        try:
            await bot.remove_cog(Profiles.Profiles(bot=bot))
            embed.add_field(name="Profiles.Profiles", value="Removed successfully!")
        except Exception as e:
            print(f"Error removing Profiles.Profiles: {e}")
            embed.add_field(name="Profiles.Profiles", value=f"Error: {e}")
    elif extension == "purge":
        try:
            await bot.remove_cog(Purge.Purge(bot=bot))
            embed.add_field(name="Purge.Purge", value="Removed successfully!")
        except Exception as e:
            print(f"Error removing Purge.Purge: {e}")
            embed.add_field(name="Purge.Purge", value=f"Error: {e}")
    elif extension == "rss":
        try:
            await bot.remove_cog(RSSFeeds.RSSFeeds(bot=bot))
            embed.add_field(name="RSSFeeds.RSSFeeds", value="Removed successfully!")
        except Exception as e:
            print(f"Error removing RSSFeeds.RSSFeeds: {e}")
            embed.add_field(name="RSSFeeds.RSSFeeds", value=f"Error: {e}")
    elif extension == "user_setup":
        try:
            await bot.remove_cog(UserSetup.UserSetup(bot=bot))
            embed.add_field(name="UserSetup.UserSetup", value="Removed successfully!")
        except Exception as e:
            print(f"Error removing UserSetup.UserSetup: {e}")
            embed.add_field(name="UserSetup.UserSetup", value=f"Error: {e}")
    else:
        embed.add_field(name="Error", value="No cogs could be removed.")
    await ctx.send(embed=embed, delete_after=30.0)
    await ctx.message.delete()

@bot.command(name="ping")
async def ping(ctx: commands.Context):
    """Retrieve the bot's current latency.
    """
    embed = discord.Embed(color=ctx.author.accent_color, title="Pong", description=f"The bot's current latency is {bot.latency} seconds!")
    await ctx.send(embed=embed, delete_after=30.0)
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