import discord
from discord import app_commands
from discord.ext import commands, tasks
from datetime import datetime, timedelta, timezone
from typing import Literal

class AutoDelete(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.autodel = {}
        self.autodeleter.start()
    
    def cog_unload(self):
        self.autodeleter.cancel()
    
    @commands.hybrid_group(name="autodelete", fallback="start")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def autodelete(self, ctx: commands.Context, amount: int, interval: Literal["Seconds", "Minutes", "Hours", "Days"]):
        """(Admin Only) Deletes all messages posted in the channel before the set amount of time ago.

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
            green = discord.Colour.green()
            embed = discord.Embed(color=green, title="Success", description=f"The autodelete for the current channel has been set up. Any messages in the current channel older than **{amount} {interval}** will be automatically deleted.")
        except Exception as e:
            red = discord.Colour.red()
            embed = discord.Embed(color=red, title="Error", description=f"{e}")
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
                green = discord.Colour.green()
                embed = discord.Embed(color=green, title="Success", description="The autodelete for the current channel has been deleted.")
        except Exception as e:
            red = discord.Colour.red()
            embed = discord.Embed(color=red, title="Error", description=f"{e}")
        await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)

    @tasks.loop(minutes=5.0)
    async def autodeleter(self):
        for chanel_id, time in self.autodel:
            channel = await self.bot.fetch_channel(chanel_id)
            today = datetime.now(timezone.utc)
            timeago = today-time
            messages = [message async for message in channel.history(limit=None, before=timeago)]
            for message in messages:
                await message.delete()

async def setup(bot: commands.Bot):
	await bot.add_cog(AutoDelete(bot), override=True)