import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

#import the env file containing the token
load_dotenv(r"D:\Code\DC Bots\Code Rework\tokens.env")
#only import bot token
bot_token = os.getenv("Columbina_token")

#assign permissions
perms = discord.Intents.default()
#perms to read message stuff
perms.message_content = True

#loading the cog
class ColumbinaBot(commands.Bot):
    async def setup_hook(self):  
        #load music cog  
        await self.load_extension("cogs.Music")
        print("Music cog loaded successfully!")
        #load commands cog
        await self.load_extension("cogs.basicfunctions")
        print("Commands cog loaded successfully!")

#prefix setting
columbina = ColumbinaBot(command_prefix = '!co', intents = perms, help_command= None)

@columbina.event
async def on_ready():
    print("Columbina is Online!")
    #set bot status
    await columbina.change_presence(activity = discord.CustomActivity(name = "Singer of crib~"))

# Leave VC if no users are in it
@columbina.event
async def on_voice_state_update(member, before, after):
    voice_client = member.guild.voice_client

    # 1. Exit immediately if the bot isn't connected to a voice channel
    if not voice_client or not voice_client.channel:
        return

    # 2. Count real users in the bot's channel
    users_in_vc = [m for m in voice_client.channel.members if not m.bot]

    # 3. Disconnect if empty
    if len(users_in_vc) == 0:
        await voice_client.disconnect()


columbina.run(bot_token)
