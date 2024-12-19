import discord
import traceback
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timezone, timedelta

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
        self.channels = []

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.channels = [c.resolve() for c in self.values]

class ChannelSelectView(discord.ui.View):
    def __init__(self, *, timeout=180.0, bot: commands.Bot, user: discord.Member):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.user = user
        self.value = None
        self.channels = None
        self.select = ChannelSelect(user=self.user)
        self.add_item(self.select)

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green, row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.channels = self.select.channels
            self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red, row=2)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = False
            self.stop()

    async def on_timeout(self):
        self.value = None
        self.stop()
    
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
                # now = datetime.now(tz=timezone.utc)
                # two_weeks = timedelta(weeks=2.0)
                # two_weeks_ago = now - two_weeks
                channel = interaction.channel
                # messages = [m async for m in channel.history(limit=None, after=two_weeks_ago)]
                # unpinned = [m for m in messages if m.pinned == False]
                # while len(unpinned) > 0:
                deleted = await channel.purge(check=lambda m: m.pinned == False, oldest_first=True) # , after=two_weeks_ago
                    # messages = [m async for m in channel.history(limit=None, after=two_weeks_ago)]
                    # unpinned = [m for m in messages if m.pinned == False]
                if len(deleted) == 0:
                    pass
                elif len(deleted) == 1:
                    delete_embed = discord.Embed(color=self.bot.red, title="Message Deleted", description=f"{user.mention} has just deleted {len(deleted)} message from {channel.mention} via the `/purge here` command.")
                    await channel.send(embed=delete_embed)
                else:
                    delete_embed = discord.Embed(color=self.bot.red, title="Messages Deleted", description=f"{user.mention} has just deleted {len(deleted)} messages from {channel.mention} via the `/purge here` command.")
                    await channel.send(embed=delete_embed)
                
                done = discord.Embed(color=self.bot.green, title="Success", description="The purge is now complete!")
                await response.edit(embed=done, view=None)
                await response.delete(delay=10.0)

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
                cancelled = discord.Embed(color=self.bot.red, title="Cancelled", description='This interaction has been cancelled. No messages have been purged.')
                await response.edit(embed=cancelled, view=None)
                await response.delete(delay=5.0)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            error_msg = await interaction.followup.send(embed=error, wait=True)
            await error_msg.delete(delay=5.0)
            print(traceback.format_exc())

    @app_commands.command(name="self")
    async def self(self, interaction: discord.Interaction):
        """Purge all of your own unpinned messages in a set list of up to 25 channels.
        """
        await interaction.response.defer()
        try:
            
            user = interaction.user
            csv = ChannelSelectView(bot=self.bot, user=user)
            embed = discord.Embed(color=self.bot.blurple, title="Purge Self", description=f"Which channel(s) would you like to purge your own unpinned messages from?")
            response = await interaction.followup.send(embed=embed, view=csv, wait=True)
            await response.pin()
            await csv.wait()
            
            if csv.value == True:

                guild = interaction.guild
                mentions = []
                for channel in csv.channels:
                    mentions.append(channel.mention)
                mentionlist = ", ".join(mentions)
                yon = YesOrNo(bot=self.bot, user=user)
                embed = discord.Embed(color=self.bot.blurple, title="Confirm Purge", description=f"Please review the list of selected channels below and confirm that you would like to continue with the purge of your own unpinned messages from the following channels:\n\n{mentionlist}")
                await response.edit(embed=embed, view=yon)
                await yon.wait()

                if yon.value == True:

                    wait = discord.Embed(color=self.bot.blurple, title="Purge in Progress", description="Please wait while the purge is in progress. This message will be edited when the purge is complete.")
                    await response.edit(embed=wait, view=None)
                    # now = datetime.now(tz=timezone.utc)
                    # two_weeks = timedelta(weeks=2.0)
                    # two_weeks_ago = now - two_weeks
                    for channel in csv.channels:
                        # messages = [m async for m in channel.history(limit=None, after=two_weeks_ago)]
                        # unpinned = [m for m in messages if m.pinned == False and m.author == user]
                        # while len(unpinned) > 0:
                        deleted = await channel.purge(check=lambda m: m.pinned == False and m.author == user, oldest_first=True) # , after=two_weeks_ago
                            # messages = [m async for m in channel.history(limit=None, after=two_weeks_ago)]
                            # unpinned = [m for m in messages if m.pinned == False and m.author == user]
                        if len(deleted) == 0:
                            pass
                        elif len(deleted) == 1:
                            delete_embed = discord.Embed(color=self.bot.red, title="Message Deleted", description=f"{user.mention} has just deleted {len(deleted)} message from {channel.mention} via the `/purge self` command.")
                            await channel.send(embed=delete_embed)
                        else:
                            delete_embed = discord.Embed(color=self.bot.red, title="Messages Deleted", description=f"{user.mention} has just deleted {len(deleted)} messages from {channel.mention} via the `/purge self` command.")
                            await channel.send(embed=delete_embed)
                    
                    success = discord.Embed(color=self.bot.green, title="Success", description=f'The purge is now complete!')
                    await response.edit(embed=success, view=None)
                    await response.delete(delay=10.0)

                    cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                    row = await cur.fetchone()
                    fetched_logging = row[0]
                    if fetched_logging is not None:
                        logging = guild.get_channel(fetched_logging)
                        now = datetime.now(tz=timezone.utc)
                        log = discord.Embed(color=self.bot.blurple, title="Purge Log", description=f"{user.mention} has just purged {user.mention}'s unpinned messages from the following channels: {mentionlist}.", timestamp=now)
                        log.set_author(name=user.display_name, icon_url=user.display_avatar)
                        log.set_thumbnail(url=user.display_avatar)
                        await logging.send(embed=log)

                elif yon.value == False:
                    cancelled = discord.Embed(color=self.bot.red, title="Cancelled", description='This interaction has been cancelled. No messages have been purged.')
                    await response.edit(embed=cancelled, view=None)
                    await response.delete(delay=5.0)

                else:
                    timed_out = discord.Embed(color=self.bot.yellow, title="Timed Out", description='This interaction has timed out. No messages have been purged.')
                    await response.edit(embed=timed_out, view=None)
                    await response.delete(delay=5.0)

            elif csv.value == False:
                cancelled = discord.Embed(color=self.bot.red, title="Cancelled", description='This interaction has been cancelled. No messages have been purged.')
                await response.edit(embed=cancelled, view=None)
                await response.delete(delay=5.0)

            else:
                timed_out = discord.Embed(color=self.bot.yellow, title="Timed Out", description='This interaction has timed out. No messages have been purged.')
                await response.edit(embed=timed_out, view=None)
                await response.delete(delay=5.0)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            error_msg = await interaction.followup.send(embed=error, wait=True)
            await error_msg.delete(delay=5.0)
            print(traceback.format_exc())

    @app_commands.command(name="member")
    @app_commands.checks.has_permissions(administrator=True)
    async def member(self, interaction: discord.Interaction, member: discord.Member):
        """(Admin Only) Purge a member's unpinned messages in a set list of up to 25 channels.

        Parameters
        -----------
        member : discord.Member
            Choose the member to whose messages you would like to purge.
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
                for channel in csv.channels:
                    mentions.append(channel.mention)
                mentionlist = ", ".join(mentions)
                yon = YesOrNo(bot=self.bot, user=user)
                embed = discord.Embed(color=self.bot.blurple, title="Confirm Purge", description=f"Please review the list of selected channels below and confirm that you would like to continue with the purge of {member.mention}'s unpinned messages from the following channels:\n\n{mentionlist}")
                await response.edit(embed=embed, view=yon)
                await yon.wait()

                if yon.value == True:

                    wait = discord.Embed(color=self.bot.blurple, title="Purge in Progress", description="Please wait while the purge is in progress. This message will be edited when the purge is complete.")
                    await response.edit(embed=wait, view=None)
                    # now = datetime.now(tz=timezone.utc)
                    # two_weeks = timedelta(weeks=2.0)
                    # two_weeks_ago = now - two_weeks
                    for channel in csv.channels:
                        # messages = [m async for m in channel.history(limit=None, after=two_weeks_ago)]
                        # unpinned = [m for m in messages if m.pinned == False and m.author == member]
                        # while len(unpinned) > 0:
                        deleted = await channel.purge(check=lambda m: m.pinned == False and m.author == member, oldest_first=True) # , after=two_weeks_ago
                            # messages = [m async for m in channel.history(limit=None, after=two_weeks_ago)]
                            # unpinned = [m for m in messages if m.pinned == False and m.author == member]
                        if len(deleted) == 0:
                            pass
                        elif len(deleted) == 1:
                            delete_embed = discord.Embed(color=self.bot.red, title="Message Deleted", description=f"{user.mention} has just deleted {len(deleted)} message from {channel.mention} via the `/purge member` command.")
                            await channel.send(embed=delete_embed)
                        else:
                            delete_embed = discord.Embed(color=self.bot.red, title="Messages Deleted", description=f"{user.mention} has just deleted {len(deleted)} messages from {channel.mention} via the `/purge member` command.")
                            await channel.send(embed=delete_embed)
                    
                    success = discord.Embed(color=self.bot.green, title="Success", description=f'The purge is now complete!')
                    await response.edit(embed=success, view=None)
                    await response.delete(delay=10.0)

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
                    await response.delete(delay=5.0)

                else:
                    timed_out = discord.Embed(color=self.bot.yellow, title="Timed Out", description='This interaction has timed out. No messages have been purged.')
                    await response.edit(embed=timed_out, view=None)
                    await response.delete(delay=5.0)

            elif csv.value == False:
                cancelled = discord.Embed(color=self.bot.red, title="Cancelled", description='This interaction has been cancelled. No messages have been purged.')
                await response.edit(embed=cancelled, view=None)
                await response.delete(delay=5.0)

            else:
                timed_out = discord.Embed(color=self.bot.yellow, title="Timed Out", description='This interaction has timed out. No messages have been purged.')
                await response.edit(embed=timed_out, view=None)
                await response.delete(delay=5.0)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            error_msg = await interaction.followup.send(embed=error, wait=True)
            await error_msg.delete(delay=5.0)
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
                for channel in csv.channels:
                    mentions.append(channel.mention)
                mentionlist = ", ".join(mentions)
                yon = YesOrNo(bot=self.bot, user=user)
                embed = discord.Embed(color=self.bot.blurple, title="Confirm Purge", description=f"Please review the list of selected channels below and confirm that you would like to continue with the purge of all unpinned messages from the following channels:\n\n{mentionlist}")
                await response.edit(embed=embed, view=yon)
                await yon.wait()

                if yon.value == True:

                    wait = discord.Embed(color=self.bot.blurple, title="Purge in Progress", description="Please wait while the purge is in progress. This message will be edited when the purge is complete.")
                    await response.edit(embed=wait, view=None)
                    # now = datetime.now(tz=timezone.utc)
                    # two_weeks = timedelta(weeks=2.0)
                    # two_weeks_ago = now - two_weeks
                    for channel in csv.channels:
                        # messages = [m async for m in channel.history(limit=None, after=two_weeks_ago)]
                        # unpinned = [m for m in messages if m.pinned == False]
                        # while len(unpinned) > 0:
                        deleted = await channel.purge(check=lambda m: m.pinned == False, oldest_first=True) # , after=two_weeks_ago
                            # messages = [m async for m in channel.history(limit=None, after=two_weeks_ago)]
                            # unpinned = [m for m in messages if m.pinned == False]
                        if len(deleted) == 0:
                            pass
                        elif len(deleted) == 1:
                            delete_embed = discord.Embed(color=self.bot.red, title="Message Deleted", description=f"{user.mention} has just deleted {len(deleted)} message from {channel.mention} via the `/purge channels` command.")
                            await channel.send(embed=delete_embed)
                        else:
                            delete_embed = discord.Embed(color=self.bot.red, title="Messages Deleted", description=f"{user.mention} has just deleted {len(deleted)} messages from {channel.mention} via the `/purge channels` command.")
                            await channel.send(embed=delete_embed)
                    
                    success = discord.Embed(color=self.bot.green, title="Success", description=f'The purge is now complete!')
                    await response.edit(embed=success, view=None)
                    await response.delete(delay=10.0)

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
                    await response.delete(delay=5.0)

                else:
                    timed_out = discord.Embed(color=self.bot.yellow, title="Timed Out", description='This interaction has timed out. No messages have been purged.')
                    await response.edit(embed=timed_out, view=None)
                    await response.delete(delay=5.0)

            elif csv.value == False:
                cancelled = discord.Embed(color=self.bot.red, title="Cancelled", description='This interaction has been cancelled. No messages have been purged.')
                await response.edit(embed=cancelled, view=None)
                await response.delete(delay=5.0)

            else:
                timed_out = discord.Embed(color=self.bot.yellow, title="Timed Out", description='This interaction has timed out. No messages have been purged.')
                await response.edit(embed=timed_out, view=None)
                await response.delete(delay=5.0)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            error_msg = await interaction.followup.send(embed=error, wait=True)
            await error_msg.delete(delay=5.0)
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
                mentions = []
                for channel in csv.channels:
                    mentions.append(channel.mention)
                mentionlist = ", ".join(mentions)
                yon = YesOrNo(bot=self.bot, user=user)
                embed = discord.Embed(color=self.bot.blurple, title="Confirm Purge", description=f"Please review the list of excluded channels below and confirm that you would like to continue with the purge of all unpinned messages **except** from the following channels:\n\n{mentionlist}")
                await response.edit(embed=embed, view=yon)
                await yon.wait()

                if yon.value == True:

                    wait = discord.Embed(color=self.bot.blurple, title="Purge in Progress", description="Please wait while the purge is in progress. This message will be edited when the purge is complete.")
                    await response.edit(embed=wait, view=None)
                    # now = datetime.now(tz=timezone.utc)
                    # two_weeks = timedelta(weeks=2.0)
                    # two_weeks_ago = now - two_weeks
                    for channel in guild.channels:
                        if channel not in csv.channels:
                            # messages = [m async for m in channel.history(limit=None, after=two_weeks_ago)]
                            # unpinned = [m for m in messages if m.pinned == False]
                            # while len(unpinned) > 0:
                            deleted = await channel.purge(check=lambda m: m.pinned == False, oldest_first=True) # , after=two_weeks_ago
                                # messages = [m async for m in channel.history(limit=None, after=two_weeks_ago)]
                                # unpinned = [m for m in messages if m.pinned == False]
                            if len(deleted) == 0:
                                pass
                            elif len(deleted) == 1:
                                delete_embed = discord.Embed(color=self.bot.red, title="Message Deleted", description=f"{user.mention} has just deleted {len(deleted)} message from {channel.mention} via the `/purge server` command.")
                                await channel.send(embed=delete_embed)
                            else:
                                delete_embed = discord.Embed(color=self.bot.red, title="Messages Deleted", description=f"{user.mention} has just deleted {len(deleted)} messages from {channel.mention} via the `/purge server` command.")
                                await channel.send(embed=delete_embed)
                    
                    success = discord.Embed(color=self.bot.green, title="Success", description=f'The purge is now complete!')
                    await response.edit(embed=success, view=None)
                    await response.delete(delay=10.0)

                    cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                    row = await cur.fetchone()
                    fetched_logging = row[0]
                    if fetched_logging is not None:
                        logging = guild.get_channel(fetched_logging)
                        now = datetime.now(tz=timezone.utc)
                        log = discord.Embed(color=self.bot.blurple, title="Purge Log", description=f"{user.mention} has just purged all unpinned messages in the server **except** from the following channels: {mentionlist}.", timestamp=now)
                        log.set_author(name=user.display_name, icon_url=user.display_avatar)
                        log.set_thumbnail(url=user.display_avatar)
                        await logging.send(embed=log)

                elif yon.value == False:
                    cancelled = discord.Embed(color=self.bot.red, title="Cancelled", description='This interaction has been cancelled. No messages have been purged.')
                    await response.edit(embed=cancelled, view=None)
                    await response.delete(delay=5.0)

                else:
                    timed_out = discord.Embed(color=self.bot.yellow, title="Timed Out", description='This interaction has timed out. No messages have been purged.')
                    await response.edit(embed=timed_out, view=None)
                    await response.delete(delay=5.0)

            elif csv.value == False:
                cancelled = discord.Embed(color=self.bot.red, title="Cancelled", description='This interaction has been cancelled. No messages have been purged.')
                await response.edit(embed=cancelled, view=None)
                await response.delete(delay=5.0)

            else:
                timed_out = discord.Embed(color=self.bot.yellow, title="Timed Out", description='This interaction has timed out. No messages have been purged.')
                await response.edit(embed=timed_out, view=None)
                await response.delete(delay=5.0)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            error_msg = await interaction.followup.send(embed=error, wait=True)
            await error_msg.delete(delay=5.0)
            print(traceback.format_exc())

async def setup(bot: commands.Bot):
    print("Setting up Cog: purge.Purge")

async def teardown(bot: commands.Bot):
    print("Tearing down Cog: purge.Purge")