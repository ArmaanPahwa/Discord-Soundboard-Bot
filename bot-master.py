# This is the master code for the bot

# bot-master.py
import os
import discord
import requests
import json
import random
import io
import aiohttp

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
#bot = commands.Bot(command_prefix='!')

# ------------------------------------
@client.event
async def on_ready():
	print(f'{client.user.name} has connected to Discord!')
	guild = discord.utils.get(client.guilds, name=GUILD)
	print(f'{client.user.name} is connected to the following server:\n')
	print(f'{guild.name}(id:{guild.id})')
	await client.change_presence(activity=discord.Game("In the creation lab."))
# ------------------------------------
def get_quote():
	response = requests.get("https://zenquotes.io/api/random")
	json_data = json.loads(response.text)
	quote = json_data[0]['q'] + " -" + json_data[0]['a']
	return quote

# ------------------------------------
sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]
encouragements = ["You can do it!", "I am here to listen :D", "*sends virtual hug*"]

# ------------------------------------
@client.event
async def on_message(message):
	if message.author == client:
		return

	if message.content.startswith('!hello'):
		await message.channel.send('Hello!')

	if message.content.startswith('!inspire'):
		quote = get_quote()
		await message.channel.send(quote)

	if any(word in message.content for word in sad_words):
		await message.channel.send(random.choice(encouragements))
    
	if message.content == "!pic":
		pics = ["pic1.jpg", "gif1.gif", "gif2.gif", "gif3.gif"]
		randomChoice = random.choice(pics)
		await message.channel.send(file=discord.File(randomChoice))
	
	if message.content == "!logout":
		await message.channel.send("Bot signing off...")
		await client.change_presence(status=discord.Status.offline)
		await client.logout()

client.run(TOKEN)