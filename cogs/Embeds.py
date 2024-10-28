import discord
import aiosqlite
from discord import app_commands
from discord.ext import commands
from typing import Optional
from datetime import datetime, timezone

class Embeds(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.hybrid_group(name="embed", fallback="send")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def embed(self, ctx: commands.Context, message_content: Optional[str], embed_color: Optional[str], embed_title: Optional[str], embed_url: Optional[str], embed_description: Optional[str]):
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
        await ctx.defer()
        try:
            if embed_color is not None:
                color = discord.Colour.from_str(embed_color)
            else:
                color = discord.Colour.blurple()
            time = datetime.now(tz=timezone.utc)
            embed = discord.Embed(color=color, title=embed_title, url=embed_url, description=embed_description, timestamp=time)
            author = ctx.author
            name = author.display_name
            icon = author.display_avatar
            embed.set_author(name=name, icon_url=icon)
            await ctx.send(content=message_content, embed=embed)
        except Exception as e:
            red = discord.Colour.red()
            error = discord.Embed(color=red, title="Error", description=f"{e}")
            await ctx.send(embed=error, delete_after=30.0)
    
    @embed.command(name="edit")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def edit(self, ctx: commands.Context, message_url: str, message_content: Optional[str], embed_color: Optional[str], embed_title: Optional[str], embed_url: Optional[str], embed_description: Optional[str]):
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
        await ctx.defer(ephemeral=True)
        try:
            conv = commands.MessageConverter()
            message = await conv.convert(ctx, message_url)
            oldembed = message.embeds[0]
            if message_content is None:
                content = message.content
            if embed_color is not None:
                color = discord.Colour.from_str(embed_color)
            else:
                color = oldembed.colour
            if embed_title is None:
                title = oldembed.title
            if embed_url is None:
                url = oldembed.url
            if embed_description is None:
                description = oldembed.description
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
            editor = ctx.author
            editor_name = editor.display_name
            editor_icon = editor.display_avatar
            embed.set_footer(text=f"Edited at {time} by {editor_name}", icon_url=editor_icon)
            await message.edit(content=content, embed=embed)
            green = discord.Colour.green()
            success = discord.Embed(color=green, title="Success", description="The embed has been successfully edited.")
            await ctx.send(embed=success, delete_after=30.0, ephemeral=True)
        except Exception as e:
            red = discord.Colour.red()
            error = discord.Embed(color=red, title="Error", description=f"{e}")
            await ctx.send(embed=error, delete_after=30.0, ephemeral=True)

    @embed.command(name="set_image")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def set_image(self, ctx: commands.Context, message_url: str, image_url: str):
        """(Admin Only) Run this command to set an embed's image.

        Parameters
        -----------
        message_url : str
            Provide the URL of the message containing the embed.
        image_url : str
            Provide the URL of the image.
        """
        await ctx.defer(ephemeral=True)
        try:
            conv = commands.MessageConverter()
            message = await conv.convert(ctx, message_url)
            content = message.content
            embed = message.embeds[0]
            embed.set_image(url=image_url)
            await message.edit(content=content, embed=embed)
            green = discord.Colour.green()
            success = discord.Embed(color=green, title="Success", description="The image has been successfully added to the embed.")
            await ctx.send(embed=success, delete_after=30.0, ephemeral=True)
        except Exception as e:
            red = discord.Colour.red()
            error = discord.Embed(color=red, title="Error", description=f"{e}")
            await ctx.send(embed=error, delete_after=30.0, ephemeral=True)

    @embed.command(name="remove_image")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def remove_image(self, ctx: commands.Context, message_url: str, image_url: str):
        """(Admin Only) Run this command to remove an embed's image.

        Parameters
        -----------
        message_url : str
            Provide the URL of the message containing the embed.
        """
        await ctx.defer(ephemeral=True)
        try:
            conv = commands.MessageConverter()
            message = await conv.convert(ctx, message_url)
            content = message.content
            embed = message.embeds[0]
            embed.set_image(url=None)
            await message.edit(content=content, embed=embed)
            green = discord.Colour.green()
            success = discord.Embed(color=green, title="Success", description="The image has been successfully removed from the embed.")
            await ctx.send(embed=success, delete_after=30.0, ephemeral=True)
        except Exception as e:
            red = discord.Colour.red()
            error = discord.Embed(color=red, title="Error", description=f"{e}")
            await ctx.send(embed=error, delete_after=30.0, ephemeral=True)

    @embed.command(name="set_thumbnail")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def set_thumbnail(self, ctx: commands.Context, message_url: str, thumbnail_url: str):
        """(Admin Only) Run this command to set an embed's thumbnail.

        Parameters
        -----------
        message_url : str
            Provide the URL of the message containing the embed.
        thumbnail_url : str
            Provide the URL of the thumbnail.
        """
        await ctx.defer(ephemeral=True)
        try:
            conv = commands.MessageConverter()
            message = await conv.convert(ctx, message_url)
            content = message.content
            embed = message.embeds[0]
            embed.set_thumbnail(url=thumbnail_url)
            await message.edit(content=content, embed=embed)
            green = discord.Colour.green()
            success = discord.Embed(color=green, title="Success", description="The thumbnail has been successfully added to the embed.")
            await ctx.send(embed=success, delete_after=30.0, ephemeral=True)
        except Exception as e:
            red = discord.Colour.red()
            error = discord.Embed(color=red, title="Error", description=f"{e}")
            await ctx.send(embed=error, delete_after=30.0, ephemeral=True)

    @embed.command(name="remove_thumbnail")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def remove_thumbnail(self, ctx: commands.Context, message_url: str):
        """(Admin Only) Run this command to remove an embed's thumbnail.

        Parameters
        -----------
        message_url : str
            Provide the URL of the message containing the embed.
        """
        await ctx.defer(ephemeral=True)
        try:
            conv = commands.MessageConverter()
            message = await conv.convert(ctx, message_url)
            content = message.content
            embed = message.embeds[0]
            embed.set_thumbnail(url=None)
            await message.edit(content=content, embed=embed)
            green = discord.Colour.green()
            success = discord.Embed(color=green, title="Success", description="The thumbnail has been successfully removed from the embed.")
            await ctx.send(embed=success, delete_after=30.0, ephemeral=True)
        except Exception as e:
            red = discord.Colour.red()
            error = discord.Embed(color=red, title="Error", description=f"{e}")
            await ctx.send(embed=error, delete_after=30.0, ephemeral=True)

    @embed.command(name="add_field")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def add_field(self, ctx: commands.Context, message_url: str, name: str, value: str, inline: bool):
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
        await ctx.defer(ephemeral=True)
        try:
            conv = commands.MessageConverter()
            message = await conv.convert(ctx, message_url)
            content = message.content
            embed = message.embeds[0]
            embed.add_field(name=name, value=value, inline=inline)
            await message.edit(content=content, embed=embed)
            green = discord.Colour.green()
            success = discord.Embed(color=green, title="Success", description="The embed has been successfully edited.")
            await ctx.send(embed=success, delete_after=30.0, ephemeral=True)
        except Exception as e:
            red = discord.Colour.red()
            error = discord.Embed(color=red, title="Error", description=f"{e}")
            await ctx.send(embed=error, delete_after=30.0, ephemeral=True)

    @embed.command(name="edit_field")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def edit_field(self, ctx: commands.Context, message_url: str, index: int, name: str, value: str, inline: bool):
        """(Admin Only) Run this command to edit a field of an embed by its index.

        Parameters
        -----------
        message_url : str
            Provide the URL of the message containing the embed.
        index : int
            Provide the index of the field to be edited.
        name : str
            Provide the name of the field to be edited.
        value : str
            Provide the value of the field to be edited.
        inline : bool
            Provide whether the edited field should be inline.
        """
        await ctx.defer(ephemeral=True)
        try:
            conv = commands.MessageConverter()
            message = await conv.convert(ctx, message_url)
            content = message.content
            embed = message.embeds[0]
            embed.set_field_at(index=index, name=name, value=value, inline=inline)
            await message.edit(content=content, embed=embed)
            green = discord.Colour.green()
            success = discord.Embed(color=green, title="Success", description="The embed field has been successfully edited.")
            await ctx.send(embed=success, delete_after=30.0, ephemeral=True)
        except Exception as e:
            red = discord.Colour.red()
            error = discord.Embed(color=red, title="Error", description=f"{e}")
            await ctx.send(embed=error, delete_after=30.0, ephemeral=True)

    @embed.command(name="insert_field")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def insert_field(self, ctx: commands.Context, message_url: str, index: int, name: str, value: str, inline: bool):
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
        await ctx.defer(ephemeral=True)
        try:
            conv = commands.MessageConverter()
            message = await conv.convert(ctx, message_url)
            content = message.content
            embed = message.embeds[0]
            embed.insert_field_at(index=index, name=name, value=value, inline=inline)
            await message.edit(content=content, embed=embed)
            green = discord.Colour.green()
            success = discord.Embed(color=green, title="Success", description="The embed field has been successfully inserted.")
            await ctx.send(embed=success, delete_after=30.0, ephemeral=True)
        except Exception as e:
            red = discord.Colour.red()
            error = discord.Embed(color=red, title="Error", description=f"{e}")
            await ctx.send(embed=error, delete_after=30.0, ephemeral=True)

    @embed.command(name="remove_field")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def remove_field(self, ctx: commands.Context, message_url: str, index: int):
        """(Admin Only) Run this command to remove a field from an embed by its index.

        Parameters
        -----------
        message_url : str
            Provide the URL of the message containing the embed.
        index : str
            Provide the index of the field to be removed.
        """
        await ctx.defer(ephemeral=True)
        try:
            conv = commands.MessageConverter()
            message = await conv.convert(ctx, message_url)
            content = message.content
            embed = message.embeds[0]
            embed.remove_field(index=index)
            await message.edit(content=content, embed=embed)
            green = discord.Colour.green()
            success = discord.Embed(color=green, title="Success", description="The embed field has been successfully removed.")
            await ctx.send(embed=success, delete_after=30.0, ephemeral=True)
        except Exception as e:
            red = discord.Colour.red()
            error = discord.Embed(color=red, title="Error", description=f"{e}")
            await ctx.send(embed=error, delete_after=30.0, ephemeral=True)

async def setup(bot: commands.Bot):
    async with aiosqlite.connect('rainbowbot.db') as db:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS "guilds" (
                "guild_id"	            INTEGER,
                "logging_channel_id"	INTEGER DEFAULT NULL,
                "welcome_channel_id"	INTEGER DEFAULT NULL,
                "goodbye_channel_id"	INTEGER DEFAULT NULL,
                "join_role_id"	        INTEGER DEFAULT NULL,
                "bot_role_id"	        INTEGER DEFAULT NULL,
                "active_role_id"	    INTEGER DEFAULT NULL,
                "inactive_role_id"	    INTEGER DEFAULT NULL,
                "inactive_months"	    INTEGER DEFAULT NULL,
                "award_singular"	    TEXT    DEFAULT NULL,
                "award_plural"	        TEXT    DEFAULT NULL,
                "award_emoji"	        TEXT    DEFAULT NULL,
                "award_react_toggle"	INTEGER DEFAULT 0,
                PRIMARY KEY("guild_id")
            )"""
        )
        await db.commit()
        await db.close()