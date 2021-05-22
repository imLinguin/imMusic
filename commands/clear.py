from lib import utils


async def run(message):
    queue = utils.get_queue(message.guild.id)

    if not await utils.check_voice_channel(message):
        await message.channel.send("You have to be in a voice channel")
        return

    if not queue:
        await message.channel.send("Queue for that server doesn't exist")
        return

    queue.tracks.clear()

    queue.voice_connection.stop()
