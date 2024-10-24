import discord
from discord.ext import commands, tasks
import aiosqlite
from datetime import datetime, timedelta, timezone

class BackgroundTasks(commands.Cog):
    def __init__(self, bot: commands.Bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.blurple = discord.Colour.blurple()

    def cog_load(self):
        self.activity_check.start()
        return super().cog_load()

    def cog_unload(self):
        self.activity_check.cancel()
        return super().cog_unload()

    @commands.Cog.listener(name="on_message")
    async def on_message(self, message: discord.Message):
        try:
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
        except Exception as e:
            print(f"On Message Error: {e}")
        
    @commands.Cog.listener(name="on_member_join")
    async def on_member_join(self, member: discord.Member):
        try:
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
                    embed = discord.Embed(color=color, description=f"{message}", timestamp=time)
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
        except Exception as e:
            print(f"On Member Join Error: {e}")

    @commands.Cog.listener(name="on_member_remove")
    async def on_member_remove(self, member: discord.Member):
        try:
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
                    embed = discord.Embed(color=color, description=f"{message}", timestamp=time)
                    avatar = member.display_avatar
                    embed.set_thumbnail(url=avatar)
                    channel = guild.get_channel(channel_id)
                    content = f"-# {member.mention}"
                    await channel.send(content=content, embed=embed)
                await db.commit()
                await db.close()
        except Exception as e:
            print(f"On Member Remove Error: {e}")

    @tasks.loop(hours=24)
    async def activity_check(self):
        try:
            async with aiosqlite.connect('rainbowbot.db') as db:
                guilds = [guild for guild in self.bot.guilds]
                for guild in guilds:
                    guild_id = guild.id
                    await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
                    cur = await db.execute("SELECT inactive_days FROM guilds WHERE guild_id = ?", (guild_id,))
                    row = await cur.fetchone()
                    days = row[0]
                    if days is not None:
                        cur = await db.execute("SELECT active_role_id FROM guilds WHERE guild_id = ?", (guild_id,))
                        row = await cur.fetchone()
                        active_id = row[0]
                        if active_id is not None:
                            active = guild.get_role(active_id)
                            cur = await db.execute("SELECT inactive_role_id FROM guilds WHERE guild_id = ?", (guild_id,))
                            row = await cur.fetchone()
                            inactive_id = row[0]
                            if inactive_id is not None:
                                inactive = guild.get_role(inactive_id)
                                now = datetime.now(tz=timezone.utc)
                                setdays = timedelta(days=float(days))
                                daysago = now-setdays
                                members = [m for m in guild.members if not m.bot]
                                newmembers = [m for m in members if m.joined_at < daysago]
                                activemembers = []
                                inactivemembers = []
                                channels = guild.text_channels
                                for channel in channels:
                                    async for message in channel.history(after=daysago):
                                        if message.author in members and message.author not in activemembers:
                                            activemembers.append(message.author)
                                for member in members:
                                    if member not in newmembers and member not in activemembers:
                                        inactivemembers.append(member)
                                    if member in newmembers and member not in activemembers:
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
                                cur = await db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild_id,))
                                row = await cur.fetchone()
                                fetched_logging = row[0]
                                if fetched_logging is not None:
                                    logging = guild.get_channel(fetched_logging)
                                    embed = discord.Embed(color=self.blurple, title="Activity Roles Assigned", timestamp=now)
                                    embed.add_field(name="Active Members", value=f"{len(activemembers)} members now have the {active.mention} role!", inline=False)
                                    embed.add_field(name="Inactive Members", value=f"{len(inactivemembers)} members now have the {inactive.mention} role!", inline=False)
                                    await logging.send(embed=embed)
                await db.commit()
                await db.close()
        except Exception as e:
            print(f"Activity Check Error: {e}")

async def setup(bot: commands.Bot):
	await bot.add_cog(BackgroundTasks(bot), override=True)