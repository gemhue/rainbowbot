# 🌈 Rainbow Bot Documentation 🌈

> [!IMPORTANT]
> If you find that any commands are not responding, first check that the bot is online. If the bot is online, run the `/commands remove` command and remove all commands from the server. Afterwards, run the `/commands add` command to add the commands that you would like. Try the unresponsive commands again - they should work. If they don't, please either open an [issue](https://github.com/gemhue/rainbowbot/issues) on GitHub or report the bug in the [support server](https://discord.gg/5x3xBSdWbE).

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

### 🏠 Server
> `/rainbowbot server`
> 
> Get the invite link for 🌈 Rainbow Bot's support server.

### 🏠 Install
> `/rainbowbot install`
> 
> Get the server install link for 🌈 Rainbow Bot.

## ♻️ AutoDelete ♻️

These commands allow you to set the messages in a channel to be automatically deleted on a rolling basis.

### ♻️ Start
> `/autodelete start <interval>`
> 
> (Admin Only) Sets the messages in the current channel to be autodeleted.
> - `interval` - Choose how often the bot should delete messages from the current channel.

### ♻️ Cancel
> `/autodelete cancel`
> 
> (Admin Only) Cancels the autodelete set for the current channel.

    
## 🏅 Awards 🏅

> [!WARNING]
> There is a known issue with the `/awards setup` command. It does not allow you to choose an award reaction toggle. These commands can't be used until this issue is resolved.

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

This command allows you to build and send embeds to selected channels.

### 📝 Build
> `/embed build`
>
> (Admin Only) Run this command to build and send an embed.


## 🪪 Profiles 🪪

These commands allow you and your server members to set up member profiles that can be viewed and edited.

### 🪪 Set
> `/profile set <name> <age> <location> <pronouns> <gender> <sexuality> <relationship_status> <family_status> <biography>`
>
> Run this command to set up your member profile. Note that all fields are optional.
> - `name` - Provide your name or nickname.
> - `age` - Provide your age or age range.
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

> [!WARNING]
> If you are deleting a large number of messages from a large number of channels, expect these commands to take some time to complete. Sometimes, even a small number of messages from a small number of channels may take some time. These commands are very prone to being ratelimited by Discord.

These commands allow you to easily mass-delete messages in a single channel or in multiple channels at once.

### 🗑️ Here
> `/purge here`
> 
> (Admin Only) Purge all unpinned messages in the current channel.

### 🗑️ Self
> `/purge self`
> 
> Purge all of your own unpinned messages in a set list of up to 25 channels.

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

> [!WARNING]
> This system is unstable. It works anywhere from unreliably to not at all. Use it at your own risk.

This command allows you to easily assign an RSS feed to a Webhook.

### 📰 Setup Webhook
> `/rssfeed setup <webhook_url> <rss_feed_url>`
> 
> (Admin Only) Run this command to set up an RSS feed to a Webhook.
> - `webhook_url` - Provide the URL for the Webhook.
> - `rss_feed_url` - Provide the URL for the RSS Feed.


## 🎫 Tickets 🎫

This command allows you to set up a simple ticketing system for your server using threads.

### 🎫 Setup
> `/tickets setup <channel> <staff_role>`
> 
> (Admin Only) Set up a ticketing system for the server.
> - `channel` - Provide the channel where the ticketing system should be posted.
> - `staff_role` - Provide the role that should be pinged when a ticket is opened.
