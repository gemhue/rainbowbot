import discord
import aiosqlite
from discord import app_commands, ChannelType
from discord.ui import ChannelSelect
from discord.ext import commands
from typing import Any
from datetime import datetime, timezone

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

class Purge(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.blurple = discord.Colour.blurple()
        self.green = discord.Colour.green()
        self.yellow = discord.Colour.yellow()
        self.red = discord.Colour.red()

    @commands.hybrid_group(name="purge", fallback="here")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def purge(self, ctx: commands.Context):
        """(Admin Only) Purge all unpinned messages in the current channel.
        """
        await ctx.defer()
        try:
            channel = ctx.channel
            messages = [m async for m in channel.history(limit=None)]
            unpinned = [m for m in messages if not m.pinned]
            deleted = []
            while len(unpinned) > 0:
                deleted += await channel.purge(check=lambda message: message.pinned == False, oldest_first=True)
                messages = [m async for m in channel.history(limit=None)]
                unpinned = [m for m in messages if not m.pinned]
            if len(deleted) == 0:
                error = discord.Embed(color=self.red, title="Error", description=f"{channel.mention} doesn't have any messages to purge!")
                await channel.send(embed=error, delete_after=30.0)
            elif len(deleted) == 1:
                embed = discord.Embed(color=self.green, title="Success", description=f'{len(deleted)} message was just purged from {channel.mention}!')
                await channel.send(embed=embed, delete_after=30.0)
            else:
                embed = discord.Embed(color=self.green, title="Success", description=f'{len(deleted)} messages were just purged from {channel.mention}!')
                await channel.send(embed=embed, delete_after=30.0)
            async with aiosqlite.connect('rainbowbot.db') as db:
                cur = await db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
                row = await cur.fetchone()
                fetched_logging = row[0]
                if fetched_logging is not None:
                    now = datetime.now(tz=timezone.utc)
                    log = discord.Embed(color=self.blurple, title="Purge Log", description=f"{ctx.author.mention} has just purged all unpinned messages from the following channel: {channel.mention}.", timestamp=now)
                    logging = self.bot.get_channel(fetched_logging)
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
                    await logging.send(embed=log)
                await db.commit()
                await db.close()
        except Exception as e:
            error = discord.Embed(color=self.red, title="Error", description=f"{e}")
            await channel.send(embed=error, delete_after=30.0)

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
        try:
            view = DropdownView()
            embed = discord.Embed(color=self.blurple, title="Purge Member", description=f"Which channel(s) would you like to purge {member.mention}'s unpinned messages from?")
            response = await ctx.send(embed=embed, view=view)
            await view.wait()
            if view.value == True:
                selected = [c.resolve() for c in view.values]
                mentions = [c.mention for c in selected]
                selectedlist = ", ".join(mentions)
                embed = discord.Embed(color=self.blurple, title="Selected Channels", description=f'{selectedlist}')
                await response.edit(embed=embed, view=None)
                for channel in selected:
                    deleted = []
                    messages = [m async for m in channel.history(limit=None)]
                    unpinned = [m for m in messages if not m.pinned]
                    while len(unpinned) > 0:
                        deleted += await channel.purge(check=lambda message: message.author == member and message.pinned == False, oldest_first=True)
                        messages = [m async for m in channel.history(limit=None)]
                        unpinned = [m for m in messages if not m.pinned]
                    if len(deleted) == 1:
                        embed = discord.Embed(color=self.green, title="Success", description=f'{len(deleted)} message was just purged from {channel.mention}!')
                        await ctx.channel.send(embed=embed, delete_after=30.0)
                    else:
                        embed = discord.Embed(color=self.green, title="Success", description=f'{len(deleted)} messages were just purged from {channel.mention}!')
                        await ctx.channel.send(embed=embed, delete_after=30.0)
                embed = discord.Embed(color=self.green, title="Done", description=f'The purge is now complete!')
                await ctx.channel.send(embed=embed, delete_after=30.0)
                async with aiosqlite.connect('rainbowbot.db') as db:
                    cur = await db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
                    row = await cur.fetchone()
                    fetched_logging = row[0]
                    if fetched_logging is not None:
                        now = datetime.now(tz=timezone.utc)
                        log = discord.Embed(color=self.blurple, title="Purge Log", description=f"{ctx.author.mention} has just purged {member.mention}'s unpinned messages from the following channels: {selectedlist}.", timestamp=now)
                        logging = self.bot.get_channel(fetched_logging)
                        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
                        await logging.send(embed=log)
                    await db.commit()
                    await db.close()
            elif view.value == False:
                cancelled = discord.Embed(color=self.red, title="Cancelled", description='This interaction has been cancelled. No messages have been purged.')
                await response.edit(embed=cancelled, delete_after=30.0, view=None)
            else:
                timed_out = discord.Embed(color=self.yellow, title="Timed Out", description='This interaction has timed out. No messages have been purged.')
                await response.edit(embed=timed_out, delete_after=30.0, view=None)
        except Exception as e:
            error = discord.Embed(color=self.red, title="Error", description=f"{e}")
            await ctx.channel.send(embed=error, delete_after=30.0)

    @purge.command(name="channels")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def channels(self, ctx: commands.Context):
        """(Admin Only) Purge all unpinned messages in a set list of up to 25 channels.
        """
        await ctx.defer()
        try:
            view = DropdownView()
            embed = discord.Embed(color=self.blurple, title="Purge Channels", description="Which channel(s) would you like to purge all unpinned messages from?")
            response = await ctx.send(embed=embed, view=view)
            await view.wait()
            if view.value == True:
                selected = [c.resolve() for c in view.values]
                mentions = [c.mention for c in selected]
                selectedlist = ", ".join(mentions)
                embed = discord.Embed(color=self.blurple, title="Selected Channels", description=f'{selectedlist}')
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
                        embed = discord.Embed(color=self.green, title="Success", description=f'{len(deleted)} message was just purged from {channel.mention}!')
                        await ctx.channel.send(embed=embed, delete_after=30.0)
                    else:
                        embed = discord.Embed(color=self.green, title="Success", description=f'{len(deleted)} messages were just purged from {channel.mention}!')
                        await ctx.channel.send(embed=embed, delete_after=30.0)
                embed = discord.Embed(color=self.green, title="Done", description=f'The purge is now complete!')
                await ctx.channel.send(embed=embed, delete_after=30.0)
                async with aiosqlite.connect('rainbowbot.db') as db:
                    cur = await db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
                    row = await cur.fetchone()
                    fetched_logging = row[0]
                    if fetched_logging is not None:
                        now = datetime.now(tz=timezone.utc)
                        log = discord.Embed(color=self.blurple, title="Purge Log", description=f"{ctx.author.mention} has just purged all unpinned messages from the following channels: {selectedlist}.", timestamp=now)
                        logging = self.bot.get_channel(fetched_logging)
                        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
                        await logging.send(embed=log)
                    await db.commit()
                    await db.close()
            elif view.value == False:
                cancelled = discord.Embed(color=self.red, title="Cancelled", description='This interaction has been cancelled. No messages have been purged.')
                await response.edit(embed=cancelled, delete_after=30.0, view=None)
            else:
                timed_out = discord.Embed(color=self.yellow, title="Timed Out", description='This interaction has timed out. No messages have been purged.')
                await response.edit(embed=timed_out, delete_after=30.0, view=None)
        except Exception as e:
            error = discord.Embed(color=self.red, title="Error", description=f"{e}")
            await ctx.channel.send(embed=error, delete_after=30.0)

    @purge.command(name="server")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def server(self, ctx: commands.Context):
        """(Admin Only) Purges all unpinned messages in a server, excluding up to 25 channels.
        """
        await ctx.defer()
        try:
            view = DropdownView()
            embed = discord.Embed(color=self.blurple, title="Purge Server", description="Which channels would you like to **exclude** from the purge of all unpinned messages?")
            response = await ctx.send(embed=embed, view=view)
            await view.wait()
            if view.value == True:
                excluded = [c.resolve() for c in view.values]
                mentions = [c.mention for c in excluded]
                excludedlist = ", ".join(mentions)
                embed = discord.Embed(color=self.blurple, title="Excluded Channels", description=f'{excludedlist}')
                await response.edit(embed=embed, view=None)
                for channel in ctx.guild.text_channels:
                    if channel not in excluded:
                        messages = [m async for m in channel.history(limit=None)]
                        unpinned = [m for m in messages if not m.pinned]
                        deleted = []
                        while len(unpinned) > 0:
                            deleted += await channel.purge(check=lambda message: message.pinned == False, oldest_first=True)
                            messages = [m async for m in channel.history(limit=None)]
                            unpinned = [m for m in messages if not m.pinned]
                        if len(deleted) == 1:
                            embed = discord.Embed(color=self.green, title="Success", description=f'{len(deleted)} message was just purged from {channel.mention}!')
                            await ctx.channel.send(embed=embed, delete_after=30.0)
                        else:
                            embed = discord.Embed(color=self.green, title="Success", description=f'{len(deleted)} messages were just purged from {channel.mention}!')
                            await ctx.channel.send(embed=embed, delete_after=30.0)
                embed = discord.Embed(color=self.green, title="Done", description=f'The purge is now complete!')
                await ctx.channel.send(embed=embed, delete_after=30.0)
                async with aiosqlite.connect('rainbowbot.db') as db:
                    cur = await db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
                    row = await cur.fetchone()
                    fetched_logging = row[0]
                    if fetched_logging is not None:
                        now = datetime.now(tz=timezone.utc)
                        log = discord.Embed(color=self.blurple, title="Purge Log", description=f"{ctx.author.mention} has just purged all unpinned messages from the server, except from the following channels: {excludedlist}.", timestamp=now)
                        logging = self.bot.get_channel(fetched_logging)
                        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
                        await logging.send(embed=log)
                    await db.commit()
                    await db.close()
            elif view.value == False:
                cancelled = discord.Embed(color=self.red, title="Cancelled", description='This interaction has been cancelled. No messages have been purged.')
                await response.edit(embed=cancelled, delete_after=30.0, view=None)
            else:
                timed_out = discord.Embed(color=self.yellow, title="Timed Out", description='This interaction has timed out. No messages have been purged.')
                await response.edit(embed=timed_out, delete_after=30.0, view=None)
        except Exception as e:
            error = discord.Embed(color=self.red, title="Error", description=f"{e}")
            await ctx.channel.send(embed=error, delete_after=30.0)

async def setup(bot: commands.Bot):
	await bot.add_cog(Purge(bot), override=True)