import logging

import lightbulb
import hikari
import miru


from ..boss_data import BOSSES
from .components._embed_colors import *
from ..common_functions import get_guild_record, reset_guild_boss_interest

plugin = lightbulb.Plugin("Bot Config")


# Create Command Group for Bossing Management
@plugin.command
@lightbulb.command('config', "Anything related to do with bot configuration")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def configuration_group(ctx: lightbulb.Context) -> None:

	await ctx.respond("Invoked Configuration Group")


# Display Boss Requirement Information
@configuration_group.child
@lightbulb.command('boss_reset', "Reset registration for weekly boss")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def get_boss_information(ctx: lightbulb.SlashContext) -> None:
	'''
	Displays information regarding bosses that matches the name
	'''
	logging.info("Boss Registration Information Triggered")

	# Get Allowed Roles
	guild_id = str(ctx.get_guild().id)
	owner_id = str(ctx.get_guild().owner_id)
	guild_info = get_guild_record(guild_id)
	allowed_roles = guild_info.get("authorized_roles")
	user_roles = ctx.member.role_ids
	
	allowed = False
	if str(ctx.member.id) == owner_id:
		allowed = True
	for role in user_roles:
		if str(role) in allowed_roles or allowed:
			allowed = True
			break

	# Reject the user
	if not allowed:
		await ctx.respond("You do not have permission for this command")
		return
	
	# If allowed
	try:
		reset_guild_boss_interest(guild_id)
	except Exception as e:
		await ctx.respond(hikari.Embed(title="Failed to reset boss registration", color=COLOR_ERROR))
	else:
		embed = hikari.Embed(
			title="Guild Bossing registration is now open",
			description="Use **/boss register** command to view instructions on how to indicate your bossing interest",
			color=COLOR_SUCCESS
		)
		await ctx.respond("@everyone", embed=embed, mentions_everyone=True)

# Function to load plugins
def load(bot):
	bot.add_plugin(plugin)