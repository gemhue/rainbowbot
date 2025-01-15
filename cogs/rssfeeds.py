import discord
import traceback
import feedparser
import aiohttp
from discord import app_commands, Webhook
from discord.ext import commands, tasks
from datetime import datetime, timezone
from time import mktime
from bs4 import BeautifulSoup

class RSSFeeds(commands.GroupCog, group_name = "rssfeed"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.database

    def cog_load(self):
        self.postrss.start()

    def cog_unload(self):
        self.postrss.cancel()

    @app_commands.command(name="setup")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup(self, interaction: discord.Interaction, webhook_url: str, rss_feed_url: str):
        """(Admin Only) Run this command to set up an RSS feed to a Webhook.

        Parameters
        -----------
        webhook_url : str
            Provide the URL for the Webhook.
        rss_feed_url : str
            Provide the URL for the RSS Feed
        """
        await interaction.response.defer()
        try:

            guild = interaction.guild
            await self.db.execute("INSERT OR IGNORE INTO webhooks (webhook_url, rss_feed_url) VALUES (?, ?)", (webhook_url, rss_feed_url))
            await self.db.commit()

            now = datetime.now(tz=timezone.utc)
            embed = discord.Embed(color=self.bot.blurple, title="RSS Feed Set", description="The RSS feed has now been set to the webhook!", timestamp=now)
            embed.add_field(name="Webhook URL", value=f"{webhook_url}", inline=False)
            embed.add_field(name="RSS Feed URL", value=f"{rss_feed_url}", inline=False)
            await interaction.followup.send(embed=embed)

            cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            fetched_logging = row[0]
            if fetched_logging is not None:
                user = interaction.user
                logging = guild.get_channel(fetched_logging)
                embed.set_author(name=user.display_name, icon_url=user.display_avatar)
                embed.set_thumbnail(url=user.display_avatar)
                await logging.send(embed=embed)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error)
            print(traceback.format_exc())
 
    async def getwebhooks(self):
        try:

            urls = []
            async with self.db.execute("SELECT webhook_url FROM webhooks") as cur:
                async for row in cur:
                    url = str(row[0])
                    if "https://discord.com/api/webhooks/" in url:
                        urls.append(url)
            return urls
        
        except Exception:
            print(traceback.format_exc())
    
    async def getfeed(self, webhook_url):
        try:

            feed = None
            await self.db.execute("INSERT OR IGNORE INTO webhooks (url) VALUES (?)", (webhook_url,))
            await self.db.commit()
            cur = await self.db.execute("SELECT rss_feed_url FROM webhooks WHERE webhook_url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                rss_url_str = str(fetched_rss_url)
                if rss_url_str.startswith("http://") or rss_url_str.startswith("https://"):
                    feed = rss_url_str
            return feed
        
        except Exception:
            print(traceback.format_exc())

    async def parsefeed(self, webhook_url, feed_url):
        try:

            feedparser.USER_AGENT = "RainbowBot/1.0 +https://rainbowbot.carrd.co/#"
            feed = feedparser.parse(feed_url)
            entries = feed.entries[:1]
            embeds = []
            for entry in entries:
                gettitle = entry.get('title', 'No Title Found')
                title = gettitle[:256]
                link = entry.get('link', feed_url)
                async with aiohttp.ClientSession() as session:
                    partialwebhook = Webhook.from_url(url=webhook_url, session=session, client=self.bot)
                    webhook = await partialwebhook.fetch()
                    channel = webhook.channel
                    embedhist = [message.embeds async for message in channel.history(limit=None)]
                    posted = False
                    for embedlist in embedhist:
                        for embed in embedlist:
                            if embed.url == link:
                                posted = True
                    if posted == False:
                        unparsed = entry.get('summary', 'No Summary Found')
                        soup = BeautifulSoup(unparsed, "html.parser")
                        getsummary = soup.get_text()
                        summary = getsummary[:256] + "..."
                        parsedtime = entry.get('published_parsed', datetime.now(timezone.utc))
                        if isinstance(parsedtime, datetime):
                            time = parsedtime
                        else:
                            time = datetime.fromtimestamp(mktime(entry.published_parsed))
                        embed = discord.Embed(color=self.bot.blurple, title=title, url=link, description=summary, timestamp=time)
                        getauthor = entry.get('author', 'No Author Found')
                        author = getauthor[:256]
                        author_url = entry.get('href', feed_url)
                        embed.set_author(name=author, url=author_url)
                        embeds.append(embed)
            return embeds
        
        except Exception:
            print(traceback.format_exc())

    @tasks.loop(minutes=5.0)
    async def postrss(self):
        try:

            urls = await self.getwebhooks()
            for url in urls:
                feed = await self.getfeed(url)
                if feed is not None:
                    embeds = await self.parsefeed(url, feed)
                    if len(embeds) > 0:
                        for embed in embeds:
                            async with aiohttp.ClientSession() as session:
                                webhook = Webhook.from_url(url=url, session=session, client=self.bot)
                                await webhook.send(embed=embed)

        except Exception:
            print(traceback.format_exc())

async def setup(bot: commands.Bot):
    print("Setting up Cog: rssfeeds.RSSFeeds")

async def teardown(bot: commands.Bot):
    print("Tearing down Cog: rssfeeds.RSSFeeds")