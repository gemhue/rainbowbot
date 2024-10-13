import discord
import aiosqlite
from discord.ext import commands
from cogs import autodelete, award, background, profile, purge, rss, user_setup

bot = commands.Bot(
    command_prefix = 'rb!',
    description = "A multi-purpose Discord bot made by GitHub user gemhue.",
    intents = discord.Intents.all(),
    activity = discord.Activity(type=discord.ActivityType.listening, name="rb!help"),
    status = discord.Status.online
)

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
    await bot.add_cog(autodelete.Cog(bot), override=True)
    await bot.add_cog(award.Cog(bot), override=True)
    await bot.add_cog(background.Cog(bot), override=True)
    await bot.add_cog(profile.Cog(bot), override=True)
    await bot.add_cog(purge.Cog(bot), override=True)
    await bot.add_cog(rss.CommandsCog(bot), override=True)
    await bot.add_cog(rss.FeedCog(bot), override=True)
    await bot.add_cog(user_setup.Cog(bot), override=True)

@bot.event
async def on_ready():
    await setup(bot)
    print(f'Logged in as {bot.user}! (ID: {bot.user.id})')

token = 'token'
bot.run(token)