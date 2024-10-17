import discord
from discord import app_commands
from discord.ext import commands
import aiosqlite
from typing import Optional

class Awards(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.hybrid_group(name="awards", fallback="set")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def awards(self, ctx: commands.Context, name_singular: str, name_plural: str, emoji: str):
        """(Admin Only) Sets the name and emoji for the server awards.

        Parameters
        -----------
        name_singular : str
            Provide the singular form of the award name. (Default: Award)
        name_plural : str
            Provide the plural form of the award name. (Default: Awards)
        emoji : str
            Choose the emoji you would like to represent the award. (Default: 🏅)
        """
        await ctx.defer(ephemeral=True)
        guild = ctx.guild
        guild_id = guild.id
        sing_low = name_singular.lower()
        plur_low = name_plural.lower()
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            await db.execute("UPDATE guilds SET award_singular = ? WHERE guild_id = ?", (sing_low, guild_id))
            cur = await db.execute("SELECT award_singular FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            fetched_sing_low = str(row[0])
            fetched_sing_cap = fetched_sing_low.title()
            await db.execute("UPDATE guilds SET award_plural = ? WHERE guild_id = ?", (plur_low, guild_id))
            cur = await db.execute("SELECT award_plural FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            fetched_plur_low = str(row[0])
            fetched_plur_cap = fetched_plur_low.title()
            await db.execute("UPDATE guilds SET award_emoji = ? WHERE guild_id = ?", (emoji, guild_id))
            cur = await db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            fetched_moji = str(row[0])
            await db.commit()
            await db.close()
        embed = discord.Embed(title="Custom Awards Set")
        embed.add_field(name="Name (Singular)", value=f"{fetched_sing_cap}", inline=False)
        embed.add_field(name="Name (Plural)", value=f"{fetched_plur_cap}", inline=False)
        embed.add_field(name="Emoji", value=f"{fetched_moji}", inline=False)
        await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)

    @awards.command(name="clear")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def clear(self, ctx: commands.Context):
        """(Admin Only) Clears all of the awards in the server.
        """
        await ctx.defer(ephemeral=True)
        guild = ctx.guild
        guild_id = guild.id
        member_ids = [member.id for member in guild.members if not member.bot]
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            cur = await db.execute("SELECT award_plural FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            plur_low = row[0]
            if plur_low is None:
                plur_low = "awards"
            plur_cap = plur_low.title()
            cur = await db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            moji = row[0]
            if moji is None:
                moji = "🏅"
            for member_id in member_ids:
                guild_member_id = int(str(guild_id) + str(member_id))
                await db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
                await db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (0, guild_member_id))
            await db.commit()
            await db.close()
        embed = discord.Embed(title=f"{moji} {plur_cap} Cleared {moji}", description=f"{guild.name} has had all its {plur_low} cleared!")
        await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)

    @awards.command(name="reaction_toggle")
    @commands.has_guild_permissions(administrator=True)
    @app_commands.checks.has_permissions(administrator=True)
    async def reaction_toggle(self, ctx: commands.Context, toggle: bool):
        """(Admin Only) Toggles the ability for users to add or remove awards with reactions.

        Parameters
        -----------
        toggle : bool
            Set to True to toggle award reactions on. Set to False to toggle award reactions off.
        """
        ctx.defer(ephemeral=True)
        guild = ctx.guild
        guild_id = guild.id
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            if toggle == True:
                toggle = 1
                await db.execute("UPDATE guilds SET award_reaction_toggle = ? WHERE guild_id = ?", (toggle, guild_id))
                cur = await db.execute(("SELECT award_reaction_toggle FROM guilds WHERE guild_id = ?", (guild_id,)))
                row = await cur.fetchone()
                fetched_toggle = row[0]
                embed = discord.Embed(title="Update", description=f"The toggle for award reactions has been set to **True** AKA {fetched_toggle}. Reacting and un-reacting to posts with the award emoji **will** now add and remove awards.")
            elif toggle == False:
                toggle = 0
                await db.execute("UPDATE guilds SET award_reaction_toggle = ? WHERE guild_id = ?", (toggle, guild_id))
                cur = await db.execute(("SELECT award_reaction_toggle FROM guilds WHERE guild_id = ?", (guild_id,)))
                row = await cur.fetchone()
                fetched_toggle = row[0]
                embed = discord.Embed(title="Update", description=f"The toggle for award reactions has been set to **False** AKA {fetched_toggle}. Reacting and un-reacting to posts with the award emoji **will not** add and remove awards.")
            else:
                embed = discord.Embed(title="❌ Error ❌", description=f"Your input could not be parsed. Please enter either True to toggle award reactions ON or False to toggle award reactions OFF.")
            await db.commit()
            await db.close()
        ctx.send(embed=embed, delete_after=30.0, ephemeral=True)

    @commands.Cog.listener(name="on_reaction_add")
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.Member):
        message = reaction.message
        channel = message.channel
        guild = message.guild
        guild_id = guild.id
        member = message.author
        member_id = member.id
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            cur = await db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            moji = row[0]
            if moji is None:
                moji = "🏅"
            if str(reaction.emoji) == moji:
                cur = await db.execute("SELECT award_react_toggle FROM guilds WHERE guild_id = ?", (guild_id,))
                row = await cur.fetchone()
                toggle = row[0]
                if toggle == 1:
                    cur = await db.execute("SELECT award_singular FROM guilds WHERE guild_id = ?", (guild_id,))
                    row = await cur.fetchone()
                    sing_low = row[0]
                    if sing_low is None:
                        sing_low = "award"
                    sing_cap = sing_low.title()
                    cur = await db.execute("SELECT award_plural FROM guilds WHERE guild_id = ?", (guild_id,))
                    row = await cur.fetchone()
                    plur_low = row[0]
                    if plur_low is None:
                        plur_low = "awards"
                    guild_member_id = int(str(guild_id) + str(member_id))
                    await db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
                    cur = await db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
                    row = await cur.fetchone()
                    current = row[0]
                    if current is None:
                        current = 0
                    new = current + 1
                    await db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (new, guild_member_id))
                    cur = await db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
                    row = await cur.fetchone()
                    new = row[0]
                    if new == 1:
                        embed = discord.Embed(title=f"{moji} {sing_cap} Added {moji}", description=f"{member.mention} now has {new} {sing_low}! ({sing_cap} added by {user.mention}.)")
                    else:
                        embed = discord.Embed(title=f"{moji} {sing_cap} Added {moji}", description=f"{member.mention} now has {new} {plur_low}! ({sing_cap} added by {user.mention}.)")
                    await channel.send(embed=embed, delete_after=30.0, reference=message)
            await db.commit()
            await db.close()

    @commands.Cog.listener(name="on_reaction_remove")
    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.Member):
        message = reaction.message
        channel = message.channel
        guild = message.guild
        guild_id = guild.id
        member = message.author
        member_id = member.id
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            cur = await db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            moji = row[0]
            if moji is None:
                moji = "🏅"
            if str(reaction.emoji) == moji:
                cur = await db.execute("SELECT award_react_toggle FROM guilds WHERE guild_id = ?", (guild_id,))
                row = await cur.fetchone()
                toggle = row[0]
                if toggle == 1:
                    cur = await db.execute("SELECT award_singular FROM guilds WHERE guild_id = ?", (guild_id,))
                    row = await cur.fetchone()
                    sing_low = row[0]
                    if sing_low is None:
                        sing_low = "award"
                    sing_cap = sing_low.title()
                    cur = await db.execute("SELECT award_plural FROM guilds WHERE guild_id = ?", (guild_id,))
                    row = await cur.fetchone()
                    plur_low = row[0]
                    if plur_low is None:
                        plur_low = "awards"
                    guild_member_id = int(str(guild_id) + str(member_id))
                    await db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
                    cur = await db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
                    row = await cur.fetchone()
                    current = row[0]
                    if current is None:
                        current = 0
                    if current > 0:
                        new = current - 1
                        await db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (new, guild_member_id))
                        cur = await db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
                        row = await cur.fetchone()
                        new = row[0]
                        if new == 0:
                            embed = discord.Embed(title=f"{moji} {sing_cap} Removed {moji}", description=f"{member.mention} no longer has any awards! ({sing_cap} removed by {user.mention}.)")
                        elif new == 1:
                            embed = discord.Embed(title=f"{moji} {sing_cap} Removed {moji}", description=f"{member.mention} now has {new} {sing_low}! ({sing_cap} removed by {user.mention}.)")
                        else:
                            embed = discord.Embed(title=f"{moji} {sing_cap} Removed {moji}", description=f"{member.mention} now has {new} {plur_low}! ({sing_cap} removed by {user.mention}.)")
                        await channel.send(embed=embed, delete_after=30.0, reference=message)
            await db.commit()
            await db.close()

    @awards.command(name="add")
    async def add(self, ctx: commands.Context, amount: Optional[int], member: Optional[discord.Member]):
        """Adds awards to the command user or another selected member.

        Parameters
        -----------
        amount : int, optional
            Choose the number of awards to add. (Default: 1)
        member : discord.Member, optional
            Choose the member to add the awards to. (Default: Self)
        """
        await ctx.defer(ephemeral=True)
        guild = ctx.guild
        guild_id = guild.id
        if amount is None:
            amount = 1
        if member is None:
            member = ctx.author
        member_id = member.id
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            cur = await db.execute("SELECT award_singular FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            sing_low = row[0]
            if sing_low is None:
                sing_low = "award"
            sing_cap = sing_low.title()
            cur = await db.execute("SELECT award_plural FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            plur_low = row[0]
            if plur_low is None:
                plur_low = "awards"
            plur_cap = plur_low.title()
            cur = await db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            moji = row[0]
            if moji is None:
                moji = "🏅"
            guild_member_id = int(str(guild_id) + str(member_id))
            await db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
            cur = await db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
            row = await cur.fetchone()
            current = row[0]
            if current is None:
                await db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (amount, guild_member_id))
            else:
                new = current + amount
                await db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (new, guild_member_id))
            cur = await db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
            row = await cur.fetchone()
            new = row[0]
            await db.commit()
            await db.close()
        if new == 1:
            embed = discord.Embed(title=f"{moji} {sing_cap} Added {moji}", description=f"{member.mention} now has {new} {sing_low}!")
        else:
            embed = discord.Embed(title=f"{moji} {plur_cap} Added {moji}", description=f"{member.mention} now has {new} {plur_low}!")
        await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)

    @awards.command(name="remove")
    async def remove(self, ctx: commands.Context, amount: Optional[int], member: Optional[discord.Member]):
        """Removes awards from the command user or another selected member.

        Parameters
        -----------
        amount : int, optional
            Choose the number of awards to remove. (Default: 1)
        member : discord.Member, optional
            Choose the member to remove the awards from. (Default: Self)
        """
        await ctx.defer(ephemeral=True)
        guild = ctx.guild
        guild_id = guild.id
        if amount is None:
            amount = 1
        if member is None:
            member = ctx.author
        member_id = member.id
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            cur = await db.execute("SELECT award_singular FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            sing_low = row[0]
            if sing_low is None:
                sing_low = "award"
            cur = await db.execute("SELECT award_plural FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            plur_low = row[0]
            if plur_low is None:
                plur_low = "awards"
            plur_cap = plur_low.title()
            cur = await db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            moji = row[0]
            if moji is None:
                moji = "🏅"
            guild_member_id = int(str(guild_id) + str(member_id))
            await db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
            cur = await db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
            row = await cur.fetchone()
            current = row[0]
            if current is None:
                current = 0
            if current == 0:
                await db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (current, guild_member_id))
                embed = discord.Embed(title=f"❌ Error ❌", description=f"{member.mention} doesn't have any {plur_low}!")
            elif current < amount:
                embed = discord.Embed(title=f"❌ Error ❌", description=f"{member.mention} doesn't have enough {plur_low}!")
            else:
                new = current - amount
                await db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (new, guild_member_id))
                cur = await db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
                row = await cur.fetchone()
                new = row[0]
                if new == 0:
                    embed = discord.Embed(title=f"{moji} {plur_cap} Removed {moji}", description=f"{member.mention} no longer has any {plur_low}!")
                elif new == 1:
                    embed = discord.Embed(title=f"{moji} {plur_cap} Removed {moji}", description=f"{member.mention} now has {new} {sing_low}!")
                else:
                    embed = discord.Embed(title=f"{moji} {plur_cap} Removed {moji}", description=f"{member.mention} now has {new} {plur_low}!")
                await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)
            await db.commit()
            await db.close()

    @awards.command(name="check")
    async def check(self, ctx: commands.Context, member: Optional[discord.Member]):
        """Returns the number of awards that the user or another selected user currently has.

        Parameters
        -----------
        member : discord.Member, optional
            Choose the member that you would like to check the number of awards for. (Default: Self)
        """
        await ctx.defer(ephemeral=True)
        guild = ctx.guild
        guild_id = guild.id
        if member is None:
            member = ctx.author
        member_id = member.id
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            cur = await db.execute("SELECT award_singular FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            sing_low = row[0]
            if sing_low is None:
                sing_low = "award"
            cur = await db.execute("SELECT award_plural FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            plur_low = row[0]
            if plur_low is None:
                plur_low = "awards"
            plur_cap = plur_low.title()
            cur = await db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            moji = row[0]
            if moji is None:
                moji = "🏅"
            guild_member_id = int(str(guild_id) + str(member_id))
            await db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
            cur = await db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
            row = await cur.fetchone()
            amount = row[0]
            if amount is None:
                amount = 0
            if amount == 0:
                await db.execute("INSERT OR IGNORE INTO awards (guild_member_id, amount) VALUES (?,?)", (guild_member_id,0))
                embed = discord.Embed(title=f"{moji} Number of {plur_cap} {moji}", description=f"{member.mention} doesn't have any {plur_low}!")
            elif amount == 1:
                embed = discord.Embed(title=f"{moji} Number of {plur_cap} {moji}", description=f"{member.mention} has {amount} {sing_low}!")
            else:
                embed = discord.Embed(title=f"{moji} Number of {plur_cap} {moji}", description=f"{member.mention} has {amount} {plur_low}!")
            await db.commit()
            await db.close()
        await ctx.send(embed=embed, delete_after=30.0, ephemeral=True)

    @awards.command(name="leaderboard")
    async def leaderboard(self, ctx: commands.Context):
        """Returns the current award leaderboard for the server."""
        await ctx.defer()
        guild = ctx.guild
        guild_id = guild.id
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)", (guild_id,))
            cur = await db.execute("SELECT award_singular FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            sing_low = row[0]
            if sing_low is None:
                sing_low = "award"
            sing_cap = sing_low.title()
            cur = await db.execute("SELECT award_emoji FROM guilds WHERE guild_id = ?", (guild_id,))
            row = await cur.fetchone()
            moji = row[0]
            if moji is None:
                moji = "🏅"
            member_awards = {}
            member_ids = [member.id for member in guild.members if not member.bot]
            for member_id in member_ids:
                guild_member_id = int(str(guild_id) + str(member_id))
                await db.execute("INSERT OR IGNORE INTO awards (guild_member_id) VALUES (?)", (guild_member_id,))
                cur = await db.execute("SELECT amount FROM awards WHERE guild_member_id = ?", (guild_member_id,))
                row = await cur.fetchone()
                amount = row[0]
                if amount is None:
                    await db.execute("UPDATE awards SET amount = ? WHERE guild_member_id = ?", (awards, guild_member_id))
                elif amount > 0:
                    member_awards[member_id] = amount
            await db.commit()
            await db.close()
        desc = []
        for member, awards in dict(sorted(member_awards.items(), key=lambda item: item[1])):
            awards = awards * moji
            desc.append(f"<@{member}>:\n{awards}")
        description = "\n\n".join(x for x in desc)
        embed = discord.Embed(title=f"{moji} {sing_cap} Leaderboard {moji}", description=description)
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
	await bot.add_cog(Awards(bot), override=True)