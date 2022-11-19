import logging

import lightbulb
import hikari
import miru


from ..boss_data import BOSSES
from .components._embed_colors import *
from ..common_functions import get_character_records, format_character_information, get_guild_record, update_guild_bossing_interest, update_character_bossing_interest

plugin = lightbulb.Plugin("Bossing Management")


# Create Command Group for Bossing Management
@plugin.command
@lightbulb.command('boss', "Anything related to do with bossing")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def bossing_group(ctx: lightbulb.Context) -> None:
	await ctx.respond("Invoked Bossing Group")


# Display Boss Requirement Information
@bossing_group.child
@lightbulb.option('boss_name', "Enter a common boss name. Eg. Lucid, nlotus, hwill, lomien, hard lotus", required=True)
@lightbulb.command('info', "Display bossing dojo requirements")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def get_boss_information(ctx: lightbulb.SlashContext) -> None:
	'''
	Displays information regarding bosses that matches the name
	'''
	logging.info("Boss Requirement Information Triggered")

	# Get boss name that user submitted
	boss_name = ctx.options.boss_name.lower()

	# Extact all matching boss information
	matching_boss = []
	for boss in BOSSES:
		if boss_name == boss["name"].lower() or boss_name in boss["alt_name"]:
			matching_boss.append(boss)

	# Display all matching info
	if matching_boss:
		for boss in matching_boss:
			embed = hikari.Embed(
				title=f"{boss['difficulty']} {boss['name']}",
				description= "Recommend Dojo Floors```" +\
					f"{'Solo':<30}:{boss.get('solo_floor')}\n" + \
					f"{'Party 4 man':<30}:{boss.get('party_floor_4_man')}\n" + \
					f"{'Party 6 man (inexperienced)':<30}:{boss.get('party_floor_6_man_new')}\n" + \
					f"{'Party 6 man (experienced)':<30}:{boss.get('party_floor_6_man_experienced')}\n```"
			)
			await ctx.respond(embed)
	else:
		await ctx.respond(hikari.Embed(title="No Boss Found"))


# Register a character to join bossing
@bossing_group.child
@lightbulb.option('bosses', "Enter the boss number you like to join separated by a comma. e.g. '1, 2, 3, 7, 15'", required=False)
@lightbulb.option('character_number', 'Enter your character number shown in "/character list". Optional if you only have 1 character', type=int, min_value=1, required=False)
@lightbulb.command('register', "Indicate your interest for bosses. Execute '/boss register' without any options to see the boss menu")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def register_bossing_character_in_guild(ctx: lightbulb.SlashContext) -> None:
	'''
	Register a character for boss in the current guild
	'''

	def get_valid_selection(selection_list: str, allowed_bosses: list) -> list:
		valid_selections = []
		if allowed_bosses is None or len(allowed_bosses) == 0:
			allowed_bosses = [boss["id"] for boss in BOSSES]
		selection_list = selection_list.split(",")
		for boss in selection_list:
			# Convert Boss ID to int 
			boss_id_selected = None
			# Add all boss
			if boss.strip().lower() == "all":
				valid_selections += [int(x) for x in allowed_bosses]
			# Remove all boss
			elif boss.strip().lower() == "-all":
				valid_selections += [-int(x) for x in allowed_bosses]
			
			# Add/remove specific numbers
			else:
				try:
					boss_id_selected = int(boss.strip())
					# Check if selection list is part of allowed_bosses
					if boss_id_selected != 0 and abs(boss_id_selected) <= len(allowed_bosses):
						# Added boss ID of selected boss
						if boss_id_selected > 0:
							valid_selections.append(str(allowed_bosses[boss_id_selected - 1]))
						elif boss_id_selected < 0:
							valid_selections.append("-"+str(allowed_bosses[abs(boss_id_selected) - 1]))
				except:
					continue
		return list(set(valid_selections))


	def edit_guild_bossing_interest(interest: dict, valid_selections: int) -> dict:
		# Edit interest
		for selection in valid_selections:
			# Get selection
			selection = int(selection)
			str_abs_selection = str(abs(selection))

			# Add / Remove Record
			record = {"discord_id": discord_id, "character_name": selected_character_name}
			if selection > 0:
				if interest.get(str_abs_selection) is None:
					interest[str_abs_selection] = []
				
				if record not in interest[str_abs_selection]:
					interest[str_abs_selection].append(record)

			# Remove from boss preference
			elif selection < 0:
				if interest.get(str_abs_selection) is not None:
					try:
						interest[str_abs_selection].remove(record)
					except:
						pass
		return interest


	def edit_character_bossing_interest(interest:list, guild_id: str) -> list:
		if interest is None:
			return [guild_id]
		else:
			# convert to set
			interest = set(interest)
			interest.add(guild_id)
			return list(interest)

	logging.info("User's registration for boss triggered")

	# Save options
	character_number = ctx.options.character_number
	bosses_selected = ctx.options.bosses

	# Get User information
	discord_id = str(ctx.author.id)
	guild_id = str(ctx.get_guild().id)
	characters = get_character_records(discord_id)
	guild_record = get_guild_record(guild_id)
	
	# (Successful Case) Show how to use command
	if bosses_selected is None:
		title = "Boss Registration Instructions"
		await display_boss_registration(ctx, title, COLOR_SUCCESS, discord_id, guild_id)
		return

	# (Failed Case) If User Does not have any character 
	if len(characters) == 0:
		embed = hikari.Embed(
			title="You have not registered any characters",
			description="Use '/character add' to add a character",
			color=COLOR_ERROR
		)

		await ctx.respond(embed)
		return

	# (Failed Case) If User has more than one character and did not provide a character number
	if len(characters) >= 1 and character_number is None:
		title = "You need to provide a character number"
		color = hikari.Color("#FF0000")
		await display_boss_registration(ctx, title, COLOR_ERROR ,discord_id, guild_id)
		return
	
	# (Failed Case) If User character number is > his number of character or < 1
	if character_number <1 or character_number > len(characters):
		title="Invalid character number"
		await display_boss_registration(ctx, title, COLOR_ERROR, discord_id, guild_id)
		return

	
	# (Successful Case) 
	# Retrieve Guild Information (Allowed Boss Runs, Boss Run Registration) 
	selected_character_name = characters[character_number-1].get('character_name')
	guild_bossing_interest = guild_record.get("bossing_interest", {})
	character_interest = characters[character_number-1].get("guilds_involved_in", [])
	
	# Edit Interest
	valid_selections = get_valid_selection(bosses_selected, guild_record.get("allowed_bosses"))

	guild_bossing_interest = edit_guild_bossing_interest(guild_bossing_interest, valid_selections)
	character_bossing_interest = edit_character_bossing_interest(character_interest, guild_id)
	
	# Update Interest
	update_guild_bossing_interest(guild_id, guild_bossing_interest)
	update_character_bossing_interest(discord_id, selected_character_name, character_bossing_interest)

	embed = hikari.Embed(
		title="Successfully updated bossing preferences",
		color=COLOR_SUCCESS
	)

	await ctx.respond(embed)
	await show_registered_bosses(ctx)
	return
			

# Show registered bosses for the week
@bossing_group.child
@lightbulb.command('show_registered', "View your registered bosses for the week")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def show_registered_bosses(ctx: lightbulb.SlashContext) -> None:
	'''
	Displays to the user which of their character has registered for boss this week
	'''
	logging.info("Show user's registered bosses triggered")
	await(show_registered_bosses(ctx))
	
# Show all registrations in the guild
@bossing_group.child
@lightbulb.command('show_guild_summary', "Displays characters that have registered for guild bossing for the week")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def show_registered_boss_guild(ctx:lightbulb.SlashContext) -> None:
	'''
	Displays to the user tho in the guild has registered for bosses
	'''
	logging.info("Show Guild Bossing Registration Triggered")

	async def display_no_registration(ctx: lightbulb.SlashContext) -> None:
		embed = hikari.Embed(
			title="Guild Boss Interest",
			description="Wow. Theres no one here. Did everyone quit maple?",
			color=COLOR_SUCCESS
		)
		await ctx.respond(embed)

	# Retrieve guild information
	guild_id = str(ctx.get_guild().id)
	guild_members = ctx.get_guild().get_members()
	guild_members_converted = {}
	for key, value in guild_members.items():
		guild_members_converted[str(key)] = str(value)
	guild_info = get_guild_record(guild_id)

	bossing_interest = guild_info.get("bossing_interest")
	
	# If no one registered
	if bossing_interest is None:
		await display_no_registration(ctx)
		return

	# if ppl once registered, but somehow all deregister
	else:
		has_bossing_interest = False
		for value in bossing_interest.values():
			if value is not None:
				has_bossing_interest = True
				break;
		
		if not has_bossing_interest:
			await display_no_registration(ctx)
			return
	
	# If there are people
	embed = hikari.Embed(
		title="Guild Boss Interest",
		color=COLOR_SUCCESS
	)

	
	bossing_data = []		# Dict containing "boss" and "user"
	character_info = {}		# All character records for users found in full_users
	full_users = set()		# Set of all disc ID 

	# Get all boss
	for boss_id_str, users in bossing_interest.items():
		# Get Boss Info
		boss_info = None
		for boss in BOSSES:
			if boss['id'] == int(boss_id_str):
				bossing_data.append({"boss": boss, "users": users})
				break

		for user in users:
			full_users.add(user["discord_id"])

	# Retrieve all character records who participates in bossing	
	all_bossing_chara = []	
	for id in full_users:
		all_bossing_chara += get_character_records(id)
	# Convert into dict for easy accessing
	for chara in all_bossing_chara:
		character_info[chara.get("character_name")] = chara

	# Format data
	bossing_data = sorted(bossing_data, key=lambda d: d['boss']['id'])
	for data in bossing_data:
		message = ""
		boss_members = data.get("users")
		if boss_members is None or len(boss_members) == 0:
			continue
		else:
			bossing_group = []
			for character in data['users']:
				character_to_add = character_info.get(character['character_name'])
				if character_to_add is not None:
					bossing_group.append(character_to_add)
			
			# sort to display
			sorted_bossing_group = sorted(bossing_group, key=lambda d: d['floor'], reverse=True)

			# Add character to message
			count = 1
			for chara in sorted_bossing_group:
				message += f"{count: >2}:{chara['character_name']:<15}{chara['job']: <15} F{chara['floor']:<7} @{guild_members_converted[chara['discord_id']]}\n"
				count += 1

		message = f"```\n{message}```"
		# Add Embed Field
		embed.add_field(data['boss']['name'], message)
	
	# Display Embed
	await ctx.respond(embed)
	





# Helper function to show currently registeres bosses
async def show_registered_bosses(ctx:lightbulb.SlashContext):
	async def display_no_bossing_interest(ctx: lightbulb.SlashContext) -> None:
		embed = hikari.Embed(
			title="You have not registered for any bosses",
			description="Use '/boss register' to to indicate your bossing interest for this week",
			color=COLOR_SUCCESS
		)
		await ctx.respond(embed)
	
	# Get User information
	discord_id = str(ctx.author.id)
	guild_id = str(ctx.get_guild().id)
	characters = get_character_records(discord_id)
	guild_record = get_guild_record(guild_id)
	guild_bossing_interest = guild_record.get("bossing_interest")

	# Get Guild Bossing Interest
	if guild_bossing_interest is None:	
		await display_no_bossing_interest(ctx)
		logging.info("No one registered for guild bossing")
		return

	# Extract character boss information
	involved_characters = []
	for character in characters:
		guild_involved_list = character.get("guilds_involved_in")
		if guild_involved_list is None:
			continue
		elif guild_id not in guild_involved_list:
			continue
		else:

			record = {"discord_id": discord_id, "character_name": character.get("character_name")}
			boss_id_list = []
			for boss_id_str, boss_interest in guild_bossing_interest.items():
				boss_id = int(boss_id_str)
				if record in boss_interest:
					boss_id_list.append(boss_id)
			
			if len(boss_id_list) != 0:
				involved_characters.append({
					"character": character,
					"bosses": boss_id_list
				})
	
	if len(involved_characters) == 0:
		await display_no_bossing_interest(ctx)
		logging.info("User's characters was not registered for guild bossing")
		return
	
	embed = hikari.Embed(
		title="Registered bosses",
		description="These are the bosses you have indicated interest for in this week",
		color=COLOR_SUCCESS
	)

	for item in involved_characters:
		field_desc = ""
		for boss in BOSSES:
			if boss.get("id") in item.get("bosses"):
				field_desc += f"- {boss['difficulty']} {boss['name']}\n"

		field_desc = f"```\n{field_desc}```"

		character = item['character']
		embed.add_field(f"{character['character_name']} - Floor {character['floor']}", field_desc)
	
	await ctx.respond(embed)


# Helper Function for register_bossing_character_in_guild()
async def display_boss_registration(ctx:lightbulb.SlashContext, title:str, color:hikari.Color, discord_id: str, guild_id: str) -> None:
	description = "To add bosses, enter the boss number you wish to join for, separated by a comma. \nE.g. '1, 2, 5, 7'\n\n" + \
				  "To remove bosses, enter the a - before boss number, separated by a comma. \nE.g. '-1, -5'\n\n" + \
				  "Unique commands: \nall -> Add all bosses, -all -> remove all commands\n\n" + \
				  "Example 1: 'all, -3, -4'\nRegister for all bosses except 3 & 4\n\n" + \
				  "Example 2: '-all, 1, 2'\nUnregister for all bosses, then register for boss 1 & 2\n\n"
	
	# Display Boss menu if no bosses is empty
	embed = hikari.Embed(
		title=title,
		description=description,
		color=color
	)

	# Retrieve guild allowed boss list
	guild_id = str(ctx.get_guild().id)
	allowed_boss_list = get_guild_record(guild_id).get("allowed_bosses")
	if allowed_boss_list is None:
		allowed_boss_list = range(1, len(BOSSES)+1)

	# extracted allowable boss list
	extracted_boss_list = []
	for boss in BOSSES:
		if boss["id"] in allowed_boss_list:
			extracted_boss_list.append(boss)

	# Display Allowable bosses
	boss_arrangement = ""
	count = 0
	for boss in extracted_boss_list:
		boss_arrangement += f"{count+1:>2}: {boss.get('difficulty', '')} {boss.get('name', '')}\n"
		count +=1 
	embed.add_field("Boss Number", f"```\n{boss_arrangement}```")

	# Get Users to display
	characters = get_character_records(discord_id)
	embed.add_field("Your Characters", format_character_information(characters))

	await ctx.respond(embed)


# Function to load plugins
def load(bot):
	bot.add_plugin(plugin)