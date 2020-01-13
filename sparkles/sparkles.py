import discord
from redbot.core import commands, checks
from redbot.core.utils import chat_formatting as cf
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
import datetime
import random

class Sparkles(commands.Cog):
    """Rates users sparkliness. 157% accurate!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sparkles(self, ctx, user):
        """Rates users sparkliness. 157% accurate!"""

        random.seed(int(ctx.message.mentions[0].id) % int(ctx.message.created_at.timestamp()),)
        x = random.randint(1, 10)
        y = ":sparkles:" *  x
        await ctx.send("{} gets a solid ** {}/10 ** \n {}".format(ctx.message.mentions[0].name, x, y))
