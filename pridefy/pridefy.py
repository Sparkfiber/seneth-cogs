from redbot.core import commands, checks
from redbot.core.utils import chat_formatting as cf
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from discord import User, File, Embed, Permissions, utils, HTTPException
from PIL import Image
import aiohttp
from random import randint
import os
import functools
import io
import traceback

images = {'ace': '/data/ace.png', 'ally': '/data/ally.png', 'androgenous': '/data/androgenous.png', 'androgyne': '/data/androgyne.png',
          'aromantic': '/data/aromantic.png', 'bdsm': '/data/bdsm.png', 'bear': '/data/bear.png', 'bisexual': '/data/bisexual.png',
          'demisexual': '/data/demisexual.png', 'fat': '/data/fat.png', 'genderfluid': '/data/genderfluid.png',
          'genderqueer': '/data/genderqueer.png', 'gynephilia': '/data/gynephilia.png', 'hermaphrodite': '/data/hermaphrodite.png',
          'intersex': '/data/intersex.png', 'intersex2': '/data/intersex2.png', 'intergender': '/data/intergender.png', 'leather': '/data/leather.png',
          'leathergirl': '/data/leathergirl.png', 'leatherqueer': '/data/leatherqueer.png', 'lesbian': '/data/lesbian.png',
          'lithromantic': '/data/lithromantic.png', 'longhair': '/data/longhair.png', 'neutrois': '/data/neutrois.png',
          'nonbinary': '/data/nonbinary.png', 'ownership': '/data/ownership.png', 'pansexual': '/data/pansexual.png',
          'polyamorous':'/data/polyamorous.png', 'polysexual': '/data/polysexual.png','questioning': '/data/questioning.png',  'gay': 'gay.png', 'puppy': '/data/puppy.png', 'rubber': '/data/rubber.png',
          'skoliosexual': '/data/skoliosexual.png', 'straight': '/data/straight.png', 'trans': '/data/trans.png',
          'trigender': '/data/trigender.png', 'twink': '/data/twink.png'}

actual_images = {}
for key, value in images.items():
	image = Image.open(value)
	actual_images[str(key)] = image.convert("RGBA")

@commands.command()
async def pridefy(ctx, flag="gay", user: User = None):
	flag = flag.lower()
	if flag not in images:
		await ctx.send(f"This is not one of the options use [p]options to see the options. If you are trying to pridefy someone else make sure to put the selected flag first. Example `[p]pridefy gay @pridefy`")
		return
	await ctx.send(f"{ctx.author.mention} starting now. Could take some time...")
	if not user:
		user = ctx.author
	try:
		gif = True
		avatar_url = user.avatar_url_as(format="gif")
	except:
		gif = False
		avatar_url = user.avatar_url_as(format="png")
	try:
		img = await avatar_url.read()

		if not img:
			return

		img = Image.open(io.BytesIO(img))

		func = functools.partial(convert_gif if gif else convert_png, img, flag)

		tempstring = await bot.loop.run_in_executor(None, func)

		await ctx.send(ctx.author.mention, file=File(f"profile{tempstring}.{'gif' if gif else 'png'}"))
	except HTTPException:
		await ctx.send("Image too big to send")
	os.remove(f"profile{tempstring}.{'gif' if gif else 'png'}")


def convert_png(img, type):
	tempstring = randint(0, 10000)
	img = convert_single(img, type)
	img.save(f"profile{tempstring}.png")
	return tempstring


def convert_single(img, type):
	avatar = img.convert("RGBA")
	new = Image.new("RGBA", avatar.size)

	pride_image_resize = actual_images[type].resize(avatar.size, Image.ANTIALIAS)

	new.paste(avatar, (0, 0), avatar)
	new.paste(pride_image_resize, (0, 0), pride_image_resize)
	return new


def convert_gif(gif, type):
	tempstring = randint(0, 10000)

	duration = gif.info["duration"]

	frames = []
	first_frame = 0

	try:
		while True:
			gif.seek(first_frame)
			frames.append(convert_single(gif, type))
			first_frame += 1
	except:
		pass

	frames[0].info["duration"] = duration
	frames[0].save(f"profile{tempstring}.gif", save_all=True, append_images=frames[1:])
	return tempstring
