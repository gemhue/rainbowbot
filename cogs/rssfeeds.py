import discord
import traceback
import feedparser
import aiohttp
from discord import app_commands, Webhook
from discord.ext import commands, tasks
from typing import Literal
from datetime import datetime, timezone
from time import mktime
from bs4 import BeautifulSoup

class RSSFeeds(commands.GroupCog, group_name = "rss"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.database

    def cog_load(self):
        self.postrss.start()

    def cog_unload(self):
        self.postrss.cancel()

    @app_commands.command(name="webhook_setup")
    @app_commands.checks.has_permissions(administrator=True)
    async def webhook_setup(self, interaction: discord.Interaction, webhook_nickname: str, webhook_url: str):
        """(Admin Only) Run this command to set up a Webhook for posting RSS feeds.

        Parameters
        -----------
        webhook_nickname : str
            Provide a nickname for the Webhook.
        webhook_url : str
            Provide the URL for the Webhook.
        """
        await interaction.response.defer()
        try:

            guild = interaction.guild
            await self.db.execute("INSERT OR IGNORE INTO webhooks (url, nickname, guild_id) VALUES (?, ?, ?)", (webhook_url, webhook_nickname, guild.id))
            await self.db.commit()

            now = datetime.now(tz=timezone.utc)
            embed = discord.Embed(color=self.bot.blurple, title="Webhook Set", description="This webhook has now been set up!", timestamp=now)
            embed.add_field(name="Webhook Nickname", value=f"{webhook_nickname}", inline=False)
            embed.add_field(name="Webhook URL", value=f"{webhook_url}", inline=False)
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

    @app_commands.command(name="webhook_check")
    @app_commands.checks.has_permissions(administrator=True)
    async def webhook_check(self, interaction: discord.Interaction, webhook_nickname: str):
        """(Admin Only) Run this command to check what RSS feeds are set to the webhook.

        Parameters
        -----------
        webhook_nickname : str
            Provide the nickname for the webhook that you would like to check.
        """
        await interaction.response.defer()
        try:

            guild = interaction.guild
            cur = await self.db.execute("SELECT url FROM webhooks WHERE nickname = ? AND guild_id = ?", (webhook_nickname, guild.id))
            row = cur.fetchone()
            webhook_url = row[0]

            if webhook_url is not None:

                now = datetime.now(tz=timezone.utc)
                embed = discord.Embed(color=self.bot.blurple, title="Webhook Check", description=f"**Webhook URL**: {webhook_url}", timestamp=now)

                cur = await self.db.execute("SELECT rss_url_1 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is not None:
                    embed.add_field(name="Position Zero", value=f"**RSS URL**: {fetched_rss_url}", inline=False)
                else:
                    embed.add_field(name="Position Zero", value="Empty", inline=False)

                cur = await self.db.execute("SELECT rss_url_2 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is not None:
                    embed.add_field(name="Position One", value=f"**RSS URL**: {fetched_rss_url}", inline=False)
                else:
                    embed.add_field(name="Position One", value="Empty", inline=False)

                cur = await self.db.execute("SELECT rss_url_3 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is not None:
                    embed.add_field(name="Position Two", value=f"**RSS URL**: {fetched_rss_url}", inline=False)
                else:
                    embed.add_field(name="Position Two", value="Empty", inline=False)

                cur = await self.db.execute("SELECT rss_url_4 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is not None:
                    embed.add_field(name="Position Three", value=f"**RSS URL**: {fetched_rss_url}", inline=False)
                else:
                    embed.add_field(name="Position Three", value="Empty", inline=False)

                cur = await self.db.execute("SELECT rss_url_5 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is not None:
                    embed.add_field(name="Position Four", value=f"**RSS URL**: {fetched_rss_url}", inline=False)
                else:
                    embed.add_field(name="Position Four", value="Empty", inline=False)

                cur = await self.db.execute("SELECT rss_url_6 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is not None:
                    embed.add_field(name="Position Five", value=f"**RSS URL**: {fetched_rss_url}", inline=False)
                else:
                    embed.add_field(name="Position Five", value="Empty", inline=False)

                cur = await self.db.execute("SELECT rss_url_7 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is not None:
                    embed.add_field(name="Position Six", value=f"**RSS URL**: {fetched_rss_url}", inline=False)
                else:
                    embed.add_field(name="Position Six", value="Empty", inline=False)

                cur = await self.db.execute("SELECT rss_url_8 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is not None:
                    embed.add_field(name="Position Seven", value=f"**RSS URL**: {fetched_rss_url}", inline=False)
                else:
                    embed.add_field(name="Position Seven", value="Empty", inline=False)

                cur = await self.db.execute("SELECT rss_url_9 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is not None:
                    embed.add_field(name="Position Eight", value=f"**RSS URL**: {fetched_rss_url}", inline=False)
                else:
                    embed.add_field(name="Position Eight", value="Empty", inline=False)

                cur = await self.db.execute("SELECT rss_url_10 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is not None:
                    embed.add_field(name="Position Nine", value=f"**RSS URL**: {fetched_rss_url}", inline=False)
                else:
                    embed.add_field(name="Position Nine", value="Empty", inline=False)

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
            
            else:
                error = discord.Embed(color=self.bot.red, title="Error", description="No webhook could be found with the provided nickname. Please try again.")
                await interaction.followup.send(embed=error)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error)
            print(traceback.format_exc())

    @app_commands.command(name="webhook_clear")
    @app_commands.checks.has_permissions(administrator=True)
    async def webhook_clear(self, interaction: discord.Interaction, webhook_nickname: str):
        """(Admin Only) Run this command to clear all RSS feeds assigned to a webhook.

        Parameters
        -----------
        webhook_nickname : str
            Provide the nickname for the webhook that you would like to clear.
        """
        await interaction.response.defer()
        try:

            guild = interaction.guild
            cur = await self.db.execute("SELECT url FROM webhooks WHERE nickname = ? AND guild_id = ?", (webhook_nickname, guild.id))
            row = cur.fetchone()
            webhook_url = row[0]

            if webhook_url is not None:

                now = datetime.now(tz=timezone.utc)
                embed = discord.Embed(color=self.bot.blurple, title="Webhook Clear", description=f"**Webhook URL**: {webhook_url}", timestamp=now)

                cur = await self.db.execute("SELECT rss_url_1 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is None:
                    embed.add_field(name="Position Zero", value="Cleared!", inline=False)
                else:
                    embed.add_field(name="Position Zero Error", value=f"{fetched_rss_url}", inline=False)

                cur = await self.db.execute("SELECT rss_url_2 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is None:
                    embed.add_field(name="Position One", value="Cleared!", inline=False)
                else:
                    embed.add_field(name="Position One Error", value=f"{fetched_rss_url}", inline=False)

                cur = await self.db.execute("SELECT rss_url_3 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is None:
                    embed.add_field(name="Position Two", value="Cleared!", inline=False)
                else:
                    embed.add_field(name="Position Two Error", value=f"{fetched_rss_url}", inline=False)

                cur = await self.db.execute("SELECT rss_url_4 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is None:
                    embed.add_field(name="Position Three", value="Cleared!", inline=False)
                else:
                    embed.add_field(name="Position Three Error", value=f"{fetched_rss_url}", inline=False)

                cur = await self.db.execute("SELECT rss_url_5 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is None:
                    embed.add_field(name="Position Four", value="Cleared", inline=False)
                else:
                    embed.add_field(name="Position Four Error", value=f"{fetched_rss_url}", inline=False)

                cur = await self.db.execute("SELECT rss_url_6 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is None:
                    embed.add_field(name="Position Five", value="Cleared!", inline=False)
                else:
                    embed.add_field(name="Position Five Error", value=f"{fetched_rss_url}", inline=False)

                cur = await self.db.execute("SELECT rss_url_7 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is None:
                    embed.add_field(name="Position Six", value="Cleared!", inline=False)
                else:
                    embed.add_field(name="Position Six Error", value=f"{fetched_rss_url}", inline=False)

                cur = await self.db.execute("SELECT rss_url_8 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is None:
                    embed.add_field(name="Position Seven", value="Cleared!", inline=False)
                else:
                    embed.add_field(name="Position Seven Error", value=f"{fetched_rss_url}", inline=False)

                cur = await self.db.execute("SELECT rss_url_9 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is None:
                    embed.add_field(name="Position Eight", value="Cleared!", inline=False)
                else:
                    embed.add_field(name="Position Eight Error", value=f"{fetched_rss_url}", inline=False)

                cur = await self.db.execute("SELECT rss_url_10 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is None:
                    embed.add_field(name="Position Nine", value="Cleared!", inline=False)
                else:
                    embed.add_field(name="Position Nine Error", value=f"{fetched_rss_url}", inline=False)

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

            else:
                error = discord.Embed(color=self.bot.red, title="Error", description="No webhook could be found with the provided nickname. Please try again.")
                await interaction.followup.send(embed=error)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error)
            print(traceback.format_exc())

    @app_commands.command(name="webhook_delete")
    @app_commands.checks.has_permissions(administrator=True)
    async def webhook_delete(self, interaction: discord.Interaction, webhook_nickname: str):
        """(Admin Only) Run this command to delete a webhook from the database.

        Parameters
        -----------
        webhook_nickname : str
            Provide the nickname for the webhook that you would like to delete.
        """
        await interaction.response.defer()
        try:

            guild = interaction.guild
            cur = await self.db.execute("SELECT url FROM webhooks WHERE nickname = ? AND guild_id = ?", (webhook_nickname, guild.id))
            row = cur.fetchone()
            webhook_url = row[0]

            if webhook_url is not None:

                now = datetime.now(tz=timezone.utc)
                embed = discord.Embed(color=self.bot.blurple, title="Webhook Delete", description=f"**Webhook URL**: {webhook_url}", timestamp=now)

                await self.db.execute("DELETE FROM webhooks WHERE url = ?", (webhook_url,))

                cur = await self.db.execute("SELECT nickname FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_nick = row[0]
                if fetched_nick is None:
                    embed.add_field(name="Success", value="The webhook was successfully deleted!", inline=False)
                else:
                    embed.add_field(name="Error", value=f"There was an error deleting the webhook. Please try again later.", inline=False)
                
                await interaction.followup.send(embed=embed)

            else:
                error = discord.Embed(color=self.bot.red, title="Error", description="No webhook could be found with the provided nickname. Please try again.")
                await interaction.followup.send(embed=error)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error)
            print(traceback.format_exc())

    @app_commands.command(name="feed_setup")
    @app_commands.checks.has_permissions(administrator=True)
    async def feed_setup(self, interaction: discord.Interaction, webhook_nickname: str, rss_feed_url: str):
        """(Admin Only) Run this command to set an RSS Feed. All fields are required.

        Parameters
        -----------
        webhook_nickname : str
            Provide the nickname for the webhook that you are assigning the RSS feed to.
        rss_feed_url : str
            Provide the URL for the RSS feed that you are assigning to the webhook.
        """
        await interaction.response.defer()
        try:

            guild = interaction.guild
            cur = await self.db.execute("SELECT url FROM webhooks WHERE nickname = ? AND guild_id = ?", (webhook_nickname, guild.id))
            row = cur.fetchone()
            webhook_url = row[0]

            if webhook_url is not None:

                now = datetime.now(tz=timezone.utc)
                embed = discord.Embed(color=self.bot.blurple, title="RSS Feed Setup", timestamp=now)

                cur = await self.db.execute("SELECT rss_url_1 FROM webhooks WHERE url = ?", (webhook_url,))
                row = await cur.fetchone()
                fetched_rss_url = row[0]
                if fetched_rss_url is None:
                    await self.db.execute("UPDATE webhooks SET rss_url_1 = ? WHERE url = ?", (rss_feed_url, webhook_url))
                    await self.db.commit()
                    embed.add_field(name="Success", value="The RSS feed has been set to the webhook at **position one**!")
                    embed.add_field(name="Webhook URL", value=f"{webhook_url}", inline=False)
                    embed.add_field(name="RSS Feed URL", value=f"{rss_feed_url}", inline=False)
                else:
                    cur = await self.db.execute("SELECT rss_url_2 FROM webhooks WHERE url = ?", (webhook_url,))
                    row = await cur.fetchone()
                    fetched_rss_url = row[0]
                    if fetched_rss_url is None:
                        await self.db.execute("UPDATE webhooks SET rss_url_2 = ? WHERE url = ?", (rss_feed_url, webhook_url))
                        await self.db.commit()
                        embed.add_field(name="Success", value="The RSS feed has been set to the webhook at **position two**!")
                        embed.add_field(name="Webhook URL", value=f"{webhook_url}", inline=False)
                        embed.add_field(name="RSS Feed URL", value=f"{rss_feed_url}", inline=False)
                    else:
                        cur = await self.db.execute("SELECT rss_url_3 FROM webhooks WHERE url = ?", (webhook_url,))
                        row = await cur.fetchone()
                        fetched_rss_url = row[0]
                        if fetched_rss_url is None:
                            await self.db.execute("UPDATE webhooks SET rss_url_3 = ? WHERE url = ?", (rss_feed_url, webhook_url))
                            await self.db.commit()
                            embed.add_field(name="Success", value="The RSS feed has been set to the webhook at **position three**!")
                            embed.add_field(name="Webhook URL", value=f"{webhook_url}", inline=False)
                            embed.add_field(name="RSS Feed URL", value=f"{rss_feed_url}", inline=False)
                        else:
                            cur = await self.db.execute("SELECT rss_url_4 FROM webhooks WHERE url = ?", (webhook_url,))
                            row = await cur.fetchone()
                            fetched_rss_url = row[0]
                            if fetched_rss_url is None:
                                await self.db.execute("UPDATE webhooks SET rss_url_4 = ? WHERE url = ?", (rss_feed_url, webhook_url))
                                await self.db.commit()
                                embed.add_field(name="Success", value="The RSS feed has been set to the webhook at **position four**!")
                                embed.add_field(name="Webhook URL", value=f"{webhook_url}", inline=False)
                                embed.add_field(name="RSS Feed URL", value=f"{rss_feed_url}", inline=False)
                            else:
                                cur = await self.db.execute("SELECT rss_url_5 FROM webhooks WHERE url = ?", (webhook_url,))
                                row = await cur.fetchone()
                                fetched_rss_url = row[0]
                                if fetched_rss_url is None:
                                    await self.db.execute("UPDATE webhooks SET rss_url_5 = ? WHERE url = ?", (rss_feed_url, webhook_url))
                                    await self.db.commit()
                                    embed.add_field(name="Success", value="The RSS feed has been set to the webhook at **position five**!")
                                    embed.add_field(name="Webhook URL", value=f"{webhook_url}", inline=False)
                                    embed.add_field(name="RSS Feed URL", value=f"{rss_feed_url}", inline=False)
                                else:
                                    cur = await self.db.execute("SELECT rss_url_6 FROM webhooks WHERE url = ?", (webhook_url,))
                                    row = await cur.fetchone()
                                    fetched_rss_url = row[0]
                                    if fetched_rss_url is None:
                                        await self.db.execute("UPDATE webhooks SET rss_url_6 = ? WHERE url = ?", (rss_feed_url, webhook_url))
                                        await self.db.commit()
                                        embed.add_field(name="Success", value="The RSS feed has been set to the webhook at **position six**!")
                                        embed.add_field(name="Webhook URL", value=f"{webhook_url}", inline=False)
                                        embed.add_field(name="RSS Feed URL", value=f"{rss_feed_url}", inline=False)
                                    else:
                                        cur = await self.db.execute("SELECT rss_url_7 FROM webhooks WHERE url = ?", (webhook_url,))
                                        row = await cur.fetchone()
                                        fetched_rss_url = row[0]
                                        if fetched_rss_url is None:
                                            await self.db.execute("UPDATE webhooks SET rss_url_7 = ? WHERE url = ?", (rss_feed_url, webhook_url))
                                            await self.db.commit()
                                            embed.add_field(name="Success", value="The RSS feed has been set to the webhook at **position seven**!")
                                            embed.add_field(name="Webhook URL", value=f"{webhook_url}", inline=False)
                                            embed.add_field(name="RSS Feed URL", value=f"{rss_feed_url}", inline=False)
                                        else:
                                            cur = await self.db.execute("SELECT rss_url_8 FROM webhooks WHERE url = ?", (webhook_url,))
                                            row = await cur.fetchone()
                                            fetched_rss_url = row[0]
                                            if fetched_rss_url is None:
                                                await self.db.execute("UPDATE webhooks SET rss_url_8 = ? WHERE url = ?", (rss_feed_url, webhook_url))
                                                await self.db.commit()
                                                embed.add_field(name="Success", value="The RSS feed has been set to the webhook at **position eight**!")
                                                embed.add_field(name="Webhook URL", value=f"{webhook_url}", inline=False)
                                                embed.add_field(name="RSS Feed URL", value=f"{rss_feed_url}", inline=False)
                                            else:
                                                cur = await self.db.execute("SELECT rss_url_9 FROM webhooks WHERE url = ?", (webhook_url,))
                                                row = await cur.fetchone()
                                                fetched_rss_url = row[0]
                                                if fetched_rss_url is None:
                                                    await self.db.execute("UPDATE webhooks SET rss_url_9 = ? WHERE url = ?", (rss_feed_url, webhook_url))
                                                    await self.db.commit()
                                                    embed.add_field(name="Success", value="The RSS feed has been set to the webhook at **position nine**!")
                                                    embed.add_field(name="Webhook URL", value=f"{webhook_url}", inline=False)
                                                    embed.add_field(name="RSS Feed URL", value=f"{rss_feed_url}", inline=False)
                                                else:
                                                    cur = await self.db.execute("SELECT rss_url_10 FROM webhooks WHERE url = ?", (webhook_url,))
                                                    row = await cur.fetchone()
                                                    fetched_rss_url = row[0]
                                                    if fetched_rss_url is None:
                                                        await self.db.execute("UPDATE webhooks SET rss_url_10 = ? WHERE url = ?", (rss_feed_url, webhook_url))
                                                        await self.db.commit()
                                                        embed.add_field(name="Success", value="The RSS feed has been set to the webhook at **position ten**!")
                                                        embed.add_field(name="Webhook URL", value=f"{webhook_url}", inline=False)
                                                        embed.add_field(name="RSS Feed URL", value=f"{rss_feed_url}", inline=False)
                                                    else:
                                                        embed.add_field(name="Error", value="This webhook is already associated with 10 RSS feeds. Please use `/rss feed_clear` or `/rss webhook_clear` to remove one or all RSS feeds from this webhook.")
                
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
            
            else:
                error = discord.Embed(color=self.bot.red, title="Error", description="No webhook could be found with the provided nickname. Please try again.")
                await interaction.followup.send(embed=error)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error)
            print(traceback.format_exc())

    @app_commands.command(name="feed_clear")
    @app_commands.checks.has_permissions(administrator=True)
    async def feed_clear(self, interaction: discord.Interaction, webhook_nickname: str, rss_feed_position: Literal[0,1,2,3,4,5,6,7,8,9]):
        """(Admin Only) Run this command to clear one RSS feed from a webhook.

        Parameters
        -----------
        webhook_nickname : str
            Provide the nickname for the webhook that contains the RSS feed to be cleared.
        rss_feed_position : int
            Provide the position (0-9) on the webhook where the RSS feed to be cleared is located.
        """
        await interaction.response.defer()
        try:

            guild = interaction.guild
            cur = await self.db.execute("SELECT url FROM webhooks WHERE nickname = ? AND guild_id = ?", (webhook_url, guild.id))
            row = cur.fetchone()
            webhook_url = row[0]

            if webhook_url is not None:

                now = datetime.now(tz=timezone.utc)
                embed = discord.Embed(color=self.bot.blurple, title="Webhook Update", description=f"**Webhook URL**: {webhook_url}", timestamp=now)

                if rss_feed_position == 0:
                    await self.db.execute("INSERT OR REPLACE INTO webhooks (rss_url_1) VALUES (NULL) WHERE url = ?", (webhook_url,))
                    await self.db.commit()
                    cur = await self.db.execute("SELECT rss_url_1 FROM webhooks WHERE url = ?", (webhook_url,))
                    row = await cur.fetchone()
                    fetched_rss_url = row[0]
                    if fetched_rss_url is None:
                        embed.add_field(name="Success", value=f"Position zero cleared!", inline=False)
                    else:
                        embed.add_field(name="Error", value=f"Position zero **not** cleared!", inline=False)

                elif rss_feed_position == 1:
                    await self.db.execute("INSERT OR REPLACE INTO webhooks (rss_url_2) VALUES (NULL) WHERE url = ?", (webhook_url,))
                    await self.db.commit()
                    cur = await self.db.execute("SELECT rss_url_2 FROM webhooks WHERE url = ?", (webhook_url,))
                    row = await cur.fetchone()
                    fetched_rss_url = row[0]
                    if fetched_rss_url is None:
                        embed.add_field(name="Success", value=f"Position one cleared!", inline=False)
                    else:
                        embed.add_field(name="Error", value=f"Position one **not** cleared!", inline=False)

                elif rss_feed_position == 2:
                    await self.db.execute("INSERT OR REPLACE INTO webhooks (rss_url_3) VALUES (NULL) WHERE url = ?", (webhook_url,))
                    await self.db.commit()
                    cur = await self.db.execute("SELECT rss_url_3 FROM webhooks WHERE url = ?", (webhook_url,))
                    row = await cur.fetchone()
                    fetched_rss_url = row[0]
                    if fetched_rss_url is None:
                        embed.add_field(name="Success", value=f"Position two cleared!", inline=False)
                    else:
                        embed.add_field(name="Error", value=f"Position two **not** cleared!", inline=False)

                elif rss_feed_position == 3:
                    await self.db.execute("INSERT OR REPLACE INTO webhooks (rss_url_4) VALUES (NULL) WHERE url = ?", (webhook_url,))
                    await self.db.commit()
                    cur = await self.db.execute("SELECT rss_url_4 FROM webhooks WHERE url = ?", (webhook_url,))
                    row = await cur.fetchone()
                    fetched_rss_url = row[0]
                    if fetched_rss_url is None:
                        embed.add_field(name="Success", value=f"Position three cleared!", inline=False)
                    else:
                        embed.add_field(name="Error", value=f"Position three **not** cleared!", inline=False)

                elif rss_feed_position == 4:
                    await self.db.execute("INSERT OR REPLACE INTO webhooks (rss_url_5) VALUES (NULL) WHERE url = ?", (webhook_url,))
                    await self.db.commit()
                    cur = await self.db.execute("SELECT rss_url_5 FROM webhooks WHERE url = ?", (webhook_url,))
                    row = await cur.fetchone()
                    fetched_rss_url = row[0]
                    if fetched_rss_url is None:
                        embed.add_field(name="Success", value=f"Position four cleared!", inline=False)
                    else:
                        embed.add_field(name="Error", value=f"Position four **not** cleared!", inline=False)

                elif rss_feed_position == 5:
                    await self.db.execute("INSERT OR REPLACE INTO webhooks (rss_url_6) VALUES (NULL) WHERE url = ?", (webhook_url,))
                    await self.db.commit()
                    cur = await self.db.execute("SELECT rss_url_6 FROM webhooks WHERE url = ?", (webhook_url,))
                    row = await cur.fetchone()
                    fetched_rss_url = row[0]
                    if fetched_rss_url is None:
                        embed.add_field(name="Success", value=f"Position five cleared!", inline=False)
                    else:
                        embed.add_field(name="Error", value=f"Position five **not** cleared!", inline=False)

                elif rss_feed_position == 6:
                    await self.db.execute("INSERT OR REPLACE INTO webhooks (rss_url_7) VALUES (NULL) WHERE url = ?", (webhook_url,))
                    await self.db.commit()
                    cur = await self.db.execute("SELECT rss_url_7 FROM webhooks WHERE url = ?", (webhook_url,))
                    row = await cur.fetchone()
                    fetched_rss_url = row[0]
                    if fetched_rss_url is None:
                        embed.add_field(name="Success", value=f"Position six cleared!", inline=False)
                    else:
                        embed.add_field(name="Error", value=f"Position six **not** cleared!", inline=False)

                elif rss_feed_position == 7:
                    await self.db.execute("INSERT OR REPLACE INTO webhooks (rss_url_8) VALUES (NULL) WHERE url = ?", (webhook_url,))
                    await self.db.commit()
                    cur = await self.db.execute("SELECT rss_url_8 FROM webhooks WHERE url = ?", (webhook_url,))
                    row = await cur.fetchone()
                    fetched_rss_url = row[0]
                    if fetched_rss_url is None:
                        embed.add_field(name="Success", value=f"Position seven cleared!", inline=False)
                    else:
                        embed.add_field(name="Error", value=f"Position seven **not** cleared!", inline=False)

                elif rss_feed_position == 8:
                    await self.db.execute("INSERT OR REPLACE INTO webhooks (rss_url_9) VALUES (NULL) WHERE url = ?", (webhook_url,))
                    await self.db.commit()
                    cur = await self.db.execute("SELECT rss_url_9 FROM webhooks WHERE url = ?", (webhook_url,))
                    row = await cur.fetchone()
                    fetched_rss_url = row[0]
                    if fetched_rss_url is None:
                        embed.add_field(name="Success", value=f"Position eight cleared!", inline=False)
                    else:
                        embed.add_field(name="Error", value=f"Position eight **not** cleared!", inline=False)

                elif rss_feed_position == 9:
                    await self.db.execute("INSERT OR REPLACE INTO webhooks (rss_url_10) VALUES (NULL) WHERE url = ?", (webhook_url,))
                    await self.db.commit()
                    cur = await self.db.execute("SELECT rss_url_10 FROM webhooks WHERE url = ?", (webhook_url,))
                    row = await cur.fetchone()
                    fetched_rss_url = row[0]
                    if fetched_rss_url is None:
                        embed.add_field(name="Success", value=f"Position nine cleared!", inline=False)
                    else:
                        embed.add_field(name="Error", value=f"Position nine **not** cleared!", inline=False)
                
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

            else:
                error = discord.Embed(color=self.bot.red, title="Error", description="No webhook could be found with the provided nickname. Please try again.")
                await interaction.followup.send(embed=error)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error)
            print(traceback.format_exc())
 
    async def getwebhooks(self):
        try:

            urls = []
            async with self.db.execute("SELECT url FROM webhooks") as cur:
                async for row in cur:
                    url = str(row[0])
                    if "https://discord.com/api/webhooks/" in url:
                        urls.append(url)
            return urls
        
        except Exception:
            print(traceback.format_exc())
    
    async def getfeeds(self, webhook_url):
        try:

            allfeeds = {}
            await self.db.execute("INSERT OR IGNORE INTO webhooks (url) VALUES (?)", (webhook_url,))
            await self.db.commit()
            feed1 = {}
            cur = await self.db.execute("SELECT rss_url_1 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                feed1["url"] = fetched_rss_url
                allfeeds["feed1"] = feed1
            feed2 = {}
            cur = await self.db.execute("SELECT rss_url_2 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                feed2["url"] = fetched_rss_url
                allfeeds["feed2"] = feed2
            feed3 = {}
            cur = await self.db.execute("SELECT rss_url_3 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                feed3["url"] = fetched_rss_url
                allfeeds["feed3"] = feed3
            feed4 = {}
            cur = await self.db.execute("SELECT rss_url_4 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                feed4["url"] = fetched_rss_url
                allfeeds["feed4"] = feed4
            feed5 = {}
            cur = await self.db.execute("SELECT rss_url_5 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                feed5["url"] = fetched_rss_url
                allfeeds["feed5"] = feed5
            feed6 = {}
            cur = await self.db.execute("SELECT rss_url_6 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                feed6["url"] = fetched_rss_url
                allfeeds["feed6"] = feed6
            feed7 = {}
            cur = await self.db.execute("SELECT rss_url_7 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                feed7["url"] = fetched_rss_url
                allfeeds["feed7"] = feed7
            feed8 = {}
            cur = await self.db.execute("SELECT rss_url_8 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                feed8["url"] = fetched_rss_url
                allfeeds["feed8"] = feed8
            feed9 = {}
            cur = await self.db.execute("SELECT rss_url_9 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                feed9["url"] = fetched_rss_url
                allfeeds["feed9"] = feed9
            feed10 = {}
            cur = await self.db.execute("SELECT rss_url_10 FROM webhooks WHERE url = ?", (webhook_url,))
            row = await cur.fetchone()
            fetched_rss_url = row[0]
            if fetched_rss_url is not None:
                feed10["url"] = fetched_rss_url
                allfeeds["feed10"] = feed10
            return allfeeds
        
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

        except Exception:
            print(traceback.format_exc())

async def setup(bot: commands.Bot):
    print("Setting up Cog: rssfeeds.RSSFeeds")

async def teardown(bot: commands.Bot):
    print("Tearing down Cog: rssfeeds.RSSFeeds")