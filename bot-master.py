import os
import discord
import music
from discord.ext import commands
from discord import FFmpegPCMAudio

### SET-UP Envoirnmental Variables
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#Setup client prefix & Intents
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# --- SETUP EVENT ---
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    print(f'{client.user.name} is connected to the following server:\n')
    for guild in client.guilds:
        print(f'{guild.name}(id:{guild.id})')
    await client.change_presence(activity=discord.Game("Jamming out to music"))

### --- CONNECT AND DISCONNECT COMMANDS ---
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

### --- LOGOUT COMMAND ---
@client.command(name='logout')
async def logout(context):
	await leaveVoice(context)
	await context.message.channel.send("Bot signing off... See you next time!")
	await client.change_presence(status=discord.Status.offline)
	await client.close()

### --- MUSIC COMMANDS ---
@client.command(name='play')
async def play(context):
	print(f'recieved play command: {context.message.content}')
	await joinVoice(context)
	if client.voice_clients:
		currentVoice = client.voice_clients[0]
		if not currentVoice.is_playing():
			source = FFmpegPCMAudio('audioSource.mp3')
			player = currentVoice.play(source)
		else:
			await context.message.channel.send("Currently playing music. Please wait for audio to complete.")

@client.command(name='stop')
async def stop(context):
	if client.voice_clients:
		currentVoice = client.voice_clients[0]
		if currentVoice.is_playing():
			currentVoice.stop()
		else:
			await context.message.channel.send("No audio is currently playing.")
	else:
		await context.message.channel.send("No audio is currently playing.")

# --- MESSAGE HANDLING ---
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    print(f'Message from {message.author}: {message.content}')

    if message.content.startswith('hello bot'):
        await message.channel.send(f'Hello {message.author.mention}!')

    await client.process_commands(message)

client.run(TOKEN)