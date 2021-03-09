# Discord-Soundboard-Bot

Enhance your discord experience with this Discord Soundboard Bot! This bot will allow users to create their own custom sounboards and store their favorite sounds to play in voice channels at anytime!

## Current Functionality
- Join Discord voice-chat
- Play local audio file indentified in Source code

## To-Do
- Play audio from remote source
- Create separate soundboard for each user
- Ability to manipulate user soundboard
- Admin controls

## Technologies Used
- **[VScode](https://code.visualstudio.com/)**: Code editor
- **[Discord](https://discord.com/)**: Digital communication application

## How to use
This bot is to be used on the [Discord](https://discord.com/) platform. As such, you must create an account to be able to use the application and bot. 

### Creating the bot information
Once an account is created, follow these steps:
1. Navigate to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click the "Create Application" button at the top right.
3. Give a ***unique name*** to your application and click the create button.
4. Once created, navigate to the bot tab.
5. Click on "Add Bot" and then confirm with "Yes, do it!".
6. Your bot has been created!

### Adding the bot to your Guild/Server
With the bot now being created, you must add it to your Discord Guild/Server. Follow these steps:
1. Navigate to the "OAuth2" Tab.
2. Under scopes, select the box next to "bot".
3. Under the bot permissions section below, select the permissions for your bot. I have used the "Administrator" settings.
4. In the scopes section, click copy next to the generated link.
5. Paste the link into a new tab and select your Guild/Server to join.


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
You should now be able to run the `bot-master.py` with full functionality through command-line!

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

## Contributing
### Bugs or Features
You can open a new issue [through this](https://github.com/ArmaanPahwa/Discord-Soundboard-Bot/issues/new) with the information and description.

####
## References
The following resources were referenced when developing the code:
- [Discord.py API Documentation](https://discordpy.readthedocs.io/en/latest/index.html): Official API documentation for the discord.py package
- [Ajay Gandecha](https://www.youtube.com/playlist?list=PLfpeXtDSa8rWW02LOjl2IW9_TLfcp_mZr): Youtube series for basic discord bot functionality
- [Beau Carnes, Freecodecamp.org](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/): Guide for beginners creating a discord bot
- [Alex Ronquillo, realpython.com](https://realpython.com/how-to-make-a-discord-bot-python/): Guide for beginners creating a discord bot
