from lib import utils


async def run(message, args):
    queue = utils.get_queue(message.guild.id)

    if not args or not args[0]:
        return
    args[0] = int(args[0])
    if args[0] > len(queue.tracks) or args[0] < 1:
        return

    if not await utils.check_voice_channel(message):
        await message.channel.send("You have to be in a voice channel")
        return

    queue.now_playing_index = args[0]-2
    queue.voice_connection.stop()
