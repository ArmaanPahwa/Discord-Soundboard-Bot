# Discord-Musicbot

Enhance your discord experience with this Discord Musicbot! This bot will allow users to listen to their own custom music downloads and links in any of their voicechannels! 

## Commands
- **!play** `url`/`query`: Joins voice channel of user and streams the specified youtube url / first result of query
- **!play download** `url`/`query`: Joins voice channel of user and downloads the specified youtube url / first result of query. Then plays it from file
- **!stop**: Stops playing the current audio song
- **!pause**: Pauses the audio
- **!resume**: Resumes the audio
- **!logout**: Disconnects from any active voice and disconnects from discord
- **!connect**: Connects to voice (debug)
- **disconnect**: Disconnects to voice (debug)

## Current Functionality
- Join Discord Guild/Server's voice-chat
- Play youtube audio through download
- Play youtube audio through streaming

## To-Do
- Implement pause/resume command
- Implement a queue system
- Implement song skipping

## Technologies Used
- **[VScode](https://code.visualstudio.com/)**: Code editor
- **[Discord](https://discord.com/)**: Digital communication application
- **[FFmpeg](https://ffmpeg.org/download.html)**: Audio source converter

## How to install
This bot is to be used on the [Discord](https://discord.com/) platform. As such, you must create an account to be able to use the application and bot. 

### Creating the bot information
Once an account is created, follow these steps:
1. Navigate to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click the "Create Application" button at the top right.
3. Give a ***unique name*** to your application and click the create button.
4. Once created, navigate to the `BOT` tab on the left menu.
5. Click on "Add Bot" and then confirm with "Yes, do it!".
6. Your bot has been created!

### Adding the bot to your Guild/Server
With the bot now being created, you must add it to your Discord Guild/Server. Follow these steps:
1. Navigate to the "OAuth2" Tab.
2. Under scopes, select the box next to "bot".
3. Under the bot permissions section below, select the permissions for your bot. I have used the "Administrator" settings.
4. In the scopes section, click copy next to the generated link.
5. Paste the link into a new tab and select your Guild/Server to join.

### Update Bot Permissions
To properly allow your bot to interact, we must update the intents of the bot.
1. Navigate to the `BOT` tab on the left menu.
2. Scroll down to the Privileged Gateway Intents section
3. Select the radio button for PRESENCE INTENT, SERVER MEMBERS INTENT, and MESSAGE CONTENT INTENT

### Installing/Managing Packages
Your bot now has access to your Guild/Server. The final steps to get the bot running is as follows:
1. Install the packages listed in the "Packages" section.
  - Ensure that [FFmpeg](https://ffmpeg.org/download.html) has been added to PATH or it's OS equivallent.

If the [dotenv](https://github.com/theskumar/python-dotenv) package is installed, preform the following steps: 
1. Create a file in the directory with the `bot-master.py` called `.env`.
2. Under the "Bot" tab of the Application Page on the Developer Portal, click the Copy Button under the Token section.
3. Add the following line:
   ```shell
   DISCORD_TOKEN=<your Discord Bot Token copied from the Developer Portal>
   ```
4. Replace `<your Discord Bot Token copied from the Developer Portal>` with your copied Token.

If this package was not installed, open the `bot-master.py` in an editor and do the following:
1. Delete the following lines of code:
   ```shell
   from dotenv import load_dotenv
   load_dotenv()
   TOKEN = os.getenv('DISCORD_TOKEN')
   ```
2. Replace the `TOKEN` in the following line with your copied Discord Bot token:
   ```shell
   client.run(TOKEN)
   ```

### Running the Bot
You should now be able to run the `bot.py` with full functionality through command-line!

## Packages
***Ensure you have [Python](https://www.python.org/downloads/) Downloaded***
- [pip](https://pypi.org/project/pip/) to aid in installing packages
- [discord.py](https://pypi.org/project/discord.py/) `pip install -U discord.py`
  - If installing through link, ensure voice is also installed.
- [dotenv](https://github.com/theskumar/python-dotenv) `pip install -U python-dotenv`
  - Not required for use. If not installed, following the instructions in the "How To Use" section above.
- [FFmpeg](https://ffmpeg.org/download.html)
  - FFmpeg is required to convert audio into a format Discord can understand. Please reference either of the following guides for how to install FFmpeg and add it to PATH:
    - Windows: [WindowsLoop.com](https://windowsloop.com/install-ffmpeg-windows-10/)
    - Linux: [Ubuntu Pit](https://www.ubuntupit.com/how-to-install-and-use-ffmpeg-on-linux-distros-beginners-guide/)
- [youtube_dl](https://youtube-dl.org/) `pip install -U youtube_dl`
  - youtube_dl is required to download and stream audio clips from youtube
## Contributing
### Bugs or Features
You can open a new issue [through this](https://github.com/ArmaanPahwa/Discord-Soundboard-Bot/issues/new) with the information and description.

####
## References
The following resources were referenced when developing the code:
- [Discord.py API Documentation](https://discordpy.readthedocs.io/en/latest/index.html): Official API documentation for the discord.py package
- [Official discord.py Github](https://github.com/Rapptz/discord.py): Official discord.py github for developers to reference
-[PythonLand tutorial](https://python.land/build-discord-bot-in-python-that-plays-music): Guide for downloading & streaming youtube files (2023 updated method)
- [Fix Youtube Streaming](https://stackoverflow.com/questions/60241517/discord-py-rewrite-and-youtube-dl): Fix for how to stream music based on official github repo
- [Ajay Gandecha](https://www.youtube.com/playlist?list=PLfpeXtDSa8rWW02LOjl2IW9_TLfcp_mZr): Youtube series for basic discord bot functionality
- [Beau Carnes, Freecodecamp.org](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/): Guide for beginners creating a discord bot
- [Alex Ronquillo, realpython.com](https://realpython.com/how-to-make-a-discord-bot-python/): Guide for beginners creating a discord bot