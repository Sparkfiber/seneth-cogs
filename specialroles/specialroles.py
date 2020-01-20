from redbot.core import commands, checks
from redbot.core.utils import chat_formatting as cf
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from discord import Object, TextChannel, Member, Embed, Role
import asyncio


class SpecialRoles(commands.Cog):
	"""Allow anyone with a certain role to give a specific role"""

	def __init__(self, bot):
		self.bot = bot
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
	async def on_reaction_add(self, reaction, user):
		if reaction.emoji != "➕":
			return
		if reaction.message.guild.id != 250309924096049164:
			return
		proxy_ctx = Object(id=None)
		proxy_ctx.guild = reaction.message.guild
		proxy_ctx.author = user
		proxy_ctx.bot = self.bot
		if not await checks.has_level(proxy_ctx, "mod"):
			return
		agerole = self.guild.get_role(398292634935754764)
		famrole = self.guild.get_role(252491587249111050)
		await reaction.message.author.add_roles(agerole)
		await reaction.message.author.add_roles(famrole)
		await proxy_ctx.send(embed=self.notice("Added <@398292634935754764> and <@252491587249111050>"))

	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):
		if reaction.emoji != "➖":
			return
		if reaction.message.guild.id != 250309924096049164:
			return
		proxy_ctx = Object(id=None)
		proxy_ctx.guild = reaction.message.guild
		proxy_ctx.author = user
		proxy_ctx.bot = self.bot
		if not await checks.has_level(proxy_ctx, "mod"):
			return
		agerole = self.guild.get_role(428207167405817856)
		famrole = self.guild.get_role(252491587249111050)
		await reaction.message.author.add_roles(agerole)
		await reaction.message.author.add_roles(famrole)
		await proxy_ctx.send(embed=self.notice("Added <@428207167405817856> and <@252491587249111050>"))
