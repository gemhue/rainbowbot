import discord
import traceback
import validators
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timezone

class CustomColorModal(discord.ui.Modal, title = "Custom Color"):
    color = None
    input = discord.ui.TextInput(label="Custom Color", placeholder="Please provide a #<hex> or rgb(r,g,b) color code...")

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)
        try:
            self.color = discord.Colour.from_str(self.input.value)
        except ValueError:
            self.color = discord.Colour.blurple()
            error = discord.Embed(color=discord.Colour.red(), title="Error", description="The input raised a ValueError. Please provide either a #<hex> or rgb(r,g,b) color code. The embed color has been reset.")
            await interaction.followup.send(embed=error, ephemeral=True)
        self.stop()
    
    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.defer(ephemeral=True, thinking=True)
        embed = discord.Embed(color=discord.Colour.red(), title="Error", description=f"{error}")
        await interaction.followup.send(embed=embed, ephemeral=True)
        print(traceback.format_exc())
        self.stop()

class ColorView(discord.ui.View):
    def __init__(self, *, timeout = 180, bot: commands.Bot, user: discord.Member):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.user = user
        self.embed = None

    @discord.ui.button(label="Red", style=discord.ButtonStyle.blurple, emoji="❤️", row=1)
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            message = interaction.message
            embed = message.embeds[0]

            embed.color = discord.Colour.red()
            self.embed = embed
            await message.edit(embed=self.embed, view=self)
    
    @discord.ui.button(label="Orange", style=discord.ButtonStyle.blurple, emoji="🧡", row=1)
    async def orange(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            message = interaction.message
            embed = message.embeds[0]

            embed.color = discord.Colour.orange()
            self.embed = embed
            await message.edit(embed=self.embed, view=self)

    @discord.ui.button(label="Yellow", style=discord.ButtonStyle.blurple, emoji="💛", row=1)
    async def yellow(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            message = interaction.message
            embed = message.embeds[0]

            embed.color = discord.Colour.yellow()
            self.embed = embed
            await message.edit(embed=self.embed, view=self)
    
    @discord.ui.button(label="Green", style=discord.ButtonStyle.blurple, emoji="💚", row=1)
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            message = interaction.message
            embed = message.embeds[0]

            embed.color = discord.Colour.green()
            self.embed = embed
            await message.edit(embed=self.embed, view=self)
    
    @discord.ui.button(label="Blue", style=discord.ButtonStyle.blurple, emoji="💙", row=2)
    async def blue(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            message = interaction.message
            embed = message.embeds[0]

            embed.color = discord.Colour.blue()
            self.embed = embed
            await message.edit(embed=self.embed, view=self)
    
    @discord.ui.button(label="Purple", style=discord.ButtonStyle.blurple, emoji="💜", row=2)
    async def purple(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            message = interaction.message
            embed = message.embeds[0]

            embed.color = discord.Colour.purple()
            self.embed = embed
            await message.edit(embed=self.embed, view=self)
    
    @discord.ui.button(label="Pink", style=discord.ButtonStyle.blurple, emoji="🩷", row=2)
    async def pink(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            message = interaction.message
            embed = message.embeds[0]

            embed.color = discord.Colour.pink()
            self.embed = embed
            await message.edit(embed=self.embed, view=self)
    
    @discord.ui.button(label="Custom", style=discord.ButtonStyle.blurple, emoji="🩶", row=2)
    async def custom(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:
            message = interaction.message
            embed = message.embeds[0]

            modal = CustomColorModal()
            await interaction.response.send_modal(modal)
            await modal.wait()

            embed.color = modal.color
            self.embed = embed
            await message.edit(embed=self.embed, view=self)
    
    @discord.ui.button(label="Save", style=discord.ButtonStyle.green, emoji="💾", row=3)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.stop()

    @discord.ui.button(label="Go Back", style=discord.ButtonStyle.blurple, emoji="⏪", row=3)
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
        await interaction.response.defer(ephemeral=True, thinking=True)
        embed = discord.Embed(color=discord.Colour.red(), title="Error", description=f"{error}")
        await interaction.followup.send(embed=embed, ephemeral=True)
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
        await interaction.response.defer(ephemeral=True, thinking=True)
        embed = discord.Embed(color=discord.Colour.red(), title="Error", description=f"{error}")
        await interaction.followup.send(embed=embed, ephemeral=True)
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
        await interaction.response.defer(ephemeral=True, thinking=True)
        embed = discord.Embed(color=discord.Colour.red(), title="Error", description=f"{error}")
        await interaction.followup.send(embed=embed, ephemeral=True)
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
        super().__init__(placeholder="Please select a field to add, edit, or remove...", min_values=1, max_values=1, options=options, row=1)
        self.user = user
        self.index = None

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if interaction.user == self.user:
            field = self.values[0]
            index = int(field)
            self.index = index
            self.view.index = index

class FieldsSelectView(discord.ui.View):
    def __init__(self, *, timeout = 180, user: discord.Member):
        super().__init__(timeout=timeout)
        self.user = user
        self.value = None
        self.index = None
        self.select = FieldsSelect(user=self.user)
        self.add_item(self.select)
    
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, emoji="✔️", row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            if self.index is None:
                self.index = self.select.index
            self.stop()

    @discord.ui.button(label="Go Back", style=discord.ButtonStyle.blurple, emoji="⏪", row=2)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = False
            self.stop()

class FieldNameModal(discord.ui.Modal, title = "Field Name"):
    field_name = None
    input = discord.ui.TextInput(label="Field Name", placeholder="Please provide a name for the field...", max_length=256)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        self.field_name = self.input.value
        self.stop()
    
    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.defer(ephemeral=True, thinking=True)
        embed = discord.Embed(color=discord.Colour.red(), title="Error", description=f"{error}")
        await interaction.followup.send(embed=embed, ephemeral=True)
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
        await interaction.response.defer(ephemeral=True, thinking=True)
        embed = discord.Embed(color=discord.Colour.red(), title="Error", description=f"{error}")
        await interaction.followup.send(embed=embed, ephemeral=True)
        print(traceback.format_exc())
        self.stop()

class FieldAddView(discord.ui.View):
    def __init__(self, *, timeout = 180, user: discord.Member):
        super().__init__(timeout=timeout)
        self.user = user
        self.index = None
        self.value = None
        self.embed = None
    
    @discord.ui.button(label="Name", style=discord.ButtonStyle.blurple, emoji="✏️", row=1)
    async def field_name(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:

            try:
                message = interaction.message
                embed = message.embeds[0]

                modal = FieldNameModal()
                await interaction.response.send_modal(modal)
                await modal.wait()

                try:
                    if self.index is None:
                        embed.add_field(name=modal.field_name, value="Default Field Value", inline=True)
                        self.index = len(embed.fields)-1
                    else:
                        field = embed.fields[self.index]
                        if field:
                            embed.set_field_at(index=self.index, name=modal.field_name, value=field.value, inline=field.inline)
                except Exception:
                    print(traceback.format_exc())
                self.embed = embed
                await message.edit(embed=self.embed, view=self)

            except Exception:
                print(traceback.format_exc())

    @discord.ui.button(label="Value", style=discord.ButtonStyle.blurple, emoji="✏️", row=1)
    async def field_value(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:

            try:
                message = interaction.message
                embed = message.embeds[0]

                modal = FieldValueModal()
                await interaction.response.send_modal(modal)
                await modal.wait()

                try:
                    if self.index is None:
                        embed.add_field(name="Default Field Name", value=modal.field_value, inline=True)
                        self.index = len(embed.fields)-1
                    else:
                        field = embed.fields[self.index]
                        if field:
                            embed.set_field_at(index=self.index, name=field.name, value=modal.field_value, inline=field.inline)
                except Exception:
                    print(traceback.format_exc())
                self.embed = embed
                await message.edit(embed=self.embed, view=self)
            
            except Exception:
                print(traceback.format_exc())

    @discord.ui.button(label="Inline Toggle", style=discord.ButtonStyle.blurple, emoji="🌗", row=1)
    async def inline_toggle(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            try:
                message = interaction.message
                embed = message.embeds[0]

                try:
                    if self.index is None:
                        embed.add_field(name="Default Field Name", value="Default Field Value", inline=True)
                        button.label = "Inline: True"
                        button.emoji = "🌕"
                        self.index = len(embed.fields)-1
                    else:
                        field = embed.fields[self.index]
                        if field:
                            if field.inline == True:
                                embed.set_field_at(index=self.index, name=field.name, value=field.value, inline=False)
                                button.label = "Inline: False"
                                button.emoji = "🌑"
                            elif field.inline == False:
                                embed.set_field_at(index=self.index, name=field.name, value=field.value, inline=True)
                                button.label = "Inline: True"
                                button.emoji = "🌕"
                except Exception:
                    print(traceback.format_exc())
                self.embed = embed
                await message.edit(embed=self.embed, view=self)
            
            except Exception:
                print(traceback.format_exc())
    
    @discord.ui.button(label="Save", style=discord.ButtonStyle.green, emoji="💾", row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.stop()

    @discord.ui.button(label="Go Back", style=discord.ButtonStyle.blurple, emoji="⏪", row=2)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = False
            self.stop()

class FieldEditView(discord.ui.View):
    def __init__(self, *, timeout = 180, user: discord.Member, index: int):
        super().__init__(timeout=timeout)
        self.user = user
        self.index = index
        self.value = None
        self.embed = None
    
    @discord.ui.button(label="Name", style=discord.ButtonStyle.blurple, emoji="✏️", row=1)
    async def field_name(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:

            try:
                message = interaction.message
                embed = message.embeds[0]

                modal = FieldNameModal()
                await interaction.response.send_modal(modal)
                await modal.wait()

                try:
                    field = embed.fields[self.index]
                    if field:
                        embed.set_field_at(index=self.index, name=modal.field_name, value=field.value, inline=field.inline)
                except IndexError:
                    embed.add_field(name=modal.field_name, value="Default Field Value", inline=True)
                self.embed = embed
                await message.edit(embed=self.embed, view=self)

            except Exception:
                print(traceback.format_exc())

    @discord.ui.button(label="Value", style=discord.ButtonStyle.blurple, emoji="✏️", row=1)
    async def field_value(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:

            try:
                message = interaction.message
                embed = message.embeds[0]

                modal = FieldValueModal()
                await interaction.response.send_modal(modal)
                await modal.wait()

                try:
                    field = embed.fields[self.index]
                    if field:
                        embed.set_field_at(index=self.index, name=field.name, value=modal.field_value, inline=field.inline)
                except IndexError:
                    embed.add_field(name="Default Field Name", value=modal.field_value, inline=True)
                self.embed = embed
                await message.edit(embed=self.embed, view=self)
            
            except Exception:
                print(traceback.format_exc())

    @discord.ui.button(label="Inline Toggle", style=discord.ButtonStyle.blurple, emoji="🌗", row=1)
    async def inline_toggle(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            try:
                message = interaction.message
                embed = message.embeds[0]

                try:
                    field = embed.fields[self.index]
                    if field.inline == True:
                        embed.set_field_at(index=self.index, name=field.name, value=field.value, inline=False)
                        button.label = "Inline: False"
                        button.emoji = "🌑"
                    elif field.inline == False:
                        embed.set_field_at(index=self.index, name=field.name, value=field.value, inline=True)
                        button.label = "Inline: True"
                        button.emoji = "🌕"
                except IndexError:
                    embed.add_field(name="Default Field Name", value="Default Field Value", inline=True)
                    button.label = "Inline: True"
                    button.emoji = "🌕"
                self.embed = embed
                await message.edit(embed=self.embed, view=self)
            
            except Exception:
                print(traceback.format_exc())
    
    @discord.ui.button(label="Save", style=discord.ButtonStyle.green, emoji="💾", row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.stop()

    @discord.ui.button(label="Go Back", style=discord.ButtonStyle.blurple, emoji="⏪", row=2)
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
        await interaction.response.defer(ephemeral=True, thinking=True)
        embed = discord.Embed(color=discord.Colour.red(), title="Error", description=f"{error}")
        await interaction.followup.send(embed=embed, ephemeral=True)
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
        await interaction.response.defer(ephemeral=True, thinking=True)
        embed = discord.Embed(color=discord.Colour.red(), title="Error", description=f"{error}")
        await interaction.followup.send(embed=embed, ephemeral=True)
        print(traceback.format_exc())
        self.stop()

class MediaEditView(discord.ui.View):
    def __init__(self, *, timeout = 180, user: discord.Member):
        super().__init__(timeout=timeout)
        self.user = user
        self.value = None
        self.embed = None
    
    @discord.ui.button(label="Add or Edit URL", style=discord.ButtonStyle.green, emoji="✏️", row=1)
    async def add_url(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:
            message = interaction.message
            embed = message.embeds[0]

            modal = URLModal()
            await interaction.response.send_modal(modal)
            await modal.wait()

            if modal.url and validators.url(modal.url):
                embed.url = modal.url
            self.embed = embed
            await message.edit(embed=self.embed, view=self)
    
    @discord.ui.button(label="Remove URL", style=discord.ButtonStyle.red, emoji="➖", row=1)
    async def remove_url(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            try:
                message = interaction.message
                embed = message.embeds[0]
                embed.url = None
                self.embed = embed
                await message.edit(embed=self.embed, view=self)
            
            except Exception:
                print(traceback.format_exc())
    
    @discord.ui.button(label="Add or Edit Image", style=discord.ButtonStyle.green, emoji="✏️", row=2)
    async def add_image(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:

            try:
                message = interaction.message
                embed = message.embeds[0]

                modal = ImageModal()
                await interaction.response.send_modal(modal)
                await modal.wait()

                if modal.image and validators.url(modal.image):
                    embed.set_image(url=modal.image)
                self.embed = embed
                await message.edit(embed=self.embed, view=self)
                
            except Exception:
                print(traceback.format_exc())
    
    @discord.ui.button(label="Remove Image", style=discord.ButtonStyle.red, emoji="➖", row=2)
    async def remove_image(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            try:
                message = interaction.message
                embed = message.embeds[0]
                embed.set_image(url=None)
                self.embed = embed
                await message.edit(embed=self.embed, view=self)
            
            except Exception:
                print(traceback.format_exc())

    @discord.ui.button(label="Add or Edit Thumbnail", style=discord.ButtonStyle.green, emoji="✏️", row=3)
    async def add_thumbnail(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:

            try:
                message = interaction.message
                embed = message.embeds[0]

                modal = ThumbnailModal()
                await interaction.response.send_modal(modal)
                await modal.wait()

                if modal.thumbnail and validators.url(modal.thumbnail):
                    embed.set_thumbnail(url=modal.thumbnail)
                self.embed = embed
                await message.edit(embed=self.embed, view=self)
                
            except Exception:
                print(traceback.format_exc())
    
    @discord.ui.button(label="Remove Thumbnail", style=discord.ButtonStyle.red, emoji="➖", row=3)
    async def remove_thumbnail(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            try:
                message = interaction.message
                embed = message.embeds[0]
                embed.set_thumbnail(url=None)
                self.embed = embed
                await message.edit(embed=self.embed, view=self)
                
            except Exception:
                print(traceback.format_exc())
    
    @discord.ui.button(label="Save", style=discord.ButtonStyle.green, emoji="💾", row=4)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.stop()

    @discord.ui.button(label="Go Back", style=discord.ButtonStyle.blurple, emoji="⏪", row=4)
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
        self.channel_id = None

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if interaction.user == self.user:
            channel = self.values[0]
            self.channel_id = channel.id
            self.view.channel_id = channel.id

class ChannelSelectView(discord.ui.View):
    def __init__(self, *, timeout=180.0, bot: commands.Bot, user: discord.Member):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.user = user
        self.value = None
        self.channel_id = None
        self.select = ChannelSelect(user=self.user)
        self.add_item(self.select)

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green, emoji="✔️", row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            if self.channel_id is None:
                self.channel_id = self.select.channel_id
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
        self.embed = None

    @discord.ui.button(label="Add or Edit Title", style=discord.ButtonStyle.blurple, emoji="✏️", row=1)
    async def edit_title(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:
            message = interaction.message
            embed = message.embeds[0]

            modal = TitleModal()
            await interaction.response.send_modal(modal)
            await modal.wait()

            if modal.title is not None:
                embed.title = modal.title
            self.embed = embed
            await message.edit(embed=self.embed, view=self)
    
    @discord.ui.button(label="Remove Title", style=discord.ButtonStyle.red, emoji="➖", row=1)
    async def remove_title(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:
            message = interaction.message
            embed = message.embeds[0]

            if embed.title is not None and embed.description is not None:
                embed.title = None
            self.embed = embed
            await message.edit(embed=self.embed, view=self)
    
    @discord.ui.button(label="Add or Edit Description", style=discord.ButtonStyle.blurple, emoji="✏️", row=1)
    async def description(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:
            message = interaction.message
            embed = message.embeds[0]

            modal = DescriptionModal()
            await interaction.response.send_modal(modal)
            await modal.wait()

            if modal.description is not None:
                embed.description = modal.description
            self.embed = embed
            await message.edit(embed=self.embed, view=self)
    
    @discord.ui.button(label="Remove Description", style=discord.ButtonStyle.red, emoji="➖", row=1)
    async def remove_description(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:
            message = interaction.message
            embed = message.embeds[0]

            if embed.description is not None and embed.title is not None:
                embed.description = None
            self.embed = embed
            await message.edit(embed=self.embed, view=self)
    
    @discord.ui.button(label="Add Field", style=discord.ButtonStyle.green, emoji="➕", row=2)
    async def add_field(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            try:
                message = interaction.message
                embed = message.embeds[0]
                if self.embed is None:
                    self.embed = embed

                view = FieldAddView(user=self.user)
                await message.edit(view=view)
                await view.wait()

                if view.value == True:
                    self.embed = view.embed
                    await message.edit(embed=self.embed, view=self)

                elif view.value == False:
                    self.embed = embed
                    await message.edit(embed=self.embed, view=self)
            
            except Exception:
                print(traceback.format_exc())

    @discord.ui.button(label="Edit Field", style=discord.ButtonStyle.blurple, emoji="✏️", row=2)
    async def edit_field(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            try:
                message = interaction.message
                embed = message.embeds[0]
                if self.embed is None:
                    self.embed = embed

                view = FieldsSelectView(user=self.user)
                await message.edit(view=view)
                await view.wait()

                if view.value == True:

                    field_view = FieldEditView(user=self.user, index=view.index)
                    await message.edit(view=field_view)
                    await field_view.wait()

                    if field_view.value == True:
                        self.embed = field_view.embed
                        await message.edit(embed=self.embed, view=self)
                    
                    elif field_view.value == False:
                        self.embed = embed
                        await message.edit(embed=self.embed, view=self)

                elif view.value == False:
                    self.embed = embed
                    await message.edit(embed=self.embed, view=self)
            
            except Exception:
                print(traceback.format_exc())
    
    @discord.ui.button(label="Remove Field", style=discord.ButtonStyle.red, emoji="➖", row=2)
    async def remove_field(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            try:
                message = interaction.message
                embed = message.embeds[0]
                if self.embed is None:
                    self.embed = embed

                view = FieldsSelectView(user=self.user)
                await message.edit(view=view)
                await view.wait()

                if view.value == True:

                    embed.remove_field(index=view.index)
                    self.embed = embed
                    await message.edit(embed=self.embed, view=self)

                elif view.value == False:
                    self.embed = embed
                    await message.edit(embed=self.embed, view=self)
            
            except Exception:
                print(traceback.format_exc())
    
    @discord.ui.button(label="Color Editor", style=discord.ButtonStyle.blurple, emoji="🌈", row=3)
    async def color(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            message = interaction.message
            embed = message.embeds[0]
            if self.embed is None:
                self.embed = embed
            
            view = ColorView(bot=self.bot, user=self.user)
            await message.edit(view=view)
            await view.wait()

            if view.value == True:

                if view.embed is not None:
                    self.embed = view.embed
                await message.edit(embed=self.embed, view=self)

            elif view.value == False:
                self.embed = embed
                await message.edit(embed=self.embed, view=self)
    
    @discord.ui.button(label="Media Editor", style=discord.ButtonStyle.blurple, emoji="📷", row=3)
    async def media(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            try:
                message = interaction.message
                embed = message.embeds[0]
                if self.embed is None:
                    self.embed = embed

                view = MediaEditView(user=self.user)
                await message.edit(view=view)
                await view.wait()

                if view.value == True:

                    if view.embed is not None:
                        self.embed = view.embed
                    await message.edit(embed=self.embed, view=self)
                
                elif view.value == False:
                    self.embed = embed
                    await message.edit(embed=self.embed, view=self)
            
            except Exception:
                print(traceback.format_exc())

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, emoji="✔️", row=4)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, emoji="✖️", row=4)
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

            view = EmbedButtons(bot=self.bot, user=user)
            embed = discord.Embed(color=self.bot.blurple, title="Default Embed Title", description="Default Embed Description")
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
                
                else:
                    timed_out = discord.Embed(color=self.bot.yellow, title="Timed Out", description="This interaction has timed out. Please try again.")
                    await response.edit(embed=timed_out, view=None)
                    await response.delete(delay=10.0)
            
            elif view.value == False:
                cancel = discord.Embed(color=self.bot.red, title="Cancelled", description="This interaction has been cancelled.")
                await response.edit(embed=cancel, view=None)
                await response.delete(delay=10.0)
            
            else:
                timed_out = discord.Embed(color=self.bot.yellow, title="Timed Out", description="This interaction has timed out. Please try again.")
                await response.edit(embed=timed_out, view=None)
                await response.delete(delay=10.0)

        except Exception as e:
            error = discord.Embed(color=self.bot.red, title="Error", description=f"{e}")
            response = await interaction.followup.send(embed=error, wait=True)
            await response.delete(delay=10.0)
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
        await interaction.response.defer()
        try:

            user = interaction.user
            ctx = commands.Context.from_interaction(interaction)
            message = await commands.MessageConverter.convert(ctx=ctx, argument=url)

            if isinstance(message, discord.Message):

                embed = message.embeds[0]
                view = EmbedButtons(bot=self.bot, user=user)
                response = await interaction.followup.send(embed=embed, view=view, wait=True)
                await view.wait()

                if view.value == True:

                    embed = view.embed
                    now = discord.utils.format_dt(datetime.now(tz=timezone.utc), style="D")
                    embed.set_footer(text=f"Edited by {user.display_name} | {now}", icon_url=f"{user.display_avatar}")
                    await message.edit(embed=embed)

                    success = discord.Embed(color=self.bot.green, title="Success", description=f"The embed has been edited. Please click [this link]({url}) to go there now.")
                    await response.edit(embed=success, view=None)
                    await response.delete(delay=10.0)
                
                elif view.value == False:
                    cancel = discord.Embed(color=self.bot.red, title="Cancelled", description="This interaction has been cancelled.")
                    await response.edit(embed=cancel, view=None)
                    await response.delete(delay=10.0)
                
                else:
                    timed_out = discord.Embed(color=self.bot.yellow, title="Timed Out", description="This interaction has timed out. Please try again.")
                    await response.edit(embed=timed_out, view=None)
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