import discord
import traceback
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timezone, timedelta
from word2number import w2n

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

class Remind(commands.GroupCog, group_name = "remind"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.database
    
    async def timeconverter(self, when: str):
        try:

            time_list = []

            year = None
            month = None
            week = None
            day = None
            hour = None
            minute = None
            second = None

            year_list = ["year", "years", "yr", "yrs"]
            month_list = ["month", "months", "mo", "mos"]
            week_list = ["week", "weeks", "wk", "wks"]
            day_list = ["day", "days", "dy", "dys"]
            hour_list = ["hour", "hours", "hr", "hrs"]
            minute_list = ["minute", "minutes", "min", "mins"]
            second_list = ["second", "seconds", "sec", "secs"]

            words = when.split(" ")
            for word in words:
                if word in year_list:
                    word_index = words.index(word)
                    number_index = word_index - 1
                    number = words[number_index]
                    if number.isdigit():
                        year = timedelta(days=365.0*number)
                    else:
                        try:
                            newnumber = w2n.word_to_num(number)
                            year = timedelta(days=365.0*newnumber)
                        except Exception:
                            year = timedelta(days=365.0)
                    if year is not None:
                        time_list.append(year)
                elif word in month_list:
                    word_index = words.index(word)
                    number_index = word_index - 1
                    number = words[number_index]
                    if number.isdigit():
                        month = timedelta(days=30.0*number)
                    else:
                        try:
                            newnumber = w2n.word_to_num(number)
                            month = timedelta(days=30.0*newnumber)
                        except Exception:
                            month = timedelta(days=30.0)
                    if month is not None:
                        time_list.append(month)
                elif word in week_list:
                    word_index = words.index(word)
                    number_index = word_index - 1
                    number = words[number_index]
                    if number.isdigit():
                        week = timedelta(weeks=1.0*number)
                    else:
                        try:
                            newnumber = w2n.word_to_num(number)
                            week = timedelta(weeks=1.0*newnumber)
                        except Exception:
                            week = timedelta(weeks=1.0)
                    if week is not None:
                        time_list.append(week)
                elif word in day_list:
                    word_index = words.index(word)
                    number_index = word_index - 1
                    number = words[number_index]
                    if number.isdigit():
                        day = timedelta(days=1.0*number)
                    else:
                        try:
                            newnumber = w2n.word_to_num(number)
                            day = timedelta(days=1.0*newnumber)
                        except Exception:
                            day = timedelta(days=1.0)
                    if day is not None:
                        time_list.append(day)
                elif word in hour_list:
                    word_index = words.index(word)
                    number_index = word_index - 1
                    number = words[number_index]
                    if number.isdigit():
                        hour = timedelta(hours=1.0*number)
                    else:
                        try:
                            newnumber = w2n.word_to_num(number)
                            hour = timedelta(hours=1.0*newnumber)
                        except Exception:
                            hour = timedelta(hours=1.0)
                    if hour is not None:
                        time_list.append(hour)
                elif word in minute_list:
                    word_index = words.index(word)
                    number_index = word_index - 1
                    number = words[number_index]
                    if number.isdigit():
                        minute = timedelta(minutes=1.0*number)
                    else:
                        try:
                            newnumber = w2n.word_to_num(number)
                            minute = timedelta(minutes=1.0*newnumber)
                        except Exception:
                            minute = timedelta(minutes=1.0)
                    if minute is not None:
                        time_list.append(minute)
                elif word in second_list:
                    word_index = words.index(word)
                    number_index = word_index - 1
                    number = words[number_index]
                    if number.isdigit():
                        second = timedelta(seconds=1.0*number)
                    else:
                        try:
                            newnumber = w2n.word_to_num(number)
                            second = timedelta(seconds=1.0*newnumber)
                        except Exception:
                            second = timedelta(seconds=1.0)
                    if second is not None:
                        time_list.append(second)

            total_time = 0
            for time in time_list:
                total_time += time
            
            if total_time > 0:
                return total_time
            else:
                return None

        except Exception:
            print(traceback.format_exc())
    
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

            ...
        
        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, delete_after=30.0)
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

            ...
        
        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, delete_after=30.0)
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

            ...
        
        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, delete_after=30.0)
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

            time = self.timeconverter(when)

            confirm = discord.Embed(color=self.bot.blurple, title="Confirm", description="Please review the following information and confirm that everything looks correct.")
            confirm.add_field(name="What", value=what)
            confirm.add_field(name="When", value=when)
            confirm.add_field(name="Where", value=where)
            yon = YesOrNo(bot=self.bot, user=user)
            response = await interaction.followup.send(embed=confirm, view=yon)
            await yon.wait()

            if yon.value == True:

                ...

            else:

                ...
        
        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, delete_after=30.0)
            print(traceback.format_exc())

async def setup(bot: commands.Bot):
    print("Setting up Cog: remind.Remind")

async def teardown(bot: commands.Bot):
    print("Tearing down Cog: remind.Remind")