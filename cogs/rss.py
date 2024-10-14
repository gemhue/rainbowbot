import discord
from discord import app_commands, Webhook
from discord.ext import commands, tasks
import aiosqlite
from typing import Literal
import feedparser
import aiohttp
from datetime import datetime, timezone
from time import mktime
from bs4 import BeautifulSoup

class CommandsCog(commands.Cog):
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

class FeedCog(commands.Cog):
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
                allfeeds["feed1"] = feed1
            feed2 = {}
            cur = await db.execute("SELECT rss_url_2 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                feed2["url"] = fetched_rss_url
                allfeeds["feed2"] = feed2
            feed3 = {}
            cur = await db.execute("SELECT rss_url_3 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                feed3["url"] = fetched_rss_url
                allfeeds["feed3"] = feed3
            feed4 = {}
            cur = await db.execute("SELECT rss_url_4 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                feed4["url"] = fetched_rss_url
                allfeeds["feed4"] = feed4
            feed5 = {}
            cur = await db.execute("SELECT rss_url_5 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                feed5["url"] = fetched_rss_url
                allfeeds["feed5"] = feed5
            feed6 = {}
            cur = await db.execute("SELECT rss_url_6 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                feed6["url"] = fetched_rss_url
                allfeeds["feed6"] = feed6
            feed7 = {}
            cur = await db.execute("SELECT rss_url_7 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                feed7["url"] = fetched_rss_url
                allfeeds["feed7"] = feed7
            feed8 = {}
            cur = await db.execute("SELECT rss_url_8 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                feed8["url"] = fetched_rss_url
                allfeeds["feed8"] = feed8
            feed9 = {}
            cur = await db.execute("SELECT rss_url_9 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                feed9["url"] = fetched_rss_url
                allfeeds["feed9"] = feed9
            feed10 = {}
            cur = await db.execute("SELECT rss_url_10 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                feed10["url"] = fetched_rss_url
                allfeeds["feed10"] = feed10
        return allfeeds

    async def parsefeed(self, webhook_url, feed_url):
        feedparser.USER_AGENT = "RainbowBot/1.0 +https://rainbowbot.carrd.co/#"
        feed = feedparser.parse(feed_url)
        entries = feed.entries[0]
        embeds = []
        for entry in entries:
            color = discord.Colour.blurple()
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
                    embed = discord.Embed(colour=color, title=title, url=link, description=summary, timestamp=time)
                    getauthor = entry.get('author', 'No Author Found')
                    author = getauthor[:256]
                    author_url = entry.get('href', feed_url)
                    embed.set_author(name=author, url=author_url)
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
                        if len(embeds) > 0:
                            for embed in embeds:
                                async with aiohttp.ClientSession() as session:
                                    webhook = Webhook.from_url(url=url, session=session, client=self.bot)
                                    await webhook.send(embed=embed)
            await db.commit()
            await db.close()

async def setup(bot):
    await bot.add_cog(CommandsCog(bot))
    await bot.add_cog(FeedCog(bot))