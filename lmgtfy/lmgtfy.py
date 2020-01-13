from redbot.core import commands, checks
from redbot.core.utils import chat_formatting as cf
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
import aiohttp
import discord
import json
import asyncio
import re
import os
import html
from xml.etree import ElementTree as ET
import random
from random import randint
from random import choice
import operator
import logging

class LMGTFY(commands.Cog):
	"""Let me Google that for you. When someone asks a dumb question they could easily find on Google. """
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def lmgtfy(self, ctx, *text):
		"""Let me just Google that for you..."""

		#Your code will go here
		text = " ".join(text)
		query=text.replace(" ", "%20")
		await ctx.send(embed=discord.Embed(color=ctx.message.author.color,
								title = "Step 1 - Visit google.com"))
		await asyncio.sleep(2)
		await ctx.send(embed=discord.Embed(color=ctx.message.author.color,
								title ="Step 2 - Type:", description=text))
		await asyncio.sleep(2)
		await ctx.send(embed=discord.Embed(color=ctx.message.author.color,
								title ="Step 3 - Click the Button"))
		await asyncio.sleep(2)
		await ctx.send(embed=discord.Embed(color=ctx.message.author.color,
								title ="That's it!", description=" https://www.google.com/search?q="+query))
