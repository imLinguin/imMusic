from lib import Queue
from lib import Track
import youtube_dl,discord,asyncio,re

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    "forcejson":True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

queues={}

def _from_url(url):
    data = ytdl.extract_info(url,download=False)
    if "entries" in data:
        data = data["entries"][0]
    URL = data['url']
    return discord.FFmpegOpusAudio(URL, **ffmpeg_options)

async def checkVoiceChannel(message):
    if not message.author.voice or not message.author.voice.channel:
            return False
    else:
        return True

async def checkChannelPerms(message):
    member = message.author
    permisions = member.voice.channel.permissions_for(message.guild.me)

    if not permisions.connect or not permisions.speak:
        return False
    
    else:
        return True

def checkForExistingQueue(message):
    try:
        return queues[message.guild.id]
    except:
        return False

async def createQueue(message):
    queues[message.guild.id] = Queue.Queue(message,await message.author.voice.channel.connect())

async def destroyQueue(message):
    ytdl.cache.remove()
    queues[message.guild.id].player = None
    await queues[message.guild.id].voiceConnection.disconnect()
    queues[message.guild.id] = None

async def addToQueue(message,query):
    
    if len(query) > 1:
        query = " ".join(query)
    else:
        query = query[0]
    info = ytdl.extract_info(query,download=False)
    if "entries" in info:
        info = info["entries"][0]
    if not info:
        return
    newTrack = Track.Track(query,info,message)
    queues[message.guild.id].tracks.append(newTrack)
    await message.channel.send("Added **{0}** by {1} to queue".format(newTrack.title,newTrack.author))

    if not queues[message.guild.id].isPlaying:
        stream(message)

def pause(message):
    queues[message.guild.id].voiceConnection.pause()

def resume(message):
    if queues[message.guild.id].voiceConnection.is_paused():
        queues[message.guild.id].voiceConnection.resume()

def skip(message):
    print("Skip")

def streamEnded(e,message):
    if e != None:
        print("Player error {0}".format(e))
    elif checkForExistingQueue(message):
        queues[message.guild.id].isPlaying = False
        queues[message.guild.id].tracks.pop(0)
        if len(queues[message.guild.id].tracks) > 0:
            stream(message)

def stream(message):
    track = queues[message.guild.id].tracks[0]
    queues[message.guild.id].player = _from_url(track.url)
    queues[message.guild.id].voiceConnection.play(queues[message.guild.id].player, after=lambda e: streamEnded(e,message))
    queues[message.guild.id].isPlaying = True