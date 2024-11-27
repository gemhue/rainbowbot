import discord
import traceback
from discord import app_commands
from discord.ext import commands
from typing import Optional
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
        try:
            self.color = discord.Colour.from_str(self.input.value)
        except ValueError:
            self.color = discord.Colour.blurple()
        self.stop()
    
    async def on_error(self, interaction: discord.Interaction, error: Exception):
        print(traceback.format_exc())
        self.stop()

class ColorView(discord.ui.View):
    def __init__(self, *, timeout = 180, bot: commands.Bot, user: discord.Member):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.user = user
        self.color = None

    @discord.ui.button(label="Red", style=discord.ButtonStyle.blurple, emoji="❤️")
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            self.color = discord.Colour.red()
            message = interaction.message
            embed = discord.Embed(color=self.color, title="Color Selected", description="You have selected **red**. Is this correct?")
            view = YesOrNo(user=self.user)
            await message.edit(embed=embed, view=view)
            await view.wait()

            if view.value == True:
                self.stop()
            
            elif view.value == False:
                embed = discord.Embed(color=self.bot.blurple, title="Color", description="Choose the embed's color.")
                await message.edit(embed=embed, view=self)
    
    @discord.ui.button(label="Orange", style=discord.ButtonStyle.blurple, emoji="🧡")
    async def orange(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            self.color = discord.Colour.orange()
            message = interaction.message
            embed = discord.Embed(color=self.color, title="Color Selected", description="You have selected **orange**. Is this correct?")
            view = YesOrNo(user=self.user)
            await message.edit(embed=embed, view=view)
            await view.wait()

            if view.value == True:
                self.stop()
            
            elif view.value == False:
                embed = discord.Embed(color=self.bot.blurple, title="Color", description="Choose the embed's color.")
                await message.edit(embed=embed, view=self)

    @discord.ui.button(label="Yellow", style=discord.ButtonStyle.blurple, emoji="💛")
    async def yellow(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            self.color = discord.Colour.yellow()
            message = interaction.message
            embed = discord.Embed(color=self.color, title="Color Selected", description="You have selected **yellow**. Is this correct?")
            view = YesOrNo(user=self.user)
            await message.edit(embed=embed, view=view)
            await view.wait()

            if view.value == True:
                self.stop()
            
            elif view.value == False:
                embed = discord.Embed(color=self.bot.blurple, title="Color", description="Choose the embed's color.")
                await message.edit(embed=embed, view=self)
    
    @discord.ui.button(label="Green", style=discord.ButtonStyle.blurple, emoji="💚")
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            self.color = discord.Colour.green()
            message = interaction.message
            embed = discord.Embed(color=self.color, title="Color Selected", description="You have selected **green**. Is this correct?")
            view = YesOrNo(user=self.user)
            await message.edit(embed=embed, view=view)
            await view.wait()

            if view.value == True:
                self.stop()
            
            elif view.value == False:
                embed = discord.Embed(color=self.bot.blurple, title="Color", description="Choose the embed's color.")
                await message.edit(embed=embed, view=self)
    
    @discord.ui.button(label="Blue", style=discord.ButtonStyle.blurple, emoji="💙")
    async def blue(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            self.color = discord.Colour.blue()
            message = interaction.message
            embed = discord.Embed(color=self.color, title="Color Selected", description="You have selected **blue**. Is this correct?")
            view = YesOrNo(user=self.user)
            await message.edit(embed=embed, view=view)
            await view.wait()

            if view.value == True:
                self.stop()
            
            elif view.value == False:
                embed = discord.Embed(color=self.bot.blurple, title="Color", description="Choose the embed's color.")
                await message.edit(embed=embed, view=self)
    
    @discord.ui.button(label="Purple", style=discord.ButtonStyle.blurple, emoji="💜")
    async def purple(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            self.color = discord.Colour.purple()
            message = interaction.message
            embed = discord.Embed(color=self.color, title="Color Selected", description="You have selected **purple**. Is this correct?")
            view = YesOrNo(user=self.user)
            await message.edit(embed=embed, view=view)
            await view.wait()

            if view.value == True:
                self.stop()
            
            elif view.value == False:
                embed = discord.Embed(color=self.bot.blurple, title="Color", description="Choose the embed's color.")
                await message.edit(embed=embed, view=self)
    
    @discord.ui.button(label="Pink", style=discord.ButtonStyle.blurple, emoji="🩷")
    async def pink(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            self.color = discord.Colour.pink()
            message = interaction.message
            embed = discord.Embed(color=self.color, title="Color Selected", description="You have selected **pink**. Is this correct?")
            view = YesOrNo(user=self.user)
            await message.edit(embed=embed, view=view)
            await view.wait()

            if view.value == True:
                self.stop()
            
            elif view.value == False:
                embed = discord.Embed(color=self.bot.blurple, title="Color", description="Choose the embed's color.")
                await message.edit(embed=embed, view=self)
    
    @discord.ui.button(label="Custom", style=discord.ButtonStyle.blurple, emoji="🩶")
    async def custom(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:

            modal = CustomColorModal()
            await interaction.response.send_modal(modal)
            await modal.wait()

            self.color = modal.color
            message = interaction.message
            embed = discord.Embed(color=self.color, title="Color Selected", description="You have selected a **custom color**. Is this correct?")
            view = YesOrNo(user=self.user)
            await message.edit(embed=embed, view=view)
            await view.wait()

            if view.value == True:
                self.stop()
            
            elif view.value == False:
                embed = discord.Embed(color=self.bot.blurple, title="Color", description="Choose the embed's color.")
                await message.edit(embed=embed, view=self)
    
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:

            message = interaction.message
            embed = discord.Embed(color=self.bot.red, title="Cancel", description="Are you sure you want to **cancel** this interaction?")
            view = YesOrNo(user=self.user)
            await message.edit(embed=embed, view=view)
            await view.wait()

            if view.value == True:
                self.color = None
                self.stop()
            
            elif view.value == False:
                embed = discord.Embed(color=self.bot.blurple, title="Color", description="Choose the embed's color.")
                await message.edit(embed=embed, view=self)

class TitleModal(discord.ui.Modal, title = "Title"):
    title = None
    input = discord.ui.TextInput(label="Title", placeholder="Please provide a title for the embed...", max_length=256)

    async def on_submit(self, interaction: discord.Interaction):
        self.title = self.input.value
        self.stop()
    
    async def on_error(self, interaction: discord.Interaction, error: Exception):
        print(traceback.format_exc())
        self.stop()

class URLModal(discord.ui.Modal, title = "URL"):
    url = None
    input = discord.ui.TextInput(label="URL", placeholder="Please provide a URL for the embed...")

    async def on_submit(self, interaction: discord.Interaction):
        self.url = self.input.value
        self.stop()
    
    async def on_error(self, interaction: discord.Interaction, error: Exception):
        print(traceback.format_exc())
        self.stop()

class DescriptionModal(discord.ui.Modal, title = "Description"):
    description = None
    input = discord.ui.TextInput(label="Description", style=discord.TextStyle.long, placeholder="Please provide a description for the embed...", max_length=4000)

    async def on_submit(self, interaction: discord.Interaction):
        self.description = self.input.value
        self.stop()
    
    async def on_error(self, interaction: discord.Interaction, error: Exception):
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
    
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, row=2)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, row=2)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.stop()

class FieldNameModal(discord.ui.Modal, title = "Field Name"):
    field_name = None
    input = discord.ui.TextInput(label="Field Name", placeholder="Please provide a name for the field...", max_length=256)

    async def on_submit(self, interaction: discord.Interaction):
        self.field_name = self.input.value
        self.stop()
    
    async def on_error(self, interaction: discord.Interaction, error: Exception):
        print(traceback.format_exc())
        self.stop()

class FieldValueModal(discord.ui.Modal, title = "Field Value"):
    field_value = None
    input = discord.ui.TextInput(label="Field Value", placeholder="Please provide a value for the field...", max_length=1024)

    async def on_submit(self, interaction: discord.Interaction):
        self.field_value = self.input.value
        self.stop()
    
    async def on_error(self, interaction: discord.Interaction, error: Exception):
        print(traceback.format_exc())
        self.stop()

class FieldEditView(discord.ui.View):
    def __init__(self, *, timeout = 180, user: discord.Member, index: int):
        super().__init__(timeout=timeout)
        self.user = user
        self.index = index
        self.field = {}
    
    @discord.ui.button(label="Name", style=discord.ButtonStyle.blurple)
    async def name(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:
            modal = FieldNameModal()
            await interaction.response.send_modal(modal)
            await modal.wait()
            self.field["name"] = modal.field_name

    @discord.ui.button(label="Value", style=discord.ButtonStyle.blurple)
    async def value(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            modal = FieldValueModal()
            await interaction.response.send_modal(modal)
            await modal.wait()
            self.field["value"] = modal.field_value

    @discord.ui.button(label="Inline: True", style=discord.ButtonStyle.blurple)
    async def inline_true(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.field["inline"] = True
            button.disabled = True
            if self.inline_false.disabled == True:
                self.inline_false.disabled = False

    @discord.ui.button(label="Inline: False", style=discord.ButtonStyle.blurple)
    async def inline_false(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.field["inline"] = False
            button.disabled = True
            if self.inline_true.disabled == True:
                self.inline_true.disabled = False
    
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.field["index"] = self.index
            self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.field = None
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

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green, row=2)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red, row=2)
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

    @discord.ui.button(label="Color", style=discord.ButtonStyle.blurple, emoji="🎨")
    async def color(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            message = interaction.message
            embed = discord.Embed(color=self.bot.blurple, title="Color", description="Choose the embed's color.")
            view = ColorView(bot=self.bot, user=self.user)
            await message.edit(embed=embed, view=view)
            await view.wait()

            if view.color is not None:
                self.embed.colour = view.color
            
            await message.edit(embed=self.embed, view=self)

    @discord.ui.button(label="Title", style=discord.ButtonStyle.blurple, emoji="👑")
    async def title(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:
            modal = TitleModal()
            await interaction.response.send_modal(modal)
            await modal.wait()

            if modal.title is not None:
                self.embed.title = modal.title
            
            message = interaction.message
            await message.edit(embed=self.embed, view=self)
    
    @discord.ui.button(label="URL", style=discord.ButtonStyle.blurple, emoji="🔗")
    async def url(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:
            modal = URLModal()
            await interaction.response.send_modal(modal)
            await modal.wait()

            if modal.url is not None:
                self.embed.url = modal.url
            
            message = interaction.message
            await message.edit(embed=self.embed, view=self)
    
    @discord.ui.button(label="Description", style=discord.ButtonStyle.blurple, emoji="📄")
    async def description(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user:
            modal = DescriptionModal()
            await interaction.response.send_modal(modal)
            await modal.wait()

            if modal.description is not None:
                self.embed.description = modal.description
            
            message = interaction.message
            await message.edit(embed=self.embed, view=self)
    
    @discord.ui.button(label="Fields", style=discord.ButtonStyle.blurple, emoji="📝")
    async def fields(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            message = interaction.message
            view = FieldsSelectView(user=self.user)
            await message.edit(view=view)
            await view.wait()

            if view.value == True:

                if view.field is not None:

                    field_view = FieldEditView(user=self.user, index=view.field)
                    await message.edit(view=field_view)
                    await field_view.wait()

                    if field_view.field:
                        index = field_view.field["index"] or None
                        name = field_view.field["name"] or None
                        value = field_view.field["value"] or None
                        inline = field_view.field["inline"] or None

                        if len(self.embed.fields) < 25:
                            self.embed.insert_field_at(index=index, name=name, value=value, inline=inline)
                        else:
                            self.embed.remove_field(index=24)
                            self.embed.insert_field_at(index=index, name=name, value=value, inline=inline)
            
            await message.edit(embed=self.embed, view=self)
    
    @discord.ui.button(label="Submit", style=discord.ButtonStyle.green, emoji="✔️")
    async def submit(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.value = True
            self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red, emoji="✖️")
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

                channel_select = discord.Embed(color=self.bot.blurple, title="Channel", description="Please use the dropdown menu below to select the channel where the embed should be sent. Press the `submit` button to submit or press the `cancel` button to cancel.")
                channel_select_view = ChannelSelectView(bot=self.bot, user=user)
                await response.edit(embed=channel_select, view=channel_select_view)
                await channel_select_view.wait()

                if channel_select_view.value == True:

                    if channel_select_view.channel_id is not None:
                        channel = guild.get_channel_or_thread(channel_select_view.channel_id)
                        await channel.send(embed=view.embed)

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
            await interaction.followup.send(embed=error)
            print(traceback.format_exc())

async def setup(bot: commands.Bot):
    print("Setting up Cog: embeds.Embeds")

async def teardown(bot: commands.Bot):
    print("Tearing down Cog: embeds.Embeds")
