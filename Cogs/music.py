import discord
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, columbina: commands.Bot):
        self.columbina = columbina

    #command to join
    @commands.command()
    async def join(self, ctx: commands.Context):
        #ignore bot
        if ctx.author.bot:
            return

        #check if user is in vc or not
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.reply(f"{ctx.author.mention} you need to be in a VC first!", silent = True)
            return

        #check if bot is already in a vc 
        if ctx.guild.voice_client:
            await ctx.reply(f"Im already in {ctx.guild.voice_client.channel.mention}")
            return

        #obtain user voice channel 
        voice_channel = ctx.author.voice.channel
        #if all conditions up fail then execute this and join    
        await voice_channel.connect()
        await ctx.reply(f"Joined {voice_channel.mention}",silent = True)

    #command to leave
    @commands.command()
    async def leave(self, ctx: commands.Context):
        #ignote bot
        if ctx.author.bot:
            return

        #check if user in vc
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.reply(f"{ctx.author.mention} you need to be in a VC!",silent = True)
            return

        #fetch user voice channel
        voice_channel = ctx.author.voice.channel

        #check if bot is in vc first
        if not ctx.guild.voice_client:
            await ctx.reply("Im not in any VC to leave!")
            return
        
        #check if user is in same vc as bot
        if ctx.guild.voice_client.channel == voice_channel:
            await ctx.guild.voice_client.disconnect()
            await ctx.reply(f"Left {voice_channel.mention}",silent = True)
        else:
            await ctx.reply(f"{ctx.author.mention} You need to be in same VC as me to make me leave!",silent = True)

#handshake setup
async def setup(columbina: commands.Bot):
    await columbina.add_cog(Music(columbina))
    print("Handshake completed, Music.py cog is now loaded")
