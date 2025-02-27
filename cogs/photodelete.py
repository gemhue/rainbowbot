import discord
import aiosqlite
import traceback
from discord.ext import commands
from datetime import datetime, timedelta, timezone

black_list = []

async def blacklist(member: discord.Member):
    black_list.append(member)

class ViewButtons(discord.ui.View):
    def __init__(self, *, bot: commands.Bot, user: discord.Member):
        super().__init__(timeout=None)
        self.bot = bot
        self.user = user
        self.value = None
    
    @discord.ui.button(label=f"Keep Media", style=discord.ButtonStyle.green, emoji="✅", row=0)
    async def keep(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        if interaction.user == self.user:
            self.value = "keep"
            self.stop()
        else:
            error = discord.Embed(color=self.bot.red, title="Error", description="You can't interact with this view!")
            error_msg = await interaction.followup.send(ephemeral=True, embed=error, wait=True)
            await error_msg.delete(delay=5.0)
    
    @discord.ui.button(label="Delete After 1 Hour", style=discord.ButtonStyle.blurple, emoji="🗑️", row=1)
    async def one_hour(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = "hour"
            self.stop()
        else:
            error = discord.Embed(color=self.bot.red, title="Error", description="You can't interact with this view!")
            error_msg = await interaction.followup.send(ephemeral=True, embed=error, wait=True)
            await error_msg.delete(delay=5.0)
    
    @discord.ui.button(label="Delete After 1 Day", style=discord.ButtonStyle.blurple, emoji="🗑️", row=1)
    async def one_day(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = "day"
            self.stop()
        else:
            error = discord.Embed(color=self.bot.red, title="Error", description="You can't interact with this view!")
            error_msg = await interaction.followup.send(ephemeral=True, embed=error, wait=True)
            await error_msg.delete(delay=5.0)
    
    @discord.ui.button(label="Delete After 1 Week", style=discord.ButtonStyle.blurple, emoji="🗑️", row=1)
    async def one_week(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = "week"
            self.stop()
        else:
            error = discord.Embed(color=self.bot.red, title="Error", description="You can't interact with this view!")
            error_msg = await interaction.followup.send(ephemeral=True, embed=error, wait=True)
            await error_msg.delete(delay=5.0)
    
    @discord.ui.button(label="Don't Ask Again", style=discord.ButtonStyle.blurple, emoji="❌", row=2)
    async def blacklist(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = "blacklist"
            self.stop()
        else:
            error = discord.Embed(color=self.bot.red, title="Error", description="You can't interact with this view!")
            error_msg = await interaction.followup.send(ephemeral=True, embed=error, wait=True)
            await error_msg.delete(delay=5.0)

class PhotoDelete(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        if isinstance(bot.database, aiosqlite.Connection):
            self.db = bot.database
    
    @commands.Cog.listener(name="on_message")
    async def on_message(self, message: discord.Message):
        if message.attachments:

            if message.attachments[0].content_type.startswith("image"):
                try:

                    user = message.author
                    channel = message.channel

                    view = ViewButtons(bot=self.bot, user=user)
                    embed = discord.Embed(
                        color=self.bot.blurple,
                        title="Schedule Photo Deletion",
                        description=f"Hello, {user.mention}! I see that you've just posted a photo. If you like, I can delete the photo after a chosen period of time. Use the bottons below to indicate if you would like me to keep the photo, delete the photo after 1 hour, delete the photo after 1 day, or delete the photo after 1 week. You can also choose the `Don't Ask Again` option if you don't want to see this again."
                    )
                    response = await channel.send(content=f"-# {user.mention}", embed=embed, view=view)
                    
                    await view.wait()

                    if view.value == "keep":
                        keep = discord.Embed(
                            color=self.bot.green,
                            title="Keep Photo",
                            description="Understood! I will **not** delete your photo. Thanks!"
                        )
                        await response.edit(content=None, embed=keep, view=None)
                        await response.delete(delay=10.0)
                    
                    elif view.value == "hour":
                        hour = discord.Embed(
                            color=self.bot.red,
                            title="Deletion Scheduled",
                            description="Understood! I will delete your photo in **1 hour**. Thanks!"
                        )
                        await response.edit(content=None, embed=hour, view=None)
                        await response.delete(delay=10.0)

                        delta = timedelta(hours=1.0)
                        now = datetime.now(tz=timezone.utc)
                        one_hour_later = now + delta

                        await discord.utils.sleep_until(when=one_hour_later)
                        await message.delete()
                    
                    elif view.value == "day":
                        day = discord.Embed(
                            color=self.bot.red,
                            title="Deletion Scheduled",
                            description="Understood! I will delete your photo in **1 day**. Thanks!"
                        )
                        await response.edit(content=None, embed=day, view=None)
                        await response.delete(delay=10.0)

                        delta = timedelta(days=1.0)
                        now = datetime.now(tz=timezone.utc)
                        one_day_later = now + delta

                        await discord.utils.sleep_until(when=one_day_later)
                        await message.delete()
                    
                    elif view.value == "week":
                        week = discord.Embed(
                            color=self.bot.red,
                            title="Deletion Scheduled",
                            description="Understood! I will delete your photo in **1 week**. Thanks!"
                        )
                        await response.edit(content=None, embed=week, view=None)
                        await response.delete(delay=10.0)

                        delta = timedelta(weeks=1.0)
                        now = datetime.now(tz=timezone.utc)
                        one_week_later = now + delta

                        await discord.utils.sleep_until(when=one_week_later)
                        await message.delete()
                    
                    elif view.value == "blacklist":
                        await blacklist(member=user)
                        blacklist_embed = discord.Embed(
                            color=self.bot.red,
                            title="Blacklisted",
                            description="You will no longer be asked if you would like any of your posted photos or videos to be deleted."
                        )
                        await response.edit(content=None, embed=blacklist_embed, view=None)
                        await response.delete(delay=10.0)
                
                except Exception:
                    print(traceback.format_exc())
            
            elif message.attachments[0].content_type.startswith("video"):
                try:

                    user = message.author
                    channel = message.channel

                    view = ViewButtons(bot=self.bot, user=user)
                    embed = discord.Embed(
                        color=self.bot.blurple,
                        title="Schedule Video Deletion",
                        description=f"Hello, {user.mention}! I see that you've just posted a video. If you like, I can delete the video after a chosen period of time. Use the bottons below to indicate if you would like me to keep the video, delete the video after 1 hour, delete the video after 1 day, or delete the video after 1 week. You can also choose the `Don't Ask Again` option if you don't want to see this again."
                    )
                    response = await channel.send(content=f"-# {user.mention}", embed=embed, view=view)
                    
                    await view.wait()

                    if view.value == "keep":
                        keep = discord.Embed(
                            color=self.bot.green,
                            title="Keep Video",
                            description="Understood! I will **not** delete your video. Thanks!"
                        )
                        await response.edit(content=None, embed=keep, view=None)
                        await response.delete(delay=10.0)
                    
                    elif view.value == "hour":
                        hour = discord.Embed(
                            color=self.bot.red,
                            title="Deletion Scheduled",
                            description="Understood! I will delete your video in **1 hour**. Thanks!"
                        )
                        await response.edit(content=None, embed=hour, view=None)
                        await response.delete(delay=10.0)

                        delta = timedelta(hours=1.0)
                        now = datetime.now(tz=timezone.utc)
                        one_hour_later = now + delta

                        await discord.utils.sleep_until(when=one_hour_later)
                        await message.delete()
                    
                    elif view.value == "day":
                        day = discord.Embed(
                            color=self.bot.red,
                            title="Deletion Scheduled",
                            description="Understood! I will delete your video in **1 day**. Thanks!"
                        )
                        await response.edit(content=None, embed=day, view=None)
                        await response.delete(delay=10.0)

                        delta = timedelta(days=1.0)
                        now = datetime.now(tz=timezone.utc)
                        one_day_later = now + delta

                        await discord.utils.sleep_until(when=one_day_later)
                        await message.delete()
                    
                    elif view.value == "week":
                        week = discord.Embed(
                            color=self.bot.red,
                            title="Deletion Scheduled",
                            description="Understood! I will delete your video in **1 week**. Thanks!"
                        )
                        await response.edit(content=None, embed=week, view=None)
                        await response.delete(delay=10.0)

                        delta = timedelta(weeks=1.0)
                        now = datetime.now(tz=timezone.utc)
                        one_week_later = now + delta

                        await discord.utils.sleep_until(when=one_week_later)
                        await message.delete()
                    
                    elif view.value == "blacklist":
                        await blacklist(member=user)
                        blacklist_embed = discord.Embed(
                            color=self.bot.red,
                            title="Blacklisted",
                            description="You will no longer be asked if you would like any of your posted photos or videos to be deleted."
                        )
                        await response.edit(content=None, embed=blacklist_embed, view=None)
                        await response.delete(delay=10.0)
                
                except Exception:
                    print(traceback.format_exc())

async def setup(bot: commands.Bot):
    print("Setting up Cog: photodelete.PhotoDelete")

async def teardown(bot: commands.Bot):
    print("Tearing down Cog: photodelete.PhotoDelete")