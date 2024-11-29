import discord
import traceback
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timezone

class YesOrNo(discord.ui.View):
    def __init__(self, *, timeout = 180, user: discord.Member):
        super().__init__(timeout=timeout)
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

class CustomColorModal(discord.ui.Modal, title = "Custom Color"):
    color = None
    input = discord.ui.TextInput(label="Custom Color", placeholder="Please provide a #<hex> or rgb(r,g,b) color code...")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            self.color = discord.Colour.from_str(self.input.value)
        except ValueError:
            self.color = discord.Colour.blurple()
        self.stop()
    
    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.defer()
        print(traceback.format_exc())
        self.stop()

class ColorView(discord.ui.View):
    def __init__(self, *, timeout = 180, bot: commands.Bot, user: discord.Member):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.user = user

    @discord.ui.button(label="Red", style=discord.ButtonStyle.blurple, emoji="❤️", row=1)
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            message = interaction.message
            embed = message.embeds[0]

            embed.color = discord.Colour.red()
            await message.edit(embed=embed, view=self)
    
    @discord.ui.button(label="Orange", style=discord.ButtonStyle.blurple, emoji="🧡", row=1)
    async def orange(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            message = interaction.message
            embed = message.embeds[0]

            embed.color = discord.Colour.orange()
            await message.edit(embed=embed, view=self)

    @discord.ui.button(label="Yellow", style=discord.ButtonStyle.blurple, emoji="💛", row=1)
    async def yellow(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            message = interaction.message
            embed = message.embeds[0]

            embed.color = discord.Colour.yellow()
            await message.edit(embed=embed, view=self)
    
    @discord.ui.button(label="Green", style=discord.ButtonStyle.blurple, emoji="💚", row=1)
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            message = interaction.message
            embed = message.embeds[0]

            embed.color = discord.Colour.green()
            await message.edit(embed=embed, view=self)
    
    @discord.ui.button(label="Blue", style=discord.ButtonStyle.blurple, emoji="💙", row=1)
    async def blue(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            message = interaction.message
            embed = message.embeds[0]

            embed.color = discord.Colour.blue()
            await message.edit(embed=embed, view=self)
    
    @discord.ui.button(label="Purple", style=discord.ButtonStyle.blurple, emoji="💜", row=1)
    async def purple(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            message = interaction.message
            embed = message.embeds[0]

            embed.color = discord.Colour.purple()
            await message.edit(embed=embed, view=self)
    
    @discord.ui.button(label="Pink", style=discord.ButtonStyle.blurple, emoji="🩷", row=1)
    async def pink(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            message = interaction.message
            embed = message.embeds[0]

            embed.color = discord.Colour.pink()
            await message.edit(embed=embed, view=self)
    
    @discord.ui.button(label="Custom", style=discord.ButtonStyle.blurple, emoji="🩶", row=1)
    async def custom(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:
            message = interaction.message
            embed = message.embeds[0]

            modal = CustomColorModal()
            await interaction.response.send_modal(modal)
            await modal.wait()

            embed.color = modal.color
            await message.edit(embed=embed, view=self)
    
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, emoji="✔️", row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, emoji="✖️", row=2)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = False
            self.stop()

class TitleModal(discord.ui.Modal, title = "Title"):
    title = None
    input = discord.ui.TextInput(label="Title", placeholder="Please provide a title for the embed...", max_length=256)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.title = self.input.value
        self.stop()
    
    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.defer()
        print(traceback.format_exc())
        self.stop()

class URLModal(discord.ui.Modal, title = "URL"):
    url = None
    input = discord.ui.TextInput(label="URL", placeholder="Please provide a URL for the embed...")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.url = self.input.value
        self.stop()
    
    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.defer()
        print(traceback.format_exc())
        self.stop()

class DescriptionModal(discord.ui.Modal, title = "Description"):
    description = None
    input = discord.ui.TextInput(label="Description", style=discord.TextStyle.long, placeholder="Please provide a description for the embed...", max_length=4000)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.description = self.input.value
        self.stop()
    
    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.defer()
        print(traceback.format_exc())
        self.stop()

class FieldsSelect(discord.ui.Select):
    def __init__(self, *, user: discord.Member):
        options = [
            discord.SelectOption(label="Field 1", value="0"),
            discord.SelectOption(label="Field 2", value="1"),
            discord.SelectOption(label="Field 3", value="2"),
            discord.SelectOption(label="Field 4", value="3"),
            discord.SelectOption(label="Field 5", value="4"),
            discord.SelectOption(label="Field 6", value="5"),
            discord.SelectOption(label="Field 7", value="6"),
            discord.SelectOption(label="Field 8", value="7"),
            discord.SelectOption(label="Field 9", value="8"),
            discord.SelectOption(label="Field 10", value="9"),
            discord.SelectOption(label="Field 11", value="10"),
            discord.SelectOption(label="Field 12", value="11"),
            discord.SelectOption(label="Field 13", value="12"),
            discord.SelectOption(label="Field 14", value="13"),
            discord.SelectOption(label="Field 15", value="14"),
            discord.SelectOption(label="Field 16", value="15"),
            discord.SelectOption(label="Field 17", value="16"),
            discord.SelectOption(label="Field 18", value="17"),
            discord.SelectOption(label="Field 19", value="18"),
            discord.SelectOption(label="Field 20", value="19"),
            discord.SelectOption(label="Field 21", value="20"),
            discord.SelectOption(label="Field 22", value="21"),
            discord.SelectOption(label="Field 23", value="22"),
            discord.SelectOption(label="Field 24", value="23"),
            discord.SelectOption(label="Field 25", value="24"),
        ]
        super().__init__(placeholder="Please select a field to edit...", min_values=1, max_values=1, options=options, row=1)
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.view.field = self.values[0]

class FieldsSelectView(discord.ui.View):
    def __init__(self, *, timeout = 180, user: discord.Member):
        super().__init__(timeout=timeout)
        self.user = user
        self.value = None
        self.field = None
        self.add_item(FieldsSelect(user=self.user))
    
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, emoji="✔️", row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, emoji="✖️", row=2)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.stop()

class FieldNameModal(discord.ui.Modal, title = "Field Name"):
    field_name = None
    input = discord.ui.TextInput(label="Field Name", placeholder="Please provide a name for the field...", max_length=256)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.field_name = self.input.value
        self.stop()
    
    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.defer()
        print(traceback.format_exc())
        self.stop()

class FieldValueModal(discord.ui.Modal, title = "Field Value"):
    field_value = None
    input = discord.ui.TextInput(label="Field Value", placeholder="Please provide a value for the field...", max_length=1024)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.field_value = self.input.value
        self.stop()
    
    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.defer()
        print(traceback.format_exc())
        self.stop()

class FieldEditView(discord.ui.View):
    def __init__(self, *, timeout = 180, user: discord.Member, index: int):
        super().__init__(timeout=timeout)
        self.user = user
        self.index = index
        self.value = None
    
    @discord.ui.button(label="Name", style=discord.ButtonStyle.blurple, emoji="🏷️", row=1)
    async def field_name(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:
            modal = FieldNameModal()
            await interaction.response.send_modal(modal)
            await modal.wait()

            message = interaction.message
            embed = message.embeds[0]
            field = embed.fields[self.index]
            if field is None:
                embed.insert_field_at(index=self.index, name=modal.field_name, value="Value")
            else:
                embed.set_field_at(index=self.index, name=modal.field_name)
            await message.edit(embed=embed, view=self)

    @discord.ui.button(label="Value", style=discord.ButtonStyle.blurple, emoji="📄", row=1)
    async def field_value(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:
            modal = FieldValueModal()
            await interaction.response.send_modal(modal)
            await modal.wait()
            
            message = interaction.message
            embed = message.embeds[0]
            field = embed.fields[self.index]
            if field is None:
                embed.insert_field_at(index=self.index, name="Name", value=modal.field_value)
            else:
                embed.set_field_at(index=self.index, value=modal.field_value)
            await message.edit(embed=embed, view=self)

    @discord.ui.button(label="Inline Toggle", style=discord.ButtonStyle.blurple, emoji="🌗", row=1)
    async def inline_toggle(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            message = interaction.message
            embed = message.embeds[0]
            field = embed.fields[self.index]
            if field is not None:
                if field.inline == True:
                    field.inline = False
                    button.label = "Inline: False"
                    button.emoji = "🌑"
                elif field.inline == False:
                    field.inline = True
                    button.label = "Inline: True"
                    button.emoji = "🌕"
            await message.edit(embed=embed, view=self)
    
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, emoji="✔️", row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, emoji="✖️", row=2)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = False
            self.stop()

class ImageModal(discord.ui.Modal, title = "Image"):
    image = None
    input = discord.ui.TextInput(label="Image", placeholder="Please provide a valid image URL...")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.image = self.input.value
        self.stop()
    
    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.defer()
        print(traceback.format_exc())
        self.stop()

class ThumbnailModal(discord.ui.Modal, title = "Thumbnail"):
    thumbnail = None
    input = discord.ui.TextInput(label="Thumbnail", placeholder="Please provide a valid thumbnail URL...")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.thumbnail = self.input.value
        self.stop()
    
    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.defer()
        print(traceback.format_exc())
        self.stop()

class VideoModal(discord.ui.Modal, title = "Video"):
    video = None
    input = discord.ui.TextInput(label="Video", placeholder="Please provide a valid video URL...")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.video = self.input.value
        self.stop()
    
    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.defer()
        print(traceback.format_exc())
        self.stop()

class MediaEditView(discord.ui.View):
    def __init__(self, *, timeout = 180, user: discord.Member):
        super().__init__(timeout=timeout)
        self.user = user
        self.value = None
    
    @discord.ui.button(label="Add or Edit Image", style=discord.ButtonStyle.blurple, emoji="➕", row=1)
    async def add_image(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:
            modal = ImageModal()
            await interaction.response.send_modal(modal)
            await modal.wait()

            message = interaction.message
            embed = message.embeds[0]
            try:
                if modal.image is not None:
                    embed.image.url = modal.image
            except Exception:
                embed.image.url = None
            await message.edit(embed=embed, view=self)
    
    @discord.ui.button(label="Remove Image", style=discord.ButtonStyle.blurple, emoji="➖", row=1)
    async def remove_image(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:
            message = interaction.message
            embed = message.embeds[0]
            embed.image.url = None
            await message.edit(embed=embed, view=self)

    @discord.ui.button(label="Add or Edit Thumbnail", style=discord.ButtonStyle.blurple, emoji="➕", row=1)
    async def add_thumbnail(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:
            modal = ThumbnailModal()
            await interaction.response.send_modal(modal)
            await modal.wait()

            message = interaction.message
            embed = message.embeds[0]
            try:
                if modal.thumbnail is not None:
                    embed.thumbnail.url = modal.thumbnail
            except Exception:
                embed.thumbnail.url = None
            await message.edit(embed=embed, view=self)
    
    @discord.ui.button(label="Remove Thumbnail", style=discord.ButtonStyle.blurple, emoji="➖", row=1)
    async def remove_thumbnail(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:
            message = interaction.message
            embed = message.embeds[0]
            embed.thumbnail.url = None
            await message.edit(embed=embed, view=self)
    
    @discord.ui.button(label="Add or Edit Video", style=discord.ButtonStyle.blurple, emoji="➕", row=1)
    async def add_video(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:
            modal = VideoModal()
            await interaction.response.send_modal(modal)
            await modal.wait()

            message = interaction.message
            embed = message.embeds[0]
            try:
                if modal.video is not None:
                    embed.video.url = modal.video
            except Exception:
                embed.video.url = None
            await message.edit(embed=embed, view=self)
    
    @discord.ui.button(label="Remove Video", style=discord.ButtonStyle.blurple, emoji="➖", row=1)
    async def remove_video(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:
            message = interaction.message
            embed = message.embeds[0]
            embed.video.url = None
            await message.edit(embed=embed, view=self)
    
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, emoji="✔️", row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, emoji="✖️", row=2)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = False
            self.stop()

class ChannelSelect(discord.ui.ChannelSelect):
    def __init__(self, *, user: discord.Member):
        super().__init__(
            channel_types=[discord.ChannelType.text],
            placeholder="Select the channel to send the embed to...",
            min_values=1,
            max_values=1,
            row=1
        )
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if interaction.user == self.user:
            channel = self.values[0]
            self.view.channel_id = channel.id

class ChannelSelectView(discord.ui.View):
    def __init__(self, *, timeout=180.0, bot: commands.Bot, user: discord.Member):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.user = user
        self.value = None
        self.add_item(ChannelSelect(user=self.user))

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green, emoji="✔️", row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red, emoji="✖️", row=2)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = False
            self.stop()

class EmbedButtons(discord.ui.View):
    def __init__(self, *, timeout = 180, bot: commands.Bot, user: discord.Member):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.user = user
        self.value = None
        self.embed = discord.Embed(color=self.bot.blurple, title="Title", description="Description")

    @discord.ui.button(label="Color", style=discord.ButtonStyle.blurple, emoji="🎨", row=1)
    async def color(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            message = interaction.message
            embed = message.embeds[0]
            
            view = ColorView(bot=self.bot, user=self.user)
            await message.edit(view=view)
            await view.wait()

            if view.value == True:
                await message.edit(embed=self.embed, view=self)

            elif view.value == False:
                await message.edit(embed=embed, view=self)

    @discord.ui.button(label="Title", style=discord.ButtonStyle.blurple, emoji="👑", row=1)
    async def title(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:
            modal = TitleModal()
            await interaction.response.send_modal(modal)
            await modal.wait()

            if modal.title is not None:
                self.embed.title = modal.title
            
            message = interaction.message
            await message.edit(embed=self.embed, view=self)
    
    @discord.ui.button(label="URL", style=discord.ButtonStyle.blurple, emoji="🔗", row=1)
    async def url(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:
            modal = URLModal()
            await interaction.response.send_modal(modal)
            await modal.wait()

            if modal.url is not None:
                self.embed.url = modal.url
            
            message = interaction.message
            await message.edit(embed=self.embed, view=self)
    
    @discord.ui.button(label="Description", style=discord.ButtonStyle.blurple, emoji="📄", row=1)
    async def description(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:
            modal = DescriptionModal()
            await interaction.response.send_modal(modal)
            await modal.wait()

            if modal.description is not None:
                self.embed.description = modal.description
            
            message = interaction.message
            await message.edit(embed=self.embed, view=self)
    
    @discord.ui.button(label="Fields", style=discord.ButtonStyle.blurple, emoji="📝", row=1)
    async def fields(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            message = interaction.message
            embed = message.embeds[0]

            view = FieldsSelectView(user=self.user)
            await message.edit(view=view)
            await view.wait()

            if view.value == True:

                if view.field is not None:

                    field_view = FieldEditView(user=self.user, index=view.field)
                    await message.edit(view=field_view)
                    await field_view.wait()

                    if field_view.value == True:
                        await message.edit(embed=self.embed, view=self)
                    
                    elif field_view.value == False:
                        await message.edit(embed=embed, view=self)

            elif view.value == False:
                await message.edit(embed=embed, view=self)
    
    @discord.ui.button(label="Media", style=discord.ButtonStyle.blurple, emoji="📷", row=1)
    async def media(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            message = interaction.message
            embed = message.embeds[0]

            view = MediaEditView(user=self.user)
            await message.edit(view=view)
            await view.wait()

            if view.value == True:
                await message.edit(embed=self.embed, view=self)
            
            elif view.value == False:
                await message.edit(embed=embed, view=self)
    
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, emoji="✔️", row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, emoji="✖️", row=2)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = False
            self.stop()

class Embeds(commands.GroupCog, group_name = "embed"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = bot.database
    
    @app_commands.command(name="build")
    @app_commands.checks.has_permissions(administrator=True)
    async def build(self, interaction: discord.Interaction):
        """(Admin Only) Run this command to build and send an embed."""
        await interaction.response.defer()
        try:

            guild = interaction.guild
            user = interaction.user
            embed = discord.Embed(color=self.bot.blurple, title="Title", description="Description")
            view = EmbedButtons(bot=self.bot, user=user)
            response = await interaction.followup.send(embed=embed, view=view, wait=True)
            await view.wait()

            if view.value == True:

                channel_select = discord.Embed(color=self.bot.blurple, title="Channel", description="Please use the dropdown menu below to select the channel where the embed should be sent. Press the `confirm` button to confirm or press the `cancel` button to cancel.")
                channel_select_view = ChannelSelectView(bot=self.bot, user=user)
                await response.edit(embed=channel_select, view=channel_select_view)
                await channel_select_view.wait()

                if channel_select_view.value == True:

                    if channel_select_view.channel_id is not None:
                        channel = guild.get_channel_or_thread(channel_select_view.channel_id)
                        embed = view.embed
                        embed.set_author(name=f"{user.display_name}", icon_url=f"{user.display_avatar}")
                        now = datetime.now(tz=timezone.utc)
                        embed.timestamp = now
                        await channel.send(embed=embed)

                        success = discord.Embed(color=self.bot.green, title="Success", description=f"The embed has been sent to {channel.mention}.")
                        await response.edit(embed=success, view=None)
                        await response.delete(delay=10.0)
                
                elif channel_select_view.value == False:
                    cancel = discord.Embed(color=self.bot.red, title="Cancelled", description="This interaction has been cancelled.")
                    await response.edit(embed=cancel, view=None)
                    await response.delete(delay=10.0)
            
            elif view.value == False:
                cancel = discord.Embed(color=self.bot.red, title="Cancelled", description="This interaction has been cancelled.")
                await response.edit(embed=cancel, view=None)
                await response.delete(delay=10.0)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            response = await interaction.followup.send(embed=error, wait=True)
            await response.delete(delay=10.0)
            print(traceback.format_exc())

async def setup(bot: commands.Bot):
    print("Setting up Cog: embeds.Embeds")

async def teardown(bot: commands.Bot):
    print("Tearing down Cog: embeds.Embeds")