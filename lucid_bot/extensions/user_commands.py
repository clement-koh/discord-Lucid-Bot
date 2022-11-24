import logging

import lightbulb
import hikari

from ..common_functions import get_character_records, format_character_information
from .components._character_component import *
from .components._embed_colors import *


plugin = lightbulb.Plugin("Character Management")

@plugin.command()
@lightbulb.command("View Characters", "View list of characters that the user added")
@lightbulb.implements(lightbulb.UserCommand)
async def user_context_view_characters(ctx: lightbulb.UserContext) -> None:
	member = ctx.app.cache.get_member(ctx.guild_id, ctx.options.target.id)
	author_discord_id = str(ctx.author.id)
	guild_record = get_guild_record(str(ctx.guild_id))

	# If user is self or user is authorized role 
	if (str(member.id) == author_discord_id) or author_discord_id in guild_record.get('authorized_roles', []):
		characters = get_character_records(str(member.id))
		embed = hikari.Embed(
			title = f"{member.display_name}'s characters",
			description = format_character_information(characters)
		)
		await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)
	else:
		await ctx.respond(hikari.Embed(title=f"No stalking {member.display_name}'s characters", description="You can only view your characters", color=COLOR_ERROR))
		return True

# Function to load plugins
def load(bot):
	bot.add_plugin(plugin)
