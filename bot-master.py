# This is the master code for the bot

# bot-master.py
import os
import youtube_dl

import discord
from discord.ext import commands
from discord import FFmpegPCMAudio

from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

ytdl_options = {
	'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0', 
	'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}]
}

ffmpeg_options = {
	'before_options': '-nostdin',
	'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_options)

class YoutubeSource(discord.PCMVolumeTransformer):
	def __init__(self, source, *, data, volume=1.0):
		super().__init__(source, volume)
		self.data = data
		self.title = data.get('title')
		self.url = data.get('webpage_url')
	
	@classmethod
	async def stream_url(cls, url, *, loop=None, download=False):
		data = ytdl.extract_info(url, download)
		if 'entries' in data:
			data = data['entries'][0]
		return cls(discord.FFmpegPCMAudio(data['url'], **ffmpeg_options), data=data)

client = commands.Bot(command_prefix='$')

@client.event
async def on_ready():
	print(f'{client.user.name} has connected to Discord!')
	guild = discord.utils.get(client.guilds, name=GUILD)
	print(f'{client.user.name} is connected to the following server:\n')
	print(f'{guild.name}(id:{guild.id})')
	await client.change_presence(activity=discord.Game("Jamming out to music"))

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


async def youtube_download(url):
	ydl_opts = {
		'format': 'bestaudio/best',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([url])


@client.command(name='download')
async def download(context, url):
	await youtube_download(url)

@client.command(name='stream')
async def youtube_stream(context, url):
	player = await YoutubeSource.stream_url(url, loop=client.loop, download=False)
	await joinVoice(context)
	if client.voice_clients:
		currentVoice = client.voice_clients[0]
		if not currentVoice.is_playing():
			currentVoice.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
			await context.message.channel.send(f'Now playing: {player.title}')
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