import discord
import traceback
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timezone

class TicketButtons(discord.ui.View):
    def __init__(self, *, timeout = None, bot: commands.Bot):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.db = bot.database

    @discord.ui.button(label="Verification", custom_id="persistent:verification", style=discord.ButtonStyle.blurple, emoji="🔑")
    async def verification(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:

            channel = interaction.channel
            user = interaction.user
            content = f"-# {user.mention}"
            thread = await channel.create_thread(name=f"{user.display_name}", reason="Verification", invitable=False)
            await thread.add_user(user)

            guild = interaction.guild
            await self.db.execute("INSERT OR IGNORE INTO tickets (guild_id) VALUES (?)", (guild.id,))
            await self.db.commit()

            cur = await self.db.execute("SELECT role_id FROM tickets WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            staff_role_id = row[0]
            staff = guild.get_role(staff_role_id)
            if staff is not None:
                content = f"-# {user.mention} {staff.mention}"

            embed = discord.Embed(color=self.bot.blurple, title="Ticket Created", description=f"Hello, {user.mention}! You have just successfully created a ticket to start the **verification** process. Please await further instruction from {staff.mention}. Thank you!")
            await thread.send(content=content, embed=embed, view=ThreadButton(bot=self.bot))

            embed = discord.Embed(color=self.bot.green, title="Ticket Created", description=f"You can find your ticket here: {thread.mention}.")
            await interaction.response.send_message(embed=embed, ephemeral=True)

            cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            fetched_logging = row[0]
            if fetched_logging is not None:
                logging = guild.get_channel(fetched_logging)
                now = datetime.now(tz=timezone.utc)
                log = discord.Embed(color=self.bot.blurple, title="Ticket Log", description=f"{interaction.user.mention} has just created a ticket.", timestamp=now)
                log.add_field(name="Reason", value="Verification", inline=False)
                log.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
                log.set_thumbnail(url=interaction.user.display_avatar)
                await logging.send(embed=log)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.response.send_message(embed=error, ephemeral=True)
            print(traceback.format_exc())
    
    @discord.ui.button(label="Question", custom_id="persistent:question", style=discord.ButtonStyle.blurple, emoji="❓")
    async def question(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:

            channel = interaction.channel
            user = interaction.user
            content = f"-# {user.mention}"
            thread = await channel.create_thread(name=f"{user.display_name}", reason="Question", invitable=False)
            await thread.add_user(user)

            guild = interaction.guild
            await self.db.execute("INSERT OR IGNORE INTO tickets (guild_id) VALUES (?)", (guild.id,))
            await self.db.commit()

            cur = await self.db.execute("SELECT role_id FROM tickets WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            staff_role_id = row[0]
            staff = guild.get_role(staff_role_id)
            if staff is not None:
                content = f"-# {user.mention} {staff.mention}"

            embed = discord.Embed(color=self.bot.blurple, title="Ticket Created", description=f"Hello, {user.mention}! You have just successfully created a ticket to ask a **question**. Please ask your question here and await a response from {staff.mention}. Thank you!")
            await thread.send(content=content, embed=embed, view=ThreadButton(bot=self.bot))

            embed = discord.Embed(color=self.bot.green, title="Ticket Created", description=f"You can find your ticket here: {thread.mention}.")
            await interaction.response.send_message(embed=embed, ephemeral=True)

            cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            fetched_logging = row[0]
            if fetched_logging is not None:
                logging = guild.get_channel(fetched_logging)
                now = datetime.now(tz=timezone.utc)
                log = discord.Embed(color=self.bot.blurple, title="Ticket Log", description=f"{interaction.user.mention} has just created a ticket.", timestamp=now)
                log.add_field(name="Reason", value="Question", inline=False)
                log.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
                log.set_thumbnail(url=interaction.user.display_avatar)
                await logging.send(embed=log)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.response.send_message(embed=error, ephemeral=True)
            print(traceback.format_exc())

    @discord.ui.button(label="Suggestion", custom_id="persistent:suggestion", style=discord.ButtonStyle.blurple, emoji="💡")
    async def suggestion(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:

            channel = interaction.channel
            user = interaction.user
            content = f"-# {user.mention}"
            thread = await channel.create_thread(name=f"{user.display_name}", reason="Suggestion", invitable=False)
            await thread.add_user(user)

            guild = interaction.guild
            await self.db.execute("INSERT OR IGNORE INTO tickets (guild_id) VALUES (?)", (guild.id,))
            await self.db.commit()

            cur = await self.db.execute("SELECT role_id FROM tickets WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            staff_role_id = row[0]
            staff = guild.get_role(staff_role_id)
            if staff is not None:
                content = f"-# {user.mention} {staff.mention}"

            embed = discord.Embed(color=self.bot.blurple, title="Ticket Created", description=f"Hello, {user.mention}! You have just successfully created a ticket to make a **suggestion**. Please provide your suggestion here and await a response from {staff.mention}. Thank you!")
            await thread.send(content=content, embed=embed, view=ThreadButton(bot=self.bot))

            embed = discord.Embed(color=self.bot.green, title="Ticket Created", description=f"You can find your ticket here: {thread.mention}.")
            await interaction.response.send_message(embed=embed, ephemeral=True)

            cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            fetched_logging = row[0]
            if fetched_logging is not None:
                logging = guild.get_channel(fetched_logging)
                now = datetime.now(tz=timezone.utc)
                log = discord.Embed(color=self.bot.blurple, title="Ticket Log", description=f"{interaction.user.mention} has just created a ticket.", timestamp=now)
                log.add_field(name="Reason", value="Suggestion", inline=False)
                log.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
                log.set_thumbnail(url=interaction.user.display_avatar)
                await logging.send(embed=log)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.response.send_message(embed=error, ephemeral=True)
            print(traceback.format_exc())

    @discord.ui.button(label="Complaint", custom_id="persistent:complaint", style=discord.ButtonStyle.blurple, emoji="📢")
    async def complaint(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:

            channel = interaction.channel
            user = interaction.user
            content = f"-# {user.mention}"
            thread = await channel.create_thread(name=f"{user.display_name}", reason="Complaint", invitable=False)
            await thread.add_user(user)

            guild = interaction.guild
            await self.db.execute("INSERT OR IGNORE INTO tickets (guild_id) VALUES (?)", (guild.id,))
            await self.db.commit()

            cur = await self.db.execute("SELECT role_id FROM tickets WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            staff_role_id = row[0]
            staff = guild.get_role(staff_role_id)
            if staff is not None:
                content = f"-# {user.mention} {staff.mention}"

            embed = discord.Embed(color=self.bot.blurple, title="Ticket Created", description=f"Hello, {user.mention}! You have just successfully created a ticket to make a **complaint**. Please provide your complaint here and await a response from {staff.mention}. Thank you!")
            await thread.send(content=content, embed=embed, view=ThreadButton(bot=self.bot))

            embed = discord.Embed(color=self.bot.green, title="Ticket Created", description=f"You can find your ticket here: {thread.mention}.")
            await interaction.response.send_message(embed=embed, ephemeral=True)

            cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            fetched_logging = row[0]
            if fetched_logging is not None:
                logging = guild.get_channel(fetched_logging)
                now = datetime.now(tz=timezone.utc)
                log = discord.Embed(color=self.bot.blurple, title="Ticket Log", description=f"{interaction.user.mention} has just created a ticket.", timestamp=now)
                log.add_field(name="Reason", value="Complaint", inline=False)
                log.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
                log.set_thumbnail(url=interaction.user.display_avatar)
                await logging.send(embed=log)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.response.send_message(embed=error, ephemeral=True)
            print(traceback.format_exc())

    @discord.ui.button(label="Report Member", custom_id="persistent:report", style=discord.ButtonStyle.blurple, emoji="🚨")
    async def report(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:

            channel = interaction.channel
            user = interaction.user
            content = f"-# {user.mention}"
            thread = await channel.create_thread(name=f"{user.display_name}", reason="Report", invitable=False)
            await thread.add_user(user)

            guild = interaction.guild
            await self.db.execute("INSERT OR IGNORE INTO tickets (guild_id) VALUES (?)", (guild.id,))
            await self.db.commit()

            cur = await self.db.execute("SELECT role_id FROM tickets WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            staff_role_id = row[0]
            staff = guild.get_role(staff_role_id)
            if staff is not None:
                content = f"-# {user.mention} {staff.mention}"

            embed = discord.Embed(color=self.bot.blurple, title="Ticket Created", description=f"Hello, {user.mention}! You have just successfully created a ticket to **report a member**. Please provide the details of the report here and await a response from {staff.mention}. Thank you!")
            await thread.send(content=content, embed=embed, view=ThreadButton(bot=self.bot))

            embed = discord.Embed(color=self.bot.green, title="Ticket Created", description=f"You can find your ticket here: {thread.mention}.")
            await interaction.response.send_message(embed=embed, ephemeral=True)

            cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            fetched_logging = row[0]
            if fetched_logging is not None:
                logging = guild.get_channel(fetched_logging)
                now = datetime.now(tz=timezone.utc)
                log = discord.Embed(color=self.bot.blurple, title="Ticket Log", description=f"{interaction.user.mention} has just created a ticket.", timestamp=now)
                log.add_field(name="Reason", value="Report", inline=False)
                log.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
                log.set_thumbnail(url=interaction.user.display_avatar)
                await logging.send(embed=log)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.response.send_message(embed=error, ephemeral=True)
            print(traceback.format_exc())

    @discord.ui.button(label="Other", custom_id="persistent:other", style=discord.ButtonStyle.blurple, emoji="✉️")
    async def other(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:

            channel = interaction.channel
            user = interaction.user
            content = f"-# {user.mention}"
            thread = await channel.create_thread(name=f"{user.display_name}", reason="Other", invitable=False)
            await thread.add_user(user)

            guild = interaction.guild
            await self.db.execute("INSERT OR IGNORE INTO tickets (guild_id) VALUES (?)", (guild.id,))
            await self.db.commit()

            cur = await self.db.execute("SELECT role_id FROM tickets WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            staff_role_id = row[0]
            staff = guild.get_role(staff_role_id)
            if staff is not None:
                content = f"-# {user.mention} {staff.mention}"

            embed = discord.Embed(color=self.bot.blurple, title="Ticket Created", description=f"Hello, {user.mention}! You have just successfully created a ticket. Please provide the reason that you created the ticket here and await a response from {staff.mention}. Thank you!")
            await thread.send(content=content, embed=embed, view=ThreadButton(bot=self.bot))

            embed = discord.Embed(color=self.bot.green, title="Ticket Created", description=f"You can find your ticket here: {thread.mention}.")
            await interaction.response.send_message(embed=embed, ephemeral=True)

            cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            fetched_logging = row[0]
            if fetched_logging is not None:
                logging = guild.get_channel(fetched_logging)
                now = datetime.now(tz=timezone.utc)
                log = discord.Embed(color=self.bot.blurple, title="Ticket Log", description=f"{interaction.user.mention} has just created a ticket.", timestamp=now)
                log.add_field(name="Ticket", value=f"{thread.mention}", inline=False)
                log.add_field(name="Reason", value="Other", inline=False)
                log.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
                log.set_thumbnail(url=interaction.user.display_avatar)
                await logging.send(embed=log)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.response.send_message(embed=error, ephemeral=True)
            print(traceback.format_exc())

class ThreadButton(discord.ui.View):
    def __init__(self, *, timeout = None, bot: commands.Bot):
        super().__init__(timeout=timeout)
        self.bot = bot
    
    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.blurple, emoji="🔒")
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            embed = discord.Embed(color=self.bot.blurple, title="Close Ticket", description="Are you sure you want to close this ticket? Please make sure that your issue is resolved before confirming.")
            await interaction.response.send_message(embed=embed, view=ConfirmButton(bot=self.bot))

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.response.send_message(embed=error)
            print(traceback.format_exc())

class ConfirmButton(discord.ui.View):
    def __init__(self, *, timeout = None, bot: commands.Bot):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.db = bot.database
    
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        try:

            guild = interaction.guild
            channel = interaction.channel
            thread = guild.get_thread(channel.id)
            if thread is not None:
                await thread.edit(locked=True)
            now = datetime.now(tz=timezone.utc)
            closed = discord.Embed(color=self.bot.green, title="Ticket Closed", description=f"This ticket has been closed by {interaction.user.mention}.", timestamp=now)
            await interaction.message.edit(embed=closed, view=None)

            cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
            row = await cur.fetchone()
            fetched_logging = row[0]
            if fetched_logging is not None:
                logging = guild.get_channel(fetched_logging)
                now = datetime.now(tz=timezone.utc)
                log = discord.Embed(color=self.bot.blurple, title="Ticket Log", description=f"{interaction.user.mention} has just closed a ticket.", timestamp=now)
                log.add_field(name="Ticket", value=f"{thread.mention}", inline=False)
                log.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
                log.set_thumbnail(url=interaction.user.display_avatar)
                await logging.send(embed=log)

            else:
                embed = discord.Embed(color=self.bot.red, title="Error", description="There was a problem closing the ticket. Please try again later.")
                await interaction.followup.send(ephemeral=True, embed=embed)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(ephemeral=True, embed=error)
            print(traceback.format_exc())
    
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        try:
            await interaction.message.delete()
            
        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(ephemeral=True, embed=error)
            print(traceback.format_exc())

class Tickets(commands.GroupCog, group_name = "tickets"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.database
    
    @app_commands.command(name="setup")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup(self, interaction: discord.Interaction, channel: discord.TextChannel, staff_role: discord.Role):
        """(Admin Only) Set up a ticketing system for the server.
        
        Parameters
        -----------
        channel : discord.TextChannel
            Provide the channel where the ticketing system should be posted.
        staff_role : discord.Role
            Provide the role that should be pinged when a ticket is opened.
        """
        await interaction.response.defer()

        try:

            guild = interaction.guild
            await self.db.execute("INSERT OR IGNORE INTO tickets (guild_id) VALUES (?)", (guild.id,))
            await self.db.commit()
            await self.db.execute("UPDATE tickets SET channel_id = ? WHERE guild_id = ?", (channel.id, guild.id))
            await self.db.commit()
            await self.db.execute("UPDATE tickets SET role_id = ? WHERE guild_id = ?", (staff_role.id, guild.id))
            await self.db.commit()
            embed = discord.Embed(color=self.bot.blurple, title="🎫 Create a Ticket", description="Creating a ticket will open a private thread where you will be able to communicate with the server's staff or moderation team. To create a ticket, choose a reason from the options below.")
            await channel.send(embed=embed, view=TicketButtons(bot=self.bot))

            success = discord.Embed(color=self.bot.green, title="Success", description=f"The ticketing system has been set up!")
            success.add_field(name="Channel", value=f"{channel.mention}", inline=False)
            success.add_field(name="Staff Role", value=f"{staff_role.mention}", inline=False)
            await interaction.followup.send(embed=success)

            cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (interaction.guild.id,))
            row = await cur.fetchone()
            fetched_logging = row[0]
            if fetched_logging is not None:
                logging = self.bot.get_channel(fetched_logging)
                now = datetime.now(tz=timezone.utc)
                log = discord.Embed(color=self.bot.blurple, title="Ticket Log", description=f"{interaction.user.mention} has just set up a ticketing system for the server.", timestamp=now)
                log.add_field(name="Channel", value=f"{channel.mention}", inline=False)
                log.add_field(name="Staff Role", value=f"{staff_role.mention}", inline=False)
                log.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
                log.set_thumbnail(url=interaction.user.display_avatar)
                await logging.send(embed=log)

        except Exception as e:

            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error)
            print(traceback.format_exc())

async def setup(bot: commands.Bot):
    bot.add_view(TicketButtons(bot=bot))
    print("Setting up Cog: tickets.Tickets")

async def teardown(bot: commands.Bot):
    print("Tearing down Cog: tickets.Tickets")
