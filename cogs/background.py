import discord
from discord.ext import commands
import aiosqlite
import datetime

bot = commands.Bot(
    command_prefix = 'rb!',
    description = "A multi-purpose Discord bot made by GitHub user gemhue.",
    intents = discord.Intents.all(),
    activity = discord.Activity(type=discord.ActivityType.listening, name="rb!help"),
    status = discord.Status.online
)

class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name="on_message")
    async def on_message(self, message: discord.Message):
        messagecont = message.content.lower()
        list1 = ['lesbian','dyke','sapphic','wlw']
        moji1 = bot.get_emoji(1274435288499884094)
        if any(x in messagecont for x in list1):
            await message.add_reaction(moji1)
        list2 = ['gay','queer','faggot','achillean','mlm']
        moji2 = bot.get_emoji(1274435330174615624)
        if any(x in messagecont for x in list2):
            await message.add_reaction(moji2)
        list3 = ['bisexual','biromantic','bi woman','bi women','bi lady','bi ladies','bi girl','bi gal','bi man','bi men','bi guy','bi dude','bi boy','bi person','bi people']
        moji3 = bot.get_emoji(1274435359878676560)
        if any(x in messagecont for x in list3):
            await message.add_reaction(moji3)
        list4 = ['asexual','aromantic','acespec','arospec','ace spec','aro spec','ace-spec','aro-spec']
        moji4 = bot.get_emoji(1274435406804291634)
        if any(x in messagecont for x in list4):
            await message.add_reaction(moji4)
        list5 = ['transgender','transsexual','trans woman','trans women','trans lady','trans ladies','trans girl','trans gal','trans man','trans men','trans guy','trans dude','trans boy','trans person','trans people']
        moji5 = bot.get_emoji(1274435448726622208)
        if any(x in messagecont for x in list5):
            await message.add_reaction(moji5)
        list6 = ['nonbinary','non binary','non-binary','enby']
        moji6 = bot.get_emoji(1274435483912638515)
        if any(x in messagecont for x in list6):
            await message.add_reaction(moji6)
        list7 = ['transfeminine','trans feminine','trans-feminine','transfem','trans fem','trans-fem']
        moji7 = bot.get_emoji(1274435557744840820)
        if any(x in messagecont for x in list7):
            await message.add_reaction(moji7)
        list8 = ['transmasculine','trans masculine','trans-masculine','transmasc','trans masc','trans-masc']
        moji8 = bot.get_emoji(1274435528883961989)
        if any(x in messagecont for x in list8):
            await message.add_reaction(moji8)
        await bot.process_commands(message)
        
    @commands.Cog.listener(name="on_member_join")
    async def on_member_join(self, member: discord.Member):
        guild = member.guild
        guild_id = guild.id
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            cur = await db.execute("SELECT welcome_channel_id FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            channel_id = row[0]
            cur = await db.execute("SELECT welcome_message FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            message = row[0]
            cur = await db.execute("SELECT join_role_id FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            role_id = row[0]
            cur = await db.execute("SELECT bot_join_role_id FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            botrole_id = row[0]
            await db.commit()
            await db.close()
        if channel_id is not None:
            channel = guild.get_channel(channel_id)
            if message is not None:
                embed = discord.Embed(color=member.accent_color, description=message, timestamp=datetime.now())
                content = f"-# {member.mention}"
                await channel.send(content=content, embed=embed)
            else:
                description = f"Welcome to {guild.name}, {member.mention}!"
                embed = discord.Embed(color=member.accent_color, description=description, timestamp=datetime.now())
                content = f"-# {member.mention}"
                await channel.send(content=content, embed=embed)
        if role_id is not None and not member.bot:
            role = guild.get_role(role_id)
            await member.add_roles(role)
        if botrole_id is not None and member.bot:
            botrole = guild.get_role(botrole_id)
            await member.add_roles(botrole)

    @commands.Cog.listener(name="on_member_remove")
    async def on_member_remove(self, member: discord.Member):
        guild = member.guild
        guild_id = guild.id
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            cur = await db.execute("SELECT goodbye_channel_id FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            channel_id = row[0]
            cur = await db.execute("SELECT goodbye_message FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            message = row[0]
            await db.commit()
            await db.close()
        if channel_id is not None:
            channel = guild.get_channel(channel_id)
            if message is not None:
                embed = discord.Embed(color=member.accent_color, description=message, timestamp=datetime.now())
                await channel.send(embed=embed)
            else:
                description = f"{member.mention} has just left {guild.name}!"
                embed = discord.Embed(color=member.accent_color, description=description, timestamp=datetime.now())
                await channel.send(embed=embed)