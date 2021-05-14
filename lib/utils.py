from logging import log
from time import time
from lib import Queue
from lib import Track
import youtube_dl
import discord
import asyncio
import time

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    "forcejson": True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    # bind to ipv4 since ipv6 addresses cause issues sometimes
    'source_address': '0.0.0.0'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
loop = asyncio.get_event_loop()
queues = {}


def _from_url(queue):
    parsed_filters = ""
    if len(queue.filters) > 0:
        parsed_filters += " -af " + ",".join(queue.filters)
    print(queue.start_time)
    ffmpeg_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn {0} -ss {1}'.format(parsed_filters, queue.start_time)
    }
    track = queue.tracks[0]
    return discord.FFmpegOpusAudio(track.stream_url, bitrate=64, codec="copy", **ffmpeg_options)


async def check_voice_channel(message):
    if not message.author.voice or not message.author.voice.channel:
        return False
    else:
        return True


async def check_channel_perms(message):
    member = message.author
    permissions = member.voice.channel.permissions_for(message.guild.me)

    if not permissions.connect or not permissions.speak:
        return False

    else:
        return True


def check_for_existing_queue(message):
    try:
        return queues[message.guild.id]
    except:
        return False


async def create_queue(message):
    queues[message.guild.id] = Queue.Queue(message, await message.author.voice.channel.connect())


async def delete_np(message):
    if queues[message.guild.id].now_playing != None:
        await queues[message.guild.id].now_playing.delete()


async def destroy_queue(message):
    queues[message.guild.id].player = None
    await queues[message.guild.id].voice_connection.disconnect()
    await delete_np(message)
    queues[message.guild.id] = None


async def add_to_queue(message, query):
    if len(query) > 1:
        query = " ".join(query)
    else:
        query = query[0]
    info = ytdl.extract_info(query, download=False)
    if "entries" in info:
        info = info["entries"][0]
    if not info:
        return
    new_track = Track.Track(query, info, message)
    queues[message.guild.id].tracks.append(new_track)
    await message.channel.send("Added **{0}** to queue".format(new_track.title))

    if not queues[message.guild.id].is_playing:
        stream(message)


def get_queue(message):
    return queues[message.guild.id]


def pause(message):
    queues[message.guild.id].voice_connection.pause()


def resume(message):
    try:
        if queues[message.guild.id] and queues[message.guild.id].voice_connection.is_paused():
            queues[message.guild.id].voice_connection.resume()
    except:
        pass


async def skip(message):
    queues[message.guild.id].player = None
    queues[message.guild.id].voice_connection.stop()


def stream_ended(e, message):
    if e:
        print("Player error {0}".format(e))
    elif check_for_existing_queue(message):
        queue = queues[message.guild.id]
        queue.is_playing = False
        if queue.filters_update:
            queue.filters_update = False
            queue.start_time = time.time(
            ) - queue.start_time
        else:
            queue.tracks.pop(0)
            queue.start_time = 0

        if len(queue.tracks) > 0:
            queue.voice_connection.stop()
            stream(message)
        else:
            fut = asyncio.run_coroutine_threadsafe(
                destroy_queue(message), loop)
            try:
                fut.result(0.2)
            except:
                pass
            print("Disconnecting from GUILD: {0}".format(message.guild.name))


def stream(message):
    queue = queues[message.guild.id]
    queue.player = _from_url(queue)
    queue.start_time = time.time()
    queue.voice_connection.play(queue.player,
                                after=lambda e: stream_ended(e, message))
    queue.is_playing = True
    func = asyncio.run_coroutine_threadsafe(
        send_embed(message), loop)

    try:
        func.result(0.2)
    except:
        pass


async def send_embed(message):
    embed = queues[message.guild.id].tracks[0].get_embed()
    await delete_np(message)
    queues[message.guild.id].now_playing = await message.channel.send(embed=embed)


async def filters_updated(message):
    queues[message.guild.id].filters_update = True
    queues[message.guild.id].voice_connection.stop()
