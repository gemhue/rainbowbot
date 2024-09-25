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
        super().__init__(channel_types=[ChannelType.text], placeholder="Select channels... (Limit: 25)", row=1)

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
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red, row=2)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.value = False
        self.stop()

class BackgroundTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name="emoji_reactions")
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
        
    @commands.Cog.listener(name="member_join")
    async def on_member_join(self, member: discord.Member):
        guild = member.guild
        channel = guilds[guild.id]["welcome channel"]
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

    @commands.Cog.listener(name="member_remove")
    async def on_member_remove(self, member: discord.Member):
        guild = member.guild
        channel = guilds[guild.id]["goodbye channel"]
        message = guilds[guild.id]["goodbye message"]
        if channel is not None:
            if message is None:
                await channel.send(f"{member.mention} has just left {guild.name}!")
            else:
                await channel.send(f"{message}")

class SetupCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sync")
    @commands.is_owner()
    async def sync(self, ctx: commands.Context):
        """Syncs the local command tree (bot owner only).
        """
        await ctx.defer()
        guild = ctx.guild
        await bot.tree.sync(guild=guild)
        embed = discord.Embed(title="Update", description=f"The bot's local command tree has been synced!")
        await ctx.send(embed=embed)
    
    @commands.command(name="globalsync")
    @commands.is_owner()
    async def globalsync(self, ctx: commands.Context):
        """Syncs the global command tree (bot owner only).
        """
        await ctx.defer()
        await bot.tree.sync(guild=None)
        embed = discord.Embed(title="Update", description=f"The bot's global command tree has been synced!")
        await ctx.send(embed=embed)

    @commands.hybrid_command(name="setchannels")
    @commands.has_guild_permissions(administrator=True)
    async def setchannels(self, ctx: commands.Context, logging_channel: Optional[discord.TextChannel], welcome_channel: Optional[discord.TextChannel], goodbye_channel: Optional[discord.TextChannel]):
        """Sets the channels for logging messages, welcome messages, and goodbye messages.

        Parameters
        -----------
        logging_channel : discord.TextChannel, optional
            Set the channels for logging messages.
        welcome_channel : discord.TextChannel, optional
            Set the channels for welcome messages.
        goodbye_channel : discord.TextChannel, optional
            Set the channels for goodbye messages.
        """
        guild = ctx.guild
        if guild in guilds:
            guilds[guild.id]["logging channel"] = logging_channel
            guilds[guild.id]["welcome channel"] = welcome_channel
            guilds[guild.id]["goodbye channel"] = goodbye_channel
        else:
            guilds[guild.id] = {}
            guilds[guild.id]["logging channel"] = logging_channel
            guilds[guild.id]["welcome channel"] = welcome_channel
            guilds[guild.id]["goodbye channel"] = goodbye_channel
        await ctx.send(f"**Logging Channel**: {logging_channel}\n**Welcome Channel**: {welcome_channel}\n**Goodbye Channel**: {goodbye_channel}")

    @commands.hybrid_command(name="setwelcome")
    @commands.has_guild_permissions(administrator=True)
    async def setwelcome(self, ctx: commands.Context, message: str):
        """Sets the welcome message for members who leave the server.

        Parameters
        -----------
        message : str
            Set the welcome message for members who leave the server.
        """
        guild = ctx.guild
        if guild.id in guilds:
            guilds[guild.id]["welcome message"] = message
        else:
            guilds[guild.id] = {}
            guilds[guild.id]["welcome message"] = message
        await ctx.send(f"**Welcome Message**: {message}")

    @commands.hybrid_command(name="setgoodbye")
    @commands.has_guild_permissions(administrator=True)
    async def setgoodbye(self, ctx: commands.Context, message: str):
        """Sets the goodbye message for members who leave the server.

        Parameters
        -----------
        message : str
            Set the goodbye message for members who leave the server.
        """
        guild = ctx.guild
        if guild.id in guilds:
            guilds[guild.id]["goodbye message"] = message
        else:
            guilds[guild.id] = {}
            guilds[guild.id]["goodbye message"] = message
        await ctx.send(f"**Goodbye Message**: {message}")

    @commands.hybrid_command(name="setjoinroles")
    @commands.has_guild_permissions(administrator=True)
    async def setjoinroles(self, ctx: commands.Context, role: discord.Role, botrole: Optional[discord.Role]):
        """Sets the roles to give to new members who join the server.

        Parameters
        -----------
        role : discord.Role
            Choose the role that you would like to give to new members on join.
        botrole : discord.Role, optional
            Choose the role that you would like to give to new bots on join.
        """
        guild = ctx.guild
        if guild.id in guilds:  
            guilds[guild.id]["join role"] = role
            message = await ctx.send(f"**Join Role**: {role}")
            if botrole is not None:
                guilds[guild.id]["bot role"] = botrole
                await message.edit(f"**Join Role**: {role}\n\n**Bot Role**: {botrole}")
        else:
            guilds[guild.id] = {}
            guilds[guild.id]["join role"] = role
            message = await ctx.send(f"**Join Role**: {role}")
            if botrole is not None:
                guilds[guild.id]["bot role"] = botrole
                await message.edit(f"**Join Role**: {role}\n\n**Bot Role**: {botrole}")

    @commands.hybrid_command(name="activityroles")
    @commands.has_guild_permissions(administrator=True)
    async def activityroles(self, ctx: commands.Context, days: int, active: discord.Role, inactive: discord.Role):
        """Assigns an active role to active members and an inactive role to inactive members.

        Parameters
        -----------
        days : int
            Set the number of days a member must be inactive before getting the inactive role.
        inactive : discord.Role
            Choose the role that you would like to give to inactive members.
        active : discord.Role
            Choose the role that you would like to give to active members.
        """
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
        await ctx.send(f"{len(activemembers)} members now have the {active} role!\n{len(inactivemembers)} members now have the {inactive} role!")

class PurgeCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="purgemember")
    @commands.has_guild_permissions(administrator=True)
    async def purgemember(self, ctx: commands.Context, member: discord.Member):
        """Purge all of a member's unpinned messages in a set list of up to 25 channels. (Admin Only)

        Parameters
        -----------
        member : discord.Member
            Provide the member who's unpinned messages you would like to purge.
        """
        await ctx.defer()
        view = DropdownView()
        embed = discord.Embed(title="🗑️ Purge Member 🗑️", description=f"Which channel(s) would you like to purge {member.mention}'s unpinned messages from?")
        response = await ctx.send(embed=embed, view=view)
        await view.wait()
        if view.value == True:
            selected = [c.resolve() for c in view.values]
            mentions = [c.mention for c in selected]
            selectedlist = ", ".join(mentions)
            embed = discord.Embed(title="📋 Selected Channels 📋", description=f'{selectedlist}')
            await response.edit(embed=embed, view=None)
            for channel in selected:
                messages = [m async for m in channel.history(limit=None)]
                unpinned = [m for m in messages if not m.pinned]
                deleted = []
                while len(unpinned) > 0:
                    deleted += await channel.purge(check=lambda message: message.author == member and message.pinned == False, oldest_first=True)
                    messages = [m async for m in channel.history(limit=None)]
                    unpinned = [m for m in messages if not m.pinned]
                if len(deleted) == 1:
                    embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} message was just removed from {channel.mention}!')
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} messages were just removed from {channel.mention}!')
                    await ctx.send(embed=embed)
        elif view.value == False:
            embed = discord.Embed(title="❌ Cancelled ❌", description='This interaction has been cancelled. No messages have been purged.')
            await response.edit(embed=embed, view=None)
        else:
            embed = discord.Embed(title="⌛ Timed Out ⌛", description='This interaction has timed out. No messages have been purged.')
            await response.edit(embed=embed, view=None)

    @commands.hybrid_command(name="purgechannels")
    @commands.has_guild_permissions(administrator=True)
    async def purgechannels(self, ctx: commands.Context):
        """Purge all unpinned messages in a set list of up to 25 channels. (Admin Only)"""
        await ctx.defer()
        view = DropdownView()
        embed = discord.Embed(title="🗑️ Purge Channels 🗑️", description="Which channel(s) would you like to purge all unpinned messages from?")
        response = await ctx.send(embed=embed, view=view)
        await view.wait()
        if view.value == True:
            selected = [c.resolve() for c in view.values]
            mentions = [c.mention for c in selected]
            selectedlist = ", ".join(mentions)
            embed = discord.Embed(title="📋 Selected Channels 📋", description=f'{selectedlist}')
            await response.edit(embed=embed, view=None)
            for channel in selected:
                messages = [m async for m in channel.history(limit=None)]
                unpinned = [m for m in messages if not m.pinned]
                deleted = []
                while len(unpinned) > 0:
                    deleted += await channel.purge(check=lambda message: message.pinned == False, oldest_first=True)
                    messages = [m async for m in channel.history(limit=None)]
                    unpinned = [m for m in messages if not m.pinned]
                if len(deleted) == 1:
                    embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} message was just removed from {channel.mention}!')
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} messages were just removed from {channel.mention}!')
                    await ctx.send(embed=embed)
        elif view.value == False:
            embed = discord.Embed(title="❌ Cancelled ❌", description='This interaction has been cancelled. No messages have been purged.')
            await response.edit(embed=embed, view=None)
        else:
            embed = discord.Embed(title="⌛ Timed Out ⌛", description='This interaction has timed out. No messages have been purged.')
            await response.edit(embed=embed, view=None)

    @commands.hybrid_command(name="purgeserver")
    @commands.has_guild_permissions(administrator=True)
    async def purgeserver(self, ctx: commands.Context):
        """Purges all unpinned messages in a server, excluding up to 25 channels. (Admin Only)"""
        await ctx.defer()
        view = DropdownView()
        embed = discord.Embed(title="🗑️ Purge Server 🗑️", description="Which channels would you like to **exclude** from the purge of all unpinned messages?")
        response = await ctx.send(embed=embed, view=view)
        await view.wait()
        if view.value == True:
            excluded = [c for c in view.values]
            mentions = [c.mention for c in excluded]
            excludedlist = ", ".join(mentions)
            embed = discord.Embed(title="📋 Excluded Channels 📋", description=f'{excludedlist}')
            await response.edit(embed=embed, view=None)
            selected = [c for c in ctx.guild.text_channels if c not in excluded]
            for channel in selected:
                messages = [m async for m in channel.history(limit=None)]
                unpinned = [m for m in messages if not m.pinned]
                deleted = []
                while len(unpinned) > 0:
                    deleted += await channel.purge(check=lambda message: message.pinned == False, oldest_first=True)
                    messages = [m async for m in channel.history(limit=None)]
                    unpinned = [m for m in messages if not m.pinned]
                if len(deleted) == 1:
                    embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} message was just removed from {channel.mention}!')
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} messages were just removed from {channel.mention}!')
                    await ctx.send(embed=embed)
        elif view.value == False:
            embed = discord.Embed(title="❌ Cancelled ❌", description='This interaction has been cancelled. No messages have been purged.')
            await response.edit(embed=embed, view=None)
        else:
            embed = discord.Embed(title="⌛ Timed Out ⌛", description='This interaction has timed out. No messages have been purged.')
            await response.edit(embed=embed, view=None)

class AwardCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="setawards")
    @commands.has_guild_permissions(administrator=True)
    async def setawards(self, ctx: commands.Context, name_singular: str, name_plural: str, emoji: str):
        """Sets the name and emoji for the server awards.

        Parameters
        -----------
        name_singular : str
            Provide the singular form of the award name. (Default: Award)
        name_plural : str
            Provide the plural form of the award name. (Default: Awards)
        emoji : str
            Choose the emoji you would like to represent the award. (Default: 🏅)
        """
        await ctx.defer(ephemeral=True)
        guild = ctx.guild
        if guild.id in guilds:
            guilds[guild.id]["singular lower"] = name_singular.lower()
            guilds[guild.id]["singular caps"] = string.capwords(name_singular)
            guilds[guild.id]["plural lower"] = name_plural.lower()
            guilds[guild.id]["plural caps"] = string.capwords(name_plural)
            guilds[guild.id]["emoji"] = emoji
        else:
            guilds[guild.id] = {}
            guilds[guild.id]["singular lower"] = name_singular.lower()
            guilds[guild.id]["singular caps"] = string.capwords(name_singular)
            guilds[guild.id]["plural lower"] = name_plural.lower()
            guilds[guild.id]["plural caps"] = string.capwords(name_plural)
            guilds[guild.id]["emoji"] = emoji
        sing_low = guilds[guild.id]["singular lower"]
        sing_cap = guilds[guild.id]["singular caps"]
        plur_low = guilds[guild.id]["plural lower"]
        plur_cap = guilds[guild.id]["plural caps"]
        moji = guilds[guild.id]["emoji"]
        embed = discord.Embed(title=f"{moji} {plur_cap} Set {moji}",description=f"The award name and emoji have been set!\n\n**Name** (singular, lowercase): {sing_low}\n\n**Name** (singular, capitalized): {sing_cap}\n\n**Name** (plural, lowercase): {plur_low}\n\n**Name** (plural, capitalized): {plur_cap}\n\n**Emoji**: {moji}")
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="clearawards")
    @commands.has_guild_permissions(administrator=True)
    async def clearawards(self, ctx: commands.Context):
        """Clears all of the awards in the server.
        """
        await ctx.defer()
        guild = ctx.guild
        sing_low = guilds[guild.id]["singular lower"] or "award"
        sing_cap = guilds[guild.id]["singular caps"] or "Award"
        plur_low = guilds[guild.id]["plural lower"] or "awards"
        plur_cap = guilds[guild.id]["plural caps"] or "Awards"
        moji = guilds[guild.id]["emoji"] or "🏅"
        if guild.id in guilds:
            members = [m for m in guild.members]
            for member in members:
                if member.id in guilds[guild.id]:
                    guilds[guild.id][member.id]["awards"] = 0
                else:
                    guilds[guild.id][member.id] = {}
                    guilds[guild.id][member.id]["awards"] = 0
        else:
            guilds[guild.id] = {}
            members = [m for m in guild.members]
            for member in members:
                guilds[guild.id][member.id] = {}
                guilds[guild.id][member.id]["awards"] = 0
        embed = discord.Embed(title=f"{moji} {plur_cap} Cleared {moji}", description=f"{guild.name} has had all its {plur_low} cleared!")
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name="awardreactiontoggle")
    @commands.has_guild_permissions(administrator=True)
    async def awardreactiontoggle(self, ctx: commands.Context, toggle: bool):
        """Toggles the ability for users to add or remove awards with reactions.

        Parameters
        -----------
        toggle : bool
            Set to True to toggle award reactions on. Set to False to toggle award reactions off.
        """
        guild = ctx.guild
        if guild in guilds[guild.id]:
            guilds[guild.id]["award react toggle"] = toggle
        else:
            guilds[guild.id] = {}
            guilds[guild.id]["award react toggle"] = toggle

    @commands.Cog.listener(name="reactionadd")
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.Member):
        message = reaction.message
        guild = message.guild
        if guilds[guild.id]["award react toggle"] == True:
            member = message.author
            sing_low = guilds[guild.id]["singular lower"] or "award"
            sing_cap = guilds[guild.id]["singular caps"] or "Award"
            plur_low = guilds[guild.id]["plural lower"] or "awards"
            plur_cap = guilds[guild.id]["plural caps"] or "Awards"
            moji = guilds[guild.id]["emoji"] or "🏅"
            if str(reaction.emoji) == moji:
                if guild.id in guilds:
                    if member.id in guilds[guild.id]:
                        guilds[guild.id][member.id]["awards"] += 1
                        awards = guilds[guild.id][member.id]["awards"]
                        embed = discord.Embed(title=f"{moji} {sing_cap} Added {moji}", description=f"{user.mention} has added 1 {sing_low} to {member.mention}'s total via an emoji reaction. {member.mention}'s new total number of {plur_low} is {awards}!")
                        await message.channel.send(embed=embed, reference=message)
                    else:
                        guilds[guild.id][member.id] = {}
                        guilds[guild.id][member.id]["awards"] = 1
                        awards = guilds[guild.id][member.id]["awards"]
                        embed = discord.Embed(title=f"{moji} {sing_cap} Added {moji}", description=f"{user.mention} has added 1 {sing_low} to {member.mention}'s total via an emoji reaction. {member.mention}'s new total number of {plur_low} is {awards}!")
                        await message.channel.send(embed=embed, reference=message)
                else:
                    guilds[guild.id] = {}
                    guilds[guild.id][member.id] = {}
                    guilds[guild.id][member.id]["awards"] = 1
                    awards = guilds[guild.id][member.id]["awards"]
                    embed = discord.Embed(title=f"{moji} {sing_cap} Added {moji}", description=f"{user.mention} has added 1 {sing_low} to {member.mention}'s total via an emoji reaction. {member.mention}'s new total number of {plur_low} is {awards}!")
                    await message.channel.send(embed=embed, reference=message)

    @commands.Cog.listener(name="reactionremove")
    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.Member):
        message = reaction.message
        guild = message.guild
        if guilds[guild.id]["award react toggle"] == True:
            member = message.author
            sing_low = guilds[guild.id]["singular lower"] or "award"
            sing_cap = guilds[guild.id]["singular caps"] or "Award"
            plur_low = guilds[guild.id]["plural lower"] or "awards"
            plur_cap = guilds[guild.id]["plural caps"] or "Awards"
            moji = guilds[guild.id]["emoji"] or "🏅"
            if str(reaction.emoji) == moji:
                if guild.id in guilds:
                    if member.id in guilds[guild.id]:
                        if guilds[guild.id][member.id]["awards"] >= 1:
                            guilds[guild.id][member.id]["awards"] -= 1
                            awards = guilds[guild.id][member.id]["awards"]
                            embed = discord.Embed(title=f"{moji} {sing_cap} Removed {moji}", description=f"{user.mention} has removed 1 {sing_low} from {member.mention}'s total via an emoji unreaction. {member.mention}'s new total number of {plur_low} is {awards}!")
                            await message.channel.send(embed=embed, reference=message)

    @commands.hybrid_command(name="addawards")
    async def addawards(self, ctx: commands.Context, amount: Optional[int] = None, member: Optional[discord.Member] = None):
        """Adds awards to the command user or another selected member.

        Parameters
        -----------
        amount : int, optional
            Choose the number of awards to add. (Default: 1)
        member : discord.Member, optional
            Choose the member to add the awards to. (Default: Self)
        """
        await ctx.defer(ephemeral=True)
        guild = ctx.guild
        amount = amount or 1
        member = member or ctx.user
        sing_low = guilds[guild.id]["singular lower"] or "award"
        sing_cap = guilds[guild.id]["singular caps"] or "Award"
        plur_low = guilds[guild.id]["plural lower"] or "awards"
        plur_cap = guilds[guild.id]["plural caps"] or "Awards"
        moji = guilds[guild.id]["emoji"] or "🏅"
        if guild.id in guilds:
            if member.id in guilds[guild.id]:
                guilds[guild.id][member.id]["awards"] += amount
                if guilds[guild.id][member.id]["awards"] == 1:
                    embed = discord.Embed(title=f"{moji} {plur_cap} Added {moji}", description=f"{member.mention} now has {guilds[guild.id][member.id]["awards"]} {sing_low}!")
                    await ctx.send(embed=embed, ephemeral=True)
                else:
                    embed = discord.Embed(title=f"{moji} {plur_cap} Added {moji}", description=f"{member.mention} now has {guilds[guild.id][member.id]["awards"]} {plur_low}!")
                    await ctx.send(embed=embed, ephemeral=True)
            else:
                guilds[guild.id][member.id]["awards"] = amount
                if guilds[guild.id][member.id]["awards"] == 1:
                    embed = discord.Embed(title=f"{moji} {plur_cap} Added {moji}", description=f"{member.mention} now has {guilds[guild.id][member.id]["awards"]} {sing_low}!")
                    await ctx.send(embed=embed, ephemeral=True)
                else:
                    embed = discord.Embed(title=f"{moji} {plur_cap} Added {moji}", description=f"{member.mention} now has {guilds[guild.id][member.id]["awards"]} {plur_low}!")
                    await ctx.send(embed=embed, ephemeral=True)
        else:
            guilds[guild.id] = {}
            guilds[guild.id][member.id]["awards"] = amount
            if guilds[guild.id][member.id]["awards"] == 1:
                embed = discord.Embed(title=f"{moji} {plur_cap} Added {moji}", description=f"{member.mention} now has {guilds[guild.id][member.id]["awards"]} {sing_low}!")
                await ctx.send(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(title=f"{moji} {plur_cap} Added {moji}", description=f"{member.mention} now has {guilds[guild.id][member.id]["awards"]} {plur_low}!")
                await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="removeawards")
    async def removeawards(self, ctx: commands.Context, amount: Optional[int] = None, member: Optional[discord.Member] = None):
        """Removes awards from the command user or another selected member.

        Parameters
        -----------
        amount : int, optional
            Choose the number of awards to remove. (Default: 1)
        member : discord.Member, optional
            Choose the member to remove the awards from. (Default: Self)
        """
        await ctx.defer(ephemeral=True)
        guild = ctx.guild
        amount = amount or 1
        member = member or ctx.user
        sing_low = guilds[guild.id]["singular lower"] or "award"
        sing_cap = guilds[guild.id]["singular caps"] or "Award"
        plur_low = guilds[guild.id]["plural lower"] or "awards"
        plur_cap = guilds[guild.id]["plural caps"] or "Awards"
        moji = guilds[guild.id]["emoji"] or "🏅"
        if guild.id in guilds:
            if member.id in guilds[guild.id]:
                if guilds[guild.id][member.id]["awards"] == 0:
                    embed = discord.Embed(title="Error", description=f"{member.mention} doesn't have any {plur_low}!")
                    await ctx.send(embed=embed, ephemeral=True)
                elif guilds[guild.id][member.id]["awards"] < amount:
                    embed = discord.Embed(title="Error", description=f"{member.mention} doesn't have enough {plur_low}!")
                    await ctx.send(embed=embed, ephemeral=True)
                else:
                    guilds[guild.id][member.id]["awards"] -= amount
                    if guilds[guild.id][member.id]["awards"] == 0:
                        embed = discord.Embed(title=f"{moji} {plur_cap} Removed {moji}", description=f"{member.mention} no longer has any {plur_low}!")
                        await ctx.send(embed=embed, ephemeral=True)
                    elif guilds[guild.id][member.id]["awards"] == 1:
                        embed = discord.Embed(title=f"{moji} {plur_cap} Removed {moji}", description=f"{member.mention} now has {guilds[guild.id][member.id]["awards"]} {sing_low}!")
                        await ctx.send(embed=embed, ephemeral=True)
                    else:
                        embed = discord.Embed(title=f"{moji} {plur_cap} Removed {moji}", description=f"{member.mention} now has {guilds[guild.id][member.id]["awards"]} {plur_low}!")
                        await ctx.send(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(title="Error", description=f"{member.mention} doesn't exist in the {sing_low} log.")
                await ctx.send(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="Error", description=f"{guild.name} doesn't exist in the {sing_low} log.")
            await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="checkawards")
    async def checkawards(self, ctx: commands.Context, member: Optional[discord.Member] = None):
        """Returns the number of awards that the user or another selected user currently has.

        Parameters
        -----------
        member : discord.Member, optional
            Choose the member that you would like to check the number of awards for. (Default: Self)
        """
        await ctx.defer(ephemeral=True)
        guild = ctx.guild
        member = member or ctx.user
        sing_low = guilds[guild.id]["singular lower"] or "award"
        sing_cap = guilds[guild.id]["singular caps"] or "Award"
        plur_low = guilds[guild.id]["plural lower"] or "awards"
        plur_cap = guilds[guild.id]["plural caps"] or "Awards"
        moji = guilds[guild.id]["emoji"] or "🏅"
        if guild.id in guilds:
            if member.id in guilds[guild.id]:
                if guilds[guild.id][member.id]["awards"] == 0:
                    embed = discord.Embed(title=f"{moji} Number of {plur_cap} {moji}", description=f"{member.mention} doesn't have any {plur_low}!")
                    await ctx.send(embed=embed, ephemeral=True)
                elif guilds[guild.id][member.id]["awards"] == 1:
                    embed = discord.Embed(title=f"{moji} Number of {plur_cap} {moji}", description=f"{member.mention} has {guilds[guild.id][member.id]["awards"]} {sing_low}!")
                    await ctx.send(embed=embed, ephemeral=True)
                else:
                    embed = discord.Embed(title=f"{moji} Number of {plur_cap} {moji}", description=f"{member.mention} has {guilds[guild.id][member.id]["awards"]} {plur_low}!")
                    await ctx.send(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(title="Error", description=f"{member.mention} doesn't exist in the {sing_low} log.")
                await ctx.send(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="Error", description=f"{guild.name} doesn't exist in the {sing_low} log.")
            await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="leaderboard")
    async def leaderboard(self, ctx: commands.Context):
        """Returns the current award leaderboard for the server."""
        await ctx.defer()
        guild = ctx.guild
        sing_low = guilds[guild.id]["singular lower"] or "award"
        sing_cap = guilds[guild.id]["singular caps"] or "Award"
        plur_low = guilds[guild.id]["plural lower"] or "awards"
        plur_cap = guilds[guild.id]["plural caps"] or "Awards"
        moji = guilds[guild.id]["emoji"] or "🏅"
        if guild.id in guilds:
            awardlog = {}
            for member in guild.members:
                if member.id in guilds[guild.id]:
                    if "awards" in guilds[guild.id][member.id]:
                        if guilds[guild.id][member.id]["awards"] > 0:
                            awards[member.id] = guilds[guild.id][member.id]["awards"]
        else:
            embed = discord.Embed(title="Error", description=f"{guild.name} doesn't exist in the {sing_low} log.")
            await ctx.send(embed=embed, ephemeral=True)
        desc = []
        for member, awards in awardlog.items():
            awards = awards * moji
            desc.append(f"<@{member}>:\n{awards}")
        description = "\n\n".join(x for x in desc)
        embed = discord.Embed(title=f"{moji} {sing_cap} Leaderboard {moji}", description=description)
        await ctx.send(embed=embed)
            

class ProfileCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="setprofile")
    async def setprofile(self, ctx: commands.Context, name: Optional[str], age: Optional[str], location: Optional[str], pronouns: Optional[str], gender: Optional[str], sexuality: Optional[str], relationship: Optional[str], family: Optional[str], biography: Optional[str]):
        """Run this command to set up your member profile. Note that all fields are optional.

        Parameters
        -----------
        name : str, optional
            Provide your name or nickname.
        age : str, optional
            Provide your age or age range.
        location : str, optional
            Provide your continent, country, state, or city of residence.
        pronouns : str, optional
            Provide your pronouns (ex. she/her, he/him, they/them, etc).
        gender : str, optional
            Provide your gender identity label (ex. woman, man, nonbinary, etc).
        sexuality : str, optional
            Provide your sexuality label (ex. lesbian, gay, bisexual, etc).
        relationship : str, optional
            Provide your relationship status (ex. single, married, etc).
        family : str, optional
            Provide your your family planning status (ex. TTC, expecting, parenting, etc).
        biography : str, optional
            Provide a brief biography (ex. family, hobbies, interests, work, etc).
        """
        await ctx.defer(ephemeral=True)
        guild = ctx.guild
        member = ctx.author
        if guild in guilds:
            if member in guilds[guild]:
                if name == None:
                    guilds[guild][member]["Name"] = guilds[guild][member]["Name"] or None
                else:
                    guilds[guild][member]["Name"] = name
                if age == None:
                    guilds[guild][member]["Age"] = guilds[guild][member]["Age"] or None
                else:
                    guilds[guild][member]["Age"] = age
                if location == None:
                    guilds[guild][member]["Location"] = guilds[guild][member]["Location"] or None
                else:
                    guilds[guild][member]["Location"] = location
                if pronouns == None:
                    guilds[guild][member]["Pronouns"] = guilds[guild][member]["Pronouns"] or None
                else:
                    guilds[guild][member]["Pronouns"] = pronouns
                if gender == None:
                    guilds[guild][member]["Gender"] = guilds[guild][member]["Gender"] or None
                else:
                    guilds[guild][member]["Gender"] = gender
                if sexuality == None:
                    guilds[guild][member]["Sexuality"] = guilds[guild][member]["Sexuality"] or None
                else:
                    guilds[guild][member]["Sexuality"] = sexuality
                if relationship == None:
                    guilds[guild][member]["Relationship Status"] = guilds[guild][member]["Relationship Status"] or None
                else:
                    guilds[guild][member]["Relationship Status"] = relationship
                if family == None:
                    guilds[guild][member]["Family Planning Status"] = guilds[guild][member]["Family Planning Status"] or None
                else:
                    guilds[guild][member]["Family Planning Status"] = family
                if biography == None:
                    guilds[guild][member]["Biography"] = guilds[guild][member]["Biography"] or None
                else:
                    guilds[guild][member]["Biography"] = biography
            else:
                guilds[guild][member] = {}
                guilds[guild][member]["Name"] = name or None
                guilds[guild][member]["Age"] = age or None
                guilds[guild][member]["Location"] = location or None
                guilds[guild][member]["Pronouns"] = pronouns or None
                guilds[guild][member]["Gender"] = gender or None
                guilds[guild][member]["Sexuality"] = sexuality or None
                guilds[guild][member]["Relationship Status"] = relationship or None
                guilds[guild][member]["Family Planning Status"] = family or None
                guilds[guild][member]["Biography"] = biography or None
        else:
            guilds[guild] = {}
            guilds[guild][member] = {}
            guilds[guild][member]["Name"] = name or None
            guilds[guild][member]["Age"] = age or None
            guilds[guild][member]["Location"] = location or None
            guilds[guild][member]["Pronouns"] = pronouns or None
            guilds[guild][member]["Gender"] = gender or None
            guilds[guild][member]["Sexuality"] = sexuality or None
            guilds[guild][member]["Relationship Status"] = relationship or None
            guilds[guild][member]["Family Planning Status"] = family or None
            guilds[guild][member]["Biography"] = biography or None
        name = guilds[guild][member]["Name"]
        age = guilds[guild][member]["Age"]
        location = guilds[guild][member]["Location"]
        pronouns = guilds[guild][member]["Pronouns"]
        gender = guilds[guild][member]["Gender"]
        sexuality = guilds[guild][member]["Sexuality"]
        relationship = guilds[guild][member]["Relationship Status"]
        family = guilds[guild][member]["Family Planning Status"]
        biography = guilds[guild][member]["Biography"]
        embed = discord.Embed(color=member.accent_color)
        embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar}")
        embed.add_field(name="🏷️ Name", value=f"{name}", inline=True)
        embed.add_field(name="🏷️ Age", value=f"{age}", inline=True)
        embed.add_field(name="🏷️ Location", value=f"{location}", inline=True)
        embed.add_field(name="🏷️ Pronouns", value=f"{pronouns}", inline=True)
        embed.add_field(name="🏷️ Gender", value=f"{gender}", inline=True)
        embed.add_field(name="🏷️ Sexuality", value=f"{sexuality}", inline=True)
        embed.add_field(name="📝 Relationship Status", value=f"{relationship}", inline=True)
        embed.add_field(name="📝 Family Planning Status", value=f"{family}", inline=True)
        embed.add_field(name="📝 Biography", value=f"{biography}", inline=False)
        embed.add_field(name="📝 Roles", value=f"{member.roles}", inline=False)
        joined = discord.utils.format_dt(member.joined_at, style="R")
        embed.set_footer(text=f"Member of {guild.name} for {joined}.")
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="setprofilename")
    async def setprofilename(self, ctx: commands.Context, name: str):
        """Run this command to set your profile name.

        Parameters
        -----------
        name : str
            Provide your name or nickname.
        """
        guild = ctx.guild
        member = ctx.author
        guilds[guild][member]["Name"] = name
        embed = discord.Embed(color=member.accent_color, title="✔️ Success ✔️", description=f"Your profile name is now set to: {name}")
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="setprofileage")
    async def setprofileage(self, ctx: commands.Context, age: str):
        """Run this command to set your profile age.

        Parameters
        -----------
        age : str
            Provide your age or age range.
        """
        guild = ctx.guild
        member = ctx.author
        guilds[guild][member]["Age"] = age
        embed = discord.Embed(color=member.accent_color, title="✔️ Success ✔️", description=f"Your profile age is now set to: {age}")
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="setprofilelocation")
    async def setprofilelocation(self, ctx: commands.Context, location: str):
        """Run this command to set your profile location.

        Parameters
        -----------
        location : str
            Provide your continent, country, state, or city of residence.
        """
        guild = ctx.guild
        member = ctx.author
        guilds[guild][member]["Location"] = location
        embed = discord.Embed(color=member.accent_color, title="✔️ Success ✔️", description=f"Your profile location is now set to: {location}")
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="setprofilepronouns")
    async def setprofilepronouns(self, ctx: commands.Context, pronouns: str):
        """Run this command to set your profile pronouns.

        Parameters
        -----------
        pronouns : str
            Provide your pronouns (ex. she/her, he/him, they/them, etc).
        """
        guild = ctx.guild
        member = ctx.author
        guilds[guild][member]["Pronouns"] = pronouns
        embed = discord.Embed(color=member.accent_color, title="✔️ Success ✔️", description=f"Your profile pronouns are now set to: {pronouns}")
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="setprofilegender")
    async def setprofilegender(self, ctx: commands.Context, gender: str):
        """Run this command to set your profile gender.

        Parameters
        -----------
        gender : str
            Provide your gender identity label (ex. woman, man, nonbinary, etc).
        """
        guild = ctx.guild
        member = ctx.author
        guilds[guild][member]["Gender"] = gender
        embed = discord.Embed(color=member.accent_color, title="✔️ Success ✔️", description=f"Your profile gender is now set to: {gender}")
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="setprofilesexuality")
    async def setprofilesexuality(self, ctx: commands.Context, sexuality: str):
        """Run this command to set your profile sexuality.

        Parameters
        -----------
        sexuality : str
            Provide your sexuality label (ex. lesbian, gay, bisexual, etc).
        """
        guild = ctx.guild
        member = ctx.author
        guilds[guild][member]["Sexuality"] = sexuality
        embed = discord.Embed(color=member.accent_color, title="✔️ Success ✔️", description=f"Your profile sexuality is now set to: {sexuality}")
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="setprofilerelationship")
    async def setprofilerelationship(self, ctx: commands.Context, relationship: str):
        """Run this command to set your profile relationship status.

        Parameters
        -----------
        relationship : str
            Provide your relationship status (ex. single, married, etc).
        """
        guild = ctx.guild
        member = ctx.author
        guilds[guild][member]["Relationship Status"] = relationship
        embed = discord.Embed(color=member.accent_color, title="✔️ Success ✔️", description=f"Your profile relationship status is now set to: {relationship}")
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="setprofilefamily")
    async def setprofilefamily(self, ctx: commands.Context, family: str):
        """Run this command to set your profile family planning status.

        Parameters
        -----------
        family : str
            Provide your your family planning status (ex. TTC, expecting, parenting, etc).
        """
        guild = ctx.guild
        member = ctx.author
        guilds[guild][member]["Family Planning Status"] = family
        embed = discord.Embed(color=member.accent_color, title="✔️ Success ✔️", description=f"Your profile family planning status is now set to: {family}")
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="setprofilebiography")
    async def setprofilebiography(self, ctx: commands.Context, biography: str):
        """Run this command to set your profile biography.

        Parameters
        -----------
        biography : str
            Provide a brief biography (ex. family, hobbies, interests, work, etc).
        """
        guild = ctx.guild
        member = ctx.author
        guilds[guild][member]["Biography"] = biography
        embed = discord.Embed(color=member.accent_color, title="✔️ Success ✔️", description=f"Your profile biography is now set to: {biography}")
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="getprofile")
    async def getprofile(self, ctx: commands.Context, member: discord.Member):
        """Run this command to retrieve a member's profile.

        Parameters
        -----------
        member : str
            Provide the member whose profile you would like to retrieve.
        """
        guild = ctx.guild
        name = guilds[guild][member]["Name"]
        age = guilds[guild][member]["Age"]
        location = guilds[guild][member]["Location"]
        pronouns = guilds[guild][member]["Pronouns"]
        gender = guilds[guild][member]["Gender"]
        sexuality = guilds[guild][member]["Sexuality"]
        relationship_status = guilds[guild][member]["Relationship Status"]
        family_planning_status = guilds[guild][member]["Family Planning Status"]
        biography = guilds[guild][member]["Biography"]
        embed = discord.Embed(color=member.accent_color)
        embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar}")
        embed.add_field(name="🏷️ Name", value=f"{name}", inline=True)
        embed.add_field(name="🏷️ Age", value=f"{age}", inline=True)
        embed.add_field(name="🏷️ Location", value=f"{location}", inline=True)
        embed.add_field(name="🏷️ Pronouns", value=f"{pronouns}", inline=True)
        embed.add_field(name="🏷️ Gender", value=f"{gender}", inline=True)
        embed.add_field(name="🏷️ Sexuality", value=f"{sexuality}", inline=True)
        embed.add_field(name="📝 Relationship Status", value=f"{relationship_status}", inline=True)
        embed.add_field(name="📝 Family Planning Status", value=f"{family_planning_status}", inline=True)
        embed.add_field(name="📝 Biography", value=f"{biography}", inline=False)
        embed.add_field(name="📝 Roles", value=f"{member.roles}", inline=False)
        joined = discord.utils.format_dt(member.joined_at, style="R")
        embed.set_footer(text=f"Member of {guild.name} for {joined}.")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(BackgroundTasks(bot), override=True)
    await bot.add_cog(SetupCommands(bot), override=True)
    await bot.add_cog(PurgeCommands(bot), override=True)
    await bot.add_cog(AwardCommands(bot), override=True)
    await bot.add_cog(ProfileCommands(bot), override=True)

@bot.event
async def on_ready():
    await setup(bot)
    print(f'Logged in as {bot.user}! (ID: {bot.user.id})')

bot.run('token')
