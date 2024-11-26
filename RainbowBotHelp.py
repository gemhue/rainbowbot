import discord
from discord.ext import commands

class CogButtons(discord.ui.View):
    def __init__(self, *, timeout = 180, user = discord.Member):
        super().__init__(timeout=timeout)
        self.user = user
    
    @discord.ui.button(label="AutoDelete", style=discord.ButtonStyle.blurple, emoji="♻️")
    async def autodelete(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            embed = discord.Embed(color=discord.Color.blurple(), title="AutoDelete", description="These commands allow you to set the messages in a channel to be automatically deleted on a rolling basis.")
            embed.add_field(
                name="/autodelete start <amount> <interval>",
                value="(Admin Only) Sets the messages in the current channel to be autodeleted.\n> `amount` - Set the amount of time. The lowest possible frequency is 30 minutes.\n> `interval` - Set the time interval. The lowest possible frequency is 30 minutes.",
                inline=False
            )
            embed.add_field(
                name="/autodelete cancel",
                value="(Admin Only) Cancels the autodelete set for the current channel.",
                inline=False
            )

            message = interaction.message
            await interaction.followup.edit_message(message_id=message.id, embed=embed, view=self)
    
    @discord.ui.button(label="Awards", style=discord.ButtonStyle.blurple, emoji="🏅")
    async def awards(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            embed = discord.Embed(color=discord.Color.blurple(), title="Awards", description="These commands allow you to set up an awards system in your server. The award name and emoji can be customized.")
            embed.add_field(
                name="/awards setup",
                value="(Admin Only) Sets the name, emoji, and leaderboard channel for the server awards.",
                inline=False
            )
            embed.add_field(
                name="/awards clear",
                value="(Admin Only) Clears every member's awards in the server.",
                inline=False
            )
            embed.add_field(
                name="/awards add <amount> <member>",
                value="Adds awards to the command user or another selected member.\n> `amount` - Choose the number of awards to add. (Default: 1)\n> `member` - Choose the member to add the awards to. (Default: Self)",
                inline=False
            )
            embed.add_field(
                name="/awards remove <amount> <member>",
                value="Removes awards from the command user or another selected member.\n> `amount` - Choose the number of awards to remove. (Default: 1)\n> `member` - Choose the member to remove the awards from. (Default: Self)",
                inline=False
            )
            embed.add_field(
                name="/awards check <member>",
                value="Returns the number of awards that the command user or another selected user currently has.\n> `member` - Choose the member that you would like to check the number of awards for. (Default: Self)",
                inline=False
            )

            message = interaction.message
            await interaction.followup.edit_message(message_id=message.id, embed=embed, view=self)

    @discord.ui.button(label="Embeds", style=discord.ButtonStyle.blurple, emoji="📝")
    async def embeds(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            embed = discord.Embed(color=discord.Color.blurple(), title="Embeds", description="These commands allow you to send and edit messages containing embeds.")
            embed.add_field(
                name="/embed send <message_content> <embed_color> <embed_title> <embed_url> <embed_description>",
                value="(Admin Only) Run this command to send an embed to the current channel.\n> `message_content` - Provide the content of the message above the embed.\n> `embed_color` - Provide the embed's color (HEX or RGB).\n> `embed_title` - Provide the embed's title.\n> `embed_url` - Provide the embed's URL.\n> `embed_description` - Provide the embed's description.",
                inline=False
            )
            embed.add_field(
                name="/embed edit <message_url> <message_content> <embed_color> <embed_title> <embed_url> <embed_description>",
                value="(Admin Only) Run this command to edit the embed of a given message URL.\n> `message_url` - Provide the URL of the message containing the embed.\n> `message_content` - Provide the new content of the message above the embed.\n> `embed_color` - Provide the embed's new color (HEX or RGB).\n> `embed_title` - Provide the embed's new title.\n> `embed_url` - Provide the embed's new URL.\n> `embed_description` - Provide the embed's new description.",
                inline=False
            )
            embed.add_field(
                name="/embed set_image <message_url> <image_url>",
                value="(Admin Only) Run this command to set an embed's image.\n> `message_url` - Provide the URL of the message containing the embed.\n> `image_url` - Provide the URL of the image.",
                inline=False
            )
            embed.add_field(
                name="/embed remove_image <message_url>",
                value="(Admin Only) Run this command to remove an embed's image.\n> `message_url` - Provide the URL of the message containing the embed.",
                inline=False
            )
            embed.add_field(
                name="/embed set_thumbnail <message_url> <thumbnail_url>",
                value="(Admin Only) Run this command to set an embed's thumbnail.\n> `message_url` - Provide the URL of the message containing the embed.\n> `thumbnail_url` - Provide the URL of the thumbnail.",
                inline=False
            )
            embed.add_field(
                name="/embed remove_thumbnail <message_url>",
                value="(Admin Only) Run this command to remove an embed's thumbnail.\n> `message_url` - Provide the URL of the message containing the embed.",
                inline=False
            )
            embed.add_field(
                name="/embed add_field <message_url> <name> <value> <inline>",
                value="(Admin Only) Run this command to add a field to an embed.\n> `message_url` - Provide the URL of the message containing the embed.\n> `name` - Provide the name of the field to be added.\n> `value` - Provide the value of the field to be added.\n> `inline` - Provide whether the field should be inline.",
                inline=False
            )
            embed.add_field(
                name="/embed edit_field <message_url> <index> <name> <value> <inline>",
                value="(Admin Only) Run this command to edit a field of an embed by its index.\n> `message_url` - Provide the URL of the message containing the embed.\n> `index` - Provide the index of the field to be edited.\n> `name` - Provide the new name of the field.\n> `value` - Provide the new value of the field.\n> `inline` - Provide whether the edited field should be inline.",
                inline=False
            )
            embed.add_field(
                name="/embed insert_field <message_url> <index> <name> <value> <inline>",
                value="(Admin Only) Run this command to insert an embed field at an index.\n> `message_url` - Provide the URL of the message containing the embed.\n> `index` - Provide the index of the field to be inserted.\n> `name` - Provide the name of the field to be inserted.\n> `value` - Provide the value of the field to be inserted.\n> `inline` - Provide whether the inserted field should be inline.",
                inline=False
            )
            embed.add_field(
                name="/embed remove_field <message_url> <index>",
                value="(Admin Only) Run this command to remove a field from an embed by its index.\n> `message_url` - Provide the URL of the message containing the embed.\n> `index` - Provide the index of the field to be removed.",
                inline=False
            )

            message = interaction.message
            await interaction.followup.edit_message(message_id=message.id, embed=embed, view=self)

    @discord.ui.button(label="Profiles", style=discord.ButtonStyle.blurple, emoji="🪪")
    async def profiles(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            embed = discord.Embed(color=discord.Color.blurple(), title="Profiles", description="These commands allow you and your server members to set up member profiles that can be viewed and edited.")
            embed.add_field(
                name="/profile set <name> <age> <location> <pronouns> <gender> <sexuality> <relationship_status> <family_status> <biography>",
                value="Run this command to set up your member profile. Note that all fields are optional.\n> `name` - Provide your name or nickname.\n> `age` - Provide your age or age range.\n> `location` - Provide your continent, country, state, or city of residence.\n> `pronouns` - Provide your pronouns (ex. she/her, he/him, they/them, etc).\n> `gender` - Provide your gender identity label (ex. woman, man, nonbinary, etc).\n> `sexuality` - Provide your sexuality label (ex. lesbian, gay, bisexual, etc).\n> `relationship_status` - Provide your relationship status (ex. single, married, etc).\n> `family_status` - Provide your your family planning status (ex. TTC, expecting, parenting, etc).\n> `biography` - Provide a brief biography (ex. family, hobbies, interests, work, etc).",
                inline=False
            )
            embed.add_field(
                name="/profile get <member>",
                value="Run this command to retrieve a member's profile.\n> `member` - Provide the member whose profile you would like to retrieve.",
                inline=False
            )

            message = interaction.message
            await interaction.followup.edit_message(message_id=message.id, embed=embed, view=self)
    
    @discord.ui.button(label="Purge", style=discord.ButtonStyle.blurple, emoji="🗑️")
    async def purge(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            embed = discord.Embed(color=discord.Color.blurple(), title="Purge", description="These commands allow you to easily mass-delete messages in a single channel or in multiple channels at once.")
            embed.add_field(
                name="/purge here",
                value="(Admin Only) Purge all unpinned messages in the current channel.",
                inline=False
            )
            embed.add_field(
                name="/purge member <member>",
                value="(Admin Only) Purge all of a member's unpinned messages in a set list of up to 25 channels.\n> `member` - Provide the member who's unpinned messages you would like to purge.",
                inline=False
            )
            embed.add_field(
                name="/purge channels",
                value="(Admin Only) Purge all unpinned messages in a set list of up to 25 channels.",
                inline=False
            )
            embed.add_field(
                name="/purge server",
                value="(Admin Only) Purges all unpinned messages in a server, excluding up to 25 channels.",
                inline=False
            )

            message = interaction.message
            await interaction.followup.edit_message(message_id=message.id, embed=embed, view=self)
    
    @discord.ui.button(label="Remind", style=discord.ButtonStyle.blurple, emoji="📅")
    async def remind(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            embed = discord.Embed(color=discord.Color.blurple(), title="Remind", description="These commands allow you to set reminders for yourself, a user, a role, or everyone.")
            embed.add_field(
                name="/remind everyone <what> <when> <where>",
                value="(Admin Only) Create a reminder for everyone.\n> `what` - What would you like the bot to remind everyone about?\n> `when` - When would you like the bot to send the reminder?\n> `where` - Where would you like the bot to send the reminder?",
                inline=False
            )
            embed.add_field(
                name="/remind role <who> <what> <when> <where>",
                value="(Admin Only) Create a reminder for all users with a specified role.\n> `who` - Choose the role that should be sent the reminder.\n> `what` - What would you like the bot to remind the role about?\n> `when` - When would you like the bot to send the reminder?\n> `where` - Where would you like the bot to send the reminder?",
                inline=False
            )
            embed.add_field(
                name="/remind user <who> <what> <when> <where>",
                value="(Admin Only) Create a reminder for a specified user.\n> `who` - Choose the user that should be sent the reminder.\n> `what` - What would you like the bot to remind the user about?\n> `when` - When would you like the bot to send the reminder?\n> `where` - Where would you like the bot to send the reminder?",
                inline=False
            )
            embed.add_field(
                name="/remind me <what> <when> <where>",
                value="Create a reminder for yourself.\n> `what` - What would you like the bot to remind you about?\n> `when` - When would you like the bot to send the reminder?\n> `where` - Where would you like the bot to send the reminder?",
                inline=False
            )

            message = interaction.message
            await interaction.followup.edit_message(message_id=message.id, embed=embed, view=self)

    @discord.ui.button(label="RSS Feeds", style=discord.ButtonStyle.blurple, emoji="📰")
    async def rss_feeds(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            embed = discord.Embed(color=discord.Color.blurple(), title="RSS Feeds", description="These commands allow you to easily assign and unassign RSS feeds to Webhooks to post new entries automatically.")
            embed.add_field(
                name="/rss webhook_setup <webhook_nickname> <webhook_url>",
                value="(Admin Only) Run this command to set up a Webhook for posting RSS feeds.\n> `webhook_nickname` - Provide a nickname for the Webhook.\n> `webhook_url` - Provide the URL for the Webhook.",
                inline=False
            )
            embed.add_field(
                name="/rss webhook_check <webhook_nickname>",
                value="(Admin Only) Run this command to check what RSS feeds are set to the webhook.\n> `webhook_nickname` - Provide the nickname for the webhook that you would like to check.",
                inline=False
            )
            embed.add_field(
                name="/rss webhook_clear <webhook_nickname>",
                value="(Admin Only) Run this command to clear all RSS feeds assigned to a webhook.\n> `webhook_nickname` - Provide the nickname for the webhook that you would like to clear.",
                inline=False
            )
            embed.add_field(
                name="/rss webhook_delete <webhook_nickname>",
                value="(Admin Only) Run this command to delete a webhook from the database.\n> `webhook_nickname` - Provide the nickname for the webhook that you would like to delete.",
                inline=False
            )
            embed.add_field(
                name="/rss feed_setup <webhook_nickname> <rss_feed_url>",
                value="(Admin Only) Run this command to set an RSS Feed. All fields are required.\n> `webhook_nickname` - Provide the nickname for the webhook that you are assigning the RSS feed to.\n> `rss_feed_url` - Provide the URL for the RSS feed that you are assigning to the webhook.",
                inline=False
            )
            embed.add_field(
                name="/rss feed_clear <webhook_nickname> <rss_feed_position>",
                value="(Admin Only) Run this command to clear one RSS feed from a webhook.\n> `webhook_nickname` - Provide the nickname for the webhook that contains the RSS feed to be cleared.\n> `rss_feed_position` - Provide the position (0-9) on the webhook where the RSS feed to be cleared is located.",
                inline=False
            )

            message = interaction.message
            await interaction.followup.edit_message(message_id=message.id, embed=embed, view=self)

    @discord.ui.button(label="Tickets", style=discord.ButtonStyle.blurple, emoji="🎫")
    async def rss_feeds(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:

            embed = discord.Embed(color=discord.Color.blurple(), title="Tickets", description="This command allows you to set up a simple ticketing system for your server using threads.")
            embed.add_field(
                name="/tickets setup <channel> <staff_role>",
                value="(Admin Only) Set up a ticketing system for the server.\n> `channel` - Provide the channel where the ticketing system should be posted.\n> `staff_role` - Provide the role that should be pinged when a ticket is opened.",
                inline=False
            )

            message = interaction.message
            await interaction.followup.edit_message(message_id=message.id, embed=embed, view=self)
    
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
    async def done(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            self.stop()

class RainbowBotHelp(commands.HelpCommand):
    def __init__(self):
        super().__init__()
    
    async def send_bot_help(self, mapping):
        ctx = self.context
        user = ctx.author
        await ctx.message.delete()
        channel = self.get_destination()
        embed = discord.Embed(color=discord.Color.blurple(), title="Help", description="If you have any questions that are not answered by this `help` command, please join the bot's support server (linked in the bot's bio).")
        view = CogButtons(user=user)
        response = await channel.send(embed=embed, view=view)
        await view.wait()
        await response.delete()