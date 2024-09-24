import discord
from discord.ext import commands
from typing import Optional
from datetime import datetime, timezone, timedelta

description = "A multi-purpose Discord bot made by GitHub user gemhue."
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='rb!', description=description, intents=intents)

guilds = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}! (ID: {bot.user.id})')

@bot.event
async def on_message(message: discord.Message):
    list1 = ['lesbian','sapphic','wlw']
    list2 = ['gay','achillean','mlm']
    list3 = ['bisexual','biromantic','bi woman','bi women','bi lady','bi ladies','bi girl','bi gal','bi man','bi men','bi guy','bi dude','bi boy','bi person','bi people']
    list4 = ['asexual','aromantic','acespec','arospec','ace spec','aro spec','ace-spec','aro-spec']
    list5 = ['transgender','transsexual','trans woman','trans women','trans lady','trans ladies','trans girl','trans gal','trans man','trans men','trans guy','trans dude','trans boy','trans person','trans people']
    list6 = ['nonbinary','non binary','non-binary','enby']
    list7 = ['transfeminine','trans feminine','trans-feminine','transfem','trans fem','trans-fem']
    list8 = ['transmasculine','trans masculine','trans-masculine','transmasc','trans masc','trans-masc']
    moji1 = bot.get_emoji(1274435288499884094)
    moji2 = bot.get_emoji(1274435330174615624)
    moji3 = bot.get_emoji(1274435359878676560)
    moji4 = bot.get_emoji(1274435406804291634)
    moji5 = bot.get_emoji(1274435448726622208)
    moji6 = bot.get_emoji(1274435483912638515)
    moji7 = bot.get_emoji(1274435557744840820)
    moji8 = bot.get_emoji(1274435528883961989)
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

@bot.event()
async def on_member_join(member):
    guild = member.guild
    channel = guilds[guild.id]["welcome"]
    message = guilds[guild.id]["welcome message"]
    role = guilds[guild.id]["join role"]
    botrole = guilds[guild.id]["bot role"]
    if channel is not None:
        if message is None:
            await channel.send(f"Welcome to {guild.name}, {member.mention}!")
        else:
            await channel.send(f"{message}")
    if role is not None and member.bot == False:
        await member.add_roles(role)
    if botrole is not None and member.bot == True:
        await member.add_roles(botrole)

@bot.event()
async def on_member_remove(member):
    guild = member.guild
    channel = guilds[guild.id]["goodbye"]
    message = guilds[guild.id]["goodbye message"]
    if channel is not None:
        if message is None:
            await channel.send(f"{member.mention} has just left {guild.name}!")
        else:
            await channel.send(f"{message}")

@bot.command()
@commands.is_owner()
async def sync(ctx):
    await bot.tree.sync()
    await ctx.send()

@bot.hybrid_command()
@commands.has_guild_permissions(administrator=True)
async def setchannels(ctx, logging_channel: Optional[discord.TextChannel], welcome_channel: Optional[discord.TextChannel], goodbye_channel: Optional[discord.TextChannel]):
    guild = ctx.guild
    guilds[guild.id]["logging"] = logging_channel
    guilds[guild.id]["welcome"] = welcome_channel
    guilds[guild.id]["goodbye"] = goodbye_channel
    await ctx.send(f"**Logging Channel**: {logging_channel}\n**Welcome Channel**: {welcome_channel}\n**Goodbye Channel**: {goodbye_channel}")

@bot.hybrid_command()
@commands.has_guild_permissions(administrator=True)
async def setwelcome(ctx, message: str):
    guild = ctx.guild
    guilds[guild.id]["welcome message"] = message
    await ctx.send(f"**Welcome Message**: {message}")

@bot.hybrid_command()
@commands.has_guild_permissions(administrator=True)
async def setgoodbye(ctx, message: str):
    guild = ctx.guild
    guilds[guild.id]["goodbye message"] = message
    await ctx.send(f"**Goodbye Message**: {message}")

@bot.hybrid_command()
@commands.has_guild_permissions(administrator=True)
async def setjoinrole(ctx, role: discord.Role, botrole: Optional[discord.Role]):
    guild = ctx.guild
    guilds[guild.id]["join role"] = role
    await ctx.send(f"**Join Role**: {role}")
    if botrole is not None:
        guilds[guild.id]["bot role"] = botrole
        await ctx.send(f"**Bot Role**: {botrole}")

@bot.hybrid_command()
@commands.has_guild_permissions(administrator=True)
async def activityroles(ctx, days: int, active: discord.Role, inactive: discord.Role):
    await ctx.defer(ephemeral=True)
    guild = ctx.guild
    channels = guild.text_channels
    members = [m for m in guild.members if not m.bot]
    today =  datetime.now(timezone.utc)
    setdays = timedelta(days=days)
    daysago = today-setdays
    newmembers = [m for m in members if m.joined_at < daysago]
    activemembers = []
    inactivemembers = []
    for channel in channels:
        async for message in channel.history(after=daysago):
            if message.author not in activemembers:
                activemembers.append(message.author)
    for member in members:
        if member not in newmembers and member not in activemembers:
            inactivemembers.append(member)
        elif member in newmembers and member not in activemembers:
            activemembers.append(member)
    for member in activemembers:
        if active not in member.roles:
            await member.add_roles(active)
        elif inactive in member.roles:
            await member.remove_roles(inactive)
    for member in inactivemembers:
        if inactive not in member.roles:
            await member.add_roles(inactive)
        elif active in member.roles:
            await member.remove_roles(active)
    activelen = len(activemembers)
    inactivelen = len(inactivemembers)
    await ctx.send(f"{activelen} members now have the {active} role!\n{inactivelen} members now have the {inactive} role!")

bot.run('token')