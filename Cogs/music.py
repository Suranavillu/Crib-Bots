import discord
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, columbina: commands.Bot):
        self.columbina = columbina