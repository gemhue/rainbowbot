import discord
import aiosqlite
import traceback
from discord.ext import commands
from datetime import datetime, timedelta, timezone

class PhotoView(discord.ui.View):
    def __init__(self, *, bot: commands.Bot, user: discord.Member):
        super().__init__(timeout=None)
        self.bot = bot
        self.user = user
        self.value = None
    
    @discord.ui.button(label="Keep Photo", style=discord.ButtonStyle.green, emoji="✅", row=0)
    async def dont_delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        if interaction.user == self.user:
            self.value = "keep"
            self.stop()
        else:
            error = discord.Embed(color=self.bot.red, title="Error", description="You can't interact with this view!")
            error_msg = await interaction.followup.send(ephemeral=True, embed=error, wait=True)
            await error_msg.delete(delay=5.0)
    
    @discord.ui.button(label="Delete After 1 Hour", style=discord.ButtonStyle.blurple, emoji="🗑️", row=0)
    async def one_hour(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = "hour"
            self.stop()
        else:
            error = discord.Embed(color=self.bot.red, title="Error", description="You can't interact with this view!")
            error_msg = await interaction.followup.send(ephemeral=True, embed=error, wait=True)
            await error_msg.delete(delay=5.0)
    
    @discord.ui.button(label="Delete After 1 Day", style=discord.ButtonStyle.blurple, emoji="🗑️", row=0)
    async def one_hour(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = "day"
            self.stop()
        else:
            error = discord.Embed(color=self.bot.red, title="Error", description="You can't interact with this view!")
            error_msg = await interaction.followup.send(ephemeral=True, embed=error, wait=True)
            await error_msg.delete(delay=5.0)
    
    @discord.ui.button(label="Delete After 1 Week", style=discord.ButtonStyle.blurple, emoji="🗑️", row=0)
    async def one_week(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = "week"
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
        self.dict = {}
    
    @commands.Cog.listener(name="on_message")
    async def on_message(self, message: discord.Message):
        if message.attachments:

            if message.attachments[0].content_type.startswith("image"):
                try:

                    user = message.author
                    channel = message.channel
                    guild = message.guild

                    view = PhotoView(bot=self.bot, user=user)
                    embed = discord.Embed(
                        color=self.bot.blurple,
                        title="Schedule Photo Deletion",
                        description=f"Hello, {user.mention}! I see that you've just posted a photo. If you like, I can delete the photo after a chosen period of time. Use the bottons below to indicate if you would like me to keep the photo, delete the photo after 1 hour, delete the photo after 1 day, or delete the photo after 1 week."
                    )
                    response = await channel.send(content=f"-# {user.mention}", embed=embed, view=view)
                    
                    await view.wait()

                    if view.value == "keep":
                        keep = discord.Embed(
                            color=self.bot.green,
                            title="Keep Photo",
                            description="Understood! I will not delete your photo. Thanks!"
                        )
                        await response.edit(content=None, embed=keep, view=None)
                    
                    elif view.value == "hour":
                        hour = discord.Embed(
                            color=self.bot.red,
                            title="Delete After 1 Hour",
                            description="Understood! I will delete your photo in 1 hour. Thanks!"
                        )
                        await response.edit(content=None, embed=hour, view=None)
                    
                    elif view.value == "day":
                        day = discord.Embed(
                            color=self.bot.red,
                            title="Delete After 1 Day",
                            description="Understood! I will delete your photo in 1 day. Thanks!"
                        )
                        await response.edit(content=None, embed=day, view=None)
                    
                    elif view.value == "week":
                        week = discord.Embed(
                            color=self.bot.red,
                            title="Delete After 1 Week",
                            description="Understood! I will delete your photo in 1 week. Thanks!"
                        )
                        await response.edit(content=None, embed=week, view=None)
                
                except Exception:
                    print(traceback.format_exc())
            
            elif message.attachments[0].content_type.startswith("video"):
                try:

                    user = message.author
                    channel = message.channel
                    guild = message.guild
                
                except Exception:
                    print(traceback.format_exc())

async def setup(bot: commands.Bot):
    print("Setting up Cog: photodelete.PhotoDelete")

async def teardown(bot: commands.Bot):
    print("Tearing down Cog: photodelete.PhotoDelete")