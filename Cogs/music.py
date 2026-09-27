from discord.ext import commands
from utils.playerengine import get_audio
import discord
import asyncio
from utils.emojis import emoji

#contains basic join and leave commands
class Music(commands.Cog):
    def __init__(self, columbina: commands.Bot):
        self.columbina = columbina
        #store queues
        self.queues = {}

    #keep organized queue for servers
    def get_queue(self, guild_id: int):
        if guild_id not in self.queues:
            self.queues[guild_id] = []
        return self.queues[guild_id]

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

        #check if bot is in vc first
        if not ctx.guild.voice_client:
            await ctx.reply("Im not in any VC to leave!")
            return
        
        #check if user in vc
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.reply(f"{ctx.author.mention} you need to be in a VC!",silent = True)
            return

        #fetch user voice channel
        voice_channel = ctx.author.voice.channel

        #check if user is in same vc as bot
        if ctx.guild.voice_client.channel == voice_channel:
            await ctx.guild.voice_client.disconnect()
            await ctx.reply(f"Left {voice_channel.mention}",silent = True)
        else:
            await ctx.reply(f"{ctx.author.mention} You need to be in same VC as me to make me leave!",silent = True)

    #play command
    @commands.command()
    async def play(self, ctx: commands.Context, *,search: str):
        #1 ignore bot
        if ctx.author.bot:
            return

        #2 verify if user in vc
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.reply(f"{ctx.author.mention} You need to be in a VC!",silent = True)
            return

        #3 get user vc id
        voice_channel = ctx.author.voice.channel

        #4 check bot voice state too
        if not ctx.guild.voice_client:
            await voice_channel.connect()
        
        #verify if user in same vc
        elif ctx.author.voice.channel != ctx.guild.voice_client.channel:
            await ctx.reply(f"{ctx.author.mention} You need to be in same VC to add or play any songs!",silent = True)
            return

        #package the request in a dict format
        track_req = {
            "search": search,
            "requester": ctx.author.mention
        }

        #get server queue list
        queue = self.get_queue(ctx.guild.id)
        botvc = ctx.guild.voice_client

        #check if music is already playing
        if botvc.is_playing():
            queue.append(track_req)
            await ctx.reply(f"Your request {search} has been pushed to `Queue`!")
            return

        searching = (f"{emoji.devload} **Searching** for `{search}` on `Youtube`")
        await ctx.reply(searching, silent = True)
        #send request to engine
        source, title, thumbnail, duration = await get_audio(search)

        # Convert to HH:MM:SS format
        hours = duration // 3600
        minutes = (duration % 3600) // 60
        seconds = duration % 60
        duration_fixed = f"{hours:02}:{minutes:02}:{seconds:02}"

        #play
        ctx.guild.voice_client.play(source, after = lambda error: self.play_next(ctx))

        embed1 = discord.Embed(
            title = f"{emoji.musicspin} Now Playing",
            description = f"{emoji.youtube} **{title}**",
            color = discord.Color.blue()
        )
        embed1.add_field(name = "Requested by: ",value = ctx.author.mention)
        embed1.add_field(name = "Duration: ",value = duration_fixed)
        #set thumbnail if ytdlp found one
        if thumbnail:
            embed1.set_thumbnail(url = thumbnail)
        embed1.set_footer(text = "Query is defaulted to Youtube~\nReport any issues to @suranavillu/@suranavi")
    
        await ctx.reply(embed = embed1, silent = True)

    #manage the queue
    def play_next(self, ctx: commands.Context):
        queue = self.get_queue(ctx.guild.id)

        #check if any song in queue
        if queue:
            next_track = queue.pop(0)

            #schedule player to run in loop
            coro = self.start_playback(ctx, next_track)
            asyncio.run_coroutine_threadsafe(coro, self.columbina.loop)

    #start playing the queue
    async def start_playback(self, ctx: commands.Context, track: dict):
        #send loading msg
        loading = await ctx.reply(f"**Loading next song from `Queue`** {emoji.devload}",silent = True)

        #fetch data
        source, title, thumbnail, duration = await get_audio(track["search"])

        # Convert to HH:MM:SS format
        hours = duration // 3600
        minutes = (duration % 3600) // 60
        seconds = duration % 60
        duration_fixed = f"{hours:02}:{minutes:02}:{seconds:02}"

        #play
        ctx.guild.voice_client.play(source, after = lambda error: self.play_next(ctx))
        embed1 = discord.Embed(
            title = f"{emoji.musicspin} Now Playing",
            description = f"{emoji.youtube} **{title}**",
            color = discord.Color.blue()
        )
        embed1.add_field(name = "Requested by: ",value = ctx.author.mention)
        embed1.add_field(name = "Duration: ",value = duration_fixed)
        #set thumbnail if ytdlp found one
        if thumbnail:
            embed1.set_thumbnail(url = thumbnail)
        embed1.set_footer(text = "Query is defaulted to Youtube~")
        
        await ctx.reply(embed = embed1, silent = True)

    #skip
    @commands.command()
    async def skip(self, ctx: commands.Context):
        if ctx.author.bot:
            return

        #verify if user in vc
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.reply(f"{ctx.author.mention} You have to be in a VC first!",silent = True)
            return

        botvc = ctx.guild.voice_client

        #verify if user in same vc
        if not botvc or not botvc.is_playing():
            await ctx.reply("No song is playing right now to skip!",silent = True)
            return

        #if user in same vc
        if ctx.author.voice.channel != botvc.channel:
            await ctx.reply(f"{ctx.author.mention} You have to be in same VC to skip!")
            return

        #stop
        botvc.stop()
        await ctx.reply(f"{ctx.author.mention} Requested to skip current song",silent = True)

    #queue display
    @commands.command()
    async def queue(self, ctx: commands.Context):
        if ctx.author.bot:
            return

        #get queue
        queue = self.get_queue(ctx.guild.id)

        if not queue:
            await ctx.reply(f"{ctx.author.mention} the queue is currently empty, add some songs to fill it!",silent = True)
            return

        #format the queue to send
        queue_list = []
        for index, track in enumerate(queue, start = 1):
            queue_list.append(f"`{index}.` **{track['search']}** | Requested by: {track['requester']}")
        description_text = "\n".join(queue_list)

        embed = discord.Embed(
            title = f"{emoji.load} Upcoming queue:",
            description = description_text,
            color = discord.Color.purple()
        )
        await ctx.reply(embed = embed,silent = True)

#handshake setup
async def setup(columbina: commands.Bot):
    await columbina.add_cog(Music(columbina))
    print("Handshake completed, Music.py cog is now loaded")
