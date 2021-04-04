from lib import Queue
from lib import Track
import youtube_dl,discord,asyncio,re

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
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

async def _from_url(url):
    data = ytdl.extract_info(url,download=False)
    if "entries" in data:
        data = data["entries"][0]
    URL = data['url']
    return discord.FFmpegPCMAudio(URL, **ffmpeg_options)

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

async def addToQueue(message,query,loop):
    if len(query) > 1 or not re.search("https:\/\/"," ".join(query)):
        # Do zrobienia wyszukiwanie na yt
        query = " ".join(query)
        info = ytdl.extract_info(query)
        if info:
            queues[message.guild.id].tracks.append(Track.Track(query,info,message))
            await stream(message,loop)
    else:
        query = query[0]
    info = ytdl.extract_info(query)
    queues[message.guild.id].tracks.append(Track.Track(query,info,message))
    if not queues[message.guild.id].isPlaying:
        await stream(message,loop)

def pause(message):
    queues[message.guild.id].voiceConnection.pause()

def resume(message):
    if queues[message.guild.id].voiceConnection.is_paused():
        queues[message.guild.id].voiceConnection.resume()

async def stream(message,loop):
    track = queues[message.guild.id].tracks[0]
    queues[message.guild.id].player = await _from_url(track.url)
    queues[message.guild.id].voiceConnection.play(queues[message.guild.id].player, after=lambda e: print(f'Player error: {e}') if e else None)
    queues[message.guild.id].isPlaying = True