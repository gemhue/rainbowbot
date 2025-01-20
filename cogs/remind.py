import discord
import aiosqlite
import traceback
import dateparser
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timezone, timedelta

class Confirm(discord.ui.View):
    def __init__(self, *, timeout = 180, bot: commands.Bot, user: discord.Member):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.user = user
        self.value = None

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
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

            embed = discord.Embed(color=self.bot.red, title="Error", description=f"{error}")
            await interaction.followup.send(embed=embed, ephemeral=True)

class ReminderButtons(discord.ui.View):
    def __init__(self, *, timeout = None, bot: commands.Bot, user: discord.Member):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.user = user
        self.value = None

    @discord.ui.button(label="Snooze (5 Minutes)", style=discord.ButtonStyle.blurple, emoji="💤")
    async def snooze(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.stop()

    @discord.ui.button(label="Close", style=discord.ButtonStyle.red, emoji="✖️")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
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

            embed = discord.Embed(color=self.bot.red, title="Error", description=f"{error}")
            await interaction.followup.send(embed=embed, ephemeral=True)

class Remind(commands.GroupCog, group_name = "remind"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        if isinstance(bot.database, aiosqlite.Connection):
            self.db = bot.database
    
    @app_commands.command(name="everyone")
    @app_commands.checks.has_permissions(administrator=True)
    async def everyone(self, interaction: discord.Interaction, what: str, when: str, where: discord.TextChannel):
        """(Admin Only) Create a reminder for everyone.

        Parameters
        -----------
        what : str
            What would you like the bot to remind everyone about?
        when : str
            When would you like the bot to send the reminder?
        where : discord.TextChannel
            Where would you like the bot to send the reminder?
        """
        await interaction.response.defer()
        try:

            user = interaction.user

            time = dateparser.parse(when)
            formatted_time1 = discord.utils.format_dt(time, style="F")
            formatted_time2 = discord.utils.format_dt(time, style="R")

            confirm = discord.Embed(color=self.bot.blurple, title="Confirm", description="Please review the following information and `confirm` that everything looks correct. Otherwise, please `cancel` the interaction and try again.")
            confirm.add_field(name="Who", value=f"@everyone", inline=False)
            confirm.add_field(name="What", value=f"{what}", inline=False)
            confirm.add_field(name="When", value=f"{formatted_time1} ({formatted_time2})", inline=False)
            confirm.add_field(name="Where", value=f"{where.mention}", inline=False)
            view = Confirm(bot=self.bot, user=user)
            response = await interaction.followup.send(embed=confirm, view=view, wait=True)
            await view.wait()

            if view.value == True:

                confirmed = discord.Embed(color=self.bot.green, title="Confirmed", description="The reminder has been set successfully.")
                await response.edit(embed=confirmed, view=None)
                await response.delete(delay=10.0)
                await discord.utils.sleep_until(when=time)

                content = f"-# @everyone"
                reminder_embed = discord.Embed(color=self.bot.blurple, title="Reminder", description=what)
                view = ReminderButtons(bot=self.bot, user=user)
                reminder = await where.send(content=content, embed=reminder_embed, allowed_mentions=discord.AllowedMentions(everyone=True), view=view)
                await view.wait()

                if view.value == True:

                    snoozing = True
                    snooze = discord.Embed(color=self.bot.blurple, title="Snoozing", description="This reminder has been snoozed for 5 minutes.")
                    await reminder.edit(content=None, embed=snooze, delete_after=10.0)
                
                elif view.value == False:

                    snoozing = False
                
                while snoozing == True:

                    now = datetime.now(tz=timezone.utc)
                    five_mins = timedelta(minutes=5.0)
                    in_5_mins = now + five_mins
                    await discord.utils.sleep_until(when=in_5_mins)

                    content = f"-# @everyone"
                    reminder_embed = discord.Embed(color=self.bot.blurple, title="Reminder", description=what)
                    view = ReminderButtons(bot=self.bot, user=user)
                    reminder = await where.send(content=content, embed=reminder_embed, allowed_mentions=discord.AllowedMentions(everyone=True), view=view)

                    if view.value == True:

                        snoozing = True
                        snooze_embed = discord.Embed(color=self.bot.blurple, title="Snoozing", description="This reminder has been snoozed for 5 minutes.")
                        await reminder.edit(content=None, embed=snooze_embed, delete_after=10.0)
                    
                    elif view.value == False:

                        snoozing = False
                
                if snoozing == False:
                    await reminder.delete()

            elif view.value == False:

                cancel = discord.Embed(color=self.bot.red, title="Cancelled", description="This interaction has been cancelled. Please try again")
                await response.edit(embed=cancel, view=None)
                await response.delete(delay=10.0)

            else:

                timeout = discord.Embed(color=self.bot.yellow, title="Timed Out", description="This interaction has timed out. Please try again")
                await response.edit(embed=timeout, view=None)
                await response.delete(delay=10.0)
        
        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, delete_after=10.0)
            print(traceback.format_exc())

    @app_commands.command(name="role")
    @app_commands.checks.has_permissions(administrator=True)
    async def role(self, interaction: discord.Interaction, who: discord.Role, what: str, when: str, where: discord.TextChannel):
        """(Admin Only) Create a reminder for all users with a specified role.

        Parameters
        -----------
        who : discord.Role
            Choose the role that should be sent the reminder.
        what : str
            What would you like the bot to remind the role about?
        when : str
            When would you like the bot to send the reminder?
        where : discord.TextChannel
            Where would you like the bot to send the reminder?
        """
        await interaction.response.defer()
        try:

            user = interaction.user

            time = dateparser.parse(when)
            formatted_time1 = discord.utils.format_dt(time, style="F")
            formatted_time2 = discord.utils.format_dt(time, style="R")

            confirm = discord.Embed(color=self.bot.blurple, title="Confirm", description="Please review the following information and `confirm` that everything looks correct. Otherwise, please `cancel` the interaction and try again.")
            confirm.add_field(name="Who", value=f"{who.mention}", inline=False)
            confirm.add_field(name="What", value=f"{what}", inline=False)
            confirm.add_field(name="When", value=f"{formatted_time1} ({formatted_time2})", inline=False)
            confirm.add_field(name="Where", value=f"{where.mention}", inline=False)
            view = Confirm(bot=self.bot, user=user)
            response = await interaction.followup.send(embed=confirm, view=view, wait=True)
            await view.wait()

            if view.value == True:

                confirmed = discord.Embed(color=self.bot.green, title="Confirmed", description="The reminder has been set successfully.")
                await response.edit(embed=confirmed, view=None)
                await response.delete(delay=10.0)
                await discord.utils.sleep_until(when=time)

                content = f"-# {who.mention}"
                reminder_embed = discord.Embed(color=self.bot.blurple, title="Reminder", description=what)
                view = ReminderButtons(bot=self.bot, user=user)
                reminder = await where.send(content=content, embed=reminder_embed, view=view)
                await view.wait()

                if view.value == True:

                    snoozing = True
                    snooze = discord.Embed(color=self.bot.blurple, title="Snoozing", description="This reminder has been snoozed for 5 minutes.")
                    await reminder.edit(content=None, embed=snooze, delete_after=10.0)
                
                elif view.value == False:

                    snoozing = False
                
                while snoozing == True:

                    now = datetime.now(tz=timezone.utc)
                    five_mins = timedelta(minutes=5.0)
                    in_5_mins = now + five_mins
                    await discord.utils.sleep_until(when=in_5_mins)

                    content = f"-# {who.mention}"
                    reminder_embed = discord.Embed(color=self.bot.blurple, title="Reminder", description=what)
                    view = ReminderButtons(bot=self.bot, user=user)
                    reminder = await where.send(content=content, embed=reminder_embed, view=view)

                    if view.value == True:

                        snoozing = True
                        snooze_embed = discord.Embed(color=self.bot.blurple, title="Snoozing", description="This reminder has been snoozed for 5 minutes.")
                        await reminder.edit(content=None, embed=snooze_embed, delete_after=10.0)
                    
                    elif view.value == False:

                        snoozing = False
                
                if snoozing == False:
                    await reminder.delete()

            elif view.value == False:

                cancel = discord.Embed(color=self.bot.red, title="Cancelled", description="This interaction has been cancelled. Please try again")
                await response.edit(embed=cancel, view=None)
                await response.delete(delay=10.0)

            else:

                timeout = discord.Embed(color=self.bot.yellow, title="Timed Out", description="This interaction has timed out. Please try again")
                await response.edit(embed=timeout, view=None)
                await response.delete(delay=10.0)
        
        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, delete_after=10.0)
            print(traceback.format_exc())

    @app_commands.command(name="user")
    @app_commands.checks.has_permissions(administrator=True)
    async def user(self, interaction: discord.Interaction, who: discord.Member, what: str, when: str, where: discord.TextChannel):
        """(Admin Only) Create a reminder for a specified user.

        Parameters
        -----------
        who : discord.Member
            Choose the user that should be sent the reminder.
        what : str
            What would you like the bot to remind the user about?
        when : str
            When would you like the bot to send the reminder?
        where : discord.TextChannel
            Where would you like the bot to send the reminder?
        """
        await interaction.response.defer()
        try:

            user = interaction.user

            time = dateparser.parse(when)
            formatted_time1 = discord.utils.format_dt(time, style="F")
            formatted_time2 = discord.utils.format_dt(time, style="R")

            confirm = discord.Embed(color=self.bot.blurple, title="Confirm", description="Please review the following information and `confirm` that everything looks correct. Otherwise, please `cancel` the interaction and try again.")
            confirm.add_field(name="Who", value=f"{who.mention}", inline=False)
            confirm.add_field(name="What", value=f"{what}", inline=False)
            confirm.add_field(name="When", value=f"{formatted_time1} ({formatted_time2})", inline=False)
            confirm.add_field(name="Where", value=f"{where.mention}", inline=False)
            view = Confirm(bot=self.bot, user=user)
            response = await interaction.followup.send(embed=confirm, view=view, wait=True)
            await view.wait()

            if view.value == True:

                confirmed = discord.Embed(color=self.bot.green, title="Confirmed", description="The reminder has been set successfully.")
                await response.edit(embed=confirmed, view=None)
                await response.delete(delay=10.0)
                await discord.utils.sleep_until(when=time)

                content = f"-# {who.mention}"
                reminder_embed = discord.Embed(color=self.bot.blurple, title="Reminder", description=what)
                view = ReminderButtons(bot=self.bot, user=who)
                reminder = await where.send(content=content, embed=reminder_embed, view=view)
                await view.wait()

                if view.value == True:

                    snoozing = True
                    snooze = discord.Embed(color=self.bot.blurple, title="Snoozing", description="This reminder has been snoozed for 5 minutes.")
                    await reminder.edit(content=None, embed=snooze, delete_after=10.0)
                
                elif view.value == False:

                    snoozing = False
                
                while snoozing == True:

                    now = datetime.now(tz=timezone.utc)
                    five_mins = timedelta(minutes=5.0)
                    in_5_mins = now + five_mins
                    await discord.utils.sleep_until(when=in_5_mins)

                    content = f"-# {who.mention}"
                    reminder_embed = discord.Embed(color=self.bot.blurple, title="Reminder", description=what)
                    view = ReminderButtons(bot=self.bot, user=who)
                    reminder = await where.send(content=content, embed=reminder_embed, view=view)

                    if view.value == True:

                        snoozing = True
                        snooze_embed = discord.Embed(color=self.bot.blurple, title="Snoozing", description="This reminder has been snoozed for 5 minutes.")
                        await reminder.edit(content=None, embed=snooze_embed, delete_after=10.0)
                    
                    elif view.value == False:

                        snoozing = False
                
                if snoozing == False:
                    await reminder.delete()

            elif view.value == False:

                cancel = discord.Embed(color=self.bot.red, title="Cancelled", description="This interaction has been cancelled. Please try again")
                await response.edit(embed=cancel, view=None)
                await response.delete(delay=10.0)

            else:

                timeout = discord.Embed(color=self.bot.yellow, title="Timed Out", description="This interaction has timed out. Please try again")
                await response.edit(embed=timeout, view=None)
                await response.delete(delay=10.0)
        
        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, delete_after=10.0)
            print(traceback.format_exc())

    @app_commands.command(name="me")
    async def me(self, interaction: discord.Interaction, what: str, when: str, where: discord.TextChannel):
        """Create a reminder for yourself.

        Parameters
        -----------
        what : str
            What would you like the bot to remind you about?
        when : str
            When would you like the bot to send the reminder?
        where : discord.TextChannel
            Where would you like the bot to send the reminder?
        """
        await interaction.response.defer()
        try:

            user = interaction.user

            time = dateparser.parse(when)
            formatted_time1 = discord.utils.format_dt(time, style="F")
            formatted_time2 = discord.utils.format_dt(time, style="R")

            confirm = discord.Embed(color=self.bot.blurple, title="Confirm", description="Please review the following information and `confirm` that everything looks correct. Otherwise, please `cancel` the interaction and try again.")
            confirm.add_field(name="What", value=f"{what}", inline=False)
            confirm.add_field(name="When", value=f"{formatted_time1} ({formatted_time2})", inline=False)
            confirm.add_field(name="Where", value=f"{where.mention}", inline=False)
            view = Confirm(bot=self.bot, user=user)
            response = await interaction.followup.send(embed=confirm, view=view, wait=True)
            await view.wait()

            if view.value == True:

                confirmed = discord.Embed(color=self.bot.green, title="Confirmed", description="The reminder has been set successfully.")
                await response.edit(embed=confirmed, view=None)
                await response.delete(delay=10.0)
                await discord.utils.sleep_until(when=time)

                content = f"-# {user.mention}"
                reminder_embed = discord.Embed(color=self.bot.blurple, title="Reminder", description=what)
                view = ReminderButtons(bot=self.bot, user=user)
                reminder = await where.send(content=content, embed=reminder_embed, view=view)
                await view.wait()

                if view.value == True:

                    snoozing = True
                    snooze = discord.Embed(color=self.bot.blurple, title="Snoozing", description="This reminder has been snoozed for 5 minutes.")
                    await reminder.edit(content=None, embed=snooze, delete_after=10.0)
                
                elif view.value == False:

                    snoozing = False
                
                while snoozing == True:

                    now = datetime.now(tz=timezone.utc)
                    five_mins = timedelta(minutes=5.0)
                    in_5_mins = now + five_mins
                    await discord.utils.sleep_until(when=in_5_mins)

                    content = f"-# {user.mention}"
                    reminder_embed = discord.Embed(color=self.bot.blurple, title="Reminder", description=what)
                    view = ReminderButtons(bot=self.bot, user=user)
                    reminder = await where.send(content=content, embed=reminder_embed, view=view)

                    if view.value == True:

                        snoozing = True
                        snooze_embed = discord.Embed(color=self.bot.blurple, title="Snoozing", description="This reminder has been snoozed for 5 minutes.")
                        await reminder.edit(content=None, embed=snooze_embed, delete_after=10.0)
                    
                    elif view.value == False:

                        snoozing = False
                
                if snoozing == False:
                    await reminder.delete()

            elif view.value == False:

                cancel = discord.Embed(color=self.bot.red, title="Cancelled", description="This interaction has been cancelled. Please try again")
                await response.edit(embed=cancel, view=None)
                await response.delete(delay=10.0)

            else:

                timeout = discord.Embed(color=self.bot.yellow, title="Timed Out", description="This interaction has timed out. Please try again")
                await response.edit(embed=timeout, view=None)
                await response.delete(delay=10.0)
        
        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, delete_after=10.0)
            print(traceback.format_exc())

async def setup(bot: commands.Bot):
    print("Setting up Cog: remind.Remind")

async def teardown(bot: commands.Bot):
    print("Tearing down Cog: remind.Remind")