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

client = commands.Bot(command_prefix='$')


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
	await leaveVoice(context)
	await context.message.channel.send("Bot signing off...")
	await client.change_presence(status=discord.Status.offline)
	await client.logout()

@client.command(name='pic')
async def randPic(context):
	pics = ["pic1.jpg", "gif1.gif", "gif2.gif", "gif3.gif"]
	randomChoice = random.choice(pics)
	await context.message.channel.send(file=discord.File(randomChoice))

@client.command(name='connect')
async def joinVocie(context):
	if client.voice_clients:
		if context.message.author.voice.channel == client.voice_clients[0].channel:
			await context.message.channel.send("Already connected to your voice channel!")
		else:
			for joinedChannel in client.voice_clients:
				await joinedChannel.disconnect()
			await context.message.author.voice.channel.connect()
	elif context.message.author.voice:
		await context.message.author.voice.channel.connect()
		await context.message.channel.send(f'Joined the {context.message.author.voice.channel.name} voice channel!')
	else:
		await context.message.channel.send("You are not connected to a voice channel.")

@client.command(name='disconnect')
async def leaveVoice(context):	
	for joinedChannel in client.voice_clients:
		await joinedChannel.disconnect()
		await context.message.channel.send("Successfully disconnected from voice channel.")

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