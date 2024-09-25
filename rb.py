import string
import discord
from discord import ChannelType
from discord.ui import ChannelSelect
from discord.ext import commands
from typing import Any, Optional
from datetime import datetime, timezone, timedelta

bot = commands.Bot(
    command_prefix='rb!',
    description="A multi-purpose Discord bot made by GitHub user gemhue.",
    intents=discord.Intents.all()
)

guilds = {}

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
        await interaction.response.defer(thinking=True, ephemeral=True)
        channels = [c.resolve() for c in self.values]
        channelment = [c.mention for c in channels]
        channellist = ", ".join(channelment)
        embed = discord.Embed(title="Selected Channels:", description=f'{channellist}')
        await interaction.followup.send(embed=embed, ephemeral=True)
        self.value = True
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey, row=2)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        self.stop()

class BackgroundTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        message = message.content.lower()
        list1 = ['lesbian','sapphic','wlw']
        moji1 = bot.get_emoji(1274435288499884094)
        if any(x in message for x in list1):
            await message.add_reaction(moji1)
        list2 = ['gay','achillean','mlm']
        moji2 = bot.get_emoji(1274435330174615624)
        if any(x in message for x in list2):
            await message.add_reaction(moji2)
        list3 = ['bisexual','biromantic','bi woman','bi women','bi lady','bi ladies','bi girl','bi gal','bi man','bi men','bi guy','bi dude','bi boy','bi person','bi people']
        moji3 = bot.get_emoji(1274435359878676560)
        if any(x in message for x in list3):
            await message.add_reaction(moji3)
        list4 = ['asexual','aromantic','acespec','arospec','ace spec','aro spec','ace-spec','aro-spec']
        moji4 = bot.get_emoji(1274435406804291634)
        if any(x in message for x in list4):
            await message.add_reaction(moji4)
        list5 = ['transgender','transsexual','trans woman','trans women','trans lady','trans ladies','trans girl','trans gal','trans man','trans men','trans guy','trans dude','trans boy','trans person','trans people']
        moji5 = bot.get_emoji(1274435448726622208)
        if any(x in message for x in list5):
            await message.add_reaction(moji5)
        list6 = ['nonbinary','non binary','non-binary','enby']
        moji6 = bot.get_emoji(1274435483912638515)
        if any(x in message for x in list6):
            await message.add_reaction(moji6)
        list7 = ['transfeminine','trans feminine','trans-feminine','transfem','trans fem','trans-fem']
        moji7 = bot.get_emoji(1274435557744840820)
        if any(x in message for x in list7):
            await message.add_reaction(moji7)
        list8 = ['transmasculine','trans masculine','trans-masculine','transmasc','trans masc','trans-masc']
        moji8 = bot.get_emoji(1274435528883961989)
        if any(x in message for x in list8):
            await message.add_reaction(moji8)
        await bot.process_commands(message)
        
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
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

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        guild = member.guild
        channel = guilds[guild.id]["goodbye"]
        message = guilds[guild.id]["goodbye message"]
        if channel is not None:
            if message is None:
                await channel.send(f"{member.mention} has just left {guild.name}!")
            else:
                await channel.send(f"{message}")

class SetupCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="Sync",
        description="Syncs the local command tree (bot owner only)."
    )
    @commands.is_owner()
    async def sync(self, ctx: commands.Context):
        await ctx.defer(thinking=True)
        guild = ctx.guild
        bot.tree.clear_commands(guild=guild)
        await bot.tree.sync(guild=guild)
        embed = discord.Embed(title="Update", description=f"The bot's local command tree has been synced!")
        await ctx.send(embed=embed)
    
    @commands.command(
        name="Global Sync",
        description="Syncs the global command tree (bot owner only)."
    )
    @commands.is_owner()
    async def globalsync(self, ctx: commands.Context):
        await ctx.defer(thinking=True)
        bot.tree.clear_commands(guild=None)
        await bot.tree.sync(guild=None)
        embed = discord.Embed(title="Update", description=f"The bot's global command tree has been synced!")
        await ctx.send(embed=embed)

    @commands.hybrid_command(
            name="Set Channels",
            description="Set the channels for logging messages, welcome messages, and goodbye messages."
    )
    @commands.has_guild_permissions(administrator=True)
    async def setchannels(self, ctx: commands.Context, logging_channel: Optional[discord.TextChannel], welcome_channel: Optional[discord.TextChannel], goodbye_channel: Optional[discord.TextChannel]):
        guild = ctx.guild
        guilds[guild.id]["logging"] = logging_channel
        guilds[guild.id]["welcome"] = welcome_channel
        guilds[guild.id]["goodbye"] = goodbye_channel
        await ctx.send(f"**Logging Channel**: {logging_channel}\n**Welcome Channel**: {welcome_channel}\n**Goodbye Channel**: {goodbye_channel}")

    @commands.hybrid_command(
            name="Set Welcome Message",
            description="Sets the welcome message for members who join the server."
    )
    @commands.has_guild_permissions(administrator=True)
    async def setwelcome(self, ctx: commands.Context, message: str):
        guild = ctx.guild
        guilds[guild.id]["welcome message"] = message
        await ctx.send(f"**Welcome Message**: {message}")

    @commands.hybrid_command(
            name="Set Goodbye Message",
            description="Sets the goodbye message for members who leave the server."
    )
    @commands.has_guild_permissions(administrator=True)
    async def setgoodbye(self, ctx: commands.Context, message: str):
        guild = ctx.guild
        guilds[guild.id]["goodbye message"] = message
        await ctx.send(f"**Goodbye Message**: {message}")

    @commands.hybrid_command(
            name="Set Join Roles",
            description="Sets the roles to give to new members who join the server."
    )
    @commands.has_guild_permissions(administrator=True)
    async def setjoinroles(self, ctx: commands.Context, role: discord.Role, botrole: Optional[discord.Role]):
        guild = ctx.guild
        guilds[guild.id]["join role"] = role
        await ctx.send(f"**Join Role**: {role}")
        if botrole is not None:
            guilds[guild.id]["bot role"] = botrole
            await ctx.send(f"**Bot Role**: {botrole}")

    @commands.hybrid_command(
            name="Activity Roles",
            description="Assigns an active role to active members and an inactive role to inactive members."
    )
    @commands.has_guild_permissions(administrator=True)
    async def activityroles(self, ctx: commands.Context, days: int, active: discord.Role, inactive: discord.Role):
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

class PurgeCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    @commands.has_guild_permissions(administrator=True)
    async def purgemember(self, ctx: commands.Context, member: discord.Member):
        await ctx.defer(thinking=True, ephemeral=True)
        view = DropdownView()
        await ctx.send(f"Which channel(s) would you like to purge {member.mention}'s messages from?", view=view, ephemeral=True)
        await view.wait()
        if view.value == True:
            purgechannels = [c for c in view.values]
            for channel in purgechannels:
                messages = [m async for m in channel.history(limit=None)]
                unpinned = [m for m in messages if not m.pinned]
                deleted = []
                while len(unpinned) > 0:
                    deleted += await channel.purge(check=lambda message: message.author == member and message.pinned == False, oldest_first=True)
                if len(deleted) == 1:
                    embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} message was just removed from {channel.mention}!')
                    await ctx.send(embed=embed, ephemeral=True)
                else:
                    embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} messages were just removed from {channel.mention}!')
                    await ctx.send(embed=embed, ephemeral=True)
        elif view.value == False:
            embed = discord.Embed(title="❌ Cancelled ❌", description=f'This interaction has been cancelled. No messages have been purged.')
            await ctx.send(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="⌛ Timed Out ⌛", description=f'This interaction has timed out. No messages have been purged.')
            await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command()
    @commands.has_guild_permissions(administrator=True)
    async def purgechannels(self, ctx: commands.Context):
        await ctx.defer(thinking=True, ephemeral=True)
        view = DropdownView()
        await ctx.send("Which channel(s) would you like to purge all unpinned messages from?", view=view, ephemeral=True)
        await view.wait()
        if view.value == True:
            purgechannels = [c for c in view.values]
            for channel in purgechannels:
                messages = [message async for message in channel.history(limit=None)]
                unpinned = [m for m in messages if not m.pinned]
                deleted = []
                while len(unpinned) > 0:
                    deleted += await channel.purge(check=lambda message: message.pinned == False, oldest_first=True)
                if len(deleted) == 1:
                    embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} message was just removed from {channel.mention}!')
                    await ctx.send(embed=embed, ephemeral=True)
                else:
                    embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} messages were just removed from {channel.mention}!')
                    await ctx.send(embed=embed, ephemeral=True)
        elif view.value == False:
            embed = discord.Embed(title="❌ Cancelled ❌", description=f'This interaction has been cancelled. No messages have been purged.')
            await ctx.send(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="⌛ Timed Out ⌛", description=f'This interaction has timed out. No messages have been purged.')
            await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command()
    @commands.has_guild_permissions(administrator=True)
    async def purgeserver(self, ctx: commands.Context):
        await ctx.defer(thinking=True, ephemeral=True)
        guild = ctx.guild
        channels = guild.text_channels
        view = DropdownView()
        await ctx.send("Which channels would you like to **exclude** from the purge? You must select at least 1 channel to exclude.", view=view, ephemeral=True)
        await view.wait()
        if view.value == True:
            excludedchannels = [c for c in view.values]
            purgechannels = [c for c in channels if c not in excludedchannels]
            for channel in purgechannels:
                messages = [message async for message in channel.history(limit=None)]
                unpinned = [m for m in messages if not m.pinned]
                deleted = []
                while len(unpinned) > 0:
                    deleted += await channel.purge(check=lambda message: message.pinned == False, oldest_first=True)
                if len(deleted) == 1:
                    embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} message was just removed from {channel.mention}!')
                    await ctx.send(embed=embed, ephemeral=True)
                else:
                    embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} messages were just removed from {channel.mention}!')
                    await ctx.send(embed=embed, ephemeral=True)
            await ctx.send(f'{ctx.user.mention} has just purged the server!', ephemeral=True)
        elif view.value == False:
            embed = discord.Embed(title="❌ Cancelled ❌", description=f'This interaction has been cancelled. No messages have been purged.')
            await ctx.send(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="⌛ Timed Out ⌛", description=f'This interaction has timed out. No messages have been purged.')
            await ctx.send(embed=embed, ephemeral=True)

class AwardCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command()
    @commands.has_guild_permissions(administrator=True)
    async def setawards(self, ctx: commands.Context, name_singular: str, name_plural: str, emoji: str):
        await ctx.defer(thinking=True, ephemeral=True)
        guild = ctx.guild
        guilds[guild.id] = {}
        guilds[guild.id]["singular_lower"] = name_singular.lower()
        guilds[guild.id]["singular_caps"] = string.capwords(name_singular)
        guilds[guild.id]["plural_lower"] = name_plural.lower()
        guilds[guild.id]["plural_caps"] = string.capwords(name_plural)
        guilds[guild.id]["emoji"] = emoji
        sing_low = guilds[guild.id]["singular_lower"]
        sing_cap = guilds[guild.id]["singular_caps"]
        plur_low = guilds[guild.id]["plural_lower"]
        plur_cap = guilds[guild.id]["plural_caps"]
        moji = guilds[guild.id]["emoji"]
        embed = discord.Embed(title=f"{moji} {plur_cap} Set {moji}",description=f"The award name and emoji have been set!\n\n**Name** (singular, lowercase): {sing_low}\n\n**Name** (singular, capitalized): {sing_cap}\n\n**Name** (plural, lowercase): {plur_low}\n\n**Name** (plural, capitalized): {plur_cap}\n\n**Emoji**: {moji}")
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command()
    @commands.has_guild_permissions(administrator=True)
    async def clearawards(self, ctx: commands.Context):
        await ctx.defer(thinking=True)
        guild = ctx.guild
        #sing_low = guilds[guild.id]["singular_lower"] or "award"
        #sing_cap = guilds[guild.id]["singular_caps"] or "Award"
        plur_low = guilds[guild.id]["plural_lower"] or "awards"
        plur_cap = guilds[guild.id]["plural_caps"] or "Awards"
        moji = guilds[guild.id]["emoji"] or "🏅"
        guilds[guild.id] = {}
        embed = discord.Embed(title=f"{moji} {plur_cap} Cleared {moji}", description=f"{guild.name} has had all its {plur_low} cleared!")
        await ctx.send(embed=embed)
    
    @commands.hybrid_command()
    @commands.has_guild_permissions(administrator=True)
    async def awardreactiontoggle(self, ctx: commands.Context, toggle: bool):
        guild = ctx.guild
        guilds[guild.id]["award_react_toggle"] = toggle

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.Member):
        message = reaction.message
        guild = message.guild
        if guilds[guild.id]["award_react_toggle"] == True:
            member = message.author
            sing_low = guilds[guild.id]["singular_lower"] or "award"
            sing_cap = guilds[guild.id]["singular_caps"] or "Award"
            plur_low = guilds[guild.id]["plural_lower"] or "awards"
            #plur_cap = guilds[guild.id]["plural_caps"] or "Awards"
            moji = guilds[guild.id]["emoji"] or "🏅"
            if str(reaction.emoji) == moji:
                if guild.id in guilds:
                    if member.id in guilds[guild.id]:
                        guilds[guild.id][member.id] += 1
                        embed = discord.Embed(title=f"{moji} {sing_cap} Added {moji}", description=f"{user.mention} has added 1 {sing_low} to {member.mention}'s total via an emoji reaction. {member.mention}'s new total number of {plur_low} is {guilds[guild.id][member.id]}!")
                        await message.channel.send(embed=embed, reference=message)
                    else:
                        guilds[guild.id][member.id] = 1
                        embed = discord.Embed(title=f"{moji} {sing_cap} Added {moji}", description=f"{user.mention} has added 1 {sing_low} to {member.mention}'s total via an emoji reaction. {member.mention}'s new total number of {plur_low} is {guilds[guild.id][member.id]}!")
                        await message.channel.send(embed=embed, reference=message)
                else:
                    guilds[guild.id] = {}
                    guilds[guild.id][member.id] = 1
                    embed = discord.Embed(title=f"{moji} {sing_cap} Added {moji}", description=f"{user.mention} has added 1 {sing_low} to {member.mention}'s total via an emoji reaction. {member.mention}'s new total number of {plur_low} is {guilds[guild.id][member.id]}!")
                    await message.channel.send(embed=embed, reference=message)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.Member):
        message = reaction.message
        guild = message.guild
        if guilds[guild.id]["award_react_toggle"] == True:
            member = message.author
            sing_low = guilds[guild.id]["singular_lower"] or "award"
            sing_cap = guilds[guild.id]["singular_caps"] or "Award"
            plur_low = guilds[guild.id]["plural_lower"] or "awards"
            #plur_cap = guilds[guild.id]["plural_caps"] or "Awards"
            moji = guilds[guild.id]["emoji"] or "🏅"
            if str(reaction.emoji) == moji:
                if guild.id in guilds:
                    if member.id in guilds[guild.id] and guilds[guild.id][member.id] >= 1:
                        guilds[guild.id][member.id] -= 1
                        embed = discord.Embed(title=f"{moji} {sing_cap} Removed {moji}", description=f"{user.mention} has removed 1 {sing_low} from {member.mention}'s total via an emoji unreaction. {member.mention}'s new total number of {plur_low} is {guilds[guild.id][member.id]}!")
                        await message.channel.send(embed=embed, reference=message)

    @commands.hybrid_command()
    async def addaward(self, ctx: commands.Context, amount: Optional[int] = None, member: Optional[discord.Member] = None):
        await ctx.defer(thinking=True, ephemeral=True)
        guild = ctx.guild
        amount = amount or 1
        member = member or ctx.user
        sing_low = guilds[guild.id]["singular_lower"] or "award"
        #sing_cap = guilds[guild.id]["singular_caps"] or "Award"
        plur_low = guilds[guild.id]["plural_lower"] or "awards"
        plur_cap = guilds[guild.id]["plural_caps"] or "Awards"
        moji = guilds[guild.id]["emoji"] or "🏅"
        if guild.id in guilds:
            if member.id in guilds[guild.id]:
                guilds[guild.id][member.id] += amount
                if guilds[guild.id][member.id] == 1:
                    embed = discord.Embed(title=f"{moji} {plur_cap} Added {moji}", description=f"{member.mention} now has {guilds[guild.id][member.id]} {sing_low}!")
                    await ctx.send(embed=embed, ephemeral=True)
                else:
                    embed = discord.Embed(title=f"{moji} {plur_cap} Added {moji}", description=f"{member.mention} now has {guilds[guild.id][member.id]} {plur_low}!")
                    await ctx.send(embed=embed, ephemeral=True)
            else:
                guilds[guild.id][member.id] = amount
                if guilds[guild.id][member.id] == 1:
                    embed = discord.Embed(title=f"{moji} {plur_cap} Added {moji}", description=f"{member.mention} now has {guilds[guild.id][member.id]} {sing_low}!")
                    await ctx.send(embed=embed, ephemeral=True)
                else:
                    embed = discord.Embed(title=f"{moji} {plur_cap} Added {moji}", description=f"{member.mention} now has {guilds[guild.id][member.id]} {plur_low}!")
                    await ctx.send(embed=embed, ephemeral=True)
        else:
            guilds[guild.id] = {}
            guilds[guild.id][member.id] = amount
            if guilds[guild.id][member.id] == 1:
                embed = discord.Embed(title=f"{moji} {plur_cap} Added {moji}", description=f"{member.mention} now has {guilds[guild.id][member.id]} {sing_low}!")
                await ctx.send(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(title=f"{moji} {plur_cap} Added {moji}", description=f"{member.mention} now has {guilds[guild.id][member.id]} {plur_low}!")
                await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command()
    async def removeaward(self, ctx: commands.Context, amount: Optional[int] = None, member: Optional[discord.Member] = None):
        await ctx.defer(thinking=True, ephemeral=True)
        guild = ctx.guild
        amount = amount or 1
        member = member or ctx.user
        sing_low = guilds[guild.id]["singular_lower"] or "award"
        #sing_cap = guilds[guild.id]["singular_caps"] or "Award"
        plur_low = guilds[guild.id]["plural_lower"] or "awards"
        plur_cap = guilds[guild.id]["plural_caps"] or "Awards"
        moji = guilds[guild.id]["emoji"] or "🏅"
        if guild.id in guilds:
            if member.id in guilds[guild.id]:
                if guilds[guild.id][member.id] == 0:
                    embed = discord.Embed(title="Error", description=f"{member.mention} doesn't have any {plur_low}!")
                    await ctx.send(embed=embed, ephemeral=True)
                elif guilds[guild.id][member.id] < amount:
                    embed = discord.Embed(title="Error", description=f"{member.mention} doesn't have enough {plur_low}!")
                    await ctx.send(embed=embed, ephemeral=True)
                else:
                    guilds[guild.id][member.id] -= amount
                    if guilds[guild.id][member.id] == 0:
                        embed = discord.Embed(title=f"{moji} {plur_cap} Removed {moji}", description=f"{member.mention} no longer has any {plur_low}!")
                        await ctx.send(embed=embed, ephemeral=True)
                    elif guilds[guild.id][member.id] == 1:
                        embed = discord.Embed(title=f"{moji} {plur_cap} Removed {moji}", description=f"{member.mention} now has {guilds[guild.id][member.id]} {sing_low}!")
                        await ctx.send(embed=embed, ephemeral=True)
                    else:
                        embed = discord.Embed(title=f"{moji} {plur_cap} Removed {moji}", description=f"{member.mention} now has {guilds[guild.id][member.id]} {plur_low}!")
                        await ctx.send(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(title="Error", description=f"{member.mention} doesn't exist in the {sing_low} log.")
                await ctx.send(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="Error", description=f"{guild.name} doesn't exist in the {sing_low} log.")
            await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command()
    async def checkawards(self, ctx: commands.Context, member: Optional[discord.Member] = None):
        await ctx.defer(thinking=True, ephemeral=True)
        guild = ctx.guild
        member = member or ctx.user
        sing_low = guilds[guild.id]["singular_lower"] or "award"
        #sing_cap = guilds[guild.id]["singular_caps"] or "Award"
        plur_low = guilds[guild.id]["plural_lower"] or "awards"
        plur_cap = guilds[guild.id]["plural_caps"] or "Awards"
        moji = guilds[guild.id]["emoji"] or "🏅"
        if guild.id in guilds:
            if member.id in guilds[guild.id]:
                if guilds[guild.id][member.id] == 0:
                    embed = discord.Embed(title=f"{moji} Number of {plur_cap} {moji}", description=f"{member.mention} doesn't have any {plur_low}!")
                    await ctx.send(embed=embed, ephemeral=True)
                elif guilds[guild.id][member.id] == 1:
                    embed = discord.Embed(title=f"{moji} Number of {plur_cap} {moji}", description=f"{member.mention} has {guilds[guild.id][member.id]} {sing_low}!")
                    await ctx.send(embed=embed, ephemeral=True)
                else:
                    embed = discord.Embed(title=f"{moji} Number of {plur_cap} {moji}", description=f"{member.mention} has {guilds[guild.id][member.id]} {plur_low}!")
                    await ctx.send(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(title="Error", description=f"{member.mention} doesn't exist in the {sing_low} log.")
                await ctx.send(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="Error", description=f"{guild.name} doesn't exist in the {sing_low} log.")
            await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command()
    async def leaderboard(self, ctx: commands.Context):
        await ctx.defer(thinking=True)
        guild = ctx.guild
        sing_low = guilds[guild.id]["singular_lower"] or "award"
        sing_cap = guilds[guild.id]["singular_caps"] or "Award"
        #plur_low = guilds[guild.id]["plural_lower"] or "awards"
        #plur_cap = guilds[guild.id]["plural_caps"] or "Awards"
        moji = guilds[guild.id]["emoji"] or "🏅"
        desc = []
        if guild.id in guilds:
            awardlog = dict(sorted(guilds[guild.id].items(), key=lambda item:item[1], reverse=True))
            for member, awards in awardlog.items():
                awards = awards * moji
                desc.append(f"<@{member}>:\n{awards}")
            description = "\n\n".join(x for x in desc)
            embed = discord.Embed(title=f"{moji} {sing_cap} Leaderboard {moji}", description=description)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Error", description=f"{guild.name} doesn't exist in the {sing_low} log.")
            await ctx.send(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(BackgroundTasks(bot), override=True)
    await bot.add_cog(SetupCommands(bot), override=True)
    await bot.add_cog(PurgeCommands(bot), override=True)
    await bot.add_cog(AwardCommands(bot), override=True)

@bot.event
async def on_ready():
    await setup()
    print(f'Logged in as {bot.user}! (ID: {bot.user.id})')

bot.run('token')
