import hikari
import miru
import logging

from lucid_bot.common_functions import get_character_records, delete_character_record, format_character_information

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
				# Delete CHaracters
				delete_character_record(discord_id, character)
				await ctx.edit_response(f"**{character}** was deleted", components=[])

				# Get Remaining Characters
				characters = get_character_records(discord_id)
				message = format_character_information(characters)
				await ctx.respond(f"<@{discord_id}> Existing Characters\n{message}")
			except Exception as e:
				logging.error(e)
				await ctx.edit_response("Bot Error: Failed to delete character", components=[])
			
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