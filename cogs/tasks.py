import discord
import aiosqlite
import traceback
from discord.ext import commands, tasks
from datetime import datetime, timedelta, timezone

class BackgroundTasks(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        if isinstance(bot.database, aiosqlite.Connection):
            self.db = bot.database

    def cog_load(self):
        self.activity_check.start()

    def cog_unload(self):
        self.activity_check.cancel()

    @commands.Cog.listener(name="on_message")
    async def on_message(self, message: discord.Message):
        try:
            support_server = self.bot.get_guild(1289953061778882644)
            message_server = message.guild
            messagecont = message.content.lower()

            if isinstance(message_server, discord.Guild):
                await self.db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (message_server.id,))
                await self.db.commit()
            
            most_recent = None
            now = datetime.now(tz=timezone.utc)
            now_float = now.timestamp()

            # lesbian_triggers = ['lesbian','dyke','sapphic','wlw','woman loving woman','woman-loving-woman','women loving women','women-loving-women','wsw','women who have sex with women']
            # if any(x in messagecont for x in lesbian_triggers):
            if "lesbian" in messagecont:
                lesbian_heart = self.bot.get_emoji(1314630157767544852)
                if lesbian_heart is None:
                    if isinstance(support_server, discord.Guild):
                        lesbian_heart = support_server.get_emoji(1314677988373168249)
                if isinstance(message_server, discord.Guild):
                    cur = await self.db.execute("SELECT most_recent_lgbt_react FROM guilds WHERE guild_id = ?", (message_server.id,))
                    row = await cur.fetchone()
                    most_recent = row[0]
                if isinstance(most_recent, float):
                    recent_time = datetime.fromtimestamp(most_recent, tz=timezone.utc)
                    since_recent = now - recent_time
                    five_mins = timedelta(minutes=5.0)
                    if since_recent > five_mins:
                        await self.db.execute("UPDATE guilds SET most_recent_lgbt_react = ? WHERE guild_id = ?", (now_float, message_server.id))
                        await self.db.commit()
                        await message.add_reaction(lesbian_heart)
                else:
                    await self.db.execute("UPDATE guilds SET most_recent_lgbt_react = ? WHERE guild_id = ?", (now_float, message_server.id))
                    await self.db.commit()
                    await message.add_reaction(lesbian_heart)

            # gay_triggers = ['gay','queer','faggot','achillean','mlm','man loving man','man-loving-man','men loving men','men-loving-men','msm','men who have sex with men']
            # if any(x in messagecont for x in gay_triggers):
            if "gay" in messagecont:
                gay_heart = self.bot.get_emoji(1314630188700794981)
                if gay_heart is None:
                    if isinstance(support_server, discord.Guild):
                        gay_heart = support_server.get_emoji(1314677987165339688)
                if isinstance(message_server, discord.Guild):
                    cur = await self.db.execute("SELECT most_recent_lgbt_react FROM guilds WHERE guild_id = ?", (message_server.id,))
                    row = await cur.fetchone()
                    most_recent = row[0]
                if isinstance(most_recent, float):
                    recent_time = datetime.fromtimestamp(most_recent, tz=timezone.utc)
                    since_recent = now - recent_time
                    five_mins = timedelta(minutes=5.0)
                    if since_recent > five_mins:
                        await self.db.execute("UPDATE guilds SET most_recent_lgbt_react = ? WHERE guild_id = ?", (now_float, message_server.id))
                        await self.db.commit()
                        await message.add_reaction(gay_heart)
                else:
                    await self.db.execute("UPDATE guilds SET most_recent_lgbt_react = ? WHERE guild_id = ?", (now_float, message_server.id))
                    await self.db.commit()
                    await message.add_reaction(gay_heart)

            # bi_triggers = ['bisexual','biromantic','bi woman','bi women','bi wife','bi lady','bi ladies','bi girl','bi gal','bi man','bi men','bi husband','bi guy','bi dude','bi boy','bi person','bi people','bi partner']
            # if any(x in messagecont for x in bi_triggers):
            if "bisexual" in messagecont:
                bi_heart = self.bot.get_emoji(1314630214600495225)
                if bi_heart is None:
                    if isinstance(support_server, discord.Guild):
                        bi_heart = support_server.get_emoji(1314677984594235412)
                if isinstance(message_server, discord.Guild):
                    cur = await self.db.execute("SELECT most_recent_lgbt_react FROM guilds WHERE guild_id = ?", (message_server.id,))
                    row = await cur.fetchone()
                    most_recent = row[0]
                if isinstance(most_recent, float):
                    recent_time = datetime.fromtimestamp(most_recent, tz=timezone.utc)
                    since_recent = now - recent_time
                    five_mins = timedelta(minutes=5.0)
                    if since_recent > five_mins:
                        await self.db.execute("UPDATE guilds SET most_recent_lgbt_react = ? WHERE guild_id = ?", (now_float, message_server.id))
                        await self.db.commit()
                        await message.add_reaction(bi_heart)
                else:
                    await self.db.execute("UPDATE guilds SET most_recent_lgbt_react = ? WHERE guild_id = ?", (now_float, message_server.id))
                    await self.db.commit()
                    await message.add_reaction(bi_heart)

            # trans_triggers = ['transgender','trans-gender','transsexual','trans-sexual','tranny','trans woman','trans women','trans lady','trans ladies','trans girl','tgirl','t-girl','trans gal','trans man','trans men','trans guy','trans dude','trans boy','tboy','t-boy','trans person','trans people','transfeminine','transfem','transmasculine','transmasc','transneutral','transneu']
            # if any(x in messagecont for x in trans_triggers):
            if "transgender" in messagecont:
                trans_heart = self.bot.get_emoji(1314630240383012936)
                if trans_heart is None:
                    if isinstance(support_server, discord.Guild):
                        trans_heart = support_server.get_emoji(1314677990017466430)
                if isinstance(message_server, discord.Guild):
                    cur = await self.db.execute("SELECT most_recent_lgbt_react FROM guilds WHERE guild_id = ?", (message_server.id,))
                    row = await cur.fetchone()
                    most_recent = row[0]
                if isinstance(most_recent, float):
                    recent_time = datetime.fromtimestamp(most_recent, tz=timezone.utc)
                    since_recent = now - recent_time
                    five_mins = timedelta(minutes=5.0)
                    if since_recent > five_mins:
                        await self.db.execute("UPDATE guilds SET most_recent_lgbt_react = ? WHERE guild_id = ?", (now_float, message_server.id))
                        await self.db.commit()
                        await message.add_reaction(trans_heart)
                else:
                    await self.db.execute("UPDATE guilds SET most_recent_lgbt_react = ? WHERE guild_id = ?", (now_float, message_server.id))
                    await self.db.commit()
                    await message.add_reaction(trans_heart)

            # enby_triggers = ['nonbinary','nonbiney','non binary','non biney','non-binary','non-biney','enby','androgyne','neutrois','maverique','agender','bigender','multigender','polygender','pangender','demigender','demiwoman','demigirl','demiman','demiboy','genderfluid','genderflux','womanflux','girlflux','manflux','boyflux','genderqueer','x-gender']
            # if any(x in messagecont for x in enby_triggers):
            if "nonbinary" in messagecont:
                enby_heart = self.bot.get_emoji(1314630267364704319)
                if enby_heart is None:
                    if isinstance(support_server, discord.Guild):
                        enby_heart = support_server.get_emoji(1314677986007715912)
                if isinstance(message_server, discord.Guild):
                    cur = await self.db.execute("SELECT most_recent_lgbt_react FROM guilds WHERE guild_id = ?", (message_server.id,))
                    row = await cur.fetchone()
                    most_recent = row[0]
                if isinstance(most_recent, float):
                    recent_time = datetime.fromtimestamp(most_recent, tz=timezone.utc)
                    since_recent = now - recent_time
                    five_mins = timedelta(minutes=5.0)
                    if since_recent > five_mins:
                        await self.db.execute("UPDATE guilds SET most_recent_lgbt_react = ? WHERE guild_id = ?", (now_float, message_server.id))
                        await self.db.commit()
                        await message.add_reaction(enby_heart)
                else:
                    await self.db.execute("UPDATE guilds SET most_recent_lgbt_react = ? WHERE guild_id = ?", (now_float, message_server.id))
                    await self.db.commit()
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
                if isinstance(channel, discord.TextChannel):
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
                logging_channel = guild.get_channel(fetched_logging)
                if isinstance(logging_channel, discord.TextChannel):
                    log = discord.Embed(color=self.bot.blurple, title="Member Log", description=f"{member.mention} has just joined {guild.name}.")
                    if role is not None:
                        if role in member.roles:
                            log.add_field(name="Role Given", value=f"{role.mention}")
                    if botrole is not None:
                        if botrole in member.roles:
                            log.add_field(name="Role Given", value=f"{botrole.mention}")
                    log.set_author(name=member.display_name, icon_url=member.display_avatar)
                    log.set_thumbnail(url=member.display_avatar)
                    await logging_channel.send(embed=log)

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
                if isinstance(channel, discord.TextChannel):
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
                logging_channel = guild.get_channel(fetched_logging)
                if isinstance(logging_channel, discord.TextChannel):
                    log = discord.Embed(color=self.bot.blurple, title="Member Log", description=f"{member.mention} has just left {guild.name}.")
                    log.set_author(name=member.display_name, icon_url=member.display_avatar)
                    log.set_thumbnail(url=member.display_avatar)
                    await logging_channel.send(embed=log)

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
                        if isinstance(active, discord.Role):

                            cur = await self.db.execute("SELECT inactive_role_id FROM guilds WHERE guild_id = ?", (guild_id,))
                            row = await cur.fetchone()
                            inactive_id = row[0]
                            if inactive_id is not None:

                                inactive = guild.get_role(inactive_id)
                                if isinstance(inactive, discord.Role):

                                    now = datetime.now(tz=timezone.utc)
                                    setdays = timedelta(days=float(months*30))
                                    daysago = now-setdays
                                    members = [m for m in guild.members if not m.bot]
                                    newmembers = [m for m in members if m.joined_at >= daysago]
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
                                        if isinstance(member, discord.Member):
                                            if active not in member.roles:
                                                await member.add_roles(active)
                                            if inactive in member.roles:
                                                await member.remove_roles(inactive)
                                    for member in inactivemembers:
                                        if isinstance(member, discord.Member):
                                            if inactive not in member.roles:
                                                await member.add_roles(inactive)
                                            if active in member.roles:
                                                await member.remove_roles(active)
                                    
                                    cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild_id,))
                                    row = await cur.fetchone()
                                    fetched_logging = row[0]
                                    if fetched_logging is not None:
                                        logging_channel = guild.get_channel(fetched_logging)
                                        if isinstance(logging_channel, discord.TextChannel):
                                            now = datetime.now(tz=timezone.utc)
                                            log = discord.Embed(color=self.bot.blurple, title="Activity Roles Assigned", timestamp=now)
                                            log.add_field(name="Active Members", value=f"{len(activemembers)} members now have the {active.mention} role!", inline=False)
                                            log.add_field(name="Inactive Members", value=f"{len(inactivemembers)} members now have the {inactive.mention} role!", inline=False)
                                            await logging_channel.send(embed=log)

        except Exception as e:
            print(traceback.format_exc())
            cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            fetched_logging = row[0]
            if fetched_logging is not None:
                logging_channel = guild.get_channel(fetched_logging)
                if isinstance(logging_channel, discord.TextChannel):
                    now = datetime.now(tz=timezone.utc)
                    log = discord.Embed(color=self.bot.blurple, title="Activity Roles Assignment Error", description=f"{e}\n\nPlease check the following:", timestamp=now)
                    log.add_field(name="Bot Permissions", value="Does the bot have both the **read message history** and **manage roles** permissions?", inline=False)
                    log.add_field(name="Bot Role Position", value="Is the bot's highest role higher in the role hierarchy than both of the activity roles?", inline=False)
                    log.add_field(name="Kick & Reinvite", value="If the permissions and role positions seem to be in order, try kicking the bot and reinviting it. The bot's invite link is [here](https://discord.com/oauth2/authorize?client_id=1263872722195316737).", inline=False)
                    log.add_field(name="Report a Bug", value="If kicking & reinviting the bot also doesn't work, submit a bug report in the bot's support server. You can join the support server by following [this](https://discord.com/invite/5x3xBSdWbE) link.", inline=False)
                    await logging_channel.send(embed=log)

async def setup(bot: commands.Bot):
    print("Setting up Cog: tasks.BackgroundTasks")
    await bot.add_cog(BackgroundTasks(bot=bot), override=True)

async def teardown(bot: commands.Bot):
    print("Tearing down Cog: tasks.BackgroundTasks")
    await bot.remove_cog("BackgroundTasks")