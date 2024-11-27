# 🌈 Rainbow Bot Documentation 🌈

🔗 [Discovery Page](https://discord.com/application-directory/1263872722195316737)

🔗 [Support Server](https://discord.gg/5x3xBSdWbE)

## 🏠 Default 🏠

These are the default commands which will allow you to customize the bot.

### 🏠 Start
> `/start`
> 
> (Admin Only) Start the bot by choosing desired functions.

### 🏠 Add Commands
> `/commands add`
> 
> (Admin Only) Add desired commands to the server.

### 🏠 Remove Commands
> `/commands remove`
> 
> (Admin Only) Remove unwanted commands from the server.


## ♻️ AutoDelete ♻️

These commands allow you to set the messages in a channel to be automatically deleted on a rolling basis.

### ♻️ Start
> `/autodelete start <amount> <interval>`
> 
> (Admin Only) Sets the messages in the current channel to be autodeleted.
> - `amount` - Set the amount of time. The lowest possible frequency is 30 minutes.
> - `interval` - Set the time interval. The lowest possible frequency is 30 minutes.

### ♻️ Cancel
> `/autodelete cancel`
> 
> (Admin Only) Cancels the autodelete set for the current channel.

    
## 🏅 Awards 🏅

These commands allow you to set up an awards system in your server. The award name and emoji can be customized.

### 🏅 Setup
> `/awards setup`
> 
> (Admin Only) Sets the name, emoji, and leaderboard channel for the server awards.

### 🏅 Clear
> `/awards clear`
> 
> (Admin Only) Clears every member's awards in the server.

### 🏅 Add
> `/awards add <amount> <member>`
> 
> Adds awards to the command user or another selected member.
> - `amount` - Choose the number of awards to add. (Default: 1)
> - `member` - Choose the member to add the awards to. (Default: Self)

### 🏅 Remove
> `/awards remove <amount> <member>`
> 
> Removes awards from the command user or another selected member.
> - `amount` - Choose the number of awards to remove. (Default: 1)
> - `member` - Choose the member to remove the awards from. (Default: Self)

### 🏅 Check
> `/awards check <member>`
> 
> Returns the number of awards that the command user or another selected user currently has.
> - `member` - Choose the member that you would like to check the number of awards for. (Default: Self)


## 📝 Embeds 📝

These commands allow you to send and edit messages containing embeds.

### 📝 Send
> `/embed send <message_content> <embed_color> <embed_title> <embed_url> <embed_description>`
>
> (Admin Only) Run this command to send an embed to the current channel.
> - `message_content` - Provide the content of the message above the embed.
> - `embed_color` - Provide the embed's color (HEX or RGB).
> - `embed_title` - Provide the embed's title.
> - `embed_url` - Provide the embed's URL.
> - `embed_description` - Provide the embed's description.

### 📝 Edit
> `/embed edit <message_url> <message_content> <embed_color> <embed_title> <embed_url> <embed_description>`
>
> (Admin Only) Run this command to edit the embed of a given message URL.
> - `message_url` - Provide the URL of the message containing the embed.
> - `message_content` - Provide the new content of the message above the embed.
> - `embed_color` - Provide the embed's new color (HEX or RGB).
> - `embed_title` - Provide the embed's new title.
> - `embed_url` - Provide the embed's new URL.
> - `embed_description` - Provide the embed's new description.

### 📝 Set Image
> `/embed set_image <message_url> <image_url>`
>
> (Admin Only) Run this command to set an embed's image.
> - `message_url` - Provide the URL of the message containing the embed.
> - `image_url` - Provide the URL of the image.

### 📝 Remove Image
> `/embed remove_image <message_url>`
>
> (Admin Only) Run this command to remove an embed's image.
> - `message_url` - Provide the URL of the message containing the embed.

### 📝 Set Thumbnail
> `/embed set_thumbnail <message_url> <thumbnail_url>`
>
> (Admin Only) Run this command to set an embed's thumbnail.
> - `message_url` - Provide the URL of the message containing the embed.
> - `thumbnail_url` - Provide the URL of the thumbnail.

### 📝 Remove Thumbnail
> `/embed remove_thumbnail <message_url>`
>
> (Admin Only) Run this command to remove an embed's thumbnail.
> - `message_url` - Provide the URL of the message containing the embed.

### 📝 Add Field
> `/embed add_field <message_url> <name> <value> <inline>`
>
> (Admin Only) Run this command to add a field to an embed.
> - `message_url` - Provide the URL of the message containing the embed.
> - `name` - Provide the name of the field to be added.
> - `value` - Provide the value of the field to be added.
> - `inline` - Provide whether the field should be inline.

### 📝 Edit Field
> `/embed edit_field <message_url> <index> <name> <value> <inline>`
>
> (Admin Only) Run this command to edit a field of an embed by its index.
> - `message_url` - Provide the URL of the message containing the embed.
> - `index` - Provide the index of the field to be edited.
> - `name` - Provide the new name of the field.
> - `value` - Provide the new value of the field.
> - `inline` - Provide whether the edited field should be inline.

### 📝 Insert Field
> `/embed insert_field <message_url> <index> <name> <value> <inline>`
>
> (Admin Only) Run this command to insert an embed field at an index.
> - `message_url` - Provide the URL of the message containing the embed.
> - `index` - Provide the index of the field to be inserted.
> - `name` - Provide the name of the field to be inserted.
> - `value` - Provide the value of the field to be inserted.
> - `inline` - Provide whether the inserted field should be inline.

### 📝 Remove Field
> `/embed remove_field <message_url> <index>`
>
> (Admin Only) Run this command to remove a field from an embed by its index.
> - `message_url` - Provide the URL of the message containing the embed.
> - `index` - Provide the index of the field to be removed.


## 🪪 Profiles 🪪

These commands allow you and your server members to set up member profiles that can be viewed and edited.

### 🪪 Set
> `/profile set <name> <age> <location> <pronouns> <gender> <sexuality> <relationship_status> <family_status> <biography>`
>
> Run this command to set up your member profile. Note that all fields are optional.
> - `name` - Provide your name or nickname.\n> `age` - Provide your age or age range.
> - `location` - Provide your continent, country, state, or city of residence.
> - `pronouns` - Provide your pronouns (ex. she/her, he/him, they/them, etc).
> - `gender` - Provide your gender identity label (ex. woman, man, nonbinary, etc).
> - `sexuality` - Provide your sexuality label (ex. lesbian, gay, bisexual, etc).
> - `relationship_status` - Provide your relationship status (ex. single, married, etc).
> - `family_status` - Provide your your family planning status (ex. TTC, expecting, parenting, etc).
> - `biography` - Provide a brief biography (ex. family, hobbies, interests, work, etc).

### 🪪 Get
> `/profile get <member>`
> 
> Run this command to retrieve a member's profile.
> - `member` - Provide the member whose profile you would like to retrieve.

    
## 🗑️ Purge 🗑️

These commands allow you to easily mass-delete messages in a single channel or in multiple channels at once.

### 🗑️ Here
> `/purge here`
> 
> (Admin Only) Purge all unpinned messages in the current channel.

### 🗑️ Member
> `/purge member <member>`
> 
> (Admin Only) Purge all of a member's unpinned messages in a set list of up to 25 channels.
> - `member` - Provide the member who's unpinned messages you would like to purge.

### 🗑️ Channels
> `/purge channels`
> 
> (Admin Only) Purge all unpinned messages in a set list of up to 25 channels.

### 🗑️ Server
> `/purge server`
> 
> (Admin Only) Purges all unpinned messages in a server, excluding up to 25 channels.


## 📅 Remind 📅

These commands allow you to set reminders for yourself, a user, a role, or everyone.

### 📅 Everyone
> `/remind everyone <what> <when> <where>`
> 
> (Admin Only) Create a reminder for everyone.
> - `what` - What would you like the bot to remind everyone about?
> - `when` - When would you like the bot to send the reminder?
> - `where` - Where would you like the bot to send the reminder?

### 📅 Role
> `/remind role <who> <what> <when> <where>`
> 
> (Admin Only) Create a reminder for all users with a specified role.
> - `who` - Choose the role that should be sent the reminder.
> - `what` - What would you like the bot to remind the role about?
> - `when` - When would you like the bot to send the reminder?
> - `where` - Where would you like the bot to send the reminder?

### 📅 User
> `/remind user <who> <what> <when> <where>`
> 
> (Admin Only) Create a reminder for a specified user.
> - `who` - Choose the user that should be sent the reminder.
> - `what` - What would you like the bot to remind the user about?
> - `when` - When would you like the bot to send the reminder?
> - `where` - Where would you like the bot to send the reminder?

### 📅 Me
> `/remind me <what> <when> <where>`
> 
> Create a reminder for yourself.
> - `what` - What would you like the bot to remind you about?
> - `when` - When would you like the bot to send the reminder?
> - `where` - Where would you like the bot to send the reminder?


## 📰 RSS Feeds 📰

These commands allow you to easily assign and unassign RSS feeds to Webhooks to post new entries automatically.

### 📰 Setup Webhook
> `/rss webhook_setup <webhook_nickname> <webhook_url>`
> 
> (Admin Only) Run this command to set up a Webhook for posting RSS feeds.
> - `webhook_nickname` - Provide a nickname for the Webhook.
> - `webhook_url` - Provide the URL for the Webhook.

### 📰 Check Webhook
> `/rss webhook_check <webhook_nickname>`
> 
> (Admin Only) Run this command to check what RSS feeds are set to the webhook.
> - `webhook_nickname` - Provide the nickname for the webhook that you would like to check.

### 📰 Clear Webhook
> `/rss webhook_clear <webhook_nickname>`
> 
> (Admin Only) Run this command to clear all RSS feeds assigned to a webhook.
> - `webhook_nickname` - Provide the nickname for the webhook that you would like to clear.

### 📰 Delete Webhook
> `/rss webhook_delete <webhook_nickname>`
> 
> (Admin Only) Run this command to delete a webhook from the database.
> - `webhook_nickname` - Provide the nickname for the webhook that you would like to delete.

### 📰 Setup Feed
> `/rss feed_setup <webhook_nickname> <rss_feed_url>`
> 
> (Admin Only) Run this command to set an RSS Feed. All fields are required.
> - `webhook_nickname` - Provide the nickname for the webhook that you are assigning the RSS feed to.
> - `rss_feed_url` - Provide the URL for the RSS feed that you are assigning to the webhook.

### 📰 Clear Feed
> `/rss feed_clear <webhook_nickname> <rss_feed_position>`
> 
> (Admin Only) Run this command to clear one RSS feed from a webhook.
> - `webhook_nickname` - Provide the nickname for the webhook that contains the RSS feed to be cleared.
> - `rss_feed_position` - Provide the position (0-9) on the webhook where the RSS feed to be cleared is located.


## 🎫 Tickets 🎫

These commands allow you to set up a simple ticketing system for your server using threads.

### 🎫 Setup
> `/tickets setup <channel> <staff_role>`
> 
> (Admin Only) Set up a ticketing system for the server.
> - `channel` - Provide the channel where the ticketing system should be posted.
> - `staff_role` - Provide the role that should be pinged when a ticket is opened.
