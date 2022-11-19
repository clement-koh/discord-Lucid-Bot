import hikari
import lightbulb
import miru

class Select_Button(miru.Button):
	def __init__(self) -> None:
		super().__init__(style=hikari.ButtonStyle.SUCCESS, label="Select")

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