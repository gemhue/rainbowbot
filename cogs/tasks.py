import discord
import traceback
from discord.ext import commands, tasks
from datetime import datetime, timedelta, timezone

class BackgroundTasks(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.database

    def cog_load(self):
        self.activity_check.start()

    def cog_unload(self):
        self.activity_check.cancel()

    @commands.Cog.listener(name="on_message")
    async def on_message(self, message: discord.Message):
        try:
            messagecont = message.content.lower()

            lesbian_triggers = ['lesbian','dyke','sapphic','wlw','woman loving woman','woman-loving-woman','women loving women','women-loving-women','wsw','women who have sex with women']
            if any(x in messagecont for x in lesbian_triggers):
                lesbian_heart = self.bot.get_emoji(1314630157767544852)
                await message.add_reaction(lesbian_heart)

            gay_triggers = ['gay','queer','faggot','achillean','mlm','man loving man','man-loving-man','men loving men','men-loving-men','msm','men who have sex with men']
            if any(x in messagecont for x in gay_triggers):
                gay_heart = self.bot.get_emoji(1314630188700794981)
                await message.add_reaction(gay_heart)

            bi_triggers = ['bisexual','biromantic','bi woman','bi women','bi wife','bi lady','bi ladies','bi girl','bi gal','bi man','bi men','bi husband','bi guy','bi dude','bi boy','bi person','bi people','bi partner']
            if any(x in messagecont for x in bi_triggers):
                bi_heart = self.bot.get_emoji(1314630214600495225)
                await message.add_reaction(bi_heart)

            trans_triggers = ['transgender','transsexual','tranny','trans woman','trans women','trans lady','trans ladies','trans girl','tgirl','t-girl','trans gal','trans man','trans men','trans guy','trans dude','trans boy','tboy','t-boy','trans person','trans people']
            if any(x in messagecont for x in trans_triggers):
                trans_heart = self.bot.get_emoji(1314630240383012936)
                await message.add_reaction(trans_heart)

            enby_triggers = ['nonbinary','non binary','non-binary','enby']
            if any(x in messagecont for x in enby_triggers):
                enby_heart = self.bot.get_emoji(1314630267364704319)
                await message.add_reaction(enby_heart)

        except Exception:
            print(traceback.format_exc())

        try:
            channel = message.channel
            ids = []
            cur = await self.db.execute("SELECT channel_id FROM autodelete")
            rows = await cur.fetchall()
            for row in rows:
                ids.append(row[0])
            for id in ids:
                if id == channel.id:
                    cur = await self.db.execute("SELECT interval FROM autodelete WHERE channel_id = ?", (id,))
                    row = await cur.fetchone()
                    interval = row[0]
                    if interval is not None:
                        minutes = timedelta(minutes=interval)
                        now = datetime.now(tz=timezone.utc)
                        delete_time = now + minutes
                        await discord.utils.sleep_until(delete_time)
                        await message.delete()
        
        except Exception:
            print(traceback.format_exc())
        
    @commands.Cog.listener(name="on_member_join")
    async def on_member_join(self, member: discord.Member):
        try:
                
            guild = member.guild
            await self.db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild.id,))
            await self.db.commit()
            
            cur = await self.db.execute("SELECT welcome_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            channel_id = row[0]
            if channel_id is not None:
                channel = guild.get_channel(channel_id)
                if channel is not None:
                    message = f"Welcome to {guild.name}, {member.mention}!"
                    time = datetime.now(tz=timezone.utc)
                    embed = discord.Embed(color=self.bot.blurple, description=f"{message}", timestamp=time)
                    embed.set_author(name=member.display_name, icon_url=member.display_avatar)
                    embed.set_thumbnail(url=member.display_avatar)
                    content = f"-# {member.mention}"
                    await channel.send(content=content, embed=embed)

            role = None
            cur = await self.db.execute("SELECT join_role_id FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            role_id = row[0]
            if role_id is not None and not member.bot:
                role = guild.get_role(role_id)
                if role is not None:
                    await member.add_roles(role)

            botrole = None
            cur = await self.db.execute("SELECT bot_role_id FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            botrole_id = row[0]
            if botrole_id is not None and member.bot:
                botrole = guild.get_role(botrole_id)
                if botrole is not None:
                    await member.add_roles(botrole)

            cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            fetched_logging = row[0]
            if fetched_logging is not None:
                logging = guild.get_channel(fetched_logging)
                if logging is not None:
                    log = discord.Embed(color=self.bot.blurple, title="Member Log", description=f"{member.mention} has just joined {guild.name}.")
                    if role is not None:
                        if role in member.roles:
                            log.add_field(name="Role Given", value=f"{role.mention}")
                    if botrole is not None:
                        if botrole in member.roles:
                            log.add_field(name="Role Given", value=f"{botrole.mention}")
                    log.set_author(name=member.display_name, icon_url=member.display_avatar)
                    log.set_thumbnail(url=member.display_avatar)
                    await logging.send(embed=embed)

        except Exception:
            print(traceback.format_exc())

    @commands.Cog.listener(name="on_member_remove")
    async def on_member_remove(self, member: discord.Member):
        try:
            
            guild = member.guild
            await self.db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild.id,))
            await self.db.commit()
            
            cur = await self.db.execute("SELECT goodbye_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            channel_id = row[0]
            if channel_id is not None:
                channel = guild.get_channel(channel_id)
                if channel is not None:
                    message = f"{member.mention} has just left {guild.name}. Goodbye for now!"
                    time = datetime.now(tz=timezone.utc)
                    embed = discord.Embed(color=self.bot.blurple, description=f"{message}", timestamp=time)
                    embed.set_author(name=member.display_name, icon_url=member.display_avatar)
                    embed.set_thumbnail(url=member.display_avatar)
                    content = f"-# {member.mention}"
                    await channel.send(content=content, embed=embed)

            cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            fetched_logging = row[0]
            if fetched_logging is not None:
                logging = guild.get_channel(fetched_logging)
                if logging is not None:
                    log = discord.Embed(color=self.bot.blurple, title="Member Log", description=f"{member.mention} has just left {guild.name}.")
                    log.set_author(name=member.display_name, icon_url=member.display_avatar)
                    log.set_thumbnail(url=member.display_avatar)
                    await logging.send(embed=embed)

        except Exception:
            print(traceback.format_exc())

    @tasks.loop(hours=24)
    async def activity_check(self):
        try:
            
            guilds = [guild for guild in self.bot.guilds]
            for guild in guilds:
                
                guild_id = guild.id
                await self.db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
                await self.db.commit()
                
                cur = await self.db.execute("SELECT inactive_months FROM guilds WHERE guild_id = ?", (guild_id,))
                row = await cur.fetchone()
                months = row[0]
                if months is not None:

                    cur = await self.db.execute("SELECT active_role_id FROM guilds WHERE guild_id = ?", (guild_id,))
                    row = await cur.fetchone()
                    active_id = row[0]
                    if active_id is not None:

                        active = guild.get_role(active_id)
                        if active is not None:

                            cur = await self.db.execute("SELECT inactive_role_id FROM guilds WHERE guild_id = ?", (guild_id,))
                            row = await cur.fetchone()
                            inactive_id = row[0]
                            if inactive_id is not None:

                                inactive = guild.get_role(inactive_id)
                                if inactive is not None:

                                    now = datetime.now(tz=timezone.utc)
                                    setdays = timedelta(days=float(months*30))
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
                                    
                                    cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild_id,))
                                    row = await cur.fetchone()
                                    fetched_logging = row[0]
                                    if fetched_logging is not None:
                                        logging = guild.get_channel(fetched_logging)
                                        if logging is not None:
                                            now = datetime.now(tz=timezone.utc)
                                            log = discord.Embed(color=self.bot.blurple, title="Activity Roles Assigned", timestamp=now)
                                            log.add_field(name="Active Members", value=f"{len(activemembers)} members now have the {active.mention} role!", inline=False)
                                            log.add_field(name="Inactive Members", value=f"{len(inactivemembers)} members now have the {inactive.mention} role!", inline=False)
                                            await logging.send(embed=log)

        except Exception:
            print(traceback.format_exc())

async def setup(bot: commands.Bot):
	await bot.add_cog(BackgroundTasks(bot=bot), override=True)

async def teardown(bot: commands.Bot):
    await bot.remove_cog("BackgroundTasks")