import discord
from discord import app_commands, ChannelType
from discord.ui import ChannelSelect
from datetime import datetime, timezone, timedelta
from typing import Any, Optional
import string

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

intents = discord.Intents.all()
client = MyClient(intents=intents)
tree = client.tree

@client.event
async def on_ready():
    guild = discord.Object(id=1274023759497662646)
    tree.clear_commands(guild=guild)
    await tree.sync(guild=guild)
    print(f'Logged in as {client.user}! (ID: {client.user.id})')

@tree.command(
    name="sync",
    description="Syncs the command tree for the server (bot owner only)."
)
@app_commands.checks.has_permissions(administrator=True)
async def sync(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    if interaction.guild.id == 1274023759497662646:
        if interaction.user.id == 323927406295384067:
            tree.clear_commands(guild=None)
            await tree.sync(guild=None)
            embed = discord.Embed(title="Update", description=f"The bot's global command tree has been synced!")
            await interaction.followup.send(embed=embed)
        else:
            embed = discord.Embed(title="Error", description=f"This action is not allowed.")

class ChannelsSelector(ChannelSelect):
    def __init__(self):
        super().__init__(
            channel_types=[ChannelType.text],
            placeholder="Select channels... (Limit: 25)",
            min_values=1,
            max_values=25,
            row=1
        )
    async def callback(self, interaction: discord.Interaction) -> Any:
        channels: list[DropdownView] = self.values
        self.view.values = [c for c in channels]
            
class DropdownView(discord.ui.View):
    def __init__(self, *, timeout=180.0):
        super().__init__(timeout=timeout)
        self.value = None
        self.add_item(ChannelsSelector())
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green, row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = True
        await interaction.response.defer(thinking=True, ephemeral=True)
        channels = [c.resolve() for c in self.values]
        channelment = [c.mention for c in channels]
        channellist = ", ".join(channelment)
        embed = discord.Embed(title="Selected Channels:", description=f'{channellist}')
        await interaction.followup.send(embed=embed, ephemeral=True)
        self.stop()
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey, row=2)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        await interaction.response.defer(thinking=True, ephemeral=True)
        embed = discord.Embed(title="Cancelled", description=f'This interaction has been cancelled.')
        await interaction.followup.send(embed=embed, ephemeral=True)
        self.stop()

@tree.command(
    name="purgeself",
    description="Purge your unpinned messages in a set list of up to 25 channels."
)
async def purgeself(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True, ephemeral=True)
    view = DropdownView()
    await interaction.followup.send("Which channel(s) would you like to purge messages from?", view=view, ephemeral=True)
    await view.wait()
    if view.value == True:
        purgechannels = [c for c in view.values]
        for channel in purgechannels:
            messages = [message async for message in channel.history(limit=None)]
            unpinned = []
            for m in messages:
                if m.pinned == False:
                    unpinned.append(m)
            deleted = []
            if len(unpinned) > 0:
                deleted += await channel.purge(check=lambda message: message.author == interaction.user and message.pinned == False, oldest_first=True)
                if len(deleted) == 1:
                    await interaction.followup.send(f'{len(deleted)} message was just removed from {channel.mention}!', ephemeral=True)
                else:
                    await interaction.followup.send(f'{len(deleted)} messages were just removed from {channel.mention}!', ephemeral=True)
        purgement = [c.mention for c in purgechannels]
        if len(purgement) > 0:
            purgelist = ", ".join(purgement)
        else:
            purgelist = purgement[0]
        await interaction.followup.send(f'{interaction.user.mention} has just purged the following channels: {purgelist}!', ephemeral=True)
    elif view.value == False:
        await interaction.followup.send('Interaction Cancelled. No messages have been purged!', ephemeral=True)
    else:
        await interaction.followup.send('Interaction Timed Out. No messages have been purged!', ephemeral=True)

@tree.command(
    name="purgechannels",
    description="Purge unpinned messages in a set list of up to 25 channels (admin only)."
)
@app_commands.checks.has_permissions(administrator=True)
async def purgechannels(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True, ephemeral=True)
    view = DropdownView()
    await interaction.followup.send("Which channel(s) would you like to purge messages from?", view=view, ephemeral=True)
    await view.wait()
    if view.value == True:
        purgechannels = [c for c in view.values]
        for channel in purgechannels:
            messages = [message async for message in channel.history(limit=None)]
            unpinned = []
            for m in messages:
                if m.pinned == False:
                    unpinned.append(m)
            deleted = []
            if len(unpinned) > 0:
                deleted += await channel.purge(check=lambda message: message.pinned == False, oldest_first=True)
                if len(deleted) == 1:
                    await interaction.followup.send(f'{len(deleted)} message was just removed from {channel.mention}!', ephemeral=True)
                else:
                    await interaction.followup.send(f'{len(deleted)} messages were just removed from {channel.mention}!', ephemeral=True)
        purgement = [c.mention for c in purgechannels]
        if len(purgement) > 0:
            purgelist = ", ".join(purgement)
        else:
            purgelist = purgement[0]
        await interaction.followup.send(f'{interaction.user.mention} has just purged the following channels: {purgelist}!', ephemeral=True)
    elif view.value == False:
        await interaction.followup.send('Interaction Cancelled. No messages have been purged!', ephemeral=True)
    else:
        await interaction.followup.send('Interaction Timed Out. No messages have been purged!', ephemeral=True)

@tree.command(
    name="purgeserver",
    description="Purges all unpinned messages in a server, excluding up to 25 channels (admin only)."
)
@app_commands.checks.has_permissions(administrator=True)
async def purgeserver(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True, ephemeral=True)
    guild = interaction.guild
    channels = guild.text_channels
    view = DropdownView()
    await interaction.followup.send("Which channels would you like to **exclude** from the purge? You must select at least 1 channel to exclude.", view=view, ephemeral=True)
    await view.wait()
    if view.value == True:
        excludedchannels = [c for c in view.values]
        purgechannels = [c for c in channels if c not in excludedchannels]
        for channel in purgechannels:
            messages = [message async for message in channel.history(limit=None)]
            unpinned = []
            for m in messages:
                if m.pinned == False:
                    unpinned.append(m)
            deleted = []
            if len(unpinned) > 0:
                deleted += await channel.purge(check=lambda message: message.pinned == False, oldest_first=True)
                if len(deleted) == 1:
                    await interaction.followup.send(f'{len(deleted)} message was just removed from {channel.mention}!', ephemeral=True)
                else:
                    await interaction.followup.send(f'{len(deleted)} messages were just removed from {channel.mention}!', ephemeral=True)
        await interaction.followup.send(f'{interaction.user.mention} has just purged the server!', ephemeral=True)
    elif view.value == False:
        await interaction.followup.send('Interaction Cancelled. No messages have been purged!', ephemeral=True)
    else:
        await interaction.followup.send('Interaction Timed Out. No messages have been purged!', ephemeral=True)

@client.event
async def on_message(message: discord.Message):
    list1 = ['lesbian','sapphic','wlw']
    list2 = ['gay','achillean','mlm']
    list3 = ['bisexual','biromantic','bi woman','bi women','bi lady','bi ladies','bi girl','bi gal','bi man','bi men','bi guy','bi dude','bi boy','bi person','bi people']
    list4 = ['asexual','aromantic','acespec','arospec','ace spec','aro spec','ace-spec','aro-spec']
    list5 = ['transgender','transsexual','trans woman','trans women','trans lady','trans ladies','trans girl','trans gal','trans man','trans men','trans guy','trans dude','trans boy','trans person','trans people']
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
    name="activityroles",
    description="Assigns all server members either an active or inactive role (admin only)."
)
@app_commands.describe(
    days="Set the number of days a member must be inactive before getting the inactive role.",
    inactive="Choose the role that you would like to give to inactive members.",
    active="Choose the role that you would like to give to active members."
)
@app_commands.checks.has_permissions(administrator=True)
async def activityroles(interaction: discord.Interaction, days: int, inactive: discord.Role, active: discord.Role):
    await interaction.response.defer(thinking=True, ephemeral=True)
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
        await interaction.followup.send(embed=embed, ephemeral=True)
    for member in inactivemembers:
        embed = discord.Embed(description=str(f"{member.mention} is inactive! They've been given the {inactive.mention} role if they didn't already have it."))
        await interaction.followup.send(embed=embed, ephemeral=True)

guilds = {}

@tree.command(
    name="addaward",
    description="Adds awards to the command user or another selected member."
)
@app_commands.describe(
    amount="Choose the number of awards to add (Default: 1).",
    member="Choose the member to add the awards to (Default: Self)."
)
async def addaward(interaction: discord.Interaction, amount: Optional[int] = None, member: Optional[discord.Member] = None):
    await interaction.response.defer(thinking=True, ephemeral=True)
    guild = interaction.guild
    amount = amount or 1
    user = member or interaction.user
    sing_low = awardset[gld.id]["singular_lower"] or "award"
    sing_cap = awardset[gld.id]["singular_caps"] or "Award"
    plur_low = awardset[gld.id]["plural_lower"] or "awards"
    moji = awardset[gld.id]["emoji"] or "🏅"
    if guild.id in guilds:
        if user.id in guilds[guild.id]:
            guilds[guild.id][user.id] += amount
            if guilds[guild.id][user.id] == 1:
                embed = discord.Embed(title=f"{moji} {plur_cap} Added {moji}", description=f"{user.mention} now has {guilds[guild.id][user.id]} {sing_low}!")
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(title=f"{moji} {plur_cap} Added {moji}", description=f"{user.mention} now has {guilds[guild.id][user.id]} {plur_low}!")
                await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            guilds[guild.id][user.id] = amount
            if guilds[guild.id][user.id] == 1:
                embed = discord.Embed(title=f"{moji} {plur_cap} Added {moji}", description=f"{user.mention} now has {guilds[guild.id][user.id]} {sing_low}!")
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(title=f"{moji} {plur_cap} Added {moji}", description=f"{user.mention} now has {guilds[guild.id][user.id]} {plur_low}!")
                await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        guilds[guild.id] = {}
        guilds[guild.id][user.id] = amount
        if guilds[guild.id][user.id] == 1:
            embed = discord.Embed(title=f"{moji} {plur_cap} Added {moji}", description=f"{user.mention} now has {guilds[guild.id][user.id]} {sing_low}!")
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title=f"{moji} {plur_cap} Added {moji}", description=f"{user.mention} now has {guilds[guild.id][user.id]} {plur_low}!")
            await interaction.followup.send(embed=embed, ephemeral=True)

@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.Member):
    msg = reaction.message
    gld = msg.guild
    mbr = msg.author
    sing_low = awardset[gld.id]["singular_lower"] or "award"
    sing_cap = awardset[gld.id]["singular_caps"] or "Award"
    plur_low = awardset[gld.id]["plural_lower"] or "awards"
    moji = awardset[gld.id]["emoji"] or "🏅"
    if str(reaction.emoji) == moji:
        if gld.id in guilds:
            if mbr.id in guilds[gld.id]:
                guilds[gld.id][mbr.id] += 1
                embed = discord.Embed(title=f"{moji} {sing_cap} Added {moji}", description=f"{user.mention} has added 1 {sing_low} to {mbr.mention}'s total via an emoji reaction. {mbr.mention}'s new total number of {plur_low} is {guilds[gld.id][mbr.id]}!")
                await msg.channel.send(embed=embed, reference=msg)
            else:
                guilds[gld.id][mbr.id] = 1
                embed = discord.Embed(title=f"{moji} {sing_cap} Added {moji}", description=f"{user.mention} has added 1 {sing_low} to {mbr.mention}'s total via an emoji reaction. {mbr.mention}'s new total number of {plur_low} is {guilds[gld.id][mbr.id]}!")
                await msg.channel.send(embed=embed, reference=msg)
        else:
            guilds[gld.id] = {}
            guilds[gld.id][mbr.id] = 1
            embed = discord.Embed(title=f"{moji} {sing_cap} Added {moji}", description=f"{user.mention} has added 1 {sing_low} to {mbr.mention}'s total via an emoji reaction. {mbr.mention}'s new total number of {plur_low} is {guilds[gld.id][mbr.id]}!")
            await msg.channel.send(embed=embed, reference=msg)

@tree.command(
    name="removeaward",
    description="Removes awards from the command user or another selected member."
)
@app_commands.describe(
    amount="Choose the number of awards to remove (Default: 1).",
    member="Choose the member to remove the awards from (Default: Self)."
)
async def removeaward(interaction: discord.Interaction, amount: Optional[int] = None, member: Optional[discord.Member] = None):
    await interaction.response.defer(thinking=True, ephemeral=True)
    guild = interaction.guild
    amount = amount or 1
    user = member or interaction.user
    sing_low = awardset[gld.id]["singular_lower"] or "award"
    sing_cap = awardset[gld.id]["singular_caps"] or "Award"
    plur_low = awardset[gld.id]["plural_lower"] or "awards"
    moji = awardset[gld.id]["emoji"] or "🏅"
    if guild.id in guilds:
        if user.id in guilds[guild.id]:
            if guilds[guild.id][user.id] == 0:
                embed = discord.Embed(title="Error", description=f"{user.mention} doesn't have any {plur_low}!")
                await interaction.followup.send(embed=embed, ephemeral=True)
            elif guilds[guild.id][user.id] < amount:
                embed = discord.Embed(title="Error", description=f"{user.mention} doesn't have enough {plur_low}!")
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                guilds[guild.id][user.id] -= amount
                if guilds[guild.id][user.id] == 0:
                    embed = discord.Embed(title=f"{moji} {plur_cap} Removed {moji}", description=f"{user.mention} no longer has any {plur_low}!")
                    await interaction.followup.send(embed=embed, ephemeral=True)
                elif guilds[guild.id][user.id] == 1:
                    embed = discord.Embed(title=f"{moji} {plur_cap} Removed {moji}", description=f"{user.mention} now has {guilds[guild.id][user.id]} {sing_low}!")
                    await interaction.followup.send(embed=embed, ephemeral=True)
                else:
                    embed = discord.Embed(title=f"{moji} {plur_cap} Removed {moji}", description=f"{user.mention} now has {guilds[guild.id][user.id]} {plur_low}!")
                    await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="Error", description=f"{user.mention} doesn't exist in the {sing_low} log.")
            await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(title="Error", description=f"{guild.name} doesn't exist in the {sing_low} log.")
        await interaction.followup.send(embed=embed, ephemeral=True)

@client.event
async def on_reaction_remove(reaction: discord.Reaction, user: discord.Member):
    msg = reaction.message
    gld = msg.guild
    mbr = msg.author
    sing_low = awardset[gld.id]["singular_lower"] or "award"
    sing_cap = awardset[gld.id]["singular_caps"] or "Award"
    plur_low = awardset[gld.id]["plural_lower"] or "awards"
    moji = awardset[gld.id]["emoji"] or "🏅"
    if str(reaction.emoji) == moji:
        if gld.id in guilds:
            if mbr.id in guilds[gld.id] and guilds[gld.id][mbr.id] >= 1:
                guilds[gld.id][mbr.id] -= 1
                embed = discord.Embed(title=f"{moji} {sing_cap} Removed {moji}", description=f"{user.mention} has removed 1 {sing_low} from {mbr.mention}'s total via an emoji unreaction. {mbr.mention}'s new total number of {plur_low} is {guilds[gld.id][mbr.id]}!")
                await msg.channel.send(embed=embed, reference=msg)

@tree.command(
    name="checkawards",
    description="Returns the number of awards that the user (or another selected user) currently has."
)
@app_commands.describe(
    member="Choose the member that you would like to check the number of awards for (Default: Self)."
)
async def checkawards(interaction: discord.Interaction, member: Optional[discord.Member] = None):
    await interaction.response.defer(thinking=True, ephemeral=True)
    guild = interaction.guild
    user = member or interaction.user
    sing_low = awardset[gld.id]["singular_lower"] or "award"
    sing_cap = awardset[gld.id]["singular_caps"] or "Award"
    plur_low = awardset[gld.id]["plural_lower"] or "awards"
    moji = awardset[gld.id]["emoji"] or "🏅"
    if guild.id in guilds:
        if user.id in guilds[guild.id]:
            if guilds[guild.id][user.id] == 0:
                embed = discord.Embed(title=f"{moji} Number of {plur_cap} {moji}", description=f"{user.mention} doesn't have any {plur_low}!")
                await interaction.followup.send(embed=embed, ephemeral=True)
            elif guilds[guild.id][user.id] == 1:
                embed = discord.Embed(title=f"{moji} Number of {plur_cap} {moji}", description=f"{user.mention} has {guilds[guild.id][user.id]} {sing_low}!")
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(title=f"{moji} Number of {plur_cap} {moji}", description=f"{user.mention} has {guilds[guild.id][user.id]} {plur_low}!")
                await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="Error", description=f"{user.mention} doesn't exist in the {sing_low} log.")
            await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        embed = discord.Embed(title="Error", description=f"{guild.name} doesn't exist in the {sing_low} log.")
        await interaction.followup.send(embed=embed, ephemeral=True)

@tree.command(
    name="clearawards",
    description="Clears all of the awards in the server."
)
async def clearawards(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    guild = interaction.guild
    sing_low = awardset[gld.id]["singular_lower"] or "award"
    sing_cap = awardset[gld.id]["singular_caps"] or "Award"
    plur_low = awardset[gld.id]["plural_lower"] or "awards"
    moji = awardset[gld.id]["emoji"] or "🏅"
    guilds[guild.id] = {}
    embed = discord.Embed(title=f"{moji} {plur_cap} Cleared {moji}", description=f"{guild.name} has had all its {plur_low} cleared!")
    await interaction.followup.send(embed=embed)

awardset = {}

@tree.command(
    name="setawards",
    description="Sets the name and emoji for the server awards."
)
@app_commands.describe(
    name_singular="Provide the singular form of the award name (Default: Award)",
    name_plural="Provide the plural form of the award name (Default: Awards)",
    emoji="Choose the emoji you would like to represent the award (Default: 🏅)."
)
async def setawards(interaction: discord.Interaction, name_singular: str, name_plural: str, emoji: str):
    await interaction.response.defer(thinking=True, ephemeral=True)
    guild = interaction.guild
    awardset[guild.id] = {}
    awardset[guild.id]["singular_lower"] = name_singular.lower()
    awardset[guild.id]["singular_caps"] = string.capwords(name_singular)
    awardset[guild.id]["plural_lower"] = name_plural.lower()
    awardset[guild.id]["plural_caps"] = string.capwords(name_plural)
    awardset[guild.id]["emoji"] = emoji
    sing_low = awardset[guild.id]["singular_lower"]
    sing_cap = awardset[guild.id]["singular_caps"]
    plur_low = awardset[guild.id]["plural_lower"]
    plur_cap = awardset[guild.id]["plural_caps"]
    moji = awardset[guild.id]["emoji"]
    embed = discord.Embed(title=f"{moji} {plur_cap} Set {moji}",description=f"The award name and emoji have been set!\n\n**Name** (singular, lowercase): {sing_low}\n\n**Name** (singular, capitalized): {sing_cap}\n\n**Name** (plural, lowercase): {plur_low}\n\n**Name** (plural, capitalized): {plur_cap}\n\n**Emoji**: {moji}")
    await interaction.followup.send(embed=embed, ephemeral=True)

@tree.command(
    name="leaderboard",
    description="Returns the current award leaderboard for the server."
)
async def leaderboard(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    guild = interaction.guild
    if guild.id in awardset:
        sing_low = awardset[guild.id]["singular_lower"] or "award"
        sing_cap = awardset[guild.id]["singular_caps"] or "Award"
        moji = awardset[guild.id]["emoji"] or "🏅"
    else:
        sing_low = "award"
        sing_cap = "Award"
        moji = "🏅"
    desc = []
    if guild.id in guilds:
        awardlog = dict(sorted(guilds[guild.id].items(), key=lambda item:item[1], reverse=True))
        for member, awards in awardlog.items():
            awards = awards * moji
            desc.append(f"<@{member}>:\n{awards}")
        description = "\n\n".join(x for x in desc)
        embed = discord.Embed(title=f"{moji} {sing_cap} Leaderboard {moji}", description=description)
        await interaction.followup.send(embed=embed)
    else:
        embed = discord.Embed(title="Error", description=f"{guild.name} doesn't exist in the {sing_low} log.")
        await interaction.followup.send(embed=embed, ephemeral=True)

profiles = {}

@tree.command(
    name="setprofile",
    description="Run this command to set up your member profile. Please note that all fields are optional."
)
@app_commands.describe(
    name="Provide your name or nickname.",
    age="Provide your age or age range.",
    location="Provide your continent, country, state, or city of residence.",
    pronouns="Provide your pronouns.",
    gender="Choose the option closest to your gender identity.",
    sexuality="Choose the option closest to your sexuality.",
    relationship_status="Choose the option closest to your relationship status.",
    family_planning_status="Choose the option closest to your family planning status."
)
@app_commands.choices(gender=[
    app_commands.Choice(name="Woman", value="Woman"),
    app_commands.Choice(name="GNC Woman", value="GNC Woman"),
    app_commands.Choice(name="Cisgender Woman", value="Cisgender Woman"),
    app_commands.Choice(name="Transgender Woman", value="Transgender Woman"),
    app_commands.Choice(name="Man", value="Man"),
    app_commands.Choice(name="GNC Man", value="GNC Man"),
    app_commands.Choice(name="Cisgender Man", value="Cisgender Man"),
    app_commands.Choice(name="Transgender Man", value="Transgender Man"),
    app_commands.Choice(name="Nonbinary", value="Nonbinary"),
    app_commands.Choice(name="Transfem Nonbinary", value="Transfem Nonbinary"),
    app_commands.Choice(name="Transmasc Nonbinary", value="Transmasc Nonbinary")
])
@app_commands.choices(sexuality=[
    app_commands.Choice(name="Lesbian", value="Lesbian"),
    app_commands.Choice(name="Aro-Spec/Ace-Spec Lesbian", value="Aro-Spec/Ace-Spec Lesbian"),
    app_commands.Choice(name="Gay", value="Gay"),
    app_commands.Choice(name="Aro-Spec/Ace-Spec Gay", value="Aro-Spec/Ace-Spec Gay"),
    app_commands.Choice(name="Bisexual", value="Bisexual"),
    app_commands.Choice(name="Aro-Spec/Ace-Spec Bisexual", value="Aro-Spec/Ace-Spec Bisexual"),
    app_commands.Choice(name="Straight", value="Straight"),
    app_commands.Choice(name="Aro-Spec/Ace-Spec Straight", value="Aro-Spec/Ace-Spec Straight"),
    app_commands.Choice(name="Aro-Spec/Ace-Spec", value="Aro-Spec/Ace-Spec")
])
@app_commands.choices(relationship_status=[
    app_commands.Choice(name="Happily Single", value="Happily Single"),
    app_commands.Choice(name="Single and Looking", value="Single and Looking"),
    app_commands.Choice(name="Dating Casually", value="Dating Casually"),
    app_commands.Choice(name="Dating Exclusively", value="Dating Exclusively"),
    app_commands.Choice(name="In an Open Relationship", value="In an Open Relationship"),
    app_commands.Choice(name="In a Closed Relationship", value="In a Closed Relationship"),
    app_commands.Choice(name="Married and Polyamorous", value="Married and Polyamorous"),
    app_commands.Choice(name="Married and Monogamous", value="Married and Monogamous")
])
@app_commands.choices(family_planning_status=[
    app_commands.Choice(name="Waiting to Try", value="Waiting to Try"),
    app_commands.Choice(name="Waiting to Try after Loss", value="Waiting to Try after Loss"),
    app_commands.Choice(name="Trying to Conceive", value="Trying to Conceive"),
    app_commands.Choice(name="Trying to Conceive after Loss", value="Trying to Conceive after Loss"),
    app_commands.Choice(name="Expecting", value="Expecting"),
    app_commands.Choice(name="Expecting after Loss", value="Expecting after Loss"),
    app_commands.Choice(name="Parenting", value="Parenting"),
    app_commands.Choice(name="Parenting after Loss", value="Parenting after Loss"),
    app_commands.Choice(name="Parenting and Waiting to Try", value="Parenting and Waiting to Try"),
    app_commands.Choice(name="Parenting and Trying to Conceive", value="Parenting and Trying to Conceive"),
    app_commands.Choice(name="Parenting and Expecting", value="Parenting and Expecting")
])
async def setprofile(interaction: discord.Interaction, name: Optional[str], age: Optional[str], location: Optional[str], pronouns: Optional[str], gender: Optional[str], sexuality: Optional[str], relationship_status: Optional[str], family_planning_status: Optional[str]):
    await interaction.response.defer(thinking=True, ephemeral=True)
    guild = interaction.guild
    member = interaction.user
    if guild in profiles:
        if member in profiles[guild]:
            if name == None:
                profiles[guild][member]["Name"] = profiles[guild][member]["Name"] or None
            else:
                profiles[guild][member]["Name"] = name
            if age == None:
                profiles[guild][member]["Age"] = profiles[guild][member]["Age"] or None
            else:
                profiles[guild][member]["Age"] = age
            if location == None:
                profiles[guild][member]["Location"] = profiles[guild][member]["Location"] or None
            else:
                profiles[guild][member]["Location"] = location
            if pronouns == None:
                profiles[guild][member]["Pronouns"] = profiles[guild][member]["Pronouns"] or None
            else:
                profiles[guild][member]["Pronouns"] = pronouns
            if gender == None:
                profiles[guild][member]["Gender"] = profiles[guild][member]["Gender"] or None
            else:
                profiles[guild][member]["Gender"] = gender
            if sexuality == None:
                profiles[guild][member]["Sexuality"] = profiles[guild][member]["Sexuality"] or None
            else:
                profiles[guild][member]["Sexuality"] = sexuality
            if relationship_status == None:
                profiles[guild][member]["Relationship Status"] = profiles[guild][member]["Relationship Status"] or None
            else:
                profiles[guild][member]["Relationship Status"] = relationship_status
            if family_planning_status == None:
                profiles[guild][member]["Family Planning Status"] = profiles[guild][member]["Family Planning Status"] or None
            else:
                profiles[guild][member]["Family Planning Status"] = family_planning_status
        else:
            profiles[guild][member] = {}
            profiles[guild][member]["Name"] = name or None
            profiles[guild][member]["Age"] = age or None
            profiles[guild][member]["Location"] = location or None
            profiles[guild][member]["Pronouns"] = pronouns or None
            profiles[guild][member]["Gender"] = gender or None
            profiles[guild][member]["Sexuality"] = sexuality or None
            profiles[guild][member]["Relationship Status"] = relationship_status or None
            profiles[guild][member]["Family Planning Status"] = family_planning_status or None
    else:
        profiles[guild] = {}
        profiles[guild][member] = {}
        profiles[guild][member]["Name"] = name or None
        profiles[guild][member]["Age"] = age or None
        profiles[guild][member]["Location"] = location or None
        profiles[guild][member]["Pronouns"] = pronouns or None
        profiles[guild][member]["Gender"] = gender or None
        profiles[guild][member]["Sexuality"] = sexuality or None
        profiles[guild][member]["Relationship Status"] = relationship_status or None
        profiles[guild][member]["Family Planning Status"] = family_planning_status or None
    name = profiles[guild][member]["Name"]
    age = profiles[guild][member]["Age"]
    location = profiles[guild][member]["Location"]
    pronouns = profiles[guild][member]["Pronouns"]
    gender = profiles[guild][member]["Gender"]
    sexuality = profiles[guild][member]["Sexuality"]
    relationship_status = profiles[guild][member]["Relationship Status"]
    family_planning_status = profiles[guild][member]["Family Planning Status"]
    embed = discord.Embed(color=member.accent_color)
    embed.set_author(name=member.name, icon_url=member.avatar)
    embed.add_field(name="Name", value=name, inline=True)
    embed.add_field(name="Age", value=age, inline=True)
    embed.add_field(name="Location", value=location, inline=True)
    embed.add_field(name="Pronouns", value=pronouns, inline=True)
    embed.add_field(name="Gender", value=gender, inline=True)
    embed.add_field(name="Sexuality", value=sexuality, inline=True)
    embed.add_field(name="Relationship Status", value=relationship_status, inline=True)
    embed.add_field(name="Family Planning Status", value=family_planning_status, inline=True)
    joined = discord.utils.format_dt(member.joined_at, style="R")
    embed.set_footer(text=f"Member of {guild.name} since {joined}.")
    await interaction.followup.send(embed=embed, ephemeral=True)

client.run('token')