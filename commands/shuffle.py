from lib import utils
from random import shuffle


async def run(message):
    if not await utils.check_voice_channel(message):
        await message.channel.send("You have to be in a voice channel")
        return

    if not utils.check_for_existing_queue(message):
        await message.channel.send("Nothing is playing")
        return

    queue = utils.get_queue(message.guild.id)

    dont_touch = queue.tracks[:queue.now_playing_index+1]
    queue.tracks = queue.tracks[queue.now_playing_index+1:]
    shuffle(queue.tracks)
    queue.tracks = dont_touch + queue.tracks

    await message.channel.send("Shuffled 🔀")
