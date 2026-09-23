import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

#import the env file containing the token
load_dotenv(r"D:\\Code\\DC Bots\\Code Rework\\tokens.env")
#only import bot token
bot_token = os.getenv("Columbina_token")

#assign permissions
perms = discord.Intents.default()
#perms to read message stuff
perms.message_content = True

#prefix setting
columbina = commands.bot(command_prefix = '!co', intents = perms)

@columbina.event
async def on_ready():
    print("Columbina is Online!")
    #set bot status
    await columbina.change_presence(activity = discord.CustomActivity(name = ""))
