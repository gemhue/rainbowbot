import discord
from discord import app_commands, ChannelType
from discord.ui import ChannelSelect
from discord.ext import commands
from typing import Any

class ChannelSelector(ChannelSelect):
    def __init__(self):
        super().__init__(
            channel_types=[ChannelType.text],
            placeholder="Select channels... (Limit: 25)",
            min_values=1,
            max_values=25,
            row=1
        )

    async def callback(self, interaction: discord.Interaction) -> Any:
        await interaction.response.defer()
        channels: list[DropdownView] = self.values
        self.view.values = [c for c in channels]

class DropdownView(discord.ui.View):
    def __init__(self, *, timeout=180.0):
        super().__init__(timeout=timeout)
        self.value = None
        self.add_item(ChannelSelector())

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green, row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red, row=2)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = False
        self.stop()

class Cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_group(name="purge", fallback="here")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def purge(self, ctx: commands.Context):
        """(Admin Only) Purge all unpinned messages in the current channel.
        """
        await ctx.defer()
        channel = ctx.channel
        messages = [m async for m in channel.history(limit=None)]
        unpinned = [m for m in messages if not m.pinned]
        deleted = []
        while len(unpinned) > 0:
            deleted += await channel.purge(check=lambda message: message.pinned == False, oldest_first=True)
            messages = [m async for m in channel.history(limit=None)]
            unpinned = [m for m in messages if not m.pinned]
        if len(deleted) == 0:
            embed = discord.Embed(title="❌ Error ❌", description=f"{channel.mention} doesn't have any messages to purge!")
            await channel.send(embed=embed, delete_after=30.0)
        elif len(deleted) == 1:
            embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} message was just purged from {channel.mention}!')
            await channel.send(embed=embed, delete_after=30.0)
        else:
            embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} messages were just purged from {channel.mention}!')
            await channel.send(embed=embed, delete_after=30.0)
        embed = discord.Embed(title="✔️ Done ✔️", description=f'The purge is now complete!')
        await channel.send(embed=embed, delete_after=30.0)

    @purge.command(name="member")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def member(self, ctx: commands.Context, member: discord.Member):
        """(Admin Only) Purge all of a member's unpinned messages in a set list of up to 25 channels.

        Parameters
        -----------
        member : discord.Member
            Provide the member who's unpinned messages you would like to purge.
        """
        await ctx.defer()
        ctxchannel = ctx.channel
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
                    embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} message was just purged from {channel.mention}!')
                    await ctxchannel.send(embed=embed, delete_after=30.0)
                else:
                    embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} messages were just purged from {channel.mention}!')
                    await ctxchannel.send(embed=embed, delete_after=30.0)
            embed = discord.Embed(title="✔️ Done ✔️", description=f'The purge is now complete!')
            await ctxchannel.send(embed=embed, delete_after=30.0)
        elif view.value == False:
            embed = discord.Embed(title="❌ Cancelled ❌", description='This interaction has been cancelled. No messages have been purged.')
            await response.edit(embed=embed, view=None)
        else:
            embed = discord.Embed(title="⌛ Timed Out ⌛", description='This interaction has timed out. No messages have been purged.')
            await response.edit(embed=embed, view=None)

    @purge.command(name="channels")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def channels(self, ctx: commands.Context):
        """(Admin Only) Purge all unpinned messages in a set list of up to 25 channels.
        """
        await ctx.defer()
        ctxchannel = ctx.channel
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
                    embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} message was just purged from {channel.mention}!')
                    await ctxchannel.send(embed=embed, delete_after=30.0)
                else:
                    embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} messages were just purged from {channel.mention}!')
                    await ctxchannel.send(embed=embed, delete_after=30.0)
            embed = discord.Embed(title="✔️ Done ✔️", description=f'The purge is now complete!')
            await ctxchannel.send(embed=embed, delete_after=30.0)
        elif view.value == False:
            embed = discord.Embed(title="❌ Cancelled ❌", description='This interaction has been cancelled. No messages have been purged.')
            await response.edit(embed=embed, view=None)
        else:
            embed = discord.Embed(title="⌛ Timed Out ⌛", description='This interaction has timed out. No messages have been purged.')
            await response.edit(embed=embed, view=None)

    @purge.command(name="server")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def server(self, ctx: commands.Context):
        """(Admin Only) Purges all unpinned messages in a server, excluding up to 25 channels.
        """
        await ctx.defer()
        ctxchannel = ctx.channel
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
            selected = [c for c in ctx.guild.text_channels]
            for channel in selected:
                if channel not in excluded:
                    messages = [m async for m in channel.history(limit=None)]
                    unpinned = [m for m in messages if not m.pinned]
                    deleted = []
                    while len(unpinned) > 0:
                        deleted += await channel.purge(check=lambda message: message.pinned == False, oldest_first=True)
                        messages = [m async for m in channel.history(limit=None)]
                        unpinned = [m for m in messages if not m.pinned]
                    if len(deleted) == 1:
                        embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} message was just purged from {channel.mention}!')
                        await ctxchannel.send(embed=embed, delete_after=30.0)
                    else:
                        embed = discord.Embed(title="✔️ Success ✔️", description=f'{len(deleted)} messages were just purged from {channel.mention}!')
                        await ctxchannel.send(embed=embed, delete_after=30.0)
            embed = discord.Embed(title="✔️ Done ✔️", description=f'The purge is now complete!')
            await ctxchannel.send(embed=embed, delete_after=30.0)
        elif view.value == False:
            embed = discord.Embed(title="❌ Cancelled ❌", description='This interaction has been cancelled. No messages have been purged.')
            await response.edit(embed=embed, view=None)
        else:
            embed = discord.Embed(title="⌛ Timed Out ⌛", description='This interaction has timed out. No messages have been purged.')
            await response.edit(embed=embed, view=None)

async def setup(bot: commands.Bot):
	await bot.add_cog(Cog(bot), override=True)