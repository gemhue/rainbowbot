import discord
import traceback
from discord import app_commands
from discord.ext import commands, tasks
from datetime import datetime, timedelta, timezone
from typing import Literal

class AutoDelete(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.database
    
    def cog_load(self):
        self.autodeleter.start()
    
    def cog_unload(self):
        self.autodeleter.cancel()
    
    @commands.hybrid_group(name="autodelete", fallback="set")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def autodelete(self, ctx: commands.Context, amount: int, interval: Literal["Minutes", "Hours", "Days"]):
        """(Admin Only) Sets the messages in the current channel to be autodeleted.

        Parameters
        -----------
        amount : int
            Set the amount of time. The lowest possible frequency is 30 minutes.
        interval : str
            Set the time interval. The lowest possible frequency is 30 minutes.
        """
        await ctx.defer(ephemeral=True)
        try:
                # Add the guild to the database if necessary
                await self.db.execute("INSERT OR INGORE INTO autodelete (channel_id) VALUES ?", (ctx.channel.id,))
                await self.db.commit()

                # Update and retrieve the amount
                await self.db.execute("UPDATE autodelete SET amount = ? WHERE channel_id = ?", (amount, ctx.channel.id))
                await self.db.commit()
                cur = await self.db.execute("SELECT amount FROM autodelete WHERE channel_id = ?", (ctx.channel.id,))
                row = await cur.fetchone()
                amount = row[0]

                # Update and retrieve the interval
                await self.db.execute("UPDATE autodelete SET interval = ? WHERE channel_id = ?", (interval, ctx.channel.id))
                await self.db.commit()
                cur = await self.db.execute("SELECT interval FROM autodelete WHERE channel_id = ?", (ctx.channel.id,))
                row = await cur.fetchone()
                interval = row[0]

                # Send a message that the AutoDelete has been set
                embed = discord.Embed(color=self.bot.green, title="Success", description=f"The autodelete for {ctx.channel.mention} has been set up. Any unpinned messages older than **{amount} {interval}** will be automatically deleted on a rolling basis. Please note that if you set a time of less than 30 minutes, messages will be deleted no more frequently than every 30 minutes.")
                await ctx.send(embed=embed, ephemeral=True)

                # Send a log to the logging channel
                cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
                row = await cur.fetchone()
                fetched_logging = row[0]
                if fetched_logging is not None:
                    now = datetime.now(tz=timezone.utc)
                    log = discord.Embed(color=self.bot.blurple, title="AutoDelete Log", description=f"{ctx.author.mention} has just set up AutoDelete for {ctx.channel.mention}. Any unpinned messages in the channel older than **{amount} {interval}** will be automatically deleted.", timestamp=now)
                    logging = self.bot.get_channel(fetched_logging)
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
                    await logging.send(embed=log)

        # Send an error message if there is an issue
        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await ctx.send(embed=error, ephemeral=True)
            print(traceback.format_exc())

    @autodelete.command(name="cancel")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def cancel(self, ctx: commands.Context):
        """(Admin Only) Cancels the autodelete in the current channel.
        """
        await ctx.defer(ephemeral=True)
        try:

                await self.db.execute("DELETE FROM autodelete WHERE channel_id = ?", (ctx.channel.id,))
                await self.db.commit()

                # Confirm that the channel_id has been removed from autodelete
                cur = await self.db.execute("SELECT EXISTS(SELECT 1 FROM autodelete WHERE channel_id = ?)", (ctx.channel.id,))
                row = await cur.fetchone()
                exists = row[0]

                if exists == 0:

                    # Send a message that the AutoDelete has been cancelled
                    embed = discord.Embed(color=self.bot.green, title="Success", description=f"The autodelete for {ctx.channel.mention} has been cancelled.")
                    await ctx.send(embed=embed, ephemeral=True)

                    # Send a log to the logging channel
                    cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
                    row = await cur.fetchone()
                    fetched_logging = row[0]
                    if fetched_logging is not None:
                        now = datetime.now(tz=timezone.utc)
                        log = discord.Embed(color=self.bot.blurple, title="AutoDelete Log", description=f"{ctx.author.mention} has just cancelled AutoDelete for {ctx.channel.mention}.", timestamp=now)
                        logging = self.bot.get_channel(fetched_logging)
                        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
                        await logging.send(embed=log)

                else:

                    # Send a message that there was an issue cancelling the AutoDelete
                    error = discord.Embed(color=self.bot.red, title="Error", description="There was an issue cancelling the AutoDelete. Please try again later.")
                    await ctx.send(embed=error, ephemeral=True)

        # Send an error message if there is an issue
        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await ctx.send(embed=error, ephemeral=True)
            print(traceback.format_exc())

    # Check for messages to AutoDelete every 30 minutes
    @tasks.loop(minutes=30.0)
    async def autodeleter(self):
        try:
            ids = []
            cur = await self.db.execute("SELECT channel_id FROM autodelete")
            rows = await cur.fetchall()
            for row in rows:
                ids.append(row[0])
            for id in ids:
                channel = await self.bot.fetch_channel(id)
                if channel is not None:
                    now = datetime.now(tz=timezone.utc)
                    cur = await self.db.execute("SELECT amount FROM autodelete WHERE channel_id = ?", (id,))
                    row = await cur.fetchone()
                    amount = row[0]
                    cur = await self.db.execute("SELECT interval FROM autodelete WHERE channel_id = ?", (id,))
                    row = await cur.fetchone()
                    interval = row[0]
                    if interval == "Seconds":
                        time = timedelta(seconds=amount)
                    elif interval == "Minutes":
                        time = timedelta(minutes=amount)
                    elif interval == "Hours":
                        time = timedelta(hours=amount)
                    elif interval == "Days":
                        time = timedelta(days=amount)
                    timeago = now-time
                    messages = [m async for m in channel.history(limit=None, before=timeago)]
                    for message in messages:
                        if not message.pinned:
                            await message.delete()
        except Exception:
            traceback.print_exc()

async def setup():
    print("Setting up Cog: AutoDelete.AutoDelete")

async def teardown():
    print("Tearing down Cog: AutoDelete.AutoDelete")