import os
import shutil
import random
import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

client = commands.Bot(command_prefix=">")
SONGS_DIR = 'Songs'

ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

@client.event
async def on_ready():
    print("Bot is ready")

@client.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit = amount+1)

@client.command()
async def join(ctx):
    await ctx.author.voice.channel.connect()    

@client.command()
async def play(ctx, url):
    
    vc = await ctx.author.voice.channel.connect()

    if 'watch?v=' in url:
        name = url[url.rfind('watch?v=') + len('watch?v=') + 1:]

    else:
        name = url[url.rfind('/') + 1:]

    if name + '.mp3' not in os.listdir(SONGS_DIR):

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file_name in os.listdir():
            if file_name.endswith('.mp3'):
                os.rename(file_name, name + '.mp3')

        shutil.move(os.path.join(name + '.mp3'), os.path.join(SONGS_DIR))

    if not vc.is_playing():
        vc.play(discord.FFmpegPCMAudio(executable = 'E:\\FFMpeg\\ffmpeg-20200515-b18fd2b-win64-static\\bin\\ffmpeg.exe', source = SONGS_DIR + '/' + name + '.mp3'))

    
@client.command()
async def disconnect(ctx):
    await ctx.voice_client.disconnect()

client.run('NzEyMzIxMzk5Mzg5NDIxNTk4.XsQqsQ.26O44I0Ko87KIejD4w28VDfxf98')