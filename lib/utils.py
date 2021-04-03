from lib import Queue
from lib import Track
import youtube_dl as ytdl

ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192', }]
    }

queues={}

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
    await queues[message.guild.id].voiceConnection.disconnect()
    queues[message.guild.id] = None

async def stream(message,query):
    queue = queues[message.guild.id]


