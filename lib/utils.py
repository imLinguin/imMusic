from time import time
from lib import Queue
from lib import Track
import youtube_dl
from discord import Embed, FFmpegOpusAudio, Color, colour
import asyncio
import time
import re

ytdl_format_options = {
    'format': 'bestaudio/best[height<=720]/mp3',
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
queues_to_check = []


def _from_url(queue):
    parsed_filters = ""
    if len(queue.filters) > 0:
        parsed_filters += " -af " + ",".join(queue.filters)
    ffmpeg_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn {0} -ss {1}'.format(parsed_filters, queue.start_time)
    }
    track = queue.tracks[queue.now_playing_index]
    return FFmpegOpusAudio(track.stream_url, bitrate=256, **ffmpeg_options)


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


async def delete_np(id):
    if queues[id].now_playing != None:
        await queues[id].now_playing.delete()


async def destroy_queue(id):
    queues[id].player = None
    print("Deleting queue from GUILD: {0}".format(id))
    try:
        await queues[id].voice_connection.disconnect()
    except:
        pass
    await delete_np(id)
    queues[id] = None


def check_supported(url):
    ies = youtube_dl.extractor.gen_extractors()
    for ie in ies:
        if (ie.suitable(url) and ie.IE_NAME != 'generic') or not re.match("://", url):
            # URL is supported
            return True
    return False


async def add_to_queue(message, query):
    info = None
    try:
        info = ytdl.extract_info(query, download=False)

        if not info:
            return
        if "entries" in info:
            info = info["entries"][0]
    except:
        await message.reply(embed=Embed(description="No results found!", colour=Color.from_rgb(237, 19, 19)))
        queues_to_check.append(message.guild.id)
        return
    try:
        queues_to_check.remove(message.guild.id)
    except:
        pass
    new_track = Track.Track(query, info, message)
    queues[message.guild.id].tracks.append(new_track)
    description = ""
    if not re.match("://", new_track.url):
        description = "Queued **{0}**".format(new_track.title)
    else:
        description = "Queued **[{0}]({1})**".format(
            new_track.title, new_track.url)
    embd = Embed(description=description, colour=Color.from_rgb(141, 41, 255))
    await message.channel.send(embed=embd)

    if not queues[message.guild.id].is_playing:
        stream(message)


def get_queue(id):
    return queues.get(id)


def pause(message):
    queues[message.guild.id].voice_connection.pause()


def resume(message):
    try:
        if queues[message.guild.id] and queues[message.guild.id].voice_connection.is_paused():
            queues[message.guild.id].voice_connection.resume()
            return True
    except:
        pass
    return False


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
            queue.now_playing_index += 1
            queue.start_time = 0

        if len(queue.tracks) > queue.now_playing_index:
            queue.voice_connection.stop()
            stream(message)
        else:
            queue.end_time = time.time()
            queues_to_check.append(queue.guild_id)


def stream(message):
    queue = queues[message.guild.id]
    queue.player = _from_url(queue)
    queue.start_time = time.time()
    queue.voice_connection.play(
        queue.player, after=lambda e: stream_ended(e, message))
    queue.is_playing = True
    func = asyncio.run_coroutine_threadsafe(
        send_embed(message), loop)

    try:
        func.result(0.2)
    except:
        pass


async def send_embed(message):
    embed = queues[message.guild.id].tracks[queues[message.guild.id].now_playing_index].get_embed()
    await delete_np(message.guild.id)
    queues[message.guild.id].now_playing = await message.channel.send(embed=embed)


async def filters_updated(message):
    queues[message.guild.id].filters_update = True
    queues[message.guild.id].voice_connection.stop()


def check_disconnection():
    while True:
        for id in queues_to_check:
            queue = queues.get(id)
            if queue:
                time_passed = time.time() - queue.end_time
                if time_passed > 2 * 60:
                    try:
                        asyncio.run_coroutine_threadsafe(
                            destroy_queue(queue.guild_id), loop).result(0.2)
                    except:
                        pass
                    queues_to_check.remove(id)
            else:
                queues_to_check.remove(id)
        time.sleep(10)
