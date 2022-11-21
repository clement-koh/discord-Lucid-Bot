import logging

import lightbulb
import hikari

from ..common_functions import create_new_character_record, get_character_records
from .components._character_component import *
from .components._embed_colors import *


plugin = lightbulb.Plugin("Character Management")

# Create Command Group for Character Management
@plugin.command
@lightbulb.command('characters', "Group of Bossing Characters")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def character_group(ctx: lightbulb.Context) -> None:
	await ctx.respond("Invoked Character Group")


# Add Character
@character_group.child
@lightbulb.option("dojo_floor", "Enter your current dojo floor for this character", type=int, min_value=0, max_value=100)
@lightbulb.option("job", "Fire Poison Mage / Adele / ... / Bishop")
@lightbulb.option("character_name", "Your Bossing Character Name")
@lightbulb.command('add', "Adds or Updates a bossing character. Names are case-sensitive(E.g. xXLucidBotXx)")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def add_character(ctx: lightbulb.SlashContext):
	'''
	Adds a new character record
	'''
	# Get User information
	discord_id = str(ctx.author.id)
	ign = ctx.options.character_name.strip()
	char_class = ctx.options.job.strip()
	floor = ctx.options.dojo_floor
	logging.debug(f"Add Character: Discord ID: {discord_id}, IGN: {ign}, Class: {char_class}, Floor: {floor}")

	# Update Database
	try:
		create_new_character_record(discord_id, ign, char_class, floor)
	except Exception as e:
		logging.error(e)
		await ctx.respond("Bot Error: Failed to add character.")
		return
	
	# Success Response
	await ctx.respond(f"**{ign}** - **{char_class}** with Dojo Floor of **{floor}** added!")

# View Characters
@character_group.child
@lightbulb.command("show", "Show all your characters")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def view_characters(ctx: lightbulb.SlashContext):
	'''
	View all characters that belongs to the user
	'''
	# Get User Information
	discord_id = str(ctx.author.id)
	logging.debug(f"View Character: Discord ID: {discord_id}")

	# Retrieve Data
	characters = []
	try:
		characters = get_character_records(discord_id)
	except Exception as e:
		logging.error(e)
		await ctx.respond(hikari.Embed(title="Bot Error: Failed to retrieve characters", color=COLOR_ERROR))
		return

	# Success
	message = format_character_information(characters)
	if not characters:
		message = "No characters found. Use `/character add` to register a character"
	embed = hikari.Embed(title="Your Character Information", description=f"{message}", color=COLOR_SUCCESS)
	await ctx.respond(embed)


# Delete Character
@character_group.child
@lightbulb.command('delete', "Removes a bossing character.")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def delete_character(ctx: lightbulb.SlashContext):
	'''
	Deletes a specific character that belongs to the user
	'''
	# Get User Information
	characters = None
	discord_id = str(ctx.author.id)
	try:
		characters = get_character_records(discord_id)
	except Exception as e:
		logging.error(e)
		await ctx.respond("Bot Error: Failed to retrieve characters")
		return

	delete_selection_menu = Character_Select(characters)
	view = Character_Deletion_View(select_view=delete_selection_menu)
	embed = hikari.Embed(title="Select a character to remove", description= "Command will timeout after 60 seconds")
	# response = await ctx.respond("```The following menu will only last for 60 seconds before it is disabled```\n\n", components=view.build(), flags=hikari.MessageFlag.EPHEMERAL, embed=embed)
	response = await ctx.respond(components=view.build(), flags=hikari.MessageFlag.EPHEMERAL, embed=embed)
	view.start(await response.message())
	await view.wait()

# Function to load plugins
def load(bot):
	bot.add_plugin(plugin)