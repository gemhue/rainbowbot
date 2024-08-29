import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

bot = commands.Bot(command_prefix='.', intents=intents)

debug_guild = discord.Object(id=1274023759497662646)

@client.event
async def on_ready():
    tree.clear_commands(guild=debug_guild)
    await tree.sync()
    print("Ready!")

@tree.command(
    name="hello",
    description="Says hello."
)
async def hello(interaction):
    embed = discord.Embed(description="Hello!")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(
    name="goodbye",
    description="Says goodbye."
)
async def goodbye(interaction):
    embed = discord.Embed(description="Goodbye!")
    await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(
    name="serverlists",
    description="(WIP) Returns a list server members and server channels."
)
@app_commands.checks.has_permissions(administrator=True)
async def serverlists(interaction):
    members = [m for m in interaction.guild.members if not m.bot]
    channels = interaction.guild.text_channels
    memberstring = ", ".join(str(x.mention) for x in members)
    channelstring = ", ".join(str(x.mention) for x in channels)
    embeds = [discord.Embed(title="Members", description=memberstring), discord.Embed(title="Channels:", description=channelstring)]
    await interaction.response.send_message(embeds=embeds, ephemeral=True)

@tree.command(
    name="memberids",
    description="(WIP) Returns a list server member IDs and server channel IDs."
)
@app_commands.checks.has_permissions(administrator=True)
async def memberids(interaction):
    members = [m for m in interaction.guild.members if not m.bot]
    memberids = []
    for x in members:
        memberids.append(x.id)
    memberidstring = ", ".join(str(x) for x in memberids)
    embed = discord.Embed(description="**Member IDs**: " + memberidstring)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(
    name="channelids",
    description="(WIP) Returns a list of server channel IDs."
)
@app_commands.checks.has_permissions(administrator=True)
async def channelids(interaction):
    channels = interaction.guild.text_channels
    channelids = []
    for x in channels:
        channelids.append(x.id)
    channelidstring = ", ".join(str(x) for x in channelids)
    embed = discord.Embed(description="**Channel IDs**: " + channelidstring)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(
    name="getactivity",
    description="(WIP) Returns a list of active and inactive server members."
)
@app_commands.checks.has_permissions(administrator=True)
async def getactivity(interaction):
    await interaction.response.defer(ephemeral=True, thinking=True)
    channels = interaction.guild.text_channels
    members = [m for m in interaction.guild.members if not m.bot]
    today =  datetime.now()
    setdays = timedelta(days=30)
    daysago = today-setdays
    activemembers = []
    inactivemembers = []
    for channel in channels:
        async for message in channel.history(after=daysago):
            for member in members:
                if message.author == member and member not in activemembers:
                    activemembers.append(member)
                else:
                    pass
    for member in members:
        if member not in activemembers:
            inactivemembers.append(member)
    # for member in activemembers:
    #     await interaction.followup.send(member.mention + " is active!", ephemeral=True)
    # for member in inactivemembers:
    #     await interaction.followup.send(member.mention + " is inactive!", ephemeral=True)
    activeembed = ", ".join(str(m.mention) for m in activemembers)
    inactiveembed = ", ".join(str(m.mention) for m in inactivemembers)
    await interaction.followup.send(embed=discord.Embed(title="Active Members:", description=activeembed), ephemeral=True)
    await interaction.followup.send(embed=discord.Embed(title="Inactive Members:", description=inactiveembed), ephemeral=True)

client.run('token')
