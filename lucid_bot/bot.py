import logging
import os
import random

import hikari
import lightbulb
import miru

from .common_functions import register_guild_in_db



bot = lightbulb.BotApp(
	token=os.environ["TOKEN"], 
	intents=hikari.Intents.ALL,
	default_enabled_guilds=int(os.environ.get("DEFAULT_GUILD_ID")),
	help_slash_command=True,
)
miru.load(bot)


# SENDS A MESSAGE WHEN THE BOT IS ONLINE
@bot.listen(hikari.StartedEvent)
async def on_started(event: hikari.StartedEvent) -> None:
	"""
	Action is performed when the device is online
	"""
	channel = await bot.rest.fetch_channel(os.environ.get("STDOUT_CHANNEL_ID"))
	await channel.send("Lucid-Bot is Online!")

@bot.listen(hikari.GuildJoinEvent)
async def on_join_guild(event: hikari.GuildJoinEvent) -> None:
	"""
	Action is performed when the bot joins a guild
	"""
	logging.info("Joined Guild Event Triggered")
	guild_name = str(event.get_guild())
	guild_id = str(event.get_guild().id)
	
	# Create record in database
	register_guild_in_db(guild_id, guild_name)
	

def run() -> None:
	if os.name != "nt":
		import uvloop
		uvloop.install()

	bot.load_extensions_from('./lucid_bot/extensions', recursive=True)
	bot.run(
		status=hikari.Status.ONLINE,
		activity=hikari.Activity(
			name="over the server",
			type=hikari.ActivityType.WATCHING
		)
	)