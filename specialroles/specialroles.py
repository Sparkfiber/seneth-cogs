from redbot.core import commands, checks
from redbot.core.utils import chat_formatting as cf
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from discord import Object, TextChannel, Member, Embed, Role
import asyncio
from prettytable import PrettyTable
import sqlite3


class SpecialRoles(commands.Cog):
    """Allow anyone with a certain role to give a specific role"""

    def __init__(self, bot):
        self.bot = bot
        con = sqlite3.connect("specialroles.sql")
        self.cur = con.cursor()

    @staticmethod
    def success(description):
        embed = Embed(color=0x2ECC71, title="✅ Success", description=description)
        return embed

    @staticmethod
    def notice(description):
        embed = Embed(color=0xE67E22, title="❕ Notice", description=description)
        return embed

    @staticmethod
    def error(description):
        embed = Embed(color=0xE74C3C, title="⚠ Error", description=description)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            return

        if not message.content:
            return

        ctx = await self.bot.get_context(message)
        if not ctx.prefix:
            return

        try:
            name = message.content.replace(ctx.prefix, "", 1).split()[0]
            if not name:
                return
        except IndexError:
            return

        member_pre_convert = (
            message.content.replace(ctx.prefix, "", 1).replace(name, "", 1).strip()
        )
        try:
            member_to_give = await commands.MemberConverter().convert(
                ctx, member_pre_convert
            )
        except BadArgument:
            return

        query = "SELECT * FROM special_roles WHERE (guild_id = $1) and (name = $2)"
        roles = await self.cur.execute(query, message.guild.id, name)
        if not roles:
            return

        roles_to_add = []
        for role in roles:
            give_role_id = role["give_role_id"]
            give_role = message.guild.get_role(give_role_id)
            if not give_role:
                continue
            if give_role not in message.author.roles:
                continue

            applied_role_id = role["applied_role_id"]
            role = message.guild.get_role(applied_role_id)
            if not role:
                continue
            roles_to_add.append(role)

        if not roles_to_add:
            return
        await member_to_give.add_roles(*roles_to_add)
        fmt = ",".join(role.name for role in roles_to_add)
        await ctx.send(embed=self.success(f"{member_to_give.name} given {fmt}"))

    @commands.command()
    @checks.is_owner()
    @commands.guild_only()
    async def builddatabase(self, ctx):
        """Build the sql database for role commands."""
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS special_roles (guild_id BIGINT, name TEXT, applied_role_id BIGINT, give_role_id BIGINT)"
        )
        await ctx.send(embed=self.success("Woot!"))

    @commands.command(
        aliases=["remove_special_role", "special_role_delete", "special_role_remove"]
    )
    @checks.admin_or_permissions(manage_guild=True)
    @commands.guild_only()
    async def delete_special_role(self, ctx, name):
        """Remove a special role"""
        query = "DELETE FROM special_roles WHERE (guild_id = $1) and (name = $2)"
        await self.cur.execute.fetchall(query, ctx.guild.id, name)
        await ctx.send(
            embed=self.success(f"Any special roles names {name} were deleted")
        )

    @commands.command(aliases=["special_roles", "special_roles_view"])
    @checks.admin_or_permissions(manage_guild=True)
    @commands.guild_only()
    async def view_special_roles(self, ctx):
        """View all special roles"""
        query = "SELECT * FROM special_roles WHERE guild_id = $1"
        roles = await self.cur.execute.fetchall(query, ctx.guild.id)
        if not roles:
            await ctx.send(embed=self.error("No special roles for this guild"))
            return

        table = PrettyTable(field_names=["Name", "Role To Apply", "Role Able To Give"])
        for role in roles:
            name = role["name"]

            applied_role = ctx.guild.get_role(role["applied_role_id"])
            if not applied_role:
                applied_role = "Deleted Role"
            else:
                applied_role = applied_role.name

            give_role = ctx.guild.get_role(role["give_role_id"])
            if not give_role:
                give_role = "Deleted Role"
            else:
                give_role = give_role.name

            table.add_row([name, applied_role, give_role])
        embed = Embed(
            title=f"Special Roles for {ctx.guild.name}", description=f"```{table}```"
        )
        await ctx.send(embed=embed)

    @commands.command(
        aliases=["add_special_role", "special_role_add", "special_role_create"]
    )
    @checks.admin_or_permissions(manage_guild=True)
    @commands.guild_only()
    async def create_special_role(
        self,
        ctx,
        name=None,
        role_to_be_applied: Role = None,
        able_to_give_role: Role = None,
    ):
        """Open a wizard to create special roles"""

        def check(message):
            return (message.channel is ctx.channel) and (message.author is ctx.author)

        try:
            if not name:
                await ctx.send(
                    embed=self.notice(
                        "What would you like the name of the special role ot be?\nThis "
                        "name will be used to give the role. For example if the name is `under18` the "
                        f"role will then be given with the command `{ctx.prefix}under18`"
                    )
                )
                name_message = await self.bot.wait_for(
                    "message", check=check, timeout=60.0
                )
                name = name_message.content
            while not role_to_be_applied:
                await ctx.send(
                    embed=self.notice(
                        f"Mention the role you would like to be applied when the command {ctx.prefix}{name}"
                        " is executed"
                    )
                )
                role_message = await self.bot.wait_for(
                    "message", check=check, timeout=60.0
                )
                if role_message.role_mentions:
                    role_to_be_applied = role_message.role_mentions[0]
                else:
                    await ctx.send(embed=self.error("No roles were mentioned"))
            while not able_to_give_role:
                await ctx.send(
                    embed=self.notice(
                        f"Mention the role you would like to able to give {role_to_be_applied.mention} when {ctx.prefix}{name}"
                        " is executed"
                    )
                )
                role_message = await self.bot.wait_for(
                    "message", check=check, timeout=60.0
                )
                if role_message.role_mentions:
                    able_to_give_role = role_message.role_mentions[0]
                else:
                    await ctx.send(embed=self.error("No roles were mentioned"))
        except asyncio.TimeoutError:
            return
        guild = ctx.guild
        applyrole = role_to_be_applied.id
        givingrole = able_to_give_role.id

        await self.cur.execute(
            "INSERT INTO special_roles (guild_id, name, applied_role_id, give_role_id) VALUES (?,?,?,?,)",
            (guild, name, applyrole, givingrole,)
        )

        await ctx.send(
            embed=self.success(
                f"Speical role made. Example usage {ctx.prefix}{name} {ctx.me.mention}"
            )
        )
