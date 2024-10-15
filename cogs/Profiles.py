import discord
from discord.ext import commands
from typing import Optional
import aiosqlite

class Profiles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.hybrid_group(name="profile", fallback="set")
    async def profile(self, ctx: commands.Context, name: Optional[str], age: Optional[str], location: Optional[str], pronouns: Optional[str], gender: Optional[str], sexuality: Optional[str], relationship_status: Optional[str], family_status: Optional[str], biography: Optional[str]):
        """Run this command to set up your member profile. Note that all fields are optional.

        Parameters
        -----------
        name : str, optional
            Provide your name or nickname.
        age : str, optional
            Provide your age or age range.
        location : str, optional
            Provide your continent, country, state, or city of residence.
        pronouns : str, optional
            Provide your pronouns (ex. she/her, he/him, they/them, etc).
        gender : str, optional
            Provide your gender identity label (ex. woman, man, nonbinary, etc).
        sexuality : str, optional
            Provide your sexuality label (ex. lesbian, gay, bisexual, etc).
        relationship_status : str, optional
            Provide your relationship status (ex. single, married, etc).
        family_status : str, optional
            Provide your your family planning status (ex. TTC, expecting, parenting, etc).
        biography : str, optional
            Provide a brief biography (ex. family, hobbies, interests, work, etc).
        """
        await ctx.defer(ephemeral=True)
        guild = ctx.guild
        member = ctx.author
        member_id = int(member.id)
        joined = discord.utils.format_dt(member.joined_at, style="D")
        joinedago = discord.utils.format_dt(member.joined_at, style="R")
        embed = discord.Embed(color=member.accent_color, title=f"{member.name}'s Member Profile", description=f"Member of {guild.name} since {joined} ({joinedago}).")
        if member.avatar is not None:
            embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar}")
        else:
            embed.set_author(name=f"{member.name}")
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO members (member_id) VALUES (?)", (member_id,))
            if name is not None:
                await db.execute("UPDATE members SET name = ? WHERE member_id = ?", (name, member_id))
            cur = await db.execute("SELECT name FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_name = row[0]
            if fetched_name is not None:
                embed.add_field(name="🏷️ Name", value=f"{fetched_name}", inline=True)
            if age is not None:
                await db.execute("UPDATE members SET age = ? WHERE member_id = ?", (age, member_id))
            cur = await db.execute("SELECT age FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_age = row[0]
            if fetched_age is not None:
                embed.add_field(name="🏷️ Age", value=f"{fetched_age}", inline=True)
            if location is not None:
                await db.execute("UPDATE members SET location = ? WHERE member_id = ?", (location, member_id))
            cur = await db.execute("SELECT location FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_location = row[0]
            if fetched_location is not None:
                embed.add_field(name="🏷️ Location", value=f"{fetched_location}", inline=True)
            if pronouns is not None:
                await db.execute("UPDATE members SET pronouns = ? WHERE member_id = ?", (pronouns, member_id))
            cur = await db.execute("SELECT pronouns FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_pronouns = row[0]
            if fetched_pronouns is not None:
                embed.add_field(name="🏷️ Pronouns", value=f"{fetched_pronouns}", inline=True)
            if gender is not None:
                await db.execute("UPDATE members SET gender = ? WHERE member_id = ?", (gender, member_id))
            cur = await db.execute("SELECT gender FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_gender = row[0]
            if fetched_gender is not None:
                embed.add_field(name="🏷️ Gender", value=f"{fetched_gender}", inline=True)
            if sexuality is not None:
                await db.execute("UPDATE members SET sexuality = ? WHERE member_id = ?", (sexuality, member_id))
            cur = await db.execute("SELECT sexuality FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_sexuality = row[0]
            if fetched_sexuality is not None:
                embed.add_field(name="🏷️ Sexuality", value=f"{fetched_sexuality}", inline=True)
            if relationship_status is not None:
                await db.execute("UPDATE members SET relationship_status = ? WHERE member_id = ?", (relationship_status, member_id))
            cur = await db.execute("SELECT relationship_status FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_relationship_status = row[0]
            if fetched_relationship_status is not None:
                embed.add_field(name="📝 Relationship Status", value=f"{fetched_relationship_status}", inline=True)
            if family_status is not None:
                await db.execute("UPDATE members SET family_status = ? WHERE member_id = ?", (family_status, member_id))
            cur = await db.execute("SELECT family_status FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_family_status = row[0]
            if fetched_family_status is not None:
                embed.add_field(name="📝 Family Planning Status", value=f"{fetched_family_status}", inline=True)
            if biography is not None:
                await db.execute("UPDATE members SET biography = ? WHERE member_id = ?", (biography, member_id))
            cur = await db.execute("SELECT biography FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_biography = row[0]
            if fetched_biography is not None:
                embed.add_field(name="📝 Biography", value=f"{fetched_biography}", inline=False)
            await db.commit()
            await db.close()
        roles = [r.mention for r in member.roles]
        roles = ", ".join(roles)
        embed.add_field(name="📝 Roles", value=f"{roles}", inline=False)
        await ctx.send(embed=embed, delete_after=60.0, ephemeral=True)

    @profile.command(name="name")
    async def name(self, ctx: commands.Context, name: str):
        """Run this command to set or update your profile name.

        Parameters
        -----------
        name : str
            Provide your name or nickname.
        """
        await ctx.defer(ephemeral=True)
        member = ctx.author
        member_id = int(ctx.author.id)
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO members (member_id) VALUES (?)", (member_id,))
            await db.execute("UPDATE members SET name = ? WHERE member_id = ?", (name, member_id))
            cur = await db.execute("SELECT name FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_name = row[0]
            await db.commit()
            await db.close()
        if fetched_name is not None:
            embed = discord.Embed(color=member.accent_color, title="✔️ Success ✔️", description=f"Your profile name is now set to: {fetched_name}")
        else:
            embed = discord.Embed(color=member.accent_color, title="❌ Error ❌", description="There was an error! Try again later.")
        await ctx.send(embed=embed, delete_after=60.0, ephemeral=True)

    @profile.command(name="age")
    async def age(self, ctx: commands.Context, age: str):
        """Run this command to set or update your profile age.

        Parameters
        -----------
        age : str
            Provide your age or age range.
        """
        await ctx.defer(ephemeral=True)
        member = ctx.author
        member_id = int(ctx.author.id)
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO members (member_id) VALUES (?)", (member_id,))
            await db.execute("UPDATE members SET age = ? WHERE member_id = ?", (age, member_id))
            cur = await db.execute("SELECT age FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_age = row[0]
            await db.commit()
            await db.close()
        if fetched_age is not None:
            embed = discord.Embed(color=member.accent_color, title="✔️ Success ✔️", description=f"Your profile age is now set to: {fetched_age}")
        else:
            embed = discord.Embed(color=member.accent_color, title="❌ Error ❌", description="There was an error! Try again later.")
        await ctx.send(embed=embed, delete_after=60.0, ephemeral=True)

    @profile.command(name="location")
    async def location(self, ctx: commands.Context, location: str):
        """Run this command to set or update your profile location.

        Parameters
        -----------
        location : str
            Provide your continent, country, state, or city of residence.
        """
        await ctx.defer(ephemeral=True)
        member = ctx.author
        member_id = int(ctx.author.id)
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO members (member_id) VALUES (?)", (member_id,))
            await db.execute("UPDATE members SET location = ? WHERE member_id = ?", (location, member_id))
            cur = await db.execute("SELECT location FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_location = row[0]
            await db.commit()
            await db.close()
        if fetched_location is not None:
            embed = discord.Embed(color=member.accent_color, title="✔️ Success ✔️", description=f"Your profile location is now set to: {fetched_location}")
        else:
            embed = discord.Embed(color=member.accent_color, title="❌ Error ❌", description="There was an error! Try again later.")
        await ctx.send(embed=embed, delete_after=60.0, ephemeral=True)

    @profile.command(name="pronouns")
    async def pronouns(self, ctx: commands.Context, pronouns: str):
        """Run this command to set or update your profile pronouns.

        Parameters
        -----------
        pronouns : str
            Provide your pronouns (ex. she/her, he/him, they/them, etc).
        """
        await ctx.defer(ephemeral=True)
        member = ctx.author
        member_id = int(ctx.author.id)
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO members (member_id) VALUES (?)", (member_id,))
            await db.execute("UPDATE members SET pronouns = ? WHERE member_id = ?", (pronouns, member_id))
            cur = await db.execute("SELECT pronouns FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_pronouns = row[0]
            await db.commit()
            await db.close()
        if fetched_pronouns is not None:
            embed = discord.Embed(color=member.accent_color, title="✔️ Success ✔️", description=f"Your profile pronouns are now set to: {fetched_pronouns}")
        else:
            embed = discord.Embed(color=member.accent_color, title="❌ Error ❌", description="There was an error! Try again later.")
        await ctx.send(embed=embed, delete_after=60.0, ephemeral=True)

    @profile.command(name="gender")
    async def gender(self, ctx: commands.Context, gender: str):
        """Run this command to set or update your profile gender.

        Parameters
        -----------
        gender : str
            Provide your gender identity label (ex. woman, man, nonbinary, etc).
        """
        await ctx.defer(ephemeral=True)
        member = ctx.author
        member_id = int(ctx.author.id)
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO members (member_id) VALUES (?)", (member_id,))
            await db.execute("UPDATE members SET gender = ? WHERE member_id = ?", (gender, member_id))
            cur = await db.execute("SELECT gender FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_gender = row[0]
            await db.commit()
            await db.close()
        if fetched_gender is not None:
            embed = discord.Embed(color=member.accent_color, title="✔️ Success ✔️", description=f"Your profile gender is now set to: {fetched_gender}")
        else:
            embed = discord.Embed(color=member.accent_color, title="❌ Error ❌", description="There was an error! Try again later.")
        await ctx.send(embed=embed, delete_after=60.0, ephemeral=True)

    @profile.command(name="sexuality")
    async def sexuality(self, ctx: commands.Context, sexuality: str):
        """Run this command to set or update your profile sexuality.

        Parameters
        -----------
        sexuality : str
            Provide your sexuality label (ex. lesbian, gay, bisexual, etc).
        """
        await ctx.defer(ephemeral=True)
        member = ctx.author
        member_id = int(ctx.author.id)
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO members (member_id) VALUES (?)", (member_id,))
            await db.execute("UPDATE members SET sexuality = ? WHERE member_id = ?", (sexuality, member_id))
            cur = await db.execute("SELECT sexuality FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_sexuality = row[0]
            await db.commit()
            await db.close()
        if fetched_sexuality is not None:
            embed = discord.Embed(color=member.accent_color, title="✔️ Success ✔️", description=f"Your profile sexuality is now set to: {fetched_sexuality}")
        else:
            embed = discord.Embed(color=member.accent_color, title="❌ Error ❌", description="There was an error! Try again later.")
        await ctx.send(embed=embed, delete_after=60.0, ephemeral=True)

    @profile.command(name="relationship")
    async def relationship(self, ctx: commands.Context, relationship_status: str):
        """Run this command to set or update your profile relationship status.

        Parameters
        -----------
        relationship_status : str
            Provide your relationship status (ex. single, married, etc).
        """
        await ctx.defer(ephemeral=True)
        member = ctx.author
        member_id = int(ctx.author.id)
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO members (member_id) VALUES (?)", (member_id,))
            await db.execute("UPDATE members SET relationship_status = ? WHERE member_id = ?", (relationship_status, member_id))
            cur = await db.execute("SELECT relationship_status FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_relationship_status = row[0]
            await db.commit()
            await db.close()
        if fetched_relationship_status is not None:
            embed = discord.Embed(color=member.accent_color, title="✔️ Success ✔️", description=f"Your profile relationship status is now set to: {fetched_relationship_status}")
        else:
            embed = discord.Embed(color=member.accent_color, title="❌ Error ❌", description="There was an error! Try again later.")
        await ctx.send(embed=embed, delete_after=60.0, ephemeral=True)

    @profile.command(name="family")
    async def family(self, ctx: commands.Context, family_status: str):
        """Run this command to set or update your profile family planning status.

        Parameters
        -----------
        family_status : str
            Provide your your family planning status (ex. TTC, expecting, parenting, etc).
        """
        await ctx.defer(ephemeral=True)
        member = ctx.author
        member_id = int(ctx.author.id)
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO members (member_id) VALUES (?)", (member_id,))
            await db.execute("UPDATE members SET family_status = ? WHERE member_id = ?", (family_status, member_id))
            cur = await db.execute("SELECT family_status FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_family_status = row[0]
            await db.commit()
            await db.close()
        if fetched_family_status is not None:
            embed = discord.Embed(color=member.accent_color, title="✔️ Success ✔️", description=f"Your profile family planning status is now set to: {fetched_family_status}")
        else:
            embed = discord.Embed(color=member.accent_color, title="❌ Error ❌", description="There was an error! Try again later.")
        await ctx.send(embed=embed, delete_after=60.0, ephemeral=True)

    @profile.command(name="biography")
    async def biography(self, ctx: commands.Context, biography: str):
        """Run this command to set or update your profile biography.

        Parameters
        -----------
        biography : str
            Provide a brief biography (ex. family, hobbies, interests, work, etc).
        """
        await ctx.defer(ephemeral=True)
        member = ctx.author
        member_id = int(ctx.author.id)
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO members (member_id) VALUES (?)", (member_id,))
            await db.execute("UPDATE members SET biography = ? WHERE member_id = ?", (biography, member_id))
            cur = await db.execute("SELECT biography FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_biography = row[0]
            await db.commit()
            await db.close()
        if fetched_biography is not None:
            embed = discord.Embed(color=member.accent_color, title="✔️ Success ✔️", description=f"Your profile biography is now set to: {fetched_biography}")
        else:
            embed = discord.Embed(color=member.accent_color, title="❌ Error ❌", description="There was an error! Try again later.")
        await ctx.send(embed=embed, delete_after=60.0, ephemeral=True)

    @profile.command(name="get")
    async def get(self, ctx: commands.Context, member: Optional[discord.Member]):
        """Run this command to retrieve a member's profile.

        Parameters
        -----------
        member : str, optional
            Provide the member whose profile you would like to retrieve.
        """
        await ctx.defer(ephemeral=True)
        guild = ctx.guild
        if member is None:
            member = ctx.author
        member_id = int(member.id)
        joined = discord.utils.format_dt(member.joined_at, style="D")
        joinedago = discord.utils.format_dt(member.joined_at, style="R")
        embed = discord.Embed(color=member.accent_color, title=f"{member.name}'s Member Profile", description=f"Member of {guild.name} since {joined} ({joinedago}).")
        if member.avatar is not None:
            embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar}")
        else:
            embed.set_author(name=f"{member.name}")
        async with aiosqlite.connect('rainbowbot.db') as db:
            await db.execute("INSERT OR IGNORE INTO members (member_id) VALUES (?)", (member_id,))
            cur = await db.execute("SELECT name FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_name = row[0]
            if fetched_name is not None:
                embed.add_field(name="🏷️ Name", value=f"{fetched_name}", inline=True)
            cur = await db.execute("SELECT age FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_age = row[0]
            if fetched_age is not None:
                embed.add_field(name="🏷️ Age", value=f"{fetched_age}", inline=True)
            cur = await db.execute("SELECT location FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_location = row[0]
            if fetched_location is not None:
                embed.add_field(name="🏷️ Location", value=f"{fetched_location}", inline=True)
            cur = await db.execute("SELECT pronouns FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_pronouns = row[0]
            if fetched_pronouns is not None:
                embed.add_field(name="🏷️ Pronouns", value=f"{fetched_pronouns}", inline=True)
            cur = await db.execute("SELECT gender FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_gender = row[0]
            if fetched_gender is not None:
                embed.add_field(name="🏷️ Gender", value=f"{fetched_gender}", inline=True)
            cur = await db.execute("SELECT sexuality FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_sexuality = row[0]
            if fetched_sexuality is not None:
                embed.add_field(name="🏷️ Sexuality", value=f"{fetched_sexuality}", inline=True)
            cur = await db.execute("SELECT relationship_status FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_relationship_status = row[0]
            if fetched_relationship_status is not None:
                embed.add_field(name="📝 Relationship Status", value=f"{fetched_relationship_status}", inline=True)
            cur = await db.execute("SELECT family_status FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_family_status = row[0]
            if fetched_family_status is not None:
                embed.add_field(name="📝 Family Planning Status", value=f"{fetched_family_status}", inline=True)
            cur = await db.execute("SELECT biography FROM members WHERE member_id = ?", (member_id,))
            row = await cur.fetchone()
            fetched_biography = row[0]
            if fetched_biography is not None:
                embed.add_field(name="📝 Biography", value=f"{fetched_biography}", inline=False)
            await db.commit()
            await db.close()
        roles = [r.mention for r in member.roles]
        roles = ", ".join(roles)
        embed.add_field(name="📝 Roles", value=f"{roles}", inline=False)
        await ctx.send(embed=embed, delete_after=60.0, ephemeral=True)

async def setup(bot: commands.Bot):
	await bot.add_cog(Profiles(bot), override=True)