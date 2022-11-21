import boto3
from boto3.dynamodb.conditions import Key
import os

AWS_CREDS = {
	"aws_access_key_id": os.environ.get("aws_secret_key_id"),
	"aws_secret_access_key": os.environ.get("aws_secret_access_key"),
	"region_name": os.environ.get("region")
}

DYNAMODB = boto3.resource("dynamodb", **AWS_CREDS)
CHARACTERS_TABLE = DYNAMODB.Table("lucid_bot_characters")
GUILD_TABLE = DYNAMODB.Table("lucid_bot_guild")

def create_new_character_record(discord_id:str, character_name:str, job:str, floor:int) -> None:
	CHARACTERS_TABLE.put_item(
		Item={
			"discord_id": discord_id,
			"character_name": character_name,
			"job":job,
			"floor":floor
		}
	)

def get_character_records(discord_id:str) -> dict:
	response = CHARACTERS_TABLE.query(
		KeyConditionExpression=Key("discord_id").eq(discord_id)
	)
	
	return response.get("Items")


def delete_character_record(discord_id:str, character_name: str) -> None:
	CHARACTERS_TABLE.delete_item(
		Key={
			"discord_id": discord_id,
			"character_name": character_name
		}
	)


def format_character_information(characters:list) -> str:
	'''
	Formats character information into a code block for discord
	'''
	if len(characters) == 0:
		return "No characters found"

	message = ""
	count = 1
	for character in characters:
		name = f"{count:>2}. {character.get('character_name')}"
		job = character.get('job')
		floor = character.get('floor')
		message += f"{name:<20} {job:<20} F{floor}\n"
		count += 1
	message = f"```\n{message}```"
	return message

def get_guild_record(guild_id:str) -> dict:
	response = GUILD_TABLE.query(
		KeyConditionExpression=Key("guild_id").eq(guild_id)
	)
	
	return response.get("Items").pop()

def update_guild_bossing_interest(guild_id:str, bossing_interest: dict) -> None:
	response = GUILD_TABLE.update_item(
		Key={"guild_id": guild_id},
		AttributeUpdates={
			"bossing_interest": {
				"Value": bossing_interest,
				"Action": "PUT"
			}
		}
	)

def update_character_bossing_interest(discord_id:str, character_name:str, bossing_interest: list):
	print(bossing_interest)
	response = CHARACTERS_TABLE.update_item(
		Key={
			"discord_id": discord_id,
			"character_name": character_name
		},
		AttributeUpdates={
			"guilds_involved_in": {
				"Value": bossing_interest,
				"Action": "PUT"
			}
		}	
	)

def register_guild_in_db(guild_id:str, guild_name:str) -> None:
	response = GUILD_TABLE.update_item(
		Key={
			'guild_id': guild_id
		},
		AttributeUpdates={
			"guild_name": {
				"Value": guild_name,
				"Action": "PUT"
			},
			"authorized_roles": {
				"Value": [],
				"Action": "PUT"
			},
		}	
	)

def reset_guild_boss_interest(guild_id) -> None:
	response = GUILD_TABLE.update_item(
		Key={
			'guild_id': guild_id
		},
		AttributeUpdates={
			"bossing_interest": {
				"Value": {},
				"Action": "PUT"
			},
		}	
	)