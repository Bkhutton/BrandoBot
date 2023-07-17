import discord
import urllib.request
import urllib.parse
import re
import yt_dlp

from discord.ext import commands
from collections import defaultdict

import config
from discord.ext import commands
from discord.ext.commands import Context


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.queue = defaultdict(list) # TODO move to audiocontroller


    def get_song_url(self, song):

        query_string = urllib.parse.urlencode({"search_query" : song})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
        video_ids = re.findall(r"watch\?v=(\S{11})", html_content.read().decode())
        return ("http://www.youtube.com/watch?v=" + video_ids[0])


    """
    Play Command:
        Params:
            - context: required parameter
            - url: Youtube URL to the song wanting to be played
        Description: Bot will join the user's current channel and play the song requested. Sequential play commands will
                    be added to a queue to be played later
    """
    @commands.command(name = "play", description = config.HELP_YT_LONG, help = config.HELP_YT_SHORT)
    async def _play(self, context: Context, *args, track: str):

        current_guild = context.guild

        if not current_guild:
            return

        if track.isspace() or not track:
            return
        
        if not context.author.voice or not context.author.voice.channel:
            await context.reply(config.NOT_CONNECTED_TO_CHANNEL, mention_author=True)
            return
        
        # old code
        # song = "{}".format(" ".join(args))
        url = self.get_song_url(track)
        
        # if(url == None):
        #     print("Include a song")
        #     await context.reply('')
        #     return

        # guild = context.guild


        # if context.author.voice == None:
        #     await context.send("Need to be in a voice channel to play music.")
        #     return

        # channel = context.author.voice.channel

        # if(channel == None):
        #     await context.send("Need to be in a channel to play music")
        #     return
        try:
            voice_client = await context.channel.connect()
        except Exception as e:
            voice_client = discord.utils.get(self.bot.voice_clients, guild=context.guild)
            print(e)


        def check_queue(error):
            if self.queue[context.guild.id] != []:
                source = self.queue[context.guild.id].pop(0)
                voice_client.play(source, after=check_queue)

        ydl_opts = {'format': 'bestaudio/best',
                    'verbose': True,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                        }],
                    }
        ffmpeg_opts = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -probesize 200M',
                       'options': '-vn'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=False)
            source = discord.FFmpegPCMAudio(source=result['url'], **ffmpeg_opts)
            if not voice_client.is_playing():
                voice_client.play(source, after=check_queue)
                await context.reply("Playing...", mention_author=True)
            else:
                self.queue[context.guild.id].append(source)
                await context.send("Adding song to queue...")

    """
    Pause Command:
        Params:
            - context: required parameter
        Description: Pauses the current AudioSource
    """
    @commands.command(name = "pause", help = "Pauses music")
    async def pause(self, context):
        guild = context.guild
        voice_client = discord.utils.get(self.bot.voice_clients, guild=guild)
        if(voice_client.is_paused()):
            await context.send("Already paused. Use !resume to continue playing!")
            return
        voice_client.pause()
        await context.send("Paused!")

    """
    Resume Command:
        Params:
            - context: required parameter
        Description: Resumes the current AudioSource
    """
    @commands.command(name = "resume", help = "Resumes music")
    async def resume(self, context):
        guild = context.guild
        voice_client = discord.utils.get(self.bot.voice_clients, guild=guild)
        if(voice_client.is_playing()):
            await context.send("Already playing music. Use !pause to pause playback")
            return
        voice_client.resume()
        await context.send("Resumed!")

    """
    Stop Command:
        Params:
            - context: required parameter
        Description: Stops all audio from playing and clears the music queue
    """
    @commands.command(name = "stop", help = "Stops the music bot")
    async def stop(self, context):
        guild = context.guild
        voice_client = discord.utils.get(self.bot.voice_clients, guild=guild)
        voice_client.stop()
        self.queue.clear()
        await voice_client.disconnect()
        await context.send("Stopped the music bot...Clearing Queue")

    """
    Skip Command:
        Params:
            - context: required parameter
        Description: Skips the current song playing and loads the next song in the queue
    """
    @commands.command(name = "skip", help = "Skips to the next song")
    async def skip(self, context):
        guild = context.guild
        voice_client = discord.utils.get(self.bot.voice_clients, guild=guild)
        voice_client.stop()
        #check_q(Exception,guild)
        # This needs to be fixed, janky workaround for now
        try:
            play.check_queue
        except:
            pass
        await context.send("Skipping...")

async def setup(bot):
    await bot.add_cog(Music(bot))
