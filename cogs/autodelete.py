import discord
import aiosqlite
import traceback
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timezone

class AutoDelete(commands.GroupCog, group_name="autodelete"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        if isinstance(bot.database, aiosqlite.Connection):
            self.db = bot.database
    
    @app_commands.command(name="start")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.choices(
        interval = [
            app_commands.Choice(name="1 Minute", value=1),
            app_commands.Choice(name="15 Minutes", value=15),
            app_commands.Choice(name="30 Minutes", value=30),
            app_commands.Choice(name="45 Minutes", value=45),
            app_commands.Choice(name="1 Hour", value=60),
            app_commands.Choice(name="6 Hours", value=360),
            app_commands.Choice(name="12 Hours", value=720),
            app_commands.Choice(name="18 Hours", value=1080),
            app_commands.Choice(name="1 Day", value=1440),
            app_commands.Choice(name="1 Week", value=10080),
            app_commands.Choice(name="2 Weeks", value=20160)
        ]
    )
    async def start(self, interaction: discord.Interaction, interval: app_commands.Choice[int]):
        """(Admin Only) Sets the messages in the current channel to be autodeleted.

        Parameters
        -----------
        interval : int
            How long should a message stay in this channel before being automatically deleted?
        """
        await interaction.response.defer(ephemeral=True)
        try:
            # Add the channel_id to the database if necessary
            await self.db.execute("INSERT OR INGORE INTO autodelete (channel_id) VALUES (?)", (interaction.channel.id,))
            await self.db.commit()

            # Update and retrieve the interval
            await self.db.execute("UPDATE autodelete SET interval = ? WHERE channel_id = ?", (interval, interaction.channel.id))
            await self.db.commit()
            cur = await self.db.execute("SELECT interval FROM autodelete WHERE channel_id = ?", (interaction.channel.id,))
            row = await cur.fetchone()
            interval = row[0]

            # Send a message that the AutoDelete has been set
            embed = discord.Embed(color=self.bot.green, title="Success", description=f"The autodelete for {interaction.channel.mention} has been set up. Any unpinned messages older than **{interval} minutes** will be automatically deleted.")
            await interaction.followup.send(embed=embed, ephemeral=True)

            # Send a log to the logging channel
            cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (interaction.guild.id,))
            row = await cur.fetchone()
            fetched_logging = row[0]
            if fetched_logging is not None:
                now = datetime.now(tz=timezone.utc)
                log = discord.Embed(color=self.bot.blurple, title="AutoDelete Log", description=f"{interaction.user.mention} has just set up AutoDelete for {interaction.channel.mention}. Any unpinned messages in the channel older than **{interval} minutes** will be automatically deleted.", timestamp=now)
                log.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
                log.set_thumbnail(url=interaction.user.display_avatar)
                logging = self.bot.get_channel(fetched_logging)
                await logging.send(embed=log)

        # Send an error message if there is an issue
        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, ephemeral=True)
            print(traceback.format_exc())

    @app_commands.command(name="cancel")
    @app_commands.checks.has_permissions(administrator=True)
    async def cancel(self, interaction: discord.Interaction):
        """(Admin Only) Cancels the autodelete set for the current channel.
        """
        await interaction.response.defer(ephemeral=True)
        try:
            # Delete the channel_id from the database
            await self.db.execute("DELETE FROM autodelete WHERE channel_id = ?", (interaction.channel.id,))
            await self.db.commit()

            # Confirm that the channel_id has been removed from autodelete
            cur = await self.db.execute("SELECT EXISTS(SELECT 1 FROM autodelete WHERE channel_id = ?)", (interaction.channel.id,))
            row = await cur.fetchone()
            exists = row[0]

            if exists == 0:

                # Send a message that the AutoDelete has been cancelled
                embed = discord.Embed(color=self.bot.green, title="Success", description=f"The autodelete for {interaction.channel.mention} has been cancelled.")
                await interaction.followup.send(embed=embed, ephemeral=True)

                # Send a log to the logging channel
                cur = await self.db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (interaction.guild.id,))
                row = await cur.fetchone()
                fetched_logging = row[0]
                if fetched_logging is not None:
                    now = datetime.now(tz=timezone.utc)
                    log = discord.Embed(color=self.bot.blurple, title="AutoDelete Log", description=f"{interaction.user.mention} has just cancelled AutoDelete for {interaction.channel.mention}.", timestamp=now)
                    log.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar)
                    log.set_thumbnail(url=interaction.user.display_avatar)
                    logging = self.bot.get_channel(fetched_logging)
                    await logging.send(embed=log)

            else:

                # Send a message that there was an issue cancelling the AutoDelete
                error = discord.Embed(color=self.bot.red, title="Error", description="There was an issue cancelling the AutoDelete. Please try again later.")
                await interaction.followup.send(embed=error, ephemeral=True)

        # Send an error message if there is an issue
        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, ephemeral=True)
            print(traceback.format_exc())

async def setup(bot: commands.Bot):
    print("Setting up Cog: autodelete.AutoDelete")

async def teardown(bot: commands.Bot):
    print("Tearing down Cog: autodelete.AutoDelete")