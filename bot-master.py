import os
import discord
import youtube_dl
import asyncio
from discord.ext import commands
from discord import FFmpegPCMAudio

### SET-UP Envoirnmental Variables
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
NAME = os.getenv('DISCORD_BOT_NAME')
DESC  = os.getenv('DISCORD_BOT_DESC')

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
		self.webpage = data.get('webpage_url')
		self.thumbnail = data.get('thumbnail')
		self.duration = data.get('duration')
	@classmethod
	async def from_url(cls, url, *, loop=None, stream=False): #Also supports basic query
		loop = loop or asyncio.get_event_loop()
		try:
			data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
		except:
			print(f'Caught error downloading link: {url}')
			return None
		if 'entries' in data:
			# take first item from a playlist
			data = data['entries'][0]
		filename = data['url'] if stream else ytdl.prepare_filename(data)
		return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class SongInfo():
	def __init__(self, author, title, url, duration, thumbnail=None):
		self.author = author
		self.title = title
		self.url = url
		self.duration = duration
		self.thumbnail = thumbnail

#Setup client prefix & Intents, queue
client = commands.Bot(command_prefix='!', intents=discord.Intents.all()) #Declare all intents for full perms
client.remove_command('help')
music_queue = []
global current_song 
current_song = SongInfo(None, '', None, None)
global loop_flag
loop_flag = False

# --- SETUP EVENT ---
@client.event
async def on_ready():
	print(f'{client.user.name} has connected to Discord!')
	print(f'{client.user.name} is connected to the following server:\n')
	for guild in client.guilds:
		print(f'{guild.name}(id:{guild.id})')
	await client.change_presence(activity=discord.Game("Jamming out to music"))

### --- CONNECT AND DISCONNECT COMMANDS ---
# - Connect -
# Will connect to voice channel of user
@client.command(name='connect')
async def joinVoice(context, msg=False):
	if not context.message.author.voice:
		await context.message.channel.send("You are not connected to a voice channel.")
	elif client.voice_clients:
		if context.message.author.voice.channel != client.voice_clients[0].channel:
			for joinedChannel in client.voice_clients:
				await joinedChannel.disconnect()
			await context.message.author.voice.channel.connect()
	else:
		await context.message.author.voice.channel.connect()
		if msg:
			await context.message.channel.send(f'Joined the {context.message.author.voice.channel.name} voice channel!')

# - Disconnect -
# Will disconnect from voice channel of user
@client.command(name='disconnect')
async def leaveVoice(context):
	for joinedChannel in client.voice_clients:
		await joinedChannel.disconnect()
		await context.message.channel.send("Successfully disconnected from voice channel.")

### --- LOGOUT COMMAND ---
# Will disconnect from voice channel and stop audio. Then will terminate program.
@client.command(name='logout')
async def logout(context):
	await leaveVoice(context)
	await context.message.channel.send("Bot signing off... See you next time!")
	await client.change_presence(status=discord.Status.offline)
	await client.close()

### --- MUSIC COMMANDS ---
# - Play Audio -
# Cannot play audio if another is playing. If audio is paused/stopped, will start a new audio and discard old
@client.command(name='play')
async def play(context):
	if not loop_flag:
		print(f'recieved play command: {context.message.content}')
	await joinVoice(context)
	if client.voice_clients:
		currentVoice = client.voice_clients[0]
		if not currentVoice.is_playing() and not currentVoice.is_paused():
			async with context.typing():
				url = context.message.content
				url = url.replace('!play ', '')
				#If used as !play download <url> you can download file. Slower but more accurate
				download_flag = False
				if url.startswith('download'):
					url = url.replace('download ', '')
					download_flag = True
					if not loop_flag:
						print(f'Downloading file: {url}')
					await context.message.channel.send(f'*Downloading file...*')

				#By default will stream
				youtubeSource = await YTDLSource.from_url(url, loop=client.loop, stream=not download_flag)
				if youtubeSource != None:
					await asyncio.sleep(0.5) #To help with song speeding up at start
					currentVoice.play(youtubeSource,after=lambda e: print('Player error: %s' % e) if e else play_next(context))
					global current_song 
					current_song = SongInfo(context.message.author, youtubeSource.title, youtubeSource.webpage, youtubeSource.duration, youtubeSource.thumbnail)
					if not loop_flag:
						print(f'Playing file: {youtubeSource.title}')
			if youtubeSource != None:
				if not loop_flag:
					await nowPlaying(context)
			else:
				await context.message.channel.send(f'**Error**: *Could not play given url.*')	
		else:
			await context.message.channel.send("Currently playing music. Please use !stop to stop current music.")

def play_next(context):
	if loop_flag:
		#print('Looping')
		asyncio.run_coroutine_threadsafe(play(context), client.loop)

# - Stop Audio -
# Will stop audio currently playing. Cannot resume audio.
@client.command(name='stop')
async def stop(context):
	if client.voice_clients:
		currentVoice = client.voice_clients[0]
		if currentVoice.is_playing():
			currentVoice.stop()
			if loop_flag:
				await loopToggle(context)
			await context.message.channel.send("Audio has been stopped and ended.")
		else:
			await context.message.channel.send("No audio is currently playing.")
	else:
		await context.message.channel.send("No audio is currently playing.")

# - Pause Audio -
# Will pause playing audio. Can replay audio through resume.
@client.command(name='pause')
async def pause(context):
	if client.voice_clients:
		currentVoice = client.voice_clients[0]
		if currentVoice.is_playing():
			currentVoice.pause()
			await context.message.channel.send("Audio has been paused!")
		else:
			await context.message.channel.send("No audio is currently playing.")
	else:
		await context.message.channel.send("No audio is currently playing.")

# - Resume Audio -
# Will resume a paused audio. Cannot resume stopped audio.
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

# - Loop Audio -
# Will toggle loop flag for song looping
@client.command('loop')
async def loopToggle(context):
	global loop_flag
	loop_flag = not loop_flag
	if loop_flag:
		await context.message.channel.send('Loop enabled.')
	else:
		await context.message.channel.send('Loop disabled.')

# - Show Current Audio -
# Will display information about the current song
@client.command(name='np')
async def nowPlaying(context):
	if current_song.title != '':
		minutes, seconds = divmod(current_song.duration, 60)
		embed = discord.Embed(title=current_song.title, 
		url=current_song.url, 
		description=f'Requested by **{current_song.author.display_name}**\nDuration: {minutes}:{seconds} minutes',
		colour=discord.Colour.blue())
		#embed.set_author(name=current_song.author.display_name, icon_url=current_song.author.display_avatar.url)
		embed.set_author(name='Now Playing ♫', icon_url='https://i.imgur.com/YDklpTp.jpg')
		if current_song.thumbnail != None:
			embed.set_thumbnail(url=current_song.thumbnail)
		await context.message.channel.send(embed=embed)
	else:
		await context.message.channel.send('No song is currently playing.')

### --- QUEUE COMMANDS ---

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
	embed.add_field(name='Current song\n', value=current_song.title)
	###Add for loop
	embed.add_field(name='\nNext songs', value=f'\n'.join(music_queue))
	await context.message.channel.send(embed=embed)


# --- INFORMATION ---
@client.command(name='help')
async def helpMenu(context):
	embed = discord.Embed(title=NAME, description= DESC, colour=discord.Colour.blue())
	commands = '''
	**!play [url / search query]**: streams the youtube url/search result
	**!play download [url / search query]**: downloads & plays the youtube url/search result
	**!stop**: stops & ends the current audio track
	**!pause**: pauses the current audio player
	**!resume**: resumes the paused audio player
	**!loop**: Toggles looping of current audio. Only works with url entry.'''
	embed.add_field(name='Commands\n', value=commands, inline=False)
	await context.message.channel.send(embed=embed)
# --- MESSAGE HANDLING ---
@client.event
async def on_message(message):
	if message.author == client.user:
		return
	
	print(f'Message from {message.author}: {message.content}') #Console print

	if message.content.startswith('hello bot'):
		await message.channel.send(f'Hello {message.author.mention}!')

	await client.process_commands(message)

client.run(TOKEN)