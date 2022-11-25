import traceback

import hikari
import miru
import logging

from lucid_bot.common_functions import get_character_records, delete_character_record, format_character_information, get_guild_record, update_guild_bossing_interest
from lucid_bot.extensions.bossing_management import edit_guild_bossing_interest, convert_boss_selection_to_boss_id
from lucid_bot.extensions.components._embed_colors import *

class Character_Select(miru.Select):
	def __init__(self, characters) -> None:
		self.character_list = []
		for character in characters:
			character_name = character.get('character_name')
			job = character.get('job')
			floor = character.get('floor')
			option = miru.SelectOption(
				label=character_name,
				description=f"{job} (F{floor})"
			)
			self.character_list.append(option)
		super().__init__(
			placeholder="Select a character",
			options=self.character_list, 
		)


	async def callback(self, ctx: miru.Context) -> None:
		self.view.selection = self.values[0]
		self.view.last_context = ctx


class Delete_Button(miru.Button):
	def __init__(self) -> None:
		super().__init__(style=hikari.ButtonStyle.PRIMARY, label="Delete")


	async def callback(self, ctx: miru.Context) -> None:
		# Record the last context for the view
		self.view.last_context = ctx

		if hasattr(self.view, "selection"):
			character = str(self.view.selection).strip()
			discord_id = str(ctx.user.id).strip()

			try:
				character_records = get_character_records(discord_id)
				selected_character = None
				for character_record in character_records:
					if character_record.get("character_name") == character:
						selected_character = character
						break;
				involved_guilds = character_record.get("guilds_involved_in", [])

				for guild_id in involved_guilds:
					print(guild_id)
					guild_record = get_guild_record(guild_id)
					valid_selections = convert_boss_selection_to_boss_id("-all", guild_record.get("allowed_bosses"))
					guild_bossing_interest = edit_guild_bossing_interest(discord_id, selected_character, guild_record.get('bossing_interest', {}), valid_selections)
					update_guild_bossing_interest(guild_id, guild_bossing_interest)
			except Exception as e:
				logging.error(f"Error while deleting bossing character from guild: {e}, {traceback.print_exc()}")
				await ctx.edit_response("Bot Error: Failed to delete character", components=[])
				self.view.stop()
				return

			try:
				# Delete CHaracters
				delete_character_record(discord_id, character)
				await ctx.edit_response(f"**{character}** was deleted", components=[])

				# Get Remaining Characters
				characters = get_character_records(discord_id)
				message = format_character_information(characters)
				embed = hikari.Embed(
					title="Remaining Characters",
					description=message,
					color=COLOR_SUCCESS)
				await ctx.respond(f"<@{discord_id}>", embed=embed, user_mentions=True)
			except Exception as e:
				logging.error(f"Failed to delete character: {e}")
				await ctx.edit_response("Bot Error: Failed to delete character", components=[])
				self.view.stop()
				return
			
			# Stop view
			self.view.stop()

		else:
			await ctx.edit_response(f"You have not selected a character")


class Cancel_Button(miru.Button):
	def __init__(self) -> None:
		super().__init__(style=hikari.ButtonStyle.DANGER, label="Cancel")
	
	
	async def callback(self, ctx: miru.Context) -> None:
		await ctx.edit_response("Action Cancelled", components=[])
		self.view.stop()


class Character_Deletion_View(miru.View):
	
	def __init__(self, select_view: miru.Select):
		super().__init__(timeout=60)

		# # Add Selection View
		self.add_item(select_view)
		self.add_item(Delete_Button())
		self.add_item(Cancel_Button())