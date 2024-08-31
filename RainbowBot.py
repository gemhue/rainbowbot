import discord
from discord import app_commands, ChannelType
from discord.ext import commands
from discord.ui import ChannelSelect
from datetime import datetime, timezone, timedelta
from typing import Any

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

bot = commands.Bot(command_prefix='.', intents=intents)

class ChannelsSelector(ChannelSelect):
    def __init__(self):
        super().__init__(
            channel_types=[ChannelType.text],
            placeholder="Select channels... (limit: 25)",
            min_values=1,
            max_values=25
        )
    async def callback(self, interaction: discord.Interaction) -> Any:
        await interaction.response.defer(ephemeral=True, thinking=True)
        channels: list[DropdownView] = self.values
        self.view.values = [c for c in channels]
        channellist = [c.mention for c in channels]
        embed = discord.Embed(description=f'{interaction.user.mention} selected the following channels:\n\n' + "\n".join(channellist))
        await interaction.followup.send(embed=embed, ephemeral=True)

class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.add_item(ChannelsSelector())
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Confirming...', ephemeral=True)
        self.value = True
        self.stop()
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Cancelling...', ephemeral=True)
        self.value = False
        self.stop()

@tree.command(
    name="purgeself",
    description="Purge your messages in a set list of channels."
)
@app_commands.describe(
    amount="Amount of messages to purge from each channel (limit: 100)"
)
async def purgeself(interaction, amount: int):
    await interaction.response.defer(thinking=True)
    view = DropdownView()
    await interaction.followup.send("Which channels would you like to purge your messages from?", view=view, ephemeral=True)
    await view.wait()
    if view.value == True:
        channels = [await c.fetch() for c in view.values]
        deleted = []
        for channel in channels:
            deleted += await channel.purge(limit=amount, check=lambda message: message.author == interaction.user)
        await interaction.followup.send(f'{len(deleted)} of your messages have been purged!')
    elif view.value == False:
        await interaction.followup.send('None of your messages have been purged!')
    else:
        await interaction.followup.send('The interaction has timed out!')

@tree.command(
    name="purgechannels",
    description="Purge messages in a set list of channels (admin only)."
)
@app_commands.checks.has_permissions(administrator=True)
@app_commands.describe(
    amount="Amount of messages to purge from each channel (limit: 100)"
)
async def purgeself(interaction, amount: int):
    await interaction.response.defer(thinking=True)
    view = DropdownView()
    await interaction.followup.send("Which channels would you like to purge messages from?", view=view, ephemeral=True)
    await view.wait()
    channels = [await c.fetch() for c in view.values]
    deleted = []
    for channel in channels:
        deleted += await channel.purge(limit=amount, check=lambda message: message.author == interaction.user)
    await interaction.followup.send(f'{len(deleted)} messages have been purged!')

@tree.command(
    name="sync",
    description="Syncs the command tree (for bot owner only)."
)
@app_commands.checks.has_permissions(administrator=True)
async def sync(interaction: discord.Interaction):
    guild = discord.Object(id=interaction.guild_id)
    if interaction.user.id == 323927406295384067:
        tree.clear_commands(guild=guild)
        await tree.sync()
        print('The command tree has been synced!')
        await interaction.response.send_message("The command tree has been synced!", ephemeral=True)
    else:
        await interaction.response.send_message("Not Allowed", ephemeral=True)

@client.event
async def on_message(message: discord.Message):
    list1 = ['lesbian','sapphic','wlw']
    list2 = ['gay','achillean','mlm']
    list3 = ['bisexual','biromantic','bi woman','bi lady','bi girl','bi gal','bi man','bi guy','bi dude','bi boy','bi person','bi people']
    list4 = ['asexual','aromantic','acespec','arospec','ace spec','aro spec','ace-spec','aro-spec']
    list5 = ['transgender','transsexual','trans woman','trans lady','trans girl','trans gal','trans man','trans guy','trans dude','trans boy','trans person','trans people']
    list6 = ['nonbinary','non binary','non-binary','enby']
    list7 = ['transfeminine','trans feminine','trans-feminine','transfem','trans fem','trans-fem']
    list8 = ['transmasculine','trans masculine','trans-masculine','transmasc','trans masc','trans-masc']
    moji1 = client.get_emoji(1274435288499884094)
    moji2 = client.get_emoji(1274435330174615624)
    moji3 = client.get_emoji(1274435359878676560)
    moji4 = client.get_emoji(1274435406804291634)
    moji5 = client.get_emoji(1274435448726622208)
    moji6 = client.get_emoji(1274435483912638515)
    moji7 = client.get_emoji(1274435557744840820)
    moji8 = client.get_emoji(1274435528883961989)
    msg = message.content.lower()
    if any(x in msg for x in list1):
        await message.add_reaction(moji1)
    if any(x in msg for x in list2):
        await message.add_reaction(moji2)
    if any(x in msg for x in list3):
        await message.add_reaction(moji3)
    if any(x in msg for x in list4):
        await message.add_reaction(moji4)
    if any(x in msg for x in list5):
        await message.add_reaction(moji5)
    if any(x in msg for x in list6):
        await message.add_reaction(moji6)
    if any(x in msg for x in list7):
        await message.add_reaction(moji7)
    if any(x in msg for x in list8):
        await message.add_reaction(moji8)

@tree.command(
    name="hello",
    description="Says hello."
)
async def hello(interaction):
    embed = discord.Embed(description="Hello!")
    await interaction.response.send_message(embed=embed)

@tree.command(
    name="goodbye",
    description="Says goodbye."
)
async def goodbye(interaction):
    embed = discord.Embed(description="Goodbye!")
    await interaction.response.send_message(embed=embed)

@tree.command(
    name="serverlists",
    description="Returns a list server members and server channels."
)
async def serverlists(interaction):
    members = [m for m in interaction.guild.members if not m.bot]
    channels = interaction.guild.text_channels
    memberstring = ", ".join(str(x.mention) for x in members)
    channelstring = ", ".join(str(x.mention) for x in channels)
    embeds = [discord.Embed(title="Members", description=memberstring), discord.Embed(title="Channels", description=channelstring)]
    await interaction.response.send_message(embeds=embeds)

@tree.command(
    name="memberids",
    description="Returns a list server member IDs."
)
async def memberids(interaction):
    members = [m for m in interaction.guild.members if not m.bot]
    memberids = []
    for x in members:
        memberids.append(x.id)
    memberidstring = ", ".join(str(x) for x in memberids)
    embed = discord.Embed(description="**Member IDs**: " + memberidstring)
    await interaction.response.send_message(embed=embed)

@tree.command(
    name="channelids",
    description="Returns a list of server channel IDs."
)
async def channelids(interaction):
    channels = interaction.guild.text_channels
    channelids = []
    for x in channels:
        channelids.append(x.id)
    channelidstring = ", ".join(str(x) for x in channelids)
    embed = discord.Embed(description="**Channel IDs**: " + channelidstring)
    await interaction.response.send_message(embed=embed)

@tree.command(
    name="activityroles",
    description="Assigns all server members either an active or inactive role (admin only)."
)
@app_commands.describe(
    days="Set the number of days a member must be inactive before getting the inactive role.",
    inactive="Choose the role that you would like to give to inactive members.",
    active="Choose the role that you would like to give to active members."
)
@app_commands.checks.has_permissions(administrator=True)
async def activityroles(interaction, days: int, inactive: discord.Role, active: discord.Role):
    await interaction.response.defer(thinking=True)
    channels = interaction.guild.text_channels
    members = [m for m in interaction.guild.members if not m.bot]
    today =  datetime.now(timezone.utc)
    setdays = timedelta(days=days)
    daysago = today-setdays
    newmembers = [m for m in members if m.joined_at < daysago]
    activemembers = []
    inactivemembers = []
    for channel in channels:
        async for message in channel.history(after=daysago):
            for member in members:
                if message.author == member and member not in activemembers:
                    activemembers.append(member)
    for member in members:
        if member not in activemembers and member not in newmembers:
            inactivemembers.append(member)
        elif member in newmembers and member not in activemembers:
            activemembers.append(member)
    for member in activemembers:
        if active not in member.roles:
            await member.add_roles(active)
            if inactive in member.roles:
                await member.remove_roles(inactive)
    for member in inactivemembers:
        if inactive not in member.roles:
            await member.add_roles(inactive)
            if active in member.roles:
                await member.remove_roles(active)
    for member in activemembers:
        embed = discord.Embed(description=str(f"{member.mention} is active! They've been given the {active.mention} role if they didn't already have it."))
        await interaction.followup.send(embed=embed)
    for member in inactivemembers:
        embed = discord.Embed(description=str(f"{member.mention} is inactive! They've been given the {inactive.mention} role if they didn't already have it."))
        await interaction.followup.send(embed=embed)

@client.event
async def on_ready():
    # guild = discord.Object(id=1274023759497662646)
    # tree.clear_commands(guild=guild)
    # await tree.sync()
    print(f'Logged in as {client.user}! (ID: {client.user.id})')

client.run('token')