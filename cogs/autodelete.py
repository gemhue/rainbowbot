import discord
from discord import app_commands
from discord.ext import commands, tasks
from datetime import datetime, timedelta, timezone
from typing import Literal

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.autodel = {}
        self.autodeleter.start()
    
    def cog_unload(self):
        self.autodeleter.cancel()
    
    @commands.hybrid_group(name="autodelete", fallback="here")
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
        channel = ctx.channel
        channel_id = channel.id
        amt = float(amount)
        if interval == "Seconds":
            time = timedelta(seconds=amt)
        if interval == "Minutes":
            time = timedelta(minutes=amt)
        if interval == "Hours":
            time = timedelta(hours=amt)
        if interval == "Days":
            time = timedelta(days=amt)
        self.autodel[channel_id] = time

    @autodelete.command(name="cancel")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def cancel(self, ctx: commands.Context):
        """(Admin Only) Cancels the autodelete.
        """
        channel = ctx.channel
        channel_id = channel.id
        if channel_id in self.autodel:
            del self.autodel[channel_id]

    @tasks.loop(minutes=5.0)
    async def autodeleter(self):
        for chanel_id, time in self.autodel:
            channel = await self.bot.fetch_channel(chanel_id)
        today =  datetime.now(timezone.utc)
        timeago = today-time
        messages = [message async for message in channel.history(limit=None, before=timeago)]
        for message in messages:
            await message.delete()

def setup(bot):
	bot.add_cog(Cog(bot))