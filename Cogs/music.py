import discord
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, columbina: commands.Bot):
        self.columbina = columbina

#join function
@commands.command()
async def join(self, ctx: commands.Context):
    #ignore bots
    if ctx.author.bot:
        return

    #check if user in vc
    if not ctx.author.voice or not ctx.author.voice.channel:
        ctx.reply(f"{ctx.author.mention} Please join a vc first!", silent = True)
