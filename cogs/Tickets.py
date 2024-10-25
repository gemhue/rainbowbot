import discord
import aiosqlite
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timezone

class TicketButtons(discord.ui.View):
    def __init__(self, *, timeout = None):
        super().__init__(timeout=timeout)
        self.blurple = discord.Colour.blurple()
        self.green = discord.Colour.green()
        self.red = discord.Colour.red()

    @discord.ui.button(label="Verification", custom_id="persistent:verification", style=discord.ButtonStyle.blurple, emoji="🔑")
    async def verification(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        try:
            async with aiosqlite.connect('rainbowbot.db') as db:
                channel = interaction.channel
                user = interaction.user
                content = f"-# {user.mention}"
                thread = await channel.create_thread(name=f"{user.display_name}", reason="Verification", invitable=False)
                guild = interaction.guild
                guild_id = guild.id
                await db.execute("INSERT OR IGNORE INTO tickets (guild_id) VALUES (?)", (guild_id,))
                cur = await db.execute("SELECT staff_role_id FROM tickets WHERE guild_id = ?", (guild_id,))
                row = await cur.fetchone()
                staff_role_id = row[0]
                staff = guild.get_role(staff_role_id)
                if staff is not None:
                    await thread.add_user(staff)
                    content = f"-# {user.mention} {staff.mention}"
                await thread.add_user(user)
                embed = discord.Embed(color=self.blurple, title="Ticket Created", description=f"Hello, {user.mention}! You have just successfully created a ticket to start the **verification** process. Please await further instruction from {staff.mention}. Thank you!")
                await thread.send(content=content, embed=embed, view=ThreadButton())
                embed = discord.Embed(color=self.green, title="Ticket Created", description=f"You can find your ticket here: {thread.mention}.")
                await interaction.followup.send(embed=embed, ephemeral=True)
                cur = await db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                row = await cur.fetchone()
                fetched_logging = row[0]
                if fetched_logging is not None:
                    logging = guild.get_channel(fetched_logging)
                    now = datetime.now(tz=timezone.utc)
                    log = discord.Embed(color=self.blurple, title="Ticket Log", description=f"{interaction.user.mention} has just created a ticket.", timestamp=now)
                    log.add_field(name="Reason", value="Verification", inline=False)
                    log.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
                    await logging.send(embed=log)
                db.commit()
                db.close()
        except Exception as e:
            error = discord.Embed(color=self.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, ephemeral=True)
    
    @discord.ui.button(label="Question", custom_id="persistent:question", style=discord.ButtonStyle.blurple, emoji="❓")
    async def question(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        try:
            async with aiosqlite.connect('rainbowbot.db') as db:
                channel = interaction.channel
                user = interaction.user
                content = f"-# {user.mention}"
                thread = await channel.create_thread(name=f"{user.display_name}", reason="Question", invitable=False)
                guild = interaction.guild
                guild_id = guild.id
                await db.execute("INSERT OR IGNORE INTO tickets (guild_id) VALUES (?)", (guild_id,))
                cur = await db.execute("SELECT staff_role_id FROM tickets WHERE guild_id = ?", (guild_id,))
                row = await cur.fetchone()
                staff_role_id = row[0]
                staff = guild.get_role(staff_role_id)
                if staff is not None:
                    await thread.add_user(staff)
                    content = f"-# {user.mention} {staff.mention}"
                await thread.add_user(user)
                embed = discord.Embed(color=self.blurple, title="Ticket Created", description=f"Hello, {user.mention}! You have just successfully created a ticket to ask a **question**. Please ask your question here and await a response from {staff.mention}. Thank you!")
                await thread.send(content=content, embed=embed, view=ThreadButton())
                embed = discord.Embed(color=self.green, title="Ticket Created", description=f"You can find your ticket here: {thread.mention}.")
                await interaction.followup.send(embed=embed, ephemeral=True)
                cur = await db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                row = await cur.fetchone()
                fetched_logging = row[0]
                if fetched_logging is not None:
                    logging = guild.get_channel(fetched_logging)
                    now = datetime.now(tz=timezone.utc)
                    log = discord.Embed(color=self.blurple, title="Ticket Log", description=f"{interaction.user.mention} has just created a ticket.", timestamp=now)
                    log.add_field(name="Reason", value="Question", inline=False)
                    log.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
                    await logging.send(embed=log)
                db.commit()
                db.close()
        except Exception as e:
            error = discord.Embed(color=self.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, ephemeral=True)

    @discord.ui.button(label="Suggestion", custom_id="persistent:suggestion", style=discord.ButtonStyle.blurple, emoji="💡")
    async def suggestion(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        try:
            async with aiosqlite.connect('rainbowbot.db') as db:
                channel = interaction.channel
                user = interaction.user
                content = f"-# {user.mention}"
                thread = await channel.create_thread(name=f"{user.display_name}", reason="Suggestion", invitable=False)
                guild = interaction.guild
                guild_id = guild.id
                await db.execute("INSERT OR IGNORE INTO tickets (guild_id) VALUES (?)", (guild_id,))
                cur = await db.execute("SELECT staff_role_id FROM tickets WHERE guild_id = ?", (guild_id,))
                row = await cur.fetchone()
                staff_role_id = row[0]
                staff = guild.get_role(staff_role_id)
                if staff is not None:
                    await thread.add_user(staff)
                    content = f"-# {user.mention} {staff.mention}"
                await thread.add_user(user)
                embed = discord.Embed(color=self.blurple, title="Ticket Created", description=f"Hello, {user.mention}! You have just successfully created a ticket to make a **suggestion**. Please provide your suggestion here and await a response from {staff.mention}. Thank you!")
                await thread.send(content=content, embed=embed, view=ThreadButton())
                embed = discord.Embed(color=self.green, title="Ticket Created", description=f"You can find your ticket here: {thread.mention}.")
                await interaction.followup.send(embed=embed, ephemeral=True)
                cur = await db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                row = await cur.fetchone()
                fetched_logging = row[0]
                if fetched_logging is not None:
                    logging = guild.get_channel(fetched_logging)
                    now = datetime.now(tz=timezone.utc)
                    log = discord.Embed(color=self.blurple, title="Ticket Log", description=f"{interaction.user.mention} has just created a ticket.", timestamp=now)
                    log.add_field(name="Reason", value="Suggestion", inline=False)
                    log.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
                    await logging.send(embed=log)
                db.commit()
                db.close()
        except Exception as e:
            error = discord.Embed(color=self.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, ephemeral=True)

    @discord.ui.button(label="Complaint", custom_id="persistent:complaint", style=discord.ButtonStyle.blurple, emoji="📢")
    async def complaint(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        try:
            async with aiosqlite.connect('rainbowbot.db') as db:
                channel = interaction.channel
                user = interaction.user
                content = f"-# {user.mention}"
                thread = await channel.create_thread(name=f"{user.display_name}", reason="Complaint", invitable=False)
                guild = interaction.guild
                guild_id = guild.id
                await db.execute("INSERT OR IGNORE INTO tickets (guild_id) VALUES (?)", (guild_id,))
                cur = await db.execute("SELECT staff_role_id FROM tickets WHERE guild_id = ?", (guild_id,))
                row = await cur.fetchone()
                staff_role_id = row[0]
                staff = guild.get_role(staff_role_id)
                if staff is not None:
                    await thread.add_user(staff)
                    content = f"-# {user.mention} {staff.mention}"
                await thread.add_user(user)
                embed = discord.Embed(color=self.blurple, title="Ticket Created", description=f"Hello, {user.mention}! You have just successfully created a ticket to make a **complaint**. Please provide your complaint here and await a response from {staff.mention}. Thank you!")
                await thread.send(content=content, embed=embed, view=ThreadButton())
                embed = discord.Embed(color=self.green, title="Ticket Created", description=f"You can find your ticket here: {thread.mention}.")
                await interaction.followup.send(embed=embed, ephemeral=True)
                cur = await db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                row = await cur.fetchone()
                fetched_logging = row[0]
                if fetched_logging is not None:
                    logging = guild.get_channel(fetched_logging)
                    now = datetime.now(tz=timezone.utc)
                    log = discord.Embed(color=self.blurple, title="Ticket Log", description=f"{interaction.user.mention} has just created a ticket.", timestamp=now)
                    log.add_field(name="Reason", value="Complaint", inline=False)
                    log.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
                    await logging.send(embed=log)
                db.commit()
                db.close()
        except Exception as e:
            error = discord.Embed(color=self.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, ephemeral=True)

    @discord.ui.button(label="Report Member", custom_id="persistent:report", style=discord.ButtonStyle.blurple, emoji="🚨")
    async def report(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        try:
            async with aiosqlite.connect('rainbowbot.db') as db:
                channel = interaction.channel
                user = interaction.user
                content = f"-# {user.mention}"
                thread = await channel.create_thread(name=f"{user.display_name}", reason="Report", invitable=False)
                guild = interaction.guild
                guild_id = guild.id
                await db.execute("INSERT OR IGNORE INTO tickets (guild_id) VALUES (?)", (guild_id,))
                cur = await db.execute("SELECT staff_role_id FROM tickets WHERE guild_id = ?", (guild_id,))
                row = await cur.fetchone()
                staff_role_id = row[0]
                staff = guild.get_role(staff_role_id)
                if staff is not None:
                    await thread.add_user(staff)
                    content = f"-# {user.mention} {staff.mention}"
                await thread.add_user(user)
                embed = discord.Embed(color=self.blurple, title="Ticket Created", description=f"Hello, {user.mention}! You have just successfully created a ticket to **report a member**. Please provide the details of the report here and await a response from {staff.mention}. Thank you!")
                await thread.send(content=content, embed=embed, view=ThreadButton())
                embed = discord.Embed(color=self.green, title="Ticket Created", description=f"You can find your ticket here: {thread.mention}.")
                await interaction.followup.send(embed=embed, ephemeral=True)
                cur = await db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                row = await cur.fetchone()
                fetched_logging = row[0]
                if fetched_logging is not None:
                    logging = guild.get_channel(fetched_logging)
                    now = datetime.now(tz=timezone.utc)
                    log = discord.Embed(color=self.blurple, title="Ticket Log", description=f"{interaction.user.mention} has just created a ticket.", timestamp=now)
                    log.add_field(name="Reason", value="Report", inline=False)
                    log.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
                    await logging.send(embed=log)
                db.commit()
                db.close()
        except Exception as e:
            error = discord.Embed(color=self.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, ephemeral=True)

    @discord.ui.button(label="Other", custom_id="persistent:other", style=discord.ButtonStyle.blurple, emoji="✉️")
    async def other(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        try:
            async with aiosqlite.connect('rainbowbot.db') as db:
                channel = interaction.channel
                user = interaction.user
                content = f"-# {user.mention}"
                thread = await channel.create_thread(name=f"{user.display_name}", reason="Other", invitable=False)
                guild = interaction.guild
                guild_id = guild.id
                await db.execute("INSERT OR IGNORE INTO tickets (guild_id) VALUES (?)", (guild_id,))
                cur = await db.execute("SELECT staff_role_id FROM tickets WHERE guild_id = ?", (guild_id,))
                row = await cur.fetchone()
                staff_role_id = row[0]
                staff = guild.get_role(staff_role_id)
                if staff is not None:
                    await thread.add_user(staff)
                    content = f"-# {user.mention} {staff.mention}"
                await thread.add_user(user)
                embed = discord.Embed(color=self.blurple, title="Ticket Created", description=f"Hello, {user.mention}! You have just successfully created a ticket. Please provide the reason that you created the ticket here and await a response from {staff.mention}. Thank you!")
                await thread.send(content=content, embed=embed, view=ThreadButton())
                embed = discord.Embed(color=self.green, title="Ticket Created", description=f"You can find your ticket here: {thread.mention}.")
                await interaction.followup.send(embed=embed, ephemeral=True)
                cur = await db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                row = await cur.fetchone()
                fetched_logging = row[0]
                if fetched_logging is not None:
                    logging = guild.get_channel(fetched_logging)
                    now = datetime.now(tz=timezone.utc)
                    log = discord.Embed(color=self.blurple, title="Ticket Log", description=f"{interaction.user.mention} has just created a ticket.", timestamp=now)
                    log.add_field(name="Reason", value="Other", inline=False)
                    log.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
                    await logging.send(embed=log)
                db.commit()
                db.close()
        except Exception as e:
            error = discord.Embed(color=self.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, ephemeral=True)

class ThreadButton(discord.ui.View):
    def __init__(self, *, timeout = None):
        super().__init__(timeout=timeout)
        self.blurple = discord.Colour.blurple()
        self.red = discord.Colour.red()
    
    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.blurple, emoji="🔒")
    async def close(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            embed = discord.Embed(color=self.blurple, title="Close Ticket", description="Are you sure you want to close this ticket? Please make sure that your issue is resolved before confirming.")
            await interaction.followup.send(embed=embed, view=ConfirmButton())
        except Exception as e:
            error = discord.Embed(color=self.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error)

class ConfirmButton(discord.ui.View):
    def __init__(self, *, timeout = None):
        super().__init__(timeout=timeout)
        self.blurple = discord.Colour.blurple()
        self.red = discord.Colour.red()
    
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, emoji="🟢")
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        try:
            guild = interaction.guild
            channel = interaction.channel
            thread = guild.get_thread(channel.id)
            if thread is not None:
                await thread.delete(reason=f"Ticket closed by {interaction.user.display_name}.")
                async with aiosqlite.connect('rainbowbot.db') as db:
                    cur = await db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                    row = await cur.fetchone()
                    fetched_logging = row[0]
                    if fetched_logging is not None:
                        logging = guild.get_channel(fetched_logging)
                        now = datetime.now(tz=timezone.utc)
                        log = discord.Embed(color=self.blurple, title="Ticket Log", description=f"{interaction.user.mention} has just closed a ticket.", timestamp=now)
                        log.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
                        await logging.send(embed=log)
                    db.commit()
                    db.close()
            else:
                embed = discord.Embed(color=self.red, title="Error", description="There was a problem closing the thread. Please try again later.")
                await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            error = discord.Embed(color=self.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, ephemeral=True)
    
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, emoji="🔴")
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        try:
            await interaction.message.delete()
        except Exception as e:
            error = discord.Embed(color=self.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, ephemeral=True)

class Tickets(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.blurple = discord.Colour.blurple()
        self.green = discord.Colour.green()
        self.red = discord.Colour.red()
    
    @commands.hybrid_group(name="tickets", fallback="setup")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def tickets(self, ctx: commands.Context, channel: discord.TextChannel, staff_role: discord.Role):
        """(Admin Only) Set up a ticketing system for the server.
        
        Parameters
        -----------
        channel : discord.TextChannel
            Provide the channel where the ticketing system should be posted.
        staff_role : discord.Role
            Provide the role that should be pinged when a ticket is opened.
        """
        await ctx.defer(ephemeral=True)
        try:
            async with aiosqlite.connect('rainbowbot.db') as db:
                guild_id = ctx.guild.id
                channel_id = channel.id
                role_id = staff_role.id
                await db.execute("INSERT OR IGNORE INTO tickets (guild_id) VALUES (?)", (guild_id,))
                await db.execute("UPDATE tickets SET channel_id = ? WHERE guild_id = ?", (channel_id, guild_id))
                await db.execute("UPDATE tickets SET role_id = ? WHERE guild_id = ?", (role_id, guild_id))
                embed = discord.Embed(color=self.blurple, title="🎫 Create a Ticket", description="Creating a ticket will open a private thread where you will be able to communicate with the server's staff or moderation team. To create a ticket, choose a reason from the options below.", view=TicketButtons())
                await channel.send(embed=embed)
                success = discord.Embed(color=self.green, title="Success", description=f"The ticketing system has been set up!")
                success.add_field(name="Channel", value=f"{channel.mention}", inline=False)
                success.add_field(name="Staff Role", value=f"{staff_role.mention}", inline=False)
                await ctx.send(embed=success, ephemeral=True)
                cur = await db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (ctx.guild.id,))
                row = await cur.fetchone()
                fetched_logging = row[0]
                if fetched_logging is not None:
                    logging = self.bot.get_channel(fetched_logging)
                    now = datetime.now(tz=timezone.utc)
                    log = discord.Embed(color=self.blurple, title="Ticket Log", description=f"{ctx.author.mention} has just set up a ticketing system for the server.", timestamp=now)
                    log.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
                    await logging.send(embed=log)
                db.commit()
                db.close()
        except Exception as e:
            error = discord.Embed(color=self.red, title="Error", description=f"{e}")
            await ctx.send(embed=error, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Tickets(bot), override=True)
    async with aiosqlite.connect('rainbowbot.db') as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS tickets(
                        guild_id INTEGER PRIMARY KEY,
                        channel_id INTEGER DEFAULT NULL,
                        role_id INTEGER DEFAULT NULL)""")
        await db.commit()
        await db.close()
    bot.add_view(TicketButtons())