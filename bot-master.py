# This is the master code for the bot

# bot-master.py
import os
import discord


from discord.ext import commands
from discord import FFmpegPCMAudio
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

@client.command(name='logout')
async def logout(context):
	await leaveVoice(context)
	await context.message.channel.send("Bot signing off...")
	await client.change_presence(status=discord.Status.offline)
	await client.logout()

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

@client.command(name='play')
async def play(context):
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
			await currentVoice.disconnect()
		else:
			await context.message.channel.send("No audio is currently playing.")
	else:
		await context.message.channel.send("No audio is currently playing.")

@client.command(name='pause')
async def pause_audio(context):
	if client.voice_clients:
		currentVoice = client.voice_clients[0]
		if currentVoice.is_playing():
			currentVoice.pause()
			await context.message.channel.send("Audio has been paused!")
		else:
			await context.message.channel.send("No audio is currently playing.")
	else:
		await context.message.channel.send("No audio is currently playing.")

@client.command(name='resume')
async def resume_audio(context):
	if client.voice_clients:
		currentVoice = client.voice_clients[0]
		if currentVoice.is_paused():
			currentVoice.resume()
			await context.message.channel.send("Audio has been resumed!")
		else:
			await context.message.channel.send("No audio has been paused.")
	else:
		await context.message.channel.send("No audio is currently playing.")

@client.event
async def on_message(message):
	if message.author == client:
		return

	if message.content.startswith('hello bot'):
		await message.channel.send(f'Hello {message.author.mention}!')
	
	await client.process_commands(message)

client.run(TOKEN)