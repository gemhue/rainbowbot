import discord
import aiosqlite
from discord import app_commands
from discord.ext import commands, tasks
from datetime import datetime, timedelta, timezone
from typing import Literal

class AutoDelete(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.autodel = {}
        self.autodeleter.start()
        self.green = discord.Colour.green()
        self.red = discord.Colour.red()
        self.blurple = discord.Colour.blurple()
    
    def cog_unload(self):
        self.autodeleter.cancel()
    
    @commands.hybrid_group(name="autodelete", fallback="start")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def autodelete(self, ctx: commands.Context, amount: int, interval: Literal["Seconds", "Minutes", "Hours", "Days"]):
        """(Admin Only) Deletes all unpinned messages posted in the channel before the set amount of time ago.

        Parameters
        -----------
        amount : int
            Set the amount of time.
        interval : str
            Set the time interval.
        """
        await ctx.defer(ephemeral=True)
        try:
            amt = float(amount)
            if interval == "Seconds":
                time = timedelta(seconds=amt)
            elif interval == "Minutes":
                time = timedelta(minutes=amt)
            elif interval == "Hours":
                time = timedelta(hours=amt)
            elif interval == "Days":
                time = timedelta(days=amt)
            channel_id = ctx.channel.id
            self.autodel[channel_id] = time
            embed = discord.Embed(color=self.green, title="Success", description=f"The autodelete for the current channel has been set up. Any unpinned messages in the current channel older than **{amount} {interval}** will be automatically deleted.")
            await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)
            async with aiosqlite.connect('rainbowbot.db') as db:
                cur = await db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
                row = await cur.fetchone()
                fetched_logging = row[0]
                if fetched_logging is not None:
                    now = datetime.now(tz=timezone.utc)
                    log = discord.Embed(color=self.blurple, title="AutoDelete Log", description=f"{ctx.author.mention} has just set up AutoDelete for {ctx.channel.mention}. Any unpinned messages in the channel older than **{amount} {interval}** will be automatically deleted.", timestamp=now)
                    logging = self.bot.get_channel(fetched_logging)
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
                    await logging.send(embed=log)
                await db.commit()
                await db.close()
        except Exception as e:
            embed = discord.Embed(color=self.red, title="Error", description=f"{e}")
            await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)

    @autodelete.command(name="cancel")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def cancel(self, ctx: commands.Context):
        """(Admin Only) Cancels the autodelete in the current channel.
        """
        await ctx.defer(ephemeral=True)
        try:
            channel_id = ctx.channel.id
            if channel_id in self.autodel:
                del self.autodel[channel_id]
                embed = discord.Embed(color=self.green, title="Success", description="The autodelete for the current channel has been deleted.")
                await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)
                async with aiosqlite.connect('rainbowbot.db') as db:
                    cur = await db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
                    row = await cur.fetchone()
                    fetched_logging = row[0]
                    if fetched_logging is not None:
                        now = datetime.now(tz=timezone.utc)
                        log = discord.Embed(color=self.blurple, title="AutoDelete Log", description=f"{ctx.author.mention} has just cancelled the AutoDelete for {ctx.channel.mention}.", timestamp=now)
                        logging = self.bot.get_channel(fetched_logging)
                        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
                        await logging.send(embed=log)
                    await db.commit()
                    await db.close()
            else:
                embed = discord.Embed(color=self.red, title="Error", description="There is no autodelete set up for the current channel.")
                await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(color=self.red, title="Error", description=f"{e}")
            await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)

    @tasks.loop(minutes=5.0)
    async def autodeleter(self):
        for chanel_id, time in self.autodel:
            channel = await self.bot.fetch_channel(chanel_id)
            today = datetime.now(timezone.utc)
            timeago = today-time
            messages = [message async for message in channel.history(limit=None, before=timeago)]
            for message in messages:
                if not message.pinned:
                    await message.delete()

async def setup(bot: commands.Bot):
	await bot.add_cog(AutoDelete(bot), override=True)