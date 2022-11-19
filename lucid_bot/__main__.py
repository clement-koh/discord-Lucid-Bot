import lightbulb
import hikari
import os

from lucid_bot import bot

# # Check if bot is ready
# @bot.listen(hikari.StartedEvent)
# async def on_started(event: hikari.StartedEvent) -> None:
# 	"""
# 	Action is performed when the device is online
# 	"""
# 	channel = await bot.rest.fetch_channel(STDOUT_CHANNEL_ID)
# 	await channel.send("Lucid-Bot is Online!")


# @bot.listen(hikari.GuildMessageCreateEvent)
# async def send_message(event):
# 	print(event)
# 	print(event.content)

# @bot.command
# @lightbulb.command("ping", "Says Pong!")
# @lightbulb.implements(lightbulb.SlashCommand)
# async def ping(ctx):
# 	await ctx.respond("Pong!")

# @bot.command
# @lightbulb.command('group', "This is a group")
# @lightbulb.implements(lightbulb.SlashCommandGroup)
# async def my_group(ctx):
# 	pass


# @my_group.child
# @lightbulb.command('subcommand', "This is a subcommand")
# @lightbulb.implements(lightbulb.SlashSubCommand)
# async def subcommand(ctx):
# 	await ctx.respond("I am a subcommand!")

# @bot.command
# @lightbulb.option("num2", "The second number", type=int)
# @lightbulb.option("num1", "The first number", type=int)
# @lightbulb.command("add", "Adds two numbers together")
# @lightbulb.implements(lightbulb.SlashCommand)
# async def add(ctx):
# 	await ctx.respond(ctx.options.num1 + ctx.options.num2)

# class DiceView(miru.View):
# 	@miru.select(
# 		placeholder="Choose a color...",
# 		options=[
# 			miru.SelectOption(label="Red"),
# 			miru.SelectOption(label="Green"),
# 			miru.SelectOption(label="Blue"),
# 		]
# 	)
# 	async def select_menu_colors(self, select: miru.Select, ctx: miru.Context) -> None:
# 		await ctx.respond(f"{select.values[0]} is the color you chose!")


# 	@miru.button(label="1d6", emoji="6️⃣", style=hikari.ButtonStyle.PRIMARY)
# 	async def button_1d6(self, button: miru.Button, ctx: miru.Context) -> None:
# 		roll = random.randint(1, 6)
# 		await ctx.edit_response(f"You rolled a **{roll}**!")

# 	@miru.button(label="Close", style=hikari.ButtonStyle.DANGER)
# 	async def btn_close(self, button: miru.Button, ctx:miru.Context) -> None:
# 		await ctx.edit_response("The menu was closed.", components=[])
# 		self.stop()
	
# 	async def on_timeout(self) -> None:
# 		await self.message.edit("The menu timed out.", components=[])
# 		self.stop()

# 	async def view_check(self, ctx: miru.Context) -> None:
# 		return ctx.user.id == 3711986857591439367



# @bot.command()
# @lightbulb.add_cooldown(15.0, 2, lightbulb.GuildBucket)
# @lightbulb.add_checks(lightbulb.owner_only, lightbulb.has_roles(1040664909312180224))
# @lightbulb.option("text", "The thing to say")
# @lightbulb.command("say", "Makes the bot say something.")
# @lightbulb.implements(lightbulb.SlashCommand)
# async def command_say(ctx: lightbulb.SlashContext) -> None:
# 	await ctx.respond(ctx.options.text) 


# @bot.command()
# @lightbulb.command("Joined Date", "See when this member joined")
# @lightbulb.implements(lightbulb.UserCommand)
# async def command_context_joined_date(ctx: lightbulb.UserContext) -> None:
# 	member = ctx.app.cache.get_member(ctx.guild_id, ctx.options.target.id)
# 	await ctx.respond(f"{member.display_name} joined at <t:{member.joined_at.timestamp():.0f}:f>")

# @bot.command()
# @lightbulb.command("Word Count", "View the word count for this message")
# @lightbulb.implements(lightbulb.MessageCommand)
# async def command_context_word_count(ctx: lightbulb.MessageContext) -> None:
# 	message = ctx.options.target
# 	words = len(message.content.split(" "))
# 	await ctx.respond(f"Message: {message.content}\nWord Count: {words:,}")


# @bot.listen(hikari.GuildMessageCreateEvent)
# async def on_message_create(event: hikari.GuildMessageCreateEvent) -> None:
# 	if event.is_bot or not event.content:
# 		return
	
# 	if event.content == "buttons":
# 		view = DiceView(timeout=60)
# 		message = await event.message.respond("Roll your dice!", components=view.build())
# 		view.start(message)
# 		await view.wait()
# 		print("All Done!")

# 	if event.content == "select":
# 		...




# 

if __name__== "__main__":
	if os.name != "nt":
		import uvloop
		uvloop.install()
	bot.run()


