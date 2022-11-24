import hikari
import lightbulb

from .components._embed_colors import *

class CustomHelp(lightbulb.BaseHelpCommand):
	async def send_bot_help(self, context):
		# Override this method to change the message sent when the help command
		# is run without any arguments.
		# embed = hikari.Embed(title="Lucid Bot Commands", color=COLOR_SUCCESS)
		# fields = [
		# 	{
		# 		"command": "Character Commands",
		# 		"description": 	"`/character add character_name job dojo_floor`:  Add a character\n\n" + \
		# 						"`/character delete`: Deletes a character\n\n" + \
		# 						"`/character show`: Displays all the characters you added\n\n"
		# 	},
		# 	{
		# 		"command": "Boss Commands",
		# 		"description": 	'`/boss info boss_name`:  Displays information on a boss. Boss name can be have common names e.g. "Normal lucid" or "nlu" or "lucid"\n\n' + \
		# 						"`/boss register`:  Display bosses  & characters to register for boss runs\n\n" + \
		# 						"`/boss register character_number boss_number`: Indicate your interest to participate in a certain boss. e.g. `/boss register` `1` `all, -1, -2`\n\n" + \
		# 						"`/boss show_registered`: Displays the bosses your character have signed up for this upcoming boss run\n\n" + \
		# 						"`/boss show_guild_summary`: Display all registrations done for this upcoming boss run\n\n"
		# 	},
		# 	{
		# 		"command": "Config Commands (Requires Permission)",
		# 		"description": "`/config boss_reset`: Resets all bossing interest for the guild\n"
		# 	}
		# ]
		
		# for field in fields:
		# 	embed.add_field(field['command'], field['description'])
		
		# await context.respond(embed)

		message ="```Character Commands```\n" + \
				"`/character add character_name job dojo_floor`:  Add a character\n\n" + \
				"`/character delete`: Deletes a character\n\n" + \
				"`/character show`: Displays all the characters you added\n\n" + \
				"```Boss Commands```\n" + \
				"`/boss info boss_name`:  Displays information on a boss. Boss name can be have common names e.g. 'Normal lucid' or 'nlu' or 'lucid'\n\n" + \
				"`/boss register`:  Display bosses  & characters to register for boss runs" + \
				"`/boss register character_number boss_number`: Indicate your interest to participate in a certain boss. e.g. `/boss register` `1` `all, -1, -2`\n\n" + \
				"`/boss show_registered`: Displays the bosses your character have signed up for this upcoming boss run\n\n" + \
				"`/boss show_guild_summary`: Display all registrations done for this upcoming boss run\n\n" + \
				"```Config Commands (Requires permission)```\n" + \
				"`/config boss_reset`: Resets all bossing interest for the guild" 
		await context.respond(message)
		return


	async def send_plugin_help(self, context, plugin):
		# Override this method to change the message sent when the help command
		# argument is the name of a plugin.
		return

	async def send_command_help(self, context, command):
		# Override this method to change the message sent when the help command
		# argument is the name or alias of a command.
		return

	async def send_group_help(self, context, group):
		# Override this method to change the message sent when the help command
		# argument is the name or alias of a command group.
		return

	async def object_not_found(self, context, obj):
		# Override this method to change the message sent when help is
		# requested for an object that does not exist
	    return

# Function to load plugins
def load(bot):
	bot.d.old_help_command = bot.help_command
	bot.help_command = CustomHelp(bot)