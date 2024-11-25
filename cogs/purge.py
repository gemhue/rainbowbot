import discord
import traceback
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timezone

class YesOrNo(discord.ui.View):
    def __init__(self, *, timeout = 180, bot: commands.Bot, user: discord.Member):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.user = user
        self.value = None

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, emoji="👍")
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.red, emoji="👎")
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = False
            self.stop()
    
    async def on_timeout(self):
        self.value = None
    
    async def on_error(self, interaction: discord.Interaction, error: Exception, item):
        await interaction.response.defer(ephemeral=True)
        if interaction.user == self.user:
            self.value = False
            self.stop()

            embed = discord.Embed(color=self.bot.red, title="Error", description="There was an error while trying to complete the command. Please try again later.")
            embed.add_field(name="Error", value=f"{error}")
            await interaction.followup.send(embed=embed, ephemeral=True)

class ChannelSelect(discord.ui.ChannelSelect):
    def __init__(self, *, user: discord.Member):
        super().__init__(
            channel_types=[discord.ChannelType.text],
            placeholder="Select up to 25 channels...",
            min_values=1,
            max_values=25,
            row=1
        )
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.view.channel_ids = [c.id for c in self.values]

class ChannelSelectView(discord.ui.View):
    def __init__(self, *, timeout=180.0, bot: commands.Bot, user: discord.Member):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.user = user
        self.value = None
        self.add_item(ChannelSelect(user=self.user))

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green, row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red, row=2)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = False
            self.stop()

    async def on_timeout(self):
        self.value = None
    
    async def on_error(self, interaction: discord.Interaction, error: Exception, item):
        await interaction.response.defer(ephemeral=True)
        if interaction.user == self.user:
            self.value = False
            self.stop()

            embed = discord.Embed(color=self.bot.red, title="Error", description="There was an error while trying to complete the command. Please try again later.")
            embed.add_field(name="Error", value=f"{error}")
            await interaction.followup.send(embed=embed, ephemeral=True)

class Purge(commands.GroupCog, group_name = "purge"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.database

    @app_commands.command(name="here")
    @app_commands.checks.has_permissions(administrator=True)
    async def here(self, interaction: discord.Interaction):
        """(Admin Only) Purge all unpinned messages in the current channel.
        """
        await interaction.response.defer()
        try:

            user = interaction.user
            guild = interaction.guild
            view = YesOrNo(bot=self.bot, user=user)
            embed = discord.Embed(color=self.bot.blurple, title="Confirm Purge", description="Are you **sure** you want to purge all unpinned messages in the current channel?")
            response = await interaction.followup.send(embed=embed, view=view, wait=True)
            await response.pin()
            await view.wait()

            if view.value == True:

                wait = discord.Embed(color=self.bot.blurple, title="Purge in Progress", description="Please wait while the purge is in progress. This message will be edited when the purge is complete.")
                await response.edit(embed=wait, view=None)
                channel = interaction.channel
                messages = [m async for m in channel.history(limit=None)]
                unpinned = [m for m in messages if not m.pinned]
                while len(unpinned) > 0:
                    await channel.purge(check=lambda message: message.pinned == False, oldest_first=True)
                    messages = [m async for m in channel.history(limit=None)]
                    unpinned = [m for m in messages if not m.pinned]
                
                done = discord.Embed(color=self.bot.green, title="Success", description="The purge is now complete!")
                await response.edit(embed=done, view=None)

                cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (interaction.guild.id,))
                row = await cur.fetchone()
                fetched_logging = row[0]
                if fetched_logging is not None:
                    logging = guild.get_channel(fetched_logging)
                    now = datetime.now(tz=timezone.utc)
                    log = discord.Embed(color=self.bot.blurple, title="Purge Log", description=f"{user.mention} has just purged all unpinned messages from the following channel: {channel.mention}.", timestamp=now)
                    log.set_author(name=user.display_name, icon_url=user.display_avatar)
                    log.set_thumbnail(url=user.display_avatar)
                    await logging.send(embed=log)

            elif view.value == False:
                cancelled = discord.Embed(color=self.bot.red, title="Cancelled", description="The purge has been cancelled. No messages have been deleted.")
                await response.edit(embed=cancelled, view=None)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, delete_after=30.0)
            print(traceback.format_exc())

    @app_commands.command(name="member")
    @app_commands.checks.has_permissions(administrator=True)
    async def member(self, interaction: discord.Interaction, member: discord.Member):
        """(Admin Only) Purge all of a member's unpinned messages in a set list of up to 25 channels.

        Parameters
        -----------
        member : discord.Member
            Provide the member who's unpinned messages you would like to purge.
        """
        await interaction.response.defer()
        try:
            
            user = interaction.user
            csv = ChannelSelectView(bot=self.bot, user=user)
            embed = discord.Embed(color=self.bot.blurple, title="Purge Member", description=f"Which channel(s) would you like to purge {member.mention}'s unpinned messages from?")
            response = await interaction.followup.send(embed=embed, view=csv, wait=True)
            await response.pin()
            await csv.wait()
            
            if csv.value == True:

                guild = interaction.guild
                mentions = []
                for id in csv.channel_ids:
                    channel = guild.get_channel(id)
                    mentions.append(channel.mention)
                mentionlist = ", ".join(mentions)
                yon = YesOrNo(bot=self.bot, user=user)
                embed = discord.Embed(color=self.bot.blurple, title="Confirm Purge", description=f"Please review the list of selected channels below and confirm that you would like to continue with the purge of {member.mention}'s unpinned messages from the following channels:\n\n{mentionlist}")
                await response.edit(embed=embed, view=yon)
                await yon.wait()

                if yon.value == True:

                    wait = discord.Embed(color=self.bot.blurple, title="Purge in Progress", description="Please wait while the purge is in progress. This message will be edited when the purge is complete.")
                    await response.edit(embed=wait, view=None)
                    for id in csv.channel_ids:
                        channel = guild.get_channel(id)
                        messages = [m async for m in channel.history(limit=None)]
                        unpinned = [m for m in messages if not m.pinned]
                        while len(unpinned) > 0:
                            await channel.purge(check=lambda message: message.author == member and message.pinned == False, oldest_first=True)
                            messages = [m async for m in channel.history(limit=None)]
                            unpinned = [m for m in messages if not m.pinned]
                    
                    success = discord.Embed(color=self.bot.green, title="Success", description=f'The purge is now complete!')
                    await response.edit(embed=success, view=None)

                    cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                    row = await cur.fetchone()
                    fetched_logging = row[0]
                    if fetched_logging is not None:
                        logging = guild.get_channel(fetched_logging)
                        now = datetime.now(tz=timezone.utc)
                        log = discord.Embed(color=self.bot.blurple, title="Purge Log", description=f"{user.mention} has just purged {member.mention}'s unpinned messages from the following channels: {mentionlist}.", timestamp=now)
                        log.set_author(name=user.display_name, icon_url=user.display_avatar)
                        log.set_thumbnail(url=user.display_avatar)
                        await logging.send(embed=log)

                elif yon.value == False:
                    cancelled = discord.Embed(color=self.bot.red, title="Cancelled", description='This interaction has been cancelled. No messages have been purged.')
                    await response.edit(embed=cancelled, view=None)

                else:
                    timed_out = discord.Embed(color=self.bot.yellow, title="Timed Out", description='This interaction has timed out. No messages have been purged.')
                    await response.edit(embed=timed_out, view=None)

            elif csv.value == False:
                cancelled = discord.Embed(color=self.bot.red, title="Cancelled", description='This interaction has been cancelled. No messages have been purged.')
                await response.edit(embed=cancelled, view=None)

            else:
                timed_out = discord.Embed(color=self.bot.yellow, title="Timed Out", description='This interaction has timed out. No messages have been purged.')
                await response.edit(embed=timed_out, view=None)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, view=None)
            print(traceback.format_exc())

    @app_commands.command(name="channels")
    @app_commands.checks.has_permissions(administrator=True)
    async def channels(self, interaction: discord.Interaction):
        """(Admin Only) Purge all unpinned messages in a set list of up to 25 channels.
        """
        await interaction.response.defer()
        try:
            
            user = interaction.user
            csv = ChannelSelectView(bot=self.bot, user=user)
            embed = discord.Embed(color=self.bot.blurple, title="Purge Channels", description=f"Which channel(s) would you like to purge all unpinned messages from?")
            response = await interaction.followup.send(embed=embed, view=csv, wait=True)
            await response.pin()
            await csv.wait()
            
            if csv.value == True:

                guild = interaction.guild
                mentions = []
                for id in csv.channel_ids:
                    channel = guild.get_channel(id)
                    mentions.append(channel.mention)
                mentionlist = ", ".join(mentions)
                yon = YesOrNo(bot=self.bot, user=user)
                embed = discord.Embed(color=self.bot.blurple, title="Confirm Purge", description=f"Please review the list of selected channels below and confirm that you would like to continue with the purge of all unpinned messages from the following channels:\n\n{mentionlist}")
                await response.edit(embed=embed, view=yon)
                await yon.wait()

                if yon.value == True:

                    wait = discord.Embed(color=self.bot.blurple, title="Purge in Progress", description="Please wait while the purge is in progress. This message will be edited when the purge is complete.")
                    await response.edit(embed=wait, view=None)
                    for id in csv.channel_ids:
                        channel = guild.get_channel(id)
                        messages = [m async for m in channel.history(limit=None)]
                        unpinned = [m for m in messages if not m.pinned]
                        while len(unpinned) > 0:
                            await channel.purge(check=lambda message: message.pinned == False, oldest_first=True)
                            messages = [m async for m in channel.history(limit=None)]
                            unpinned = [m for m in messages if not m.pinned]
                    
                    success = discord.Embed(color=self.bot.green, title="Success", description=f'The purge is now complete!')
                    await response.edit(embed=success, view=None)

                    cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                    row = await cur.fetchone()
                    fetched_logging = row[0]
                    if fetched_logging is not None:
                        logging = guild.get_channel(fetched_logging)
                        now = datetime.now(tz=timezone.utc)
                        log = discord.Embed(color=self.bot.blurple, title="Purge Log", description=f"{user.mention} has just purged all unpinned messages from the following channels: {mentionlist}.", timestamp=now)
                        log.set_author(name=user.display_name, icon_url=user.display_avatar)
                        log.set_thumbnail(url=user.display_avatar)
                        await logging.send(embed=log)

                elif yon.value == False:
                    cancelled = discord.Embed(color=self.bot.red, title="Cancelled", description='This interaction has been cancelled. No messages have been purged.')
                    await response.edit(embed=cancelled, view=None)

                else:
                    timed_out = discord.Embed(color=self.bot.yellow, title="Timed Out", description='This interaction has timed out. No messages have been purged.')
                    await response.edit(embed=timed_out, view=None)

            elif csv.value == False:
                cancelled = discord.Embed(color=self.bot.red, title="Cancelled", description='This interaction has been cancelled. No messages have been purged.')
                await response.edit(embed=cancelled, view=None)

            else:
                timed_out = discord.Embed(color=self.bot.yellow, title="Timed Out", description='This interaction has timed out. No messages have been purged.')
                await response.edit(embed=timed_out, view=None)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, view=None)
            print(traceback.format_exc())

    @app_commands.command(name="server")
    @app_commands.checks.has_permissions(administrator=True)
    async def server(self, interaction: discord.Interaction):
        """(Admin Only) Purges all unpinned messages in a server, excluding up to 25 channels.
        """
        await interaction.response.defer()
        try:
            
            user = interaction.user
            csv = ChannelSelectView(bot=self.bot, user=user)
            embed = discord.Embed(color=self.bot.blurple, title="Exclude Channels", description=f"Which channel(s) would you like to **exclude** from the purge?")
            response = await interaction.followup.send(embed=embed, view=csv, wait=True)
            await response.pin()
            await csv.wait()
            
            if csv.value == True:

                guild = interaction.guild
                excluded = []
                mentions = []
                for id in csv.channel_ids:
                    channel = guild.get_channel(id)
                    excluded.append(channel)
                    mentions.append(channel.mention)
                mentionlist = ", ".join(mentions)
                yon = YesOrNo(bot=self.bot, user=user)
                embed = discord.Embed(color=self.bot.blurple, title="Confirm Purge", description=f"Please review the list of excluded channels below and confirm that you would like to continue with the purge of all unpinned messages **except** from the following channels:\n\n{mentionlist}")
                await response.edit(embed=embed, view=yon)
                await yon.wait()

                if yon.value == True:

                    wait = discord.Embed(color=self.bot.blurple, title="Purge in Progress", description="Please wait while the purge is in progress. This message will be edited when the purge is complete.")
                    await response.edit(embed=wait, view=None)
                    for channel in guild.channels:
                        if channel not in excluded:
                            messages = [m async for m in channel.history(limit=None)]
                            unpinned = [m for m in messages if not m.pinned]
                            while len(unpinned) > 0:
                                await channel.purge(check=lambda message: message.pinned == False, oldest_first=True)
                                messages = [m async for m in channel.history(limit=None)]
                                unpinned = [m for m in messages if not m.pinned]
                    
                    success = discord.Embed(color=self.bot.green, title="Success", description=f'The purge is now complete!')
                    await response.edit(embed=success, view=None)

                    cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                    row = await cur.fetchone()
                    fetched_logging = row[0]
                    if fetched_logging is not None:
                        logging = guild.get_channel(fetched_logging)
                        now = datetime.now(tz=timezone.utc)
                        log = discord.Embed(color=self.bot.blurple, title="Purge Log", description=f"{user.mention} has just purged all unpinned messages from the following channels: {mentionlist}.", timestamp=now)
                        log.set_author(name=user.display_name, icon_url=user.display_avatar)
                        log.set_thumbnail(url=user.display_avatar)
                        await logging.send(embed=log)

                elif yon.value == False:
                    cancelled = discord.Embed(color=self.bot.red, title="Cancelled", description='This interaction has been cancelled. No messages have been purged.')
                    await response.edit(embed=cancelled, view=None)

                else:
                    timed_out = discord.Embed(color=self.bot.yellow, title="Timed Out", description='This interaction has timed out. No messages have been purged.')
                    await response.edit(embed=timed_out, view=None)

            elif csv.value == False:
                cancelled = discord.Embed(color=self.bot.red, title="Cancelled", description='This interaction has been cancelled. No messages have been purged.')
                await response.edit(embed=cancelled, view=None)

            else:
                timed_out = discord.Embed(color=self.bot.yellow, title="Timed Out", description='This interaction has timed out. No messages have been purged.')
                await response.edit(embed=timed_out, view=None)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, view=None)
            print(traceback.format_exc())

async def setup(bot: commands.Bot):
    print("Setting up Cog: purge.Purge")

async def teardown(bot: commands.Bot):
    print("Tearing down Cog: purge.Purge")
