import discord
from discord.ext import commands
import aiosqlite
from datetime import datetime

class BackgroundTasks(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener(name="on_message")
    async def on_message(self, message: discord.Message):
        messagecont = message.content.lower()
        list1 = ['lesbian','dyke','sapphic','wlw']
        moji1 = self.bot.get_emoji(1274435288499884094)
        if any(x in messagecont for x in list1):
            await message.add_reaction(moji1)
        list2 = ['gay','queer','faggot','achillean','mlm']
        moji2 = self.bot.get_emoji(1274435330174615624)
        if any(x in messagecont for x in list2):
            await message.add_reaction(moji2)
        list3 = ['bisexual','biromantic','bi woman','bi women','bi lady','bi ladies','bi girl','bi gal','bi man','bi men','bi guy','bi dude','bi boy','bi person','bi people']
        moji3 = self.bot.get_emoji(1274435359878676560)
        if any(x in messagecont for x in list3):
            await message.add_reaction(moji3)
        list4 = ['asexual','aromantic','acespec','arospec','ace spec','aro spec','ace-spec','aro-spec']
        moji4 = self.bot.get_emoji(1274435406804291634)
        if any(x in messagecont for x in list4):
            await message.add_reaction(moji4)
        list5 = ['transgender','transsexual','trans woman','trans women','trans lady','trans ladies','trans girl','trans gal','trans man','trans men','trans guy','trans dude','trans boy','trans person','trans people']
        moji5 = self.bot.get_emoji(1274435448726622208)
        if any(x in messagecont for x in list5):
            await message.add_reaction(moji5)
        list6 = ['nonbinary','non binary','non-binary','enby']
        moji6 = self.bot.get_emoji(1274435483912638515)
        if any(x in messagecont for x in list6):
            await message.add_reaction(moji6)
        list7 = ['transfeminine','trans feminine','trans-feminine','transfem','trans fem','trans-fem']
        moji7 = self.bot.get_emoji(1274435557744840820)
        if any(x in messagecont for x in list7):
            await message.add_reaction(moji7)
        list8 = ['transmasculine','trans masculine','trans-masculine','transmasc','trans masc','trans-masc']
        moji8 = self.bot.get_emoji(1274435528883961989)
        if any(x in messagecont for x in list8):
            await message.add_reaction(moji8)
        
    @commands.Cog.listener(name="on_member_join")
    async def on_member_join(self, member: discord.Member):
        async with aiosqlite.connect('rainbowbot.db') as db:
            guild = member.guild
            guild_id = guild.id
            await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            cur = await db.execute("SELECT welcome_channel_id FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            channel_id = row[0]
            if channel_id is not None:
                cur = await db.execute("SELECT welcome_message FROM guilds WHERE guild_id = ?", (guild_id,))
                row = await cur.fetchone()
                message = row[0]
                if message is None:
                    message = f"Welcome to {guild.name}, {member.mention}!"
                color = member.accent_color
                time = datetime.now()
                embed = discord.Embed(color=color, description=message, timestamp=time)
                avatar = member.display_avatar
                embed.set_thumbnail(url=avatar)
                channel = guild.get_channel(channel_id)
                content = f"-# {member.mention}"
                await channel.send(content=content, embed=embed)
            cur = await db.execute("SELECT join_role_id FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            role_id = row[0]
            if role_id is not None and not member.bot:
                role = guild.get_role(role_id)
                await member.add_roles(role)
            cur = await db.execute("SELECT bot_join_role_id FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            botrole_id = row[0]
            if botrole_id is not None and member.bot:
                botrole = guild.get_role(botrole_id)
                await member.add_roles(botrole)
            await db.commit()
            await db.close()

    @commands.Cog.listener(name="on_member_remove")
    async def on_member_remove(self, member: discord.Member):
        async with aiosqlite.connect('rainbowbot.db') as db:
            guild = member.guild
            guild_id = guild.id
            await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            cur = await db.execute("SELECT goodbye_channel_id FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            channel_id = row[0]
            if channel_id is not None:
                cur = await db.execute("SELECT goodbye_message FROM guilds WHERE guild_id = ?", (guild_id,))
                row = await cur.fetchone()
                message = row[0]
                if message is None:
                    message = f"{member.mention} has just left {guild.name}!"
                color = member.accent_color
                time = datetime.now()
                embed = discord.Embed(color=color, description=message, timestamp=time)
                avatar = member.display_avatar
                embed.set_thumbnail(url=avatar)
                channel = guild.get_channel(channel_id)
                content = f"-# {member.mention}"
                await channel.send(content=content, embed=embed)
            await db.commit()
            await db.close()

async def setup(bot: commands.Bot):
	await bot.add_cog(BackgroundTasks(bot), override=True)