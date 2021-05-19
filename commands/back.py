from lib import utils


async def run(message):
    if not await utils.check_voice_channel(message):
        await message.reply("You have to be in a voice channel")
        return
    if not utils.check_for_existing_queue(message):
        await message.reply("No queue found on this server")
        return

    queue = utils.get_queue(message.guild.id)

    queue.now_playing_index -= 2
    queue.voice_connection.stop()
