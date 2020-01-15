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

images = {'ace': 'bundled_data_path(self) / ace.png', 'ally': 'bundled_data_path(self) / ally.png', 'androgenous': 'bundled_data_path(self) / androgenous.png', 'androgyne': 'bundled_data_path(self) / androgyne.png',
          'aromantic': 'bundled_data_path(self) / aromantic.png', 'bdsm': 'bundled_data_path(self) / bdsm.png', 'bear': 'bundled_data_path(self) / bear.png', 'bisexual': 'bundled_data_path(self) / bisexual.png',
          'demisexual': 'bundled_data_path(self) / demisexual.png', 'fat': 'bundled_data_path(self) / fat.png', 'genderfluid': 'bundled_data_path(self) / genderfluid.png',
          'genderqueer': 'bundled_data_path(self) / genderqueer.png', 'gynephilia': 'bundled_data_path(self) / gynephilia.png', 'hermaphrodite': 'bundled_data_path(self) / hermaphrodite.png',
          'intersex': 'bundled_data_path(self) / intersex.png', 'intersex2': 'bundled_data_path(self) / intersex2.png', 'intergender': 'bundled_data_path(self) / intergender.png', 'leather': 'bundled_data_path(self) / leather.png',
          'leathergirl': 'bundled_data_path(self) / leathergirl.png', 'leatherqueer': 'bundled_data_path(self) / leatherqueer.png', 'lesbian': 'bundled_data_path(self) / lesbian.png',
          'lithromantic': 'bundled_data_path(self) / lithromantic.png', 'longhair': 'bundled_data_path(self) / longhair.png', 'neutrois': 'bundled_data_path(self) / neutrois.png',
          'nonbinary': 'bundled_data_path(self) / nonbinary.png', 'ownership': 'bundled_data_path(self) / ownership.png', 'pansexual': 'bundled_data_path(self) / pansexual.png',
          'polyamorous':'bundled_data_path(self) / polyamorous.png', 'polysexual': 'bundled_data_path(self) / polysexual.png','questioning': 'bundled_data_path(self) / questioning.png',  'gay': 'gay.png', 'puppy': 'bundled_data_path(self) / puppy.png', 'rubber': 'bundled_data_path(self) / rubber.png',
          'skoliosexual': 'bundled_data_path(self) / skoliosexual.png', 'straight': 'bundled_data_path(self) / straight.png', 'trans': 'bundled_data_path(self) / trans.png',
          'trigender': 'bundled_data_path(self) / trigender.png', 'twink': 'bundled_data_path(self) / twink.png'}

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
