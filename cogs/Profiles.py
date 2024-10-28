import discord
import aiosqlite
from discord.ext import commands
from datetime import datetime, timezone
from typing import Optional

class Profiles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.blurple = discord.Colour.blurple()
        self.red = discord.Colour.red()
    
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
        try:
            async with aiosqlite.connect('rainbowbot.db') as db:
                guild = ctx.guild
                if member is None:
                    member = ctx.author
                member_id = member.id
                joined = discord.utils.format_dt(member.joined_at, style="D")
                joinedago = discord.utils.format_dt(member.joined_at, style="R")
                profile = discord.Embed(color=member.accent_color, title=f"{member.display_name}'s Member Profile", description=f"Member of {guild.name} since {joined} ({joinedago}).")
                profile.set_author(name=f"{member.display_name}", icon_url=f"{member.display_avatar}")
                await db.execute("INSERT OR IGNORE INTO members (member_id) VALUES (?)", (member_id,))

                # Set and retrieve the member's name
                if name is not None:
                    await db.execute("UPDATE members SET name = ? WHERE member_id = ?", (name, member_id))
                cur = await db.execute("SELECT name FROM members WHERE member_id = ?", (member_id,))
                row = await cur.fetchone()
                fetched_name = row[0]
                if fetched_name is not None:
                    profile.add_field(name="🏷️ Name", value=f"{fetched_name}", inline=True)
                
                # Set and retrieve the member's age
                if age is not None:
                    await db.execute("UPDATE members SET age = ? WHERE member_id = ?", (age, member_id))
                cur = await db.execute("SELECT age FROM members WHERE member_id = ?", (member_id,))
                row = await cur.fetchone()
                fetched_age = row[0]
                if fetched_age is not None:
                    profile.add_field(name="🏷️ Age", value=f"{fetched_age}", inline=True)
                
                # Set and retrieve the member's location
                if location is not None:
                    await db.execute("UPDATE members SET location = ? WHERE member_id = ?", (location, member_id))
                cur = await db.execute("SELECT location FROM members WHERE member_id = ?", (member_id,))
                row = await cur.fetchone()
                fetched_location = row[0]
                if fetched_location is not None:
                    profile.add_field(name="🏷️ Location", value=f"{fetched_location}", inline=True)
                
                # Set and retrieve the member's pronouns
                if pronouns is not None:
                    await db.execute("UPDATE members SET pronouns = ? WHERE member_id = ?", (pronouns, member_id))
                cur = await db.execute("SELECT pronouns FROM members WHERE member_id = ?", (member_id,))
                row = await cur.fetchone()
                fetched_pronouns = row[0]
                if fetched_pronouns is not None:
                    profile.add_field(name="🏷️ Pronouns", value=f"{fetched_pronouns}", inline=True)
                
                # Set and retrieve the member's gender
                if gender is not None:
                    await db.execute("UPDATE members SET gender = ? WHERE member_id = ?", (gender, member_id))
                cur = await db.execute("SELECT gender FROM members WHERE member_id = ?", (member_id,))
                row = await cur.fetchone()
                fetched_gender = row[0]
                if fetched_gender is not None:
                    profile.add_field(name="🏷️ Gender", value=f"{fetched_gender}", inline=True)
                
                # Set and retrieve the member's sexuality
                if sexuality is not None:
                    await db.execute("UPDATE members SET sexuality = ? WHERE member_id = ?", (sexuality, member_id))
                cur = await db.execute("SELECT sexuality FROM members WHERE member_id = ?", (member_id,))
                row = await cur.fetchone()
                fetched_sexuality = row[0]
                if fetched_sexuality is not None:
                    profile.add_field(name="🏷️ Sexuality", value=f"{fetched_sexuality}", inline=True)
                
                # Set and retrieve the member's relationship status
                if relationship_status is not None:
                    await db.execute("UPDATE members SET relationship_status = ? WHERE member_id = ?", (relationship_status, member_id))
                cur = await db.execute("SELECT relationship_status FROM members WHERE member_id = ?", (member_id,))
                row = await cur.fetchone()
                fetched_relationship_status = row[0]
                if fetched_relationship_status is not None:
                    profile.add_field(name="📝 Relationship Status", value=f"{fetched_relationship_status}", inline=True)
                
                # Set and retrieve the member's family planning status
                if family_status is not None:
                    await db.execute("UPDATE members SET family_status = ? WHERE member_id = ?", (family_status, member_id))
                cur = await db.execute("SELECT family_status FROM members WHERE member_id = ?", (member_id,))
                row = await cur.fetchone()
                fetched_family_status = row[0]
                if fetched_family_status is not None:
                    profile.add_field(name="📝 Family Planning Status", value=f"{fetched_family_status}", inline=True)
                
                # Set and retrieve the member's biography
                if biography is not None:
                    await db.execute("UPDATE members SET biography = ? WHERE member_id = ?", (biography, member_id))
                cur = await db.execute("SELECT biography FROM members WHERE member_id = ?", (member_id,))
                row = await cur.fetchone()
                fetched_biography = row[0]
                if fetched_biography is not None:
                    profile.add_field(name="📝 Biography", value=f"{fetched_biography}", inline=False)
                
                # Retrieve the member's roles
                roles = []
                for role in member.roles:
                    if role.name != "@everyone":
                        roles.append(role)
                if len(roles) > 0:
                    roles = ", ".join(roles)
                    profile.add_field(name="📝 Roles", value=f"{roles}", inline=False)
                
                # Send the message
                await ctx.send(embed=profile, ephemeral=True)

                # Send a log to the logging channel, if one is set
                cur = await db.execute("SELECT logging_channel_id FROM guilds WHERE guild_id = ?", (guild.id,))
                row = await cur.fetchone()
                fetched_logging = row[0]
                if fetched_logging is not None:
                    logging_channel = await guild.fetch_channel(fetched_logging)
                    timestamp = datetime.now(tz=timezone.utc)
                    log = discord.Embed(color=self.blurple, title="Profile Log", description=f"{member.mention} has just set their profile!", timestamp=timestamp)
                    log.set_author(name=member.display_name, icon_url=member.display_avatar)
                    await logging_channel.send(embed=log)
                
                await db.commit()
                await db.close()
        
        # Send an error message if there's an issue
        except Exception as e:
            error = discord.Embed(color=self.red, title="Error", description=f"{e}")
            await ctx.send(embed=error, ephemeral=True)

    @profile.command(name="get")
    async def get(self, ctx: commands.Context, member: Optional[discord.Member]):
        """Run this command to retrieve a member's profile.

        Parameters
        -----------
        member : str, optional
            Provide the member whose profile you would like to retrieve.
        """
        await ctx.defer(ephemeral=True)
        try:
            async with aiosqlite.connect('rainbowbot.db') as db:
                guild = ctx.guild
                if member is None:
                    member = ctx.author
                member_id = member.id
                joined = discord.utils.format_dt(member.joined_at, style="D")
                joinedago = discord.utils.format_dt(member.joined_at, style="R")
                profile = discord.Embed(color=member.accent_color, title=f"{member.display_name}'s Member Profile", description=f"Member of {guild.name} since {joined} ({joinedago}).")
                profile.set_author(name=f"{member.display_name}", icon_url=f"{member.display_avatar}")
                await db.execute("INSERT OR IGNORE INTO members (member_id) VALUES (?)", (member_id,))

                # Retrieve the member's name
                cur = await db.execute("SELECT name FROM members WHERE member_id = ?", (member_id,))
                row = await cur.fetchone()
                fetched_name = row[0]
                if fetched_name is not None:
                    profile.add_field(name="🏷️ Name", value=f"{fetched_name}", inline=True)
                
                # Retrieve the member's age
                cur = await db.execute("SELECT age FROM members WHERE member_id = ?", (member_id,))
                row = await cur.fetchone()
                fetched_age = row[0]
                if fetched_age is not None:
                    profile.add_field(name="🏷️ Age", value=f"{fetched_age}", inline=True)
                
                # Retrieve the member's location
                cur = await db.execute("SELECT location FROM members WHERE member_id = ?", (member_id,))
                row = await cur.fetchone()
                fetched_location = row[0]
                if fetched_location is not None:
                    profile.add_field(name="🏷️ Location", value=f"{fetched_location}", inline=True)
                
                # Retrieve the member's pronouns
                cur = await db.execute("SELECT pronouns FROM members WHERE member_id = ?", (member_id,))
                row = await cur.fetchone()
                fetched_pronouns = row[0]
                if fetched_pronouns is not None:
                    profile.add_field(name="🏷️ Pronouns", value=f"{fetched_pronouns}", inline=True)
                
                # Retrieve the member's gender
                cur = await db.execute("SELECT gender FROM members WHERE member_id = ?", (member_id,))
                row = await cur.fetchone()
                fetched_gender = row[0]
                if fetched_gender is not None:
                    profile.add_field(name="🏷️ Gender", value=f"{fetched_gender}", inline=True)
                
                # Retrieve the member's sexuality
                cur = await db.execute("SELECT sexuality FROM members WHERE member_id = ?", (member_id,))
                row = await cur.fetchone()
                fetched_sexuality = row[0]
                if fetched_sexuality is not None:
                    profile.add_field(name="🏷️ Sexuality", value=f"{fetched_sexuality}", inline=True)
                
                # Retrieve the member's relationship status
                cur = await db.execute("SELECT relationship_status FROM members WHERE member_id = ?", (member_id,))
                row = await cur.fetchone()
                fetched_relationship_status = row[0]
                if fetched_relationship_status is not None:
                    profile.add_field(name="📝 Relationship Status", value=f"{fetched_relationship_status}", inline=True)
                
                # Retrieve the member's family planning status
                cur = await db.execute("SELECT family_status FROM members WHERE member_id = ?", (member_id,))
                row = await cur.fetchone()
                fetched_family_status = row[0]
                if fetched_family_status is not None:
                    profile.add_field(name="📝 Family Planning Status", value=f"{fetched_family_status}", inline=True)
                
                # Retrieve the member's biography
                cur = await db.execute("SELECT biography FROM members WHERE member_id = ?", (member_id,))
                row = await cur.fetchone()
                fetched_biography = row[0]
                if fetched_biography is not None:
                    profile.add_field(name="📝 Biography", value=f"{fetched_biography}", inline=False)
                
                # Retrieve the member's roles
                roles = []
                for role in member.roles:
                    if role.name != "@everyone":
                        roles.append(role)
                if len(roles) > 0:
                    roles = ", ".join(roles)
                    profile.add_field(name="📝 Roles", value=f"{roles}", inline=False)
                
                # Send the message
                await ctx.send(embed=profile, ephemeral=True)

                await db.commit()
                await db.close()
        
        # Send an error message if there's an issue
        except Exception as e:
            error = discord.Embed(color=self.red, title="Error", description=f"{e}")
            await ctx.send(embed=error, ephemeral=True)

async def setup(bot: commands.Bot):
    async with aiosqlite.connect('rainbowbot.db') as db:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS "members"(
                member_id           INTEGER,
                name                TEXT DEFAULT NULL,
                age                 TEXT DEFAULT NULL,
                location            TEXT DEFAULT NULL,
                pronouns            TEXT DEFAULT NULL,
                gender              TEXT DEFAULT NULL,
                sexuality           TEXT DEFAULT NULL,
                relationship_status TEXT DEFAULT NULL,
                family_status       TEXT DEFAULT NULL,
                biography           TEXT DEFAULT NULL,
                PRIMARY KEY("member_id")
            )"""
        )
        await db.commit()
        await db.close()