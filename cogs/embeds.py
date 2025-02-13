import discord
import traceback
import validators
from discord import app_commands
from discord.ext import commands
from typing import Optional
from datetime import datetime, timezone

class ChannelSelect(discord.ui.ChannelSelect):
    def __init__(self):
        super().__init__(
            channel_types = [discord.ChannelType.text],
            placeholder = "Select the channel to send the embed to...",
            min_values = 1,
            max_values = 1,
            row = 0
        )
        self.channel = None

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        channel = self.values[0]
        self.channel = channel
        if not self.view.channel:
            self.view.channel = self.channel

        # Debugging print
        print(f"ChannelSelect callback: {self.channel.name}")

class ChannelSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None
        self.channel = None

        self.select = ChannelSelect()
        self.add_item(self.select)

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, emoji="✔️", row=1)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if not self.channel:
            self.channel = self.select.channel
        self.value = True
        self.stop()

        # Debugging print
        print(f"ChannelSelectView confirm: {self.channel.name}")
    
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, emoji="✖️", row=1)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = False
        self.stop()

class FieldNameModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Field Name", timeout=None)
        self.field_name = None

        self.input = discord.ui.TextInput(
            label="Field Name",
            placeholder="Please provide a name for the field...",
            max_length=256
        )
        self.add_item(self.input)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.field_name = self.input.value
        self.stop()

class FieldValueModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Field Value", timeout=None)
        self.field_value = None

        self.input = discord.ui.TextInput(
            label="Field Value",
            style=discord.TextStyle.long,
            placeholder="Please provide a value for the field...",
            max_length=1024
        )
        self.add_item(self.input)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.field_value = self.input.value
        self.stop()

class FieldEditor(discord.ui.View):
    def __init__(self, *, index: Optional[int] = None):
        super().__init__(timeout=None)
        self.embed = None
        self.index = index
    
    @discord.ui.button(label="Set Name", style=discord.ButtonStyle.blurple, emoji="✏️", row=0)
    async def set_name(self, interaction: discord.Interaction, button: discord.ui.Button):
        message = interaction.message
        embed = message.embeds[0]

        modal = FieldNameModal()
        await interaction.response.send_modal(modal)
        await modal.wait()

        if isinstance(modal.field_name, str):
            if self.index is None:
                embed.add_field(name=modal.field_name, value="Default Field Value", inline=True)
                self.index = len(embed.fields)-1
            else:
                field = embed.fields[self.index]
                embed.set_field_at(index=self.index, name=modal.field_name, value=field.value, inline=field.inline)
        self.embed = embed
        await interaction.followup.edit_message(message_id=message.id, embed=self.embed, view=self)
    
    @discord.ui.button(label="Set Value", style=discord.ButtonStyle.blurple, emoji="✏️", row=0)
    async def set_value(self, interaction: discord.Interaction, button: discord.ui.Button):
        message = interaction.message
        embed = message.embeds[0]

        modal = FieldValueModal()
        await interaction.response.send_modal(modal)
        await modal.wait()

        if isinstance(modal.field_value, str):
            if self.index is None:
                embed.add_field(name="Default Field Name", value=modal.field_value, inline=True)
                self.index = len(embed.fields)-1
            else:
                field = embed.fields[self.index]
                embed.set_field_at(index=self.index, name=field.name, value=modal.field_value, inline=field.inline)
        self.embed = embed
        await interaction.followup.edit_message(message_id=message.id, embed=self.embed, view=self)
    
    @discord.ui.button(label="Inline Toggle", style=discord.ButtonStyle.blurple, emoji="🌓", row=0)
    async def inline_toggle(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message
        embed = message.embeds[0]

        if self.index is None:
            embed.add_field(name="Default Field Name", value="Default Field Value", inline=True)
            button.label = "Inline: True"
            button.emoji = "🌕"
            self.index = len(embed.fields)-1
        else:
            field = embed.fields[self.index]
            if field.inline == True:
                embed.set_field_at(index=self.index, name=field.name, value=field.value, inline=False)
                button.label = "Inline: False"
                button.emoji = "🌑"
            else:
                embed.set_field_at(index=self.index, name=field.name, value=field.value, inline=True)
                button.label = "Inline: True"
                button.emoji = "🌕"
        self.embed = embed
        await interaction.followup.edit_message(message_id=message.id, embed=self.embed, view=self)

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, emoji="✔️", row=1)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True
        self.stop()
    
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, emoji="✖️", row=1)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = False
        self.stop()

class FieldSelect(discord.ui.Select):
    def __init__(self):
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
            discord.SelectOption(label="Field 25", value="24")
        ]
        super().__init__(
            placeholder = "Select a field...",
            min_values = 1,
            max_values = 1,
            options = options,
            row = 0
        )
        self.index = None

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        index = self.values[0]
        self.index = int(index)
        if not self.view.index:
            self.view.index = self.index

        # Debugging print
        print(f"FieldSelect callback: {self.index}")

class FieldSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None
        self.index = None
        
        self.select = FieldSelect()
        self.add_item(self.select)

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, emoji="✔️", row=1)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if not self.index:
            self.index = self.select.index
        self.value = True
        self.stop()

        # Debugging print
        print(f"FieldSelectView confirm: {self.index}")
    
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, emoji="✖️", row=1)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = False
        self.stop()

class FieldView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.embed = None
    
    @discord.ui.button(label="Add Field", style=discord.ButtonStyle.green, emoji="➕", row=0)
    async def add_field(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message
        embed = message.embeds[0]
        self.embed = embed
        
        view = FieldEditor()
        await interaction.followup.edit_message(message_id=message.id, embed=embed, view=view)
        await view.wait()

        if view.value == True:
            self.embed = view.embed
        await interaction.followup.edit_message(message_id=message.id, embed=self.embed, view=self)
    
    @discord.ui.button(label="Edit Field", style=discord.ButtonStyle.green, emoji="✏️", row=0)
    async def edit_field(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message
        embed = message.embeds[0]
        self.embed = embed

        view = FieldSelectView()
        await interaction.followup.edit_message(message_id=message.id, embed=embed, view=view)
        await view.wait()

        if view.value == True:

            if isinstance(view.index, int):
                fieldview = FieldEditor(index=view.index)
                await interaction.followup.edit_message(message_id=message.id, embed=embed, view=fieldview)
                await fieldview.wait()

                if fieldview.value == True:
                    self.embed = fieldview.embed
        await interaction.followup.edit_message(message_id=message.id, embed=self.embed, view=self)

    @discord.ui.button(label="Remove Field", style=discord.ButtonStyle.red, emoji="➖", row=0)
    async def remove_field(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message
        embed = message.embeds[0]
        self.embed = embed

        view = FieldSelectView()
        await interaction.followup.edit_message(message_id=message.id, embed=embed, view=view)
        await view.wait()

        if view.value == True:
            if isinstance(view.index, int):
                embed.remove_field(index=view.index)
                self.embed = embed
        await interaction.followup.edit_message(message_id=message.id, embed=self.embed, view=self)
    
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, emoji="✔️", row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True
        self.stop()
    
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, emoji="✖️", row=2)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = False
        self.stop()

class ColorSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Red", value="#dd2e44", description="Set the embed color to red (#dd2e44)!", emoji="❤️"),
            discord.SelectOption(label="Orange", value="#f4900c", description="Set the embed color to orange (#f4900c)!", emoji="🧡"),
            discord.SelectOption(label="Yellow", value="#fdcb58", description="Set the embed color to yellow (#fdcb58)!", emoji="💛"),
            discord.SelectOption(label="Green", value="#78b159", description="Set the embed color to green (#78b159)!", emoji="💚"),
            discord.SelectOption(label="Cyan", value="#88c9f9", description="Set the embed color to cyan (#88c9f9)!", emoji="🩵"),
            discord.SelectOption(label="Blue", value="#5dadec", description="Set the embed color to blue (#5dadec)!", emoji="💙"),
            discord.SelectOption(label="Purple", value="#aa8ed6", description="Set the embed color to purple (#aa8ed6)!", emoji="💜"),
            discord.SelectOption(label="Pink", value="#f4abba", description="Set the embed color to pink (#f4abba)!", emoji="🩷"),
            discord.SelectOption(label="White", value="#e6e7e8", description="Set the embed color to white (#e6e7e8)!", emoji="🤍"),
            discord.SelectOption(label="Gray", value="#99aab5", description="Set the embed color to gray (#99aab5)!", emoji="🩶"),
            discord.SelectOption(label="Black", value="#31373d", description="Set the embed color to black (#31373d)!", emoji="🖤"),
            discord.SelectOption(label="Brown", value="#c1694f", description="Set the embed color to brown (#c1694f)!", emoji="🤎")
        ]
        super().__init__(
            placeholder = "Choose a color...",
            min_values = 1,
            max_values = 1,
            options = options,
            row = 0
        )
        self.color = None

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        color = self.values[0]
        self.color = discord.Colour.from_str(color)
        if not self.view.color:
            self.view.color = self.color
        
        # Debugging print
        print(f"ColorSelect callback: {self.color.__str__}")

class ColorSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None
        self.color = None
        
        self.select = ColorSelect()
        self.add_item(self.select)

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, emoji="✔️", row=1)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if not self.color:
            self.color = self.select.color
        self.value = True
        self.stop()

        # Debugging print
        print(f"ColorSelectView confirm: {self.color.__str__}")
    
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, emoji="✖️", row=1)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = False
        self.stop()

class URLModal(discord.ui.Modal, title = "Embed URL"):
    embed_url = None
    input = discord.ui.TextInput(
            label="Embed URL",
            placeholder="Please provide a URL for the embed..."
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.embed_url = self.input.value
        self.stop()

class ImageURLModal(discord.ui.Modal, title = "Image URL"):
    image_url = None
    input = discord.ui.TextInput(
            label="Image URL",
            placeholder="Please provide an image URL for the embed..."
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.image_url = self.input.value
        self.stop()

class ThumbnailURLModal(discord.ui.Modal, title = "Thumbnail URL"):
    thumbnail_url = None
    input = discord.ui.TextInput(
            label="Thumbnail URL",
            placeholder="Please provide a thumbnail URL for the embed..."
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.thumbnail_url = self.input.value
        self.stop()

class MediaEditor(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.embed = None
        self.value = None
    
    @discord.ui.button(label="Set URL", style=discord.ButtonStyle.blurple, emoji="✏️", row=0)
    async def set_url(self, interaction: discord.Interaction, button: discord.ui.Button):
        message = interaction.message
        embed = message.embeds[0]
        self.embed = embed

        modal = URLModal()
        await interaction.response.send_modal(modal)
        await modal.wait()

        if isinstance(modal.embed_url, str):
            if validators.url(modal.embed_url):
                embed.url = modal.embed_url
                self.embed = embed
        await interaction.followup.edit_message(message_id=message.id, embed=self.embed, view=self)

        # Debugging print
        if self.embed.url:
            print(f"MediaEditor set_url: {self.embed.url}")
    
    @discord.ui.button(label="Remove URL", style=discord.ButtonStyle.gray, emoji="➖", row=0)
    async def remove_url(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message
        embed = message.embeds[0]
        
        embed.url = None
        self.embed = embed
        await interaction.followup.edit_message(message_id=message.id, embed=self.embed, view=self)

    @discord.ui.button(label="Set Image", style=discord.ButtonStyle.blurple, emoji="✏️", row=1)
    async def set_image(self, interaction: discord.Interaction, button: discord.ui.Button):
        message = interaction.message
        embed = message.embeds[0]
        self.embed = embed

        modal = ImageURLModal()
        await interaction.response.send_modal(modal)
        await modal.wait()

        if isinstance(modal.image_url, str):
            if validators.url(modal.image_url):
                embed.set_image(modal.image_url)
                self.embed = embed
        await interaction.followup.edit_message(message_id=message.id, embed=self.embed, view=self)

        # Debugging print
        if self.embed.image:
            print(f"MediaEditor set_image: {self.embed.image.url}")
    
    @discord.ui.button(label="Remove Image", style=discord.ButtonStyle.gray, emoji="➖", row=1)
    async def remove_image(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message
        embed = message.embeds[0]
        
        embed.set_image(None)
        self.embed = embed
        await interaction.followup.edit_message(message_id=message.id, embed=self.embed, view=self)

    @discord.ui.button(label="Set Thumbnail", style=discord.ButtonStyle.blurple, emoji="✏️", row=2)
    async def set_thumbnail(self, interaction: discord.Interaction, button: discord.ui.Button):
        message = interaction.message
        embed = message.embeds[0]
        self.embed = embed

        modal = ThumbnailURLModal()
        await interaction.response.send_modal(modal)
        await modal.wait()

        if isinstance(modal.thumbnail_url, str):
            if validators.url(modal.thumbnail_url):
                embed.set_thumbnail(modal.thumbnail_url)
                self.embed = embed
        await interaction.followup.edit_message(message_id=message.id, embed=self.embed, view=self)

        # Debugging print
        if self.embed.thumbnail:
            print(f"MediaEditor set_thumbnail: {self.embed.thumbnail.url}")
    
    @discord.ui.button(label="Remove Thumbnail", style=discord.ButtonStyle.gray, emoji="➖", row=2)
    async def remove_thumbnail(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message
        embed = message.embeds[0]

        embed.set_thumbnail(None)
        self.embed = embed
        await interaction.followup.edit_message(message_id=message.id, embed=self.embed, view=self)
    
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, emoji="✔️", row=3)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True
        self.stop()
    
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, emoji="✖️", row=3)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = False
        self.stop()

class TitleModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Title", timeout=None)
        self.embed_title = None

        self.input = discord.ui.TextInput(
            label="Title",
            placeholder="Please provide a title for the embed...",
            max_length=256
        )
        self.add_item(self.input)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.embed_title = self.input.value
        self.stop()

        # Debugging print
        print(f"TitleModal on_submit: {self.embed_title}")

class DescriptionModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Description", timeout=None)
        self.embed_description = None

        self.input = discord.ui.TextInput(
            label="Description",
            style=discord.TextStyle.long,
            placeholder="Please provide a description for the embed...",
            max_length=4096
        )
        self.add_item(self.input)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.embed_description = self.input.value
        self.stop()

        # Debugging print
        print(f"DescriptionModal on_submit: {self.embed_description}")

class EmbedEditor(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.embed = None
        self.value = None
    
    @discord.ui.button(label="Set Title", style=discord.ButtonStyle.blurple, emoji="✏️", row=0)
    async def set_title(self, interaction: discord.Interaction, button: discord.ui.Button):
        message = interaction.message
        embed = message.embeds[0]

        modal = TitleModal()
        await interaction.response.send_modal(modal)
        await modal.wait()

        if isinstance(modal.embed_title, str):
            embed.title = modal.embed_title
        self.embed = embed
        await interaction.followup.edit_message(message_id=message.id, embed=self.embed, view=self)

        # Debugging print
        print(f"EmbedEditor set_title: {self.embed.title}")
    
    @discord.ui.button(label="Remove Title", style=discord.ButtonStyle.gray, emoji="➖", row=0)
    async def remove_title(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message
        embed = message.embeds[0]

        embed.title = None
        self.embed = embed
        await interaction.followup.edit_message(message_id=message.id, embed=self.embed, view=self)
    
    @discord.ui.button(label="Set Description", style=discord.ButtonStyle.blurple, emoji="✏️", row=1)
    async def set_description(self, interaction: discord.Interaction, button: discord.ui.Button):
        message = interaction.message
        embed = message.embeds[0]

        modal = DescriptionModal()
        await interaction.response.send_modal(modal)
        await modal.wait()

        if isinstance(modal.embed_description, str):
            embed.description = modal.embed_description
        self.embed = embed
        await interaction.followup.edit_message(message_id=message.id, embed=self.embed, view=self)

        # Debugging print
        print(f"EmbedEditor set_description: {self.embed.description}")
    
    @discord.ui.button(label="Remove Description", style=discord.ButtonStyle.gray, emoji="➖", row=1)
    async def remove_description(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message
        embed = message.embeds[0]

        embed.description = None
        self.embed = embed
        await interaction.followup.edit_message(message_id=message.id, embed=self.embed, view=self)
    
    @discord.ui.button(label="Field Editor", style=discord.ButtonStyle.gray, emoji="📋", row=2)
    async def field_editor(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message
        embed = message.embeds[0]
        self.embed = embed
        
        view = FieldView()
        await interaction.followup.edit_message(message_id=message.id, embed=embed, view=view)
        await view.wait()

        if view.value == True:
            embed = view.embed
            self.embed = embed
        await interaction.followup.edit_message(message_id=message.id, embed=self.embed, view=self)
    
    @discord.ui.button(label="Color Editor", style=discord.ButtonStyle.gray, emoji="🎨", row=2)
    async def color_editor(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message
        embed = message.embeds[0]
        self.embed = embed

        view = ColorSelectView()
        await interaction.followup.edit_message(message_id=message.id, embed=embed, view=view)
        await view.wait()

        if view.value == True:
            if isinstance(view.color, discord.Colour):
                embed.colour = view.color
                self.embed = embed
        await interaction.followup.edit_message(message_id=message.id, embed=self.embed, view=self)
    
    @discord.ui.button(label="Media Editor", style=discord.ButtonStyle.gray, emoji="📷", row=2)
    async def media_editor(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        message = interaction.message
        embed = message.embeds[0]
        self.embed = embed
        
        view = MediaEditor()
        await interaction.followup.edit_message(message_id=message.id, embed=embed, view=view)
        await view.wait()

        if view.value == True:
            embed = view.embed
            self.embed = embed
        await interaction.followup.edit_message(message_id=message.id, embed=self.embed, view=self)
    
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, emoji="✔️", row=3)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = True
        self.stop()
    
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, emoji="✖️", row=3)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.value = False
        self.stop()

class Embeds(commands.GroupCog, group_name = "embed"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="build")
    @app_commands.checks.has_permissions(administrator=True)
    async def build(self, interaction: discord.Interaction):
        """(Admin Only) Run this command to build and send an embed."""
        await interaction.response.defer(ephemeral=True)
        try:
            embed = discord.Embed(
                color=self.bot.blurple,
                title="Default Embed Title",
                description="Default Embed Description"
            )
            view = EmbedEditor()
            response = await interaction.followup.send(ephemeral=True, embed=embed, view=view, wait=True)
            await view.wait()

            if view.value == True:

                embed = view.embed
                channelselect = ChannelSelectView()
                await interaction.followup.edit_message(message_id=response.id, embed=embed, view=channelselect)
                await channelselect.wait()

                if channelselect.value == True:

                    if isinstance(channelselect.channel, discord.TextChannel):
                        user = interaction.user
                        embed.set_author(name=user.display_name, icon_url=user.display_avatar)
                        embed.timestamp = datetime.now(tz=timezone.utc)
                        message = await channelselect.channel.send(embed=view.embed)

                        if isinstance(message, discord.Message):
                            success = discord.Embed(color=self.bot.green, title="Success", description=f"The embed has been sent to {channelselect.channel.mention} successfully!")
                            success.add_field(name="Link to Message", value=f"{message.jump_url}", inline=False)
                            await interaction.followup.edit_message(message_id=response.id, embed=success, view=None)

                        else:
                            debug = discord.Embed(color=self.bot.red, title="Error", description="The sent message is not recognised as a `discord.Message`.")
                            await interaction.followup.edit_message(message_id=response.id, embed=debug, view=None)
                    
                    else:
                        debug = discord.Embed(color=self.bot.red, title="Error", description="The selected channel is not recognised as a `discord.TextChannel`.")
                        await interaction.followup.edit_message(message_id=response.id, embed=debug, view=None)

                else:
                    cancel = discord.Embed(color=self.bot.red, title="Cancelled", description="This interaction has been cancelled.")
                    await interaction.followup.edit_message(message_id=response.id, embed=cancel, view=None)
            
            else:
                cancel = discord.Embed(color=self.bot.red, title="Cancelled", description="This interaction has been cancelled.")
                await interaction.followup.edit_message(message_id=response.id, embed=cancel, view=None)
        
        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(ephemeral=True, embed=error)
            print(traceback.format_exc())

    @app_commands.command(name="edit")
    @app_commands.checks.has_permissions(administrator=True)
    async def edit(self, interaction: discord.Interaction, url: str):
        """(Admin Only) Run this command to edit and existing embed.

        Parameters
        -----------
        url : str
            Provide the URL of the message containing the embed.
        """
        await interaction.response.defer(ephemeral=True)
        try:
            ctx = await commands.Context.from_interaction(interaction)
            converter = commands.MessageConverter()
            message = await converter.convert(ctx=ctx, argument=url)

            embed = None
            if isinstance(message, discord.Message):
                embed = message.embeds[0]
            
            if isinstance(embed, discord.Embed):
                view = EmbedEditor()
                response = await interaction.followup.send(ephemeral=True, embed=embed, view=view, wait=True)
                await view.wait()

                if view.value == True:

                    embed = view.embed
                    channelselect = ChannelSelectView()
                    await interaction.followup.edit_message(message_id=response.id, embed=embed, view=channelselect)
                    await channelselect.wait()

                    if channelselect.value == True:

                        if isinstance(channelselect.channel, discord.TextChannel):
                            user = interaction.user
                            embed.set_author(name=user.display_name, icon_url=user.display_avatar)
                            embed.timestamp = datetime.now(tz=timezone.utc)
                            message = await channelselect.channel.send(embed=view.embed)

                            if isinstance(message, discord.Message):
                                success = discord.Embed(color=self.bot.green, title="Success", description=f"The embed has been sent to {channelselect.channel.mention} successfully!")
                                success.add_field(name="Link to Message", value=f"{message.jump_url}", inline=False)
                                await interaction.followup.edit_message(message_id=response.id, embed=success, view=None)

                            else:
                                debug = discord.Embed(color=self.bot.red, title="Error", description="The sent message is not recognised as a `discord.Message`.")
                                await interaction.followup.edit_message(message_id=response.id, embed=debug, view=None)
                        
                        else:
                            debug = discord.Embed(color=self.bot.red, title="Error", description="The selected channel is not recognised as a `discord.TextChannel`.")
                            await interaction.followup.edit_message(message_id=response.id, embed=debug, view=None)

                    else:
                        cancel = discord.Embed(color=self.bot.red, title="Cancelled", description="This interaction has been cancelled.")
                        await interaction.followup.edit_message(message_id=response.id, embed=cancel, view=None)
                
                else:
                    cancel = discord.Embed(color=self.bot.red, title="Cancelled", description="This interaction has been cancelled.")
                    await interaction.followup.edit_message(message_id=response.id, embed=cancel, view=None)
        
        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            await interaction.followup.send(ephemeral=True, embed=error)
            print(traceback.format_exc())

async def setup(bot: commands.Bot):
    print("Setting up Cog: embeds.Embeds")

async def teardown(bot: commands.Bot):
    print("Tearing down Cog: embeds.Embeds")