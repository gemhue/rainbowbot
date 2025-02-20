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
            ...
        else:
            error = discord.Embed(color=self.bot.red, title="Error", description="You can't interact with this view!")
            error_msg = await interaction.followup.send(ephemeral=True, embed=error, wait=True)
            await error_msg.delete(delay=5.0)
    
    @discord.ui.button(label="Delete After 1 Hour", style=discord.ButtonStyle.blurple, emoji="🗑️", row=0)
    async def one_hour(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            ...
        else:
            error = discord.Embed(color=self.bot.red, title="Error", description="You can't interact with this view!")
            error_msg = await interaction.followup.send(ephemeral=True, embed=error, wait=True)
            await error_msg.delete(delay=5.0)
    
    @discord.ui.button(label="Delete After 1 Day", style=discord.ButtonStyle.blurple, emoji="🗑️", row=0)
    async def one_hour(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            ...
        else:
            error = discord.Embed(color=self.bot.red, title="Error", description="You can't interact with this view!")
            error_msg = await interaction.followup.send(ephemeral=True, embed=error, wait=True)
            await error_msg.delete(delay=5.0)
    
    @discord.ui.button(label="Delete After 1 Week", style=discord.ButtonStyle.blurple, emoji="🗑️", row=0)
    async def one_week(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            ...
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
                    guild = message.guild
                
                except Exception:
                    print(traceback.format_exc())
            
            elif message.attachments[0].content_type.startswith("video"):
                try:

                    user = message.author
                    channel = message.channel
                    guild = message.guild
                
                except Exception:
                    print(traceback.format_exc())