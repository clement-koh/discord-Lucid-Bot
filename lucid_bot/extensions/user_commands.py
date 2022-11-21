import logging

import lightbulb
import hikari

from ..common_functions import get_character_records, format_character_information
from .components._character_component import *


plugin = lightbulb.Plugin("Character Management")

@plugin.command()
@lightbulb.add_checks(lightbulb.checks.has_guild_permissions(hikari.Permissions.MANAGE_ROLES))
@lightbulb.command("View Character List", "View list of characters that the user added")
@lightbulb.implements(lightbulb.UserCommand)
async def user_context_view_characters(ctx: lightbulb.UserContext) -> None:
	member = ctx.app.cache.get_member(ctx.guild_id, ctx.options.target.id)
	characters = get_character_records(str(member.id))
	embed = hikari.Embed(
		title = f"{member.display_name}'s characters",
		description = format_character_information(characters)
	)
	await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)

@user_context_view_characters.set_error_handler
async def user_context_view_character_error_handler(event: lightbulb.UserCommandErrorEvent):
	if isinstance(event.exception, lightbulb.errors.MissingRequiredPermission):
		await event.context.respond("You do not have the required permission", flags=hikari.MessageFlag.EPHEMERAL)
		return True

# Function to load plugins
def load(bot):
	bot.add_plugin(plugin)
