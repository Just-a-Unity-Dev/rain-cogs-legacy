from redbot.core import commands, Config, checks
import discord
import random

class RainCogs(commands.Cog):
	"""multipurpose cog"""

	def __init__(self, bot) -> None:
		self.bot = bot
		self.config = Config.get_conf(self, 23975432657)
		default_guild = {
			"blessrole": None
		}
		self.config.register_guild(**default_guild)

	@commands.group()
	async def rain(self, ctx: commands.Context) -> None:
		"""
		it's a cold cog, afterall.
		"""
		pass

	@rain.group()
	@checks.admin_or_permissions(manage_guild=True)
	async def config(self, ctx: commands.Context) -> None:
		"""
		configuration for rain cogs
		"""
		pass

	@rain.group()
	async def manifest(self, ctx: commands.Context) -> None:
		await ctx.reply(content="my physical manifestation... a plushie!", file=discord.File(r"./rain.png"))

	@config.command(name="blessrole")
	async def config_blessrole(self, ctx: commands.Context, blessRole) -> None:
		"""set the bless role (role id)"""
		if blessRole is None:
			await self.config.guild(ctx.guild).blessrole.set(None)
			return await ctx.reply("Reset the value of `blessrole` to `None`")
		await self.config.guild(ctx.guild).blessrole.set(int(blessRole))
		await ctx.reply(f"Set the value of `blessrole` to `{str(int(blessRole))}`")

	async def blessing(self, ctx: commands.Context, target: discord.Member, roleToggle: bool):
		guild = ctx.guild
		blessed_role = await self.config.guild(guild).blessrole()
		role = guild.get_role(blessed_role)
		try:
			if roleToggle == True:
				await target.add_roles(role, reason="blessed")
				return await ctx.send(content=f"blessed {target.mention}")
			else:
				await target.remove_roles(role, reason="deblessed")
				return await ctx.send(content=f"deblessed {target.mention}")
		except discord.errors.Forbidden:
			return await ctx.send("the server admin didn't set up roles correctly, uh oh!\n\n*just so you know, this is not your fault. ping a server admin to fix this.*")

	@rain.command()
	async def rgif(self, ctx: commands.Context):
		"""the AI will send you one random gif for free"""
		if self.gifs is not self.gifs:
			# make sure the gif database is UP TO DATE.
			with open("./gifs.txt", "r") as f:
				self.gifs = [line.rstrip() for line in f]

		await ctx.reply(self.gifs[0, len(self.gifs) - 1])


	@rain.command()
	@checks.admin_or_permissions(manage_roles=True)
	async def bless(self, ctx: commands.Context, target: discord.Member) -> None:
		"""
		verifies a user
		"""
		if not target:
			return await ctx.send_help()
		if ctx.me is target:
			return await ctx.send("you cant bless me! i'm already blessed internally!")
		if ctx.author is target:
			return await ctx.send("you cant bless yourself!")

		blessed_role = await self.config.guild(ctx.guild).blessrole()
		if not blessed_role:
			return await ctx.send("the server admin didn't set up bless roles correctly, uh oh!\n\n*just so you know, this is not your fault. ping a server admin to fix this.*")
		await self.blessing(ctx, target, True)
	
	@rain.command(aliases=["shadowrealm", "debless"])
	@checks.admin_or_permissions(manage_roles=True)
	async def unbless(self, ctx: commands.Context, target: discord.Member) -> None:
		"""
		deverifies a user
		"""
		if not target:
			return await ctx.send_help()
		if ctx.me is target:
			return await ctx.send("you cant unbless me!")
		if ctx.author is target:
			return await ctx.send("you cant unbless yourself!")
		blessed_role = await self.config.guild(ctx.guild).blessrole()
		if not blessed_role:
			return await ctx.send("the server admin didn't set up bless roles correctly, uh oh!\n\n*just so you know, this is not your fault")
		await self.blessing(ctx, target, False)
