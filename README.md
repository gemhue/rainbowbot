# rainbowbot

Activity Role Command
/activityroles - Assigns all server members either an active or inactive role. (Admin Only)
<days> (Required) - Set the number of days a member must be inactive before getting the inactive role.
<inactive> (Required) - Choose the role that you would like to give to inactive members.
<active> (Required) - Choose the role that you would like to give to active members.

Server Purge Command
/purgeserver - Purges all unpinned messages in a server, excluding up to 25 channels. (Admin Only)

Channel Purge Command
/purgechannels - Purge unpinned messages in a set list of up to 25 channels. (Admin Only)

Self Purge Command
/purgeself - Purge your unpinned messages in a set list of up to 25 channels.

Award Set Command
/setawards - Sets the name and emoji for the server awards.
<name_singular> (Required) - Provide the singular form of the award name. (Default: Award)
<name_plural> (Required) - Provide the plural form of the award name. (Default: Awards)
<emoji> (Required) - Choose the emoji you would like to represent the award. (Default: 🏅)

Award Add Command
/addaward - Adds awards to the command user or another selected member.
<amount> (Optional) - Choose the number of awards to add. (Default: 1)
<member> (Optional) - Choose the member to add the awards to. (Default: Self)

Award Remove Command
/removeaward - Removes awards from the command user or another selected member.
<amount> (Optional) - Choose the amount of awards to remove. (Default: 1)
<member> (Optional) - Choose the member to remove the awards from. (Default: Self)

Note: You can also add an award to another user (or yourself) by reacting to a message with the emoji set in the /setawards command. Removing the reaction will remove the award.

Award Check Command
/checkawards - Returns the number of awards that the user (or another selected user) currently has.
<member> (Optional) - Choose the member that you would like to check the number of awards for. (Default: Self)

Award Clear Command
/clearawards - Clears all of the awards in the server.

Award Leaderboard Command
/leaderboard - Returns the current award leaderboard for the server.
