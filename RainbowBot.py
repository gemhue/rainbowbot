import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import app_commands

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

Bot = commands.Bot(command_prefix='.', intents=intents)

debug_guild = discord.Object(id=1274023759497662646)

@client.event
async def on_ready():
    tree.clear_commands(guild=debug_guild)
    await tree.sync(guild=debug_guild)
    print("Ready!")

@tree.command(
    name="hello",
    description="Says hello.",
    guild=debug_guild
)
async def hello(interaction):
    await interaction.response.send_message("Hello!")

@tree.command(
    name="goodbye",
    description="Says goodbye.",
    guild=debug_guild
)
async def goodbye(interaction):
    await interaction.response.send_message("Goodbye!")

@tree.command(
    name="serverlists",
    description="(WIP) Returns a list server members and server channels.",
    guild=debug_guild
)
async def serverlists(interaction):
    members = interaction.guild.members
    channels = interaction.guild.channels
    memberstring = ", ".join(str(x) for x in members)
    channelstring = ", ".join(str(x) for x in channels)
    await interaction.response.send_message("**Members**: " + memberstring + "\n" + "**Channels**: " + channelstring)

@tree.command(
    name="serverids",
    description="(WIP) Returns a list server member IDs and server channel IDs.",
    guild=debug_guild
)
async def serverids(interaction):
    members = interaction.guild.members
    channels = interaction.guild.channels
    memberids = []
    for x in members:
        memberids.append(x.id)
    channelids = []
    for x in channels:
        channelids.append(x.id)
    memberidstring = ", ".join(str(x) for x in memberids)
    channelidstring = ", ".join(str(x) for x in channelids)
    await interaction.response.send_message("**Member IDs**: " + memberidstring + "\n" + "**Channel IDs**: " + channelidstring)

client.run(TOKEN)