import os
import discord
from discord.ext import commands

### SET-UP Envoirnmental Variables
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#Setup client prefix & Intents
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

#Event for when bot is ready
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    print(f'{client.user.name} is connected to the following server:\n')
    for guild in client.guilds:
        print(f'{guild.name}(id:{guild.id})')
    await client.change_presence(activity=discord.Game("Jamming out to music"))

@client.command(name='connect')
async def joinVoice(context):
	if not context.message.author.voice:
		await context.message.channel.send("You are not connected to a voice channel.")
	elif client.voice_clients:
		if context.message.author.voice.channel != client.voice_clients[0].channel:
			for joinedChannel in client.voice_clients:
				await joinedChannel.disconnect()
			await context.message.author.voice.channel.connect()
	else:
		await context.message.author.voice.channel.connect()
		await context.message.channel.send(f'Joined the {context.message.author.voice.channel.name} voice channel!')

@client.command(name='disconnect')
async def leaveVoice(context):
	for joinedChannel in client.voice_clients:
		await joinedChannel.disconnect()
		await context.message.channel.send("Successfully disconnected from voice channel.")

@client.command(name='logout')
async def logout(context):
	await leaveVoice(context)
	await context.message.channel.send("Bot signing off... See you next time!")
	await client.change_presence(status=discord.Status.offline)
	await client.close()

#Event for each message
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    print(f'Message from {message.author}: {message.content}')

    if message.content.startswith('hello bot'):
        await message.channel.send(f'Hello {message.author.mention}!')

    await client.process_commands(message)

client.run(TOKEN)