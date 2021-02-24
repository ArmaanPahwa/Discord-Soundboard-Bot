# This is the master code for the bot

# bot-master.py
import os
import discord
import requests
import json
import random
import io
import aiohttp

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = commands.Bot(command_prefix='$$')


@client.event
async def on_ready():
	print(f'{client.user.name} has connected to Discord!')
	guild = discord.utils.get(client.guilds, name=GUILD)
	print(f'{client.user.name} is connected to the following server:\n')
	print(f'{guild.name}(id:{guild.id})')
	await client.change_presence(activity=discord.Game("In the creation lab."))

def get_quote():
	response = requests.get("https://zenquotes.io/api/random")
	json_data = json.loads(response.text)
	quote = json_data[0]['q'] + " -" + json_data[0]['a']
	return quote

@client.command(name='logout')
async def logout(context):
	await context.message.channel.send("Bot signing off...")
	await client.change_presence(status=discord.Status.offline)
	await client.logout()

@client.command(name='pic')
async def randPic(context):
	pics = ["pic1.jpg", "gif1.gif", "gif2.gif", "gif3.gif"]
	randomChoice = random.choice(pics)
	await context.message.channel.send(file=discord.File(randomChoice))

@client.event
async def on_message(message):
	if message.author == client:
		return

	if message.content.startswith('hello bot'):
		await message.channel.send(f'Hello {message.author.mention}!')

	if message.content.startswith('inspire me'):
		quote = get_quote()
		await message.channel.send(quote)
	
	await client.process_commands(message)

client.run(TOKEN)