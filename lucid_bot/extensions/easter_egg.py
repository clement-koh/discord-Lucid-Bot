import random

import hikari
import lightbulb
import miru

plugin = lightbulb.Plugin("Easter Egg")

prank_user_ids = [222344990167138305] 

lookout_messages = [
		"buy",
		"f2p",
		"free to play",
		"free 2 play",
		"spend",
		"fund"
	] 

reply_messages = [
		"Cough",
		"Free to Pay?",
		"Are you sure about that? 😏",
		"I saw that 😏",
		"Pay to Win? 😏"
	]

@plugin.listener(hikari.GuildMessageCreateEvent)
async def send_p2w_prank_message(event: hikari.GuildMessageCreateEvent) -> None:
	
	# If message author is not targeted for prank
	if int(event.author.id) not in prank_user_ids:
		return None
	
	# Check if message fits easter egg criteria
	message_content = str(event.message.content)
	if check_f2p(message_content):

		# React to the message
		try:
			await event.message.add_reaction("dogelaugh", 1034327280287236156)
		except:
			await event.message.add_reaction("👀")
		
		# Quote and formulate reply to the message
		reply_message = ""
		for message in message_content.split("\n"):
			if check_f2p(message):
				reply_message += f"> {message}\n" 
		reply_message += reply_messages[random.randint(0, len(reply_messages) - 1)]
		
		# Reply the message
		await event.message.respond(reply_message, reply=True)


def check_f2p(message):
	if any((lookout_message in message.lower()) for lookout_message in lookout_messages):
		return True
	return False

# Function to load plugins
def load(bot):
	bot.add_plugin(plugin)