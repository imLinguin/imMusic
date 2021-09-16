from time import time
from lib import Queue
from lib import Track
from lib import spotify
import youtube_dl
from discord import Embed, FFmpegOpusAudio, Color
import asyncio
import time
import re
import math

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
    return FFmpegOpusAudio(track.stream_url, bitrate=queue.bitrate, **ffmpeg_options)


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
    if queues.get(id).now_playing:
        await queues[id].now_playing.delete()
        queues.get(id).now_playing = None


async def destroy_queue(id):
    await delete_np(id)
    queue = queues.get(id)
    queue.player = None
    print("Deleting queue from GUILD: {0}".format(id))
    try:
        await queue.voice_connection.disconnect()
        if queue.queue_message:
            await queue.queue_message.delete()
    except:
        pass
    del queues[id]


def check_supported(url):
    ies = youtube_dl.extractor.gen_extractors()
    for ie in ies:
        if (ie.suitable(url) and ie.IE_NAME != 'generic') or not re.match("://", url) or spotify.is_playlist(url) or spotify.is_track(url):
            # URL is supported
            return True
    return False


async def announce_single_song(track, channel):
    description = ""
    if not re.match("://", track.url):
        description = "Queued **{0}** [{1}]".format(
            track.title, track.requestedBy.mention)
    else:
        description = "Queued **[{0}]({1})** [{2}]".format(
            track.title, track.url, track.requestedBy.mention)
    embd = Embed(description=description, colour=Color.from_rgb(
        141, 41, 255))
    await channel.send(embed=embd, delete_after=20)


async def add_to_queue(message, query):
    info = None
    if spotify.is_track(query):
        info = spotify.get_track(query)
        new_track = Track.Track(query, info, message)
        queues[message.guild.id].tracks.append(new_track)
        await announce_single_song(new_track, message.channel)
    elif spotify.is_playlist(query):
        info = spotify.get_playlist(query)
        tracks_count = len(info)
        for track in info:
            queues[message.guild.id].tracks.append(
                Track.Track(query, track, message))

        embd = Embed(description="Queued **{0}** tracks".format(
            tracks_count), colour=Color.from_rgb(141, 41, 255))
        await message.channel.send(embed=embd, delete_after=20)
    else:
        try:
            info = ytdl.extract_info(query, download=False)
            if not info:
                return
            if "entries" in info:
                info = info["entries"][0]
            info["cover"] = info.get("thumbnail")
        except:
            await message.channel.send(embed=Embed(description="No results found or content is 18+", colour=Color.from_rgb(237, 19, 19)))
            if len(queues[message.guild.id].tracks) == 0:
                queues[message.guild.id].end_time = time.time()
                queues_to_check.append(message.guild.id)
            return
        new_track = Track.Track(query, info, message)
        await announce_single_song(new_track, message.channel)
        queues[message.guild.id].tracks.append(new_track)
    try:
        queues_to_check.remove(message.guild.id)
    except:
        pass
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
            if queue.loop != 2:
                queue.now_playing_index += 1
            queue.start_time = 0

        if len(queue.tracks) > queue.now_playing_index:
            queue.voice_connection.stop()
            stream(message)
        elif queue.loop == 1:
            queue.voice_connection.stop()
            queue.now_playing_index = 0
            stream(message)
        else:
            queue.end_time = time.time()
            queues_to_check.append(queue.guild_id)


def stream(message):
    queue = queues[message.guild.id]
    current = queue.tracks[queue.now_playing_index]

    if not current.stream_url:
        info = ytdl.extract_info("{1} {0}".format(
            current.title, current.author), download=False)
        if "entries" in info:
            info = info["entries"][0]
        current.stream_url = info.get("url")
        current.duration = info.get("duration")
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


def gen_progress_bar(start_time, duration):
    progress = "**["
    fill = "█"
    empty = "▁"
    width = 15
    current = time.time() - start_time
    minutes_start = math.floor(current/60)
    seconds_start = math.floor(current - (math.floor(current/60)*60))
    if minutes_start < 10:
        minutes_start = f"0{minutes_start}"
    if seconds_start < 10:
        seconds_start = f"0{seconds_start}"
    minutes_end = math.floor(duration/60)
    seconds_end = math.floor(duration - (math.floor(duration/60)*60))
    if minutes_end < 10:
        minutes_end = f"0{minutes_end}"
    if seconds_end < 10:
        seconds_end = f"0{seconds_end}"

    formatted_start = f"{minutes_start}:{seconds_start} "
    formatted_end = f" {minutes_end}:{seconds_end}"
    percentage = (current / duration)

    filled = round(width * percentage)
    emptyed = width - filled
    for i in range(filled):
        progress += fill
    for i in range(emptyed):
        progress += empty
    return formatted_start + progress + "]**" + formatted_end


async def send_embed(message):
    queue = queues[message.guild.id]
    track = queue.tracks[queue.now_playing_index]
    next_track = ""
    if len(queue.tracks) > 1 and queue.now_playing_index + 1 < len(queue.tracks):
        next_track = queue.tracks[queue.now_playing_index + 1].title
    else:
        next_track = "None"
    embed = Embed(title=track.title,
                  description=f"{gen_progress_bar(queue.start_time, track.duration)}", color=Color.from_rgb(0, 241, 183))
    embed.set_thumbnail(url=track.cover)
    embed.add_field(name="Next", value=next_track)
    embed.add_field(name="Requested by", value=track.requestedBy.mention)
    if not queue.now_playing:
        queue.now_playing = await message.channel.send(embed=embed)
        await queue.now_playing.add_reaction("⏮")
        await queue.now_playing.add_reaction("⏯")
        await queue.now_playing.add_reaction("⏭")
        await queue.now_playing.add_reaction("⏹")
        await queue.now_playing.add_reaction("🔀")
        await queue.now_playing.add_reaction("🔃")
    else:
        await queue.now_playing.edit(embed=embed)
    queue.now_playing_interval_helper = time.time()


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
        for id in queues.keys():
            if queues[id].now_playing and queues[id].is_playing and (time.time() - queues[id].now_playing_interval_helper) > 30:
                try:
                    asyncio.run_coroutine_threadsafe(
                        send_embed(queues[id].now_playing), loop).result(0.2)
                except:
                    pass
        time.sleep(10)
