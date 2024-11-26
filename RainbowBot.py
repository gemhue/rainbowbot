import discord
import aiosqlite
import logging
import traceback
import os
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv()
token = os.getenv("token")

class CogButtons(discord.ui.View):
    def __init__(self, *, timeout = 180):
        super().__init__(timeout=timeout)
    
    @discord.ui.button(label="AutoDelete", style=discord.ButtonStyle.blurple, emoji="♻️")
    async def autodelete(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message

        embed = discord.Embed(color=discord.Color.blurple(), title="AutoDelete", description="These commands allow you to set the messages in a channel to be automatically deleted on a rolling basis.")
        embed.add_field(
            name="/autodelete start <amount> <interval>",
            value="(Admin Only) Sets the messages in the current channel to be autodeleted.\n\n> `amount` - Set the amount of time. The lowest possible frequency is 30 minutes.\n\n> `interval` - Set the time interval. The lowest possible frequency is 30 minutes.",
            inline=False
        )
        embed.add_field(
            name="/autodelete cancel",
            value="(Admin Only) Cancels the autodelete set for the current channel.",
            inline=False
        )

        await interaction.followup.edit_message(message_id=message.id, embed=embed, view=self)
    
    @discord.ui.button(label="Awards", style=discord.ButtonStyle.blurple, emoji="🏅")
    async def awards(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message

        embed = discord.Embed(color=discord.Color.blurple(), title="Awards", description="These commands allow you to set up an awards system in your server. The award name and emoji can be customized.")
        embed.add_field(
            name="/awards setup",
            value="(Admin Only) Sets the name, emoji, and leaderboard channel for the server awards.",
            inline=False
        )
        embed.add_field(
            name="/awards clear",
            value="(Admin Only) Clears every member's awards in the server.",
            inline=False
        )
        embed.add_field(
            name="/awards add <amount> <member>",
            value="Adds awards to the command user or another selected member.\n\n> `amount` - Choose the number of awards to add. (Default: 1)\n\n> `member` - Choose the member to add the awards to. (Default: Self)",
            inline=False
        )
        embed.add_field(
            name="/awards remove <amount> <member>",
            value="Removes awards from the command user or another selected member.\n\n> `amount` - Choose the number of awards to remove. (Default: 1)\n\n> `member` - Choose the member to remove the awards from. (Default: Self)",
            inline=False
        )
        embed.add_field(
            name="/awards check <member>",
            value="Returns the number of awards that the command user or another selected user currently has.\n\n> `member` - Choose the member that you would like to check the number of awards for. (Default: Self)",
            inline=False
        )

        await interaction.followup.edit_message(message_id=message.id, embed=embed, view=self)

    @discord.ui.button(label="Embeds", style=discord.ButtonStyle.blurple, emoji="📝")
    async def embeds(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message

        embed = discord.Embed(color=discord.Color.blurple(), title="Embeds", description="These commands allow you to send and edit messages containing embeds.")
        embed.add_field(
            name="/embed send <message_content> <embed_color> <embed_title> <embed_url> <embed_description>",
            value="(Admin Only) Run this command to send an embed to the current channel.\n\n> `message_content` - Provide the content of the message above the embed.\n\n> `embed_color` - Provide the embed's color (HEX or RGB).\n\n> `embed_title` - Provide the embed's title.\n\n> `embed_url` - Provide the embed's URL.\n\n> `embed_description` - Provide the embed's description.",
            inline=False
        )
        embed.add_field(
            name="/embed edit <message_url> <message_content> <embed_color> <embed_title> <embed_url> <embed_description>",
            value="(Admin Only) Run this command to edit the embed of a given message URL.\n\n> `message_url` - Provide the URL of the message containing the embed.\n\n> `message_content` - Provide the new content of the message above the embed.\n\n> `embed_color` - Provide the embed's new color (HEX or RGB).\n\n> `embed_title` - Provide the embed's new title.\n\n> `embed_url` - Provide the embed's new URL.\n\n> `embed_description` - Provide the embed's new description.",
            inline=False
        )
        embed.add_field(
            name="/embed set_image <message_url> <image_url>",
            value="(Admin Only) Run this command to set an embed's image.\n\n> `message_url` - Provide the URL of the message containing the embed.\n\n> `image_url` - Provide the URL of the image.",
            inline=False
        )
        embed.add_field(
            name="/embed remove_image <message_url>",
            value="(Admin Only) Run this command to remove an embed's image.\n\n> `message_url` - Provide the URL of the message containing the embed.",
            inline=False
        )
        embed.add_field(
            name="/embed set_thumbnail <message_url> <thumbnail_url>",
            value="(Admin Only) Run this command to set an embed's thumbnail.\n\n> `message_url` - Provide the URL of the message containing the embed.\n\n> `thumbnail_url` - Provide the URL of the thumbnail.",
            inline=False
        )
        embed.add_field(
            name="/embed remove_thumbnail <message_url>",
            value="(Admin Only) Run this command to remove an embed's thumbnail.\n\n> `message_url` - Provide the URL of the message containing the embed.",
            inline=False
        )
        embed.add_field(
            name="/embed add_field <message_url> <name> <value> <inline>",
            value="(Admin Only) Run this command to add a field to an embed.\n\n> `message_url` - Provide the URL of the message containing the embed.\n\n> `name` - Provide the name of the field to be added.\n\n> `value` - Provide the value of the field to be added.\n\n> `inline` - Provide whether the field should be inline.",
            inline=False
        )
        embed.add_field(
            name="/embed edit_field <message_url> <index> <name> <value> <inline>",
            value="(Admin Only) Run this command to edit a field of an embed by its index.\n\n> `message_url` - Provide the URL of the message containing the embed.\n\n> `index` - Provide the index of the field to be edited.\n\n> `name` - Provide the new name of the field.\n\n> `value` - Provide the new value of the field.\n\n> `inline` - Provide whether the edited field should be inline.",
            inline=False
        )
        embed.add_field(
            name="/embed insert_field <message_url> <index> <name> <value> <inline>",
            value="(Admin Only) Run this command to insert an embed field at an index.\n\n> `message_url` - Provide the URL of the message containing the embed.\n\n> `index` - Provide the index of the field to be inserted.\n\n> `name` - Provide the name of the field to be inserted.\n\n> `value` - Provide the value of the field to be inserted.\n\n> `inline` - Provide whether the inserted field should be inline.",
            inline=False
        )
        embed.add_field(
            name="/embed remove_field <message_url> <index>",
            value="(Admin Only) Run this command to remove a field from an embed by its index.\n\n> `message_url` - Provide the URL of the message containing the embed.\n\n> `index` - Provide the index of the field to be removed.",
            inline=False
        )

        await interaction.followup.edit_message(message_id=message.id, embed=embed, view=self)

    @discord.ui.button(label="Profiles", style=discord.ButtonStyle.blurple, emoji="🪪")
    async def profiles(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message

        embed = discord.Embed(color=discord.Color.blurple(), title="AutoDelete", description="These commands allow you to set the messages in a channel to be automatically deleted on a rolling basis.")
        embed.add_field(name="/autodelete start <amount> <interval>",
                        value="(Admin Only) Sets the messages in the current channel to be autodeleted.\n\n> `amount` - Set the amount of time. The lowest possible frequency is 30 minutes.\n\n> `interval` - Set the time interval. The lowest possible frequency is 30 minutes.",
                        inline=False)
        embed.add_field(name="/autodelete cancel",
                        value="(Admin Only) Cancels the autodelete set for the current channel.",
                        inline=False)

        await interaction.followup.edit_message(message_id=message.id, embed=embed, view=self)
    
    @discord.ui.button(label="Purge", style=discord.ButtonStyle.blurple, emoji="🗑️")
    async def purge(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message

        embed = discord.Embed(color=discord.Color.blurple(), title="AutoDelete", description="These commands allow you to set the messages in a channel to be automatically deleted on a rolling basis.")
        embed.add_field(name="/autodelete start <amount> <interval>",
                        value="(Admin Only) Sets the messages in the current channel to be autodeleted.\n\n> `amount` - Set the amount of time. The lowest possible frequency is 30 minutes.\n\n> `interval` - Set the time interval. The lowest possible frequency is 30 minutes.",
                        inline=False)
        embed.add_field(name="/autodelete cancel",
                        value="(Admin Only) Cancels the autodelete set for the current channel.",
                        inline=False)

        await interaction.followup.edit_message(message_id=message.id, embed=embed, view=self)
    
    @discord.ui.button(label="Remind", style=discord.ButtonStyle.blurple, emoji="📅")
    async def remind(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message

        embed = discord.Embed(color=discord.Color.blurple(), title="AutoDelete", description="These commands allow you to set the messages in a channel to be automatically deleted on a rolling basis.")
        embed.add_field(name="/autodelete start <amount> <interval>",
                        value="(Admin Only) Sets the messages in the current channel to be autodeleted.\n\n> `amount` - Set the amount of time. The lowest possible frequency is 30 minutes.\n\n> `interval` - Set the time interval. The lowest possible frequency is 30 minutes.",
                        inline=False)
        embed.add_field(name="/autodelete cancel",
                        value="(Admin Only) Cancels the autodelete set for the current channel.",
                        inline=False)

        await interaction.followup.edit_message(message_id=message.id, embed=embed, view=self)

    @discord.ui.button(label="RSS Feeds", style=discord.ButtonStyle.blurple, emoji="📰")
    async def rss_feeds(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message

        embed = discord.Embed(color=discord.Color.blurple(), title="AutoDelete", description="These commands allow you to set the messages in a channel to be automatically deleted on a rolling basis.")
        embed.add_field(name="/autodelete start <amount> <interval>",
                        value="(Admin Only) Sets the messages in the current channel to be autodeleted.\n\n> `amount` - Set the amount of time. The lowest possible frequency is 30 minutes.\n\n> `interval` - Set the time interval. The lowest possible frequency is 30 minutes.",
                        inline=False)
        embed.add_field(name="/autodelete cancel",
                        value="(Admin Only) Cancels the autodelete set for the current channel.",
                        inline=False)

        await interaction.followup.edit_message(message_id=message.id, embed=embed, view=self)

    @discord.ui.button(label="Tickets", style=discord.ButtonStyle.blurple, emoji="🎫")
    async def rss_feeds(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message

        embed = discord.Embed(color=discord.Color.blurple(), title="AutoDelete", description="These commands allow you to set the messages in a channel to be automatically deleted on a rolling basis.")
        embed.add_field(name="/autodelete start <amount> <interval>",
                        value="(Admin Only) Sets the messages in the current channel to be autodeleted.\n\n> `amount` - Set the amount of time. The lowest possible frequency is 30 minutes.\n\n> `interval` - Set the time interval. The lowest possible frequency is 30 minutes.",
                        inline=False)
        embed.add_field(name="/autodelete cancel",
                        value="(Admin Only) Cancels the autodelete set for the current channel.",
                        inline=False)

        await interaction.followup.edit_message(message_id=message.id, embed=embed, view=self)
    
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def done(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.stop()

class RainbowBotHelp(commands.HelpCommand):
    def __init__(self):
        super().__init__()
    
    async def send_bot_help(self, mapping):
        embed = discord.Embed(color=discord.Color.blurple(), title="Help", description="If you have any questions that are not answered by this `help` command, please join the bot's support server (linked in the bot's bio).")

        view = CogButtons()

        channel = self.get_destination()
        response = await channel.send(embed=embed, view=view)
        await view.wait()
        await response.delete()

class RainbowBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = commands.when_mentioned_or("rb!"),
            help_command = RainbowBotHelp(),
            description = "A multi-purpose Discord bot made by GitHub user gemhue.",
            intents = discord.Intents.all(),
            activity = discord.Activity(type=discord.ActivityType.listening, name="rb!help"),
            status = discord.Status.online
        )
        self.blurple = discord.Colour.blurple()
        self.green = discord.Colour.green()
        self.yellow = discord.Colour.yellow()
        self.red = discord.Colour.red()
    
    async def setup_hook(self):
        self.database = await aiosqlite.connect("rainbowbot.db")
        print("Connected to Database: rainbowbot.db")

bot = RainbowBot()
handler = logging.FileHandler(filename="rainbowbot.log", encoding="utf-8", mode="w")

@bot.command(name="sync", hidden=True)
@commands.is_owner()
async def sync(ctx: commands.Context, where: str):
    """(Bot Owner Only) Syncs the local command tree.
    """
    await ctx.defer()
    guild = ctx.guild
    now = datetime.now(tz=timezone.utc)
    if where == "here" or where == "local":
        await bot.tree.sync(guild=guild)
        embed = discord.Embed(color=bot.green, title="Success", description=f"The bot's local command tree has been synced!", timestamp=now)
    elif where == "all" or where == "global":
        await bot.tree.sync(guild=None)
        embed = discord.Embed(color=bot.green, title="Success", description=f"The bot's global command tree has been synced!", timestamp=now)
    else:
        embed = discord.Embed(color=bot.red, title="Error", description=f"The bot's command tree has not been synced! Please specify if you would like to sync `here` or `all`.", timestamp=now)
    await ctx.send(embed=embed, delete_after=10.0)
    await ctx.message.delete()

    # Send a log to the logging channel
    cur = await bot.database.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
    row = await cur.fetchone()
    fetched_logging = row[0]
    if fetched_logging is not None:
        logging = ctx.guild.get_channel(fetched_logging)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
        embed.set_thumbnail(url=ctx.author.display_avatar)
        await logging.send(embed=embed)

@bot.command(name="clear", hidden=True)
@commands.is_owner()
async def clear(ctx: commands.Context, where: str):
    """(Bot Owner Only) Clears the local command tree.
    """
    await ctx.defer()
    guild = ctx.guild
    now = datetime.now(tz=timezone.utc)
    if where == "here" or where == "local":
        bot.tree.clear_commands(guild=guild)
        embed = discord.Embed(color=bot.green, title="Success", description=f"The bot's local command tree has been cleared!", timestamp=now)
    elif where == "all" or where == "global":
        bot.tree.clear_commands(guild=None)
        embed = discord.Embed(color=bot.green, title="Success", description=f"The bot's global command tree has been cleared!", timestamp=now)
    else:
        embed = discord.Embed(color=bot.red, title="Error", description=f"The bot's command tree has not been cleared! Please specify if you would like to clear \`here\` or \`all\`.", timestamp=now)
    await ctx.send(embed=embed, delete_after=10.0)
    await ctx.message.delete()
    
    # Send a log to the logging channel
    cur = await bot.database.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
    row = await cur.fetchone()
    fetched_logging = row[0]
    if fetched_logging is not None:
        logging = ctx.guild.get_channel(fetched_logging)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
        embed.set_thumbnail(url=ctx.author.display_avatar)
        await logging.send(embed=embed)

async def allcogs(x):
    files = []
    cogs = []
    cogsdict = {}
    folder = "./cogs"
    for file in os.listdir(folder):
        if file.endswith(".py"):
            files.append(file[:-3])
    for file in files:
        if x == "cogs":
            cogs.append(f"cogs.{file}")
        elif x == "modules":
            title = file.title()
            cogs.append(f"{file}.{title}")
        elif x == "names":
            cogs.append(file)
        elif x == "names_lower":
            name = file.lower()
            cogs.append(name)
        elif x == "names_dict":
            lower = file.lower()
            cogsdict[lower] = file
    if len(cogs) > 0:
        return cogs
    elif len(cogsdict) > 0:
        return cogsdict
    else:
        return None

@bot.command(name="get_cogs", aliases=["get_cog","getcogs","getcog"], hidden=True)
@commands.is_owner()
async def get_cogs(ctx: commands.Context):
    """(Bot Owner Only) Returns all of the bot's cogs.
    """
    await ctx.defer()
    now = datetime.now(tz=timezone.utc)
    embed = discord.Embed(color=bot.blurple, title="Cogs", timestamp=now)
    for cog in await allcogs(x="names"):
        embed.add_field(name=cog, value="Retreived successfully!")
    await ctx.send(embed=embed, delete_after=10.0)
    await ctx.message.delete()

    # Send a log to the logging channel
    cur = await bot.database.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
    row = await cur.fetchone()
    fetched_logging = row[0]
    if fetched_logging is not None:
        logging = ctx.guild.get_channel(fetched_logging)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
        embed.set_thumbnail(url=ctx.author.display_avatar)
        await logging.send(embed=embed)

@bot.command(name="load", hidden=True)
@commands.is_owner()
async def load(ctx: commands.Context, extension: str):
    """(Bot Owner Only) Loads one or all of the bot's cogs.

    Parameters
    -----------
    extension : str
        Provide the extension that you would like to load (or all).
    """
    await ctx.defer()
    now = datetime.now(tz=timezone.utc)
    embed = discord.Embed(color=bot.blurple, title="Load Cogs", timestamp=now)
    lower = extension.lower()
    if lower == "all":
        for cog in await allcogs(x="cogs"):
            try:
                await bot.load_extension(cog)
                embed.add_field(name=cog, value="Loaded successfully!")
            except Exception as e:
                embed.add_field(name=cog, value=f"Error: {e}")
                print(traceback.format_exc())
    elif lower in await allcogs(x="names_lower"):
        for cog in await allcogs(x="cogs"):
            if cog.lower() == f"cogs.{lower}":
                try:
                    await bot.load_extension(cog)
                    embed.add_field(name=cog, value="Loaded successfully!")
                except Exception as e:
                    embed.add_field(name=cog, value=f"Error: {e}")
                    print(traceback.format_exc())
    else:
        embed.add_field(name="Error", value="No cogs could be loaded.")
    await ctx.send(embed=embed, delete_after=10.0)
    await ctx.message.delete()
    
    # Send a log to the logging channel
    cur = await bot.database.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
    row = await cur.fetchone()
    fetched_logging = row[0]
    if fetched_logging is not None:
        logging = ctx.guild.get_channel(fetched_logging)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
        embed.set_thumbnail(url=ctx.author.display_avatar)
        await logging.send(embed=embed)

@bot.command(name="unload", hidden=True)
@commands.is_owner()
async def unload(ctx: commands.Context, extension: str):
    """(Bot Owner Only) Unloads one or all of the bot's cogs.

    Parameters
    -----------
    extension : str
        Provide the extension that you would like to unload (or all).
    """
    await ctx.defer()
    now = datetime.now(tz=timezone.utc)
    embed = discord.Embed(color=bot.blurple, title="Unload Cogs", timestamp=now)
    lower = extension.lower()
    if lower == "all":
        for cog in await allcogs(x="cogs"):
            try:
                await bot.unload_extension(cog)
                embed.add_field(name=cog, value="Unloaded successfully!")
            except Exception as e:
                embed.add_field(name=cog, value=f"Error: {e}")
                print(traceback.format_exc())
    elif lower in await allcogs(x="names_lower"):
        for cog in await allcogs(x="cogs"):
            if cog.lower() == f"cogs.{lower}":
                try:
                    await bot.unload_extension(cog)
                    embed.add_field(name=cog, value="Unloaded successfully!")
                except Exception as e:
                    embed.add_field(name=cog, value=f"Error: {e}")
                    print(traceback.format_exc())
    else:
        embed.add_field(name="Error", value="No cogs could be unloaded.")
    await ctx.send(embed=embed, delete_after=10.0)
    await ctx.message.delete()
    
    # Send a log to the logging channel
    cur = await bot.database.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
    row = await cur.fetchone()
    fetched_logging = row[0]
    if fetched_logging is not None:
        logging = ctx.guild.get_channel(fetched_logging)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
        embed.set_thumbnail(url=ctx.author.display_avatar)
        await logging.send(embed=embed)

@bot.command(name="reload", hidden=True)
@commands.is_owner()
async def reload(ctx: commands.Context, extension: str):
    """(Bot Owner Only) Reloads one or all of the bot's cogs.

    Parameters
    -----------
    extension : str
        Provide the extension that you would like to reload (or all).
    """
    await ctx.defer()
    now = datetime.now(tz=timezone.utc)
    embed = discord.Embed(color=bot.blurple, title="Reload Cogs", timestamp=now)
    lower = extension.lower()
    if lower == "all":
        for cog in await allcogs(x="cogs"):
            try:
                await bot.reload_extension(cog)
                embed.add_field(name=cog, value="Reloaded successfully!")
            except Exception as e:
                embed.add_field(name=cog, value=f"Error: {e}")
                print(traceback.format_exc())
    elif lower in await allcogs(x="names_lower"):
        for cog in await allcogs(x="cogs"):
            if cog.lower() == f"cogs.{lower}":
                try:
                    await bot.reload_extension(cog)
                    embed.add_field(name=cog, value="Reloaded successfully!")
                except Exception as e:
                    embed.add_field(name=cog, value=f"Error: {e}")
                    print(traceback.format_exc())
    else:
        embed.add_field(name="Error", value="No cogs could be reloaded.")
    await ctx.send(embed=embed, delete_after=10.0)
    await ctx.message.delete()
    
    # Send a log to the logging channel
    cur = await bot.database.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
    row = await cur.fetchone()
    fetched_logging = row[0]
    if fetched_logging is not None:
        logging = ctx.guild.get_channel(fetched_logging)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
        embed.set_thumbnail(url=ctx.author.display_avatar)
        await logging.send(embed=embed)  

@bot.command(name="ping")
async def ping(ctx: commands.Context):
    """Retrieve the bot's current latency.
    """
    await ctx.defer()
    try:
        now = datetime.now(tz=timezone.utc)
        embed = discord.Embed(color=bot.blurple, title="Pong", description=f"The bot's current latency is {bot.latency} seconds!", timestamp=now)
    except Exception as e:
        embed = discord.Embed(color=bot.red, title="Error", description=f"{e}")
        print(traceback.format_exc())
    await ctx.send(embed=embed, delete_after=10.0)
    await ctx.message.delete()

    # Send a log to the logging channel
    cur = await bot.database.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
    row = await cur.fetchone()
    fetched_logging = row[0]
    if fetched_logging is not None:
        logging = ctx.guild.get_channel(fetched_logging)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
        embed.set_thumbnail(url=ctx.author.display_avatar)
        await logging.send(embed=embed)

@bot.event
async def on_ready(bot=bot):
    print(f'Logged in as {bot.user}! (ID: {bot.user.id})')

bot.run(token, log_handler=handler, log_level=logging.DEBUG)