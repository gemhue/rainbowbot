import discord
import traceback
from discord import app_commands
from discord.ext import commands
from typing import Optional
from datetime import datetime, timezone

class Embeds(commands.GroupCog, group_name = "embed"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.database
    
    @app_commands.command(name="send")
    @app_commands.checks.has_permissions(administrator=True)
    async def send(self, interaction: discord.Interaction, message_content: Optional[str], embed_color: Optional[str], embed_title: Optional[str], embed_url: Optional[str], embed_description: Optional[str]):
        """(Admin Only) Run this command to send an embed to the current channel.

        Parameters
        -----------
        message_content : str, optional
            Provide the content of the message above the embed.
        embed_color : str, optional
            Provide the embed's color (HEX or RGB).
        embed_title : str, optional
            Provide the embed's title.
        embed_url : str, optional
            Provide the embed's url.
        embed_description : str, optional
            Provide the embed's description.
        """
        await interaction.response.defer()
        try:

            if embed_color is not None:
                color = discord.Colour.from_str(embed_color)
            else:
                color = self.bot.blurple
            time = datetime.now(tz=timezone.utc)
            embed = discord.Embed(color=color, title=embed_title, url=embed_url, description=embed_description, timestamp=time)
            user = interaction.user
            name = user.display_name
            icon = user.display_avatar
            embed.set_author(name=name, icon_url=icon)
            await interaction.followup.send(content=message_content, embed=embed)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error)
            print(traceback.format_exc())
    
    @app_commands.command(name="edit")
    @app_commands.checks.has_permissions(administrator=True)
    async def edit(self, interaction: discord.Interaction, message_url: str, message_content: Optional[str], embed_color: Optional[str], embed_title: Optional[str], embed_url: Optional[str], embed_description: Optional[str]):
        """(Admin Only) Run this command to edit the embed of a given message URL.

        Parameters
        -----------
        message_url : str
            Provide the URL of the message containing the embed.
        message_content : str, optional
            Provide the new content of the message above the embed.
        embed_color : str, optional
            Provide the embed's new color (HEX or RGB).
        embed_title : str, optional
            Provide the embed's new title.
        embed_url : str, optional
            Provide the embed's new URL.
        embed_description : str, optional
            Provide the embed's new description.
        """
        await interaction.response.defer(ephemeral=True)
        try:

            conv = commands.MessageConverter()
            ctx = await self.bot.get_context(interaction)
            message = await conv.convert(ctx, message_url)
            oldembed = message.embeds[0]
            if message_content is None:
                content = message.content
            else:
                content = message_content
            if embed_color is not None:
                color = discord.Colour.from_str(embed_color)
            else:
                color = oldembed.colour
            if embed_title is None:
                title = oldembed.title
            else:
                title = embed_title
            if embed_url is None:
                url = oldembed.url
            else:
                url = embed_url
            if embed_description is None:
                description = oldembed.description
            else:
                description = embed_description
            timestamp = oldembed.timestamp
            embed = discord.Embed(color=color, title=title, url=url, description=description, timestamp=timestamp)
            fields = oldembed.fields
            for field in fields:
                field_name = field.name
                field_value = field.value
                field_inline = field.inline
                embed.add_field(name=field_name, value=field_value, inline=field_inline)
            author = embed.author
            name = author.name
            icon = author.icon_url
            embed.set_author(name=name, icon_url=icon)
            timenow = datetime.now(tz=timezone.utc)
            time = discord.utils.format_dt(timenow, style="D")
            editor = interaction.user
            editor_name = editor.display_name
            editor_icon = editor.display_avatar
            embed.set_footer(text=f"Edited at {time} by {editor_name}", icon_url=editor_icon)
            await message.edit(content=content, embed=embed)
            
            success = discord.Embed(color=self.bot.green, title="Success", description="The embed has been successfully edited.")
            await interaction.followup.send(embed=success, ephemeral=True)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, ephemeral=True)
            print(traceback.format_exc())

    @app_commands.command(name="set_image")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_image(self, interaction: discord.Interaction, message_url: str, image_url: str):
        """(Admin Only) Run this command to set an embed's image.

        Parameters
        -----------
        message_url : str
            Provide the URL of the message containing the embed.
        image_url : str
            Provide the URL of the image.
        """
        await interaction.response.defer(ephemeral=True)
        try:

            conv = commands.MessageConverter()
            ctx = await self.bot.get_context(interaction)
            message = await conv.convert(ctx, message_url)
            content = message.content
            embed = message.embeds[0]
            embed.set_image(url=image_url)
            await message.edit(content=content, embed=embed)

            success = discord.Embed(color=self.bot.green, title="Success", description="The image has been successfully added to the embed.")
            await interaction.followup.send(embed=success, ephemeral=True)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, ephemeral=True)
            print(traceback.format_exc())

    @app_commands.command(name="remove_image")
    @app_commands.checks.has_permissions(administrator=True)
    async def remove_image(self, interaction: discord.Interaction, message_url: str):
        """(Admin Only) Run this command to remove an embed's image.

        Parameters
        -----------
        message_url : str
            Provide the URL of the message containing the embed.
        """
        await interaction.response.defer(ephemeral=True)
        try:

            conv = commands.MessageConverter()
            ctx = await self.bot.get_context(interaction)
            message = await conv.convert(ctx, message_url)
            content = message.content
            embed = message.embeds[0]
            embed.set_image(url=None)
            await message.edit(content=content, embed=embed)

            success = discord.Embed(color=self.bot.green, title="Success", description="The image has been successfully removed from the embed.")
            await interaction.followup.send(embed=success, ephemeral=True)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, ephemeral=True)
            print(traceback.format_exc())

    @app_commands.command(name="set_thumbnail")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_thumbnail(self, interaction: discord.Interaction, message_url: str, thumbnail_url: str):
        """(Admin Only) Run this command to set an embed's thumbnail.

        Parameters
        -----------
        message_url : str
            Provide the URL of the message containing the embed.
        thumbnail_url : str
            Provide the URL of the thumbnail.
        """
        await interaction.response.defer(ephemeral=True)
        try:

            conv = commands.MessageConverter()
            ctx = await self.bot.get_context(interaction)
            message = await conv.convert(ctx, message_url)
            content = message.content
            embed = message.embeds[0]
            embed.set_thumbnail(url=thumbnail_url)
            await message.edit(content=content, embed=embed)

            success = discord.Embed(color=self.bot.green, title="Success", description="The thumbnail has been successfully added to the embed.")
            await interaction.followup.send(embed=success, ephemeral=True)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, ephemeral=True)
            print(traceback.format_exc())

    @app_commands.command(name="remove_thumbnail")
    @app_commands.checks.has_permissions(administrator=True)
    async def remove_thumbnail(self, interaction: discord.Interaction, message_url: str):
        """(Admin Only) Run this command to remove an embed's thumbnail.

        Parameters
        -----------
        message_url : str
            Provide the URL of the message containing the embed.
        """
        await interaction.response.defer(ephemeral=True)
        try:

            conv = commands.MessageConverter()
            ctx = await self.bot.get_context(interaction)
            message = await conv.convert(ctx, message_url)
            content = message.content
            embed = message.embeds[0]
            embed.set_thumbnail(url=None)
            await message.edit(content=content, embed=embed)

            success = discord.Embed(color=self.bot.green, title="Success", description="The thumbnail has been successfully removed from the embed.")
            await interaction.followup.send(embed=success, ephemeral=True)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, ephemeral=True)
            print(traceback.format_exc())

    @app_commands.command(name="add_field")
    @app_commands.checks.has_permissions(administrator=True)
    async def add_field(self, interaction: discord.Interaction, message_url: str, name: str, value: str, inline: bool):
        """(Admin Only) Run this command to add a field to an embed.

        Parameters
        -----------
        message_url : str
            Provide the URL of the message containing the embed.
        name : str
            Provide the name of the field to be added.
        value : str
            Provide the value of the field to be added.
        inline : bool
            Provide whether the field should be inline.
        """
        await interaction.response.defer(ephemeral=True)
        try:

            conv = commands.MessageConverter()
            ctx = await self.bot.get_context(interaction)
            message = await conv.convert(ctx, message_url)
            content = message.content
            embed = message.embeds[0]
            embed.add_field(name=name, value=value, inline=inline)
            await message.edit(content=content, embed=embed)

            success = discord.Embed(color=self.bot.green, title="Success", description="The embed has been successfully edited.")
            await interaction.followup.send(embed=success, ephemeral=True)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, ephemeral=True)
            print(traceback.format_exc())

    @app_commands.command(name="edit_field")
    @app_commands.checks.has_permissions(administrator=True)
    async def edit_field(self, interaction: discord.Interaction, message_url: str, index: int, name: str, value: str, inline: bool):
        """(Admin Only) Run this command to edit a field of an embed by its index.

        Parameters
        -----------
        message_url : str
            Provide the URL of the message containing the embed.
        index : int
            Provide the index of the field to be edited.
        name : str
            Provide the new name of the field.
        value : str
            Provide the new value of the field.
        inline : bool
            Provide whether the edited field should be inline.
        """
        await interaction.response.defer(ephemeral=True)
        try:

            conv = commands.MessageConverter()
            ctx = await self.bot.get_context(interaction)
            message = await conv.convert(ctx, message_url)
            content = message.content
            embed = message.embeds[0]
            embed.set_field_at(index=index, name=name, value=value, inline=inline)
            await message.edit(content=content, embed=embed)

            success = discord.Embed(color=self.bot.green, title="Success", description="The embed field has been successfully edited.")
            await interaction.followup.send(embed=success, ephemeral=True)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, ephemeral=True)
            print(traceback.format_exc())

    @app_commands.command(name="insert_field")
    @app_commands.checks.has_permissions(administrator=True)
    async def insert_field(self, interaction: discord.Interaction, message_url: str, index: int, name: str, value: str, inline: bool):
        """(Admin Only) Run this command to insert an embed field at an index.

        Parameters
        -----------
        message_url : str
            Provide the URL of the message containing the embed.
        index : int
            Provide the index of the field to be inserted.
        name : str
            Provide the name of the field to be inserted.
        value : str
            Provide the value of the field to be inserted.
        inline : bool
            Provide whether the inserted field should be inline.
        """
        await interaction.response.defer(ephemeral=True)
        try:

            conv = commands.MessageConverter()
            ctx = await self.bot.get_context(interaction)
            message = await conv.convert(ctx, message_url)
            content = message.content
            embed = message.embeds[0]
            embed.insert_field_at(index=index, name=name, value=value, inline=inline)
            await message.edit(content=content, embed=embed)

            success = discord.Embed(color=self.bot.green, title="Success", description="The embed field has been successfully inserted.")
            await interaction.followup.send(embed=success, ephemeral=True)
            
        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, ephemeral=True)
            print(traceback.format_exc())

    @app_commands.command(name="remove_field")
    @app_commands.checks.has_permissions(administrator=True)
    async def remove_field(self, interaction: discord.Interaction, message_url: str, index: int):
        """(Admin Only) Run this command to remove a field from an embed by its index.

        Parameters
        -----------
        message_url : str
            Provide the URL of the message containing the embed.
        index : str
            Provide the index of the field to be removed.
        """
        await interaction.response.defer(ephemeral=True)
        try:

            conv = commands.MessageConverter()
            ctx = await self.bot.get_context(interaction)
            message = await conv.convert(ctx, message_url)
            content = message.content
            embed = message.embeds[0]
            embed.remove_field(index=index)
            await message.edit(content=content, embed=embed)

            success = discord.Embed(color=self.bot.green, title="Success", description="The embed field has been successfully removed.")
            await interaction.followup.send(embed=success, ephemeral=True)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(embed=error, ephemeral=True)
            print(traceback.format_exc())

async def setup(bot: commands.Bot):
    print("Setting up Cog: embeds.Embeds")

async def teardown(bot: commands.Bot):
    print("Tearing down Cog: embeds.Embeds")
