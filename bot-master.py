import os
import discord
import youtube_dl
from discord.ext import commands
from discord import FFmpegPCMAudio

### SET-UP Envoirnmental Variables
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# -- MUSIC --
youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
	'format': 'bestaudio/best',
	'restrictfilenames': True,
	'noplaylist': True,
	'nocheckcertificate': True,
	'ignoreerrors': False,
	'logtostderr': False,
	'quiet': True,
	'no_warnings': True,
	'default_search': 'auto',
	'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ffmpeg_options = {
	'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
class YTDLSource(discord.PCMVolumeTransformer):
	def __init__(self, source, *, data, volume=0.5):
		super().__init__(source, volume)
		self.data = data
		self.title = data.get('title')
		self.url = data.get('url')
	@classmethod
	async def from_url(cls, url, *, loop=None, stream=False):
		loop = loop or asyncio.get_event_loop()
		data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
		if 'entries' in data:
			# take first item from a playlist
			data = data['entries'][0]
		filename = data['url'] if stream else ytdl.prepare_filename(data)
		return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

#Setup client prefix & Intents, queue
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
music_queue = []
current_song = ""

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
			async with context.typing():
				url = context.message.content
				url = url.replace('!play ', '')
				#If used as !play download <url> you can download file. Slower but more accurate
				download_flag = False
				if url.startswith('download'):
					url = url.replace('download ', '')
					download_flag = True
					print(f'Downloading file: {url}')

				#By default will stream
				youtubeSource = await YTDLSource.from_url(url, loop=client.loop, stream=not download_flag)
				currentVoice.play(youtubeSource,after=lambda e: print('Player error: %s' % e) if e else None)
				print(f'Playing file: {youtubeSource.title}')
			await context.message.channel.send(f'**Now Playing:** {youtubeSource.title}')
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

@client.command(name='add')
async def add(context):
	title = context.message.content
	title = title.replace('!add ', '')
	music_queue.append(title)
	await context.message.channel.send(f'Added song: `{title}` to the queue.')

@client.command(name='remove')
async def remove(context):
	position = context.message.content
	position = position.replace('!remove ', '')
	try:
		pos = int(position)
		pos -= 1 #If 1 is entered, position in list is 0
		if pos < 0 or pos >= len(music_queue):
			await context.message.channel.send(f'Error, please enter a valid position')
		else:
			title = music_queue.pop(pos)
			await context.message.channel.send(f'Removed song: `{title}`')
	except ValueError:
		await context.message.channel.send(f"Please enter a valid numerical input {context.message.author.mention}")

@client.command(name='queue')
async def showQueue(context):
	embed = discord.Embed(title=f'Music Queue', colour=discord.Colour.blue())
	embed.add_field(name='Current song\n', value=current_song)
	###Add for loop
	embed.add_field(name='\nNext songs', value=f'\n'.join(music_queue))
	await context.message.channel.send(embed=embed)


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