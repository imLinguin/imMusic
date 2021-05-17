from lib import utils


async def run(message, args):
    queue = utils.get_queue(message)
    if not queue:
        await message.channel.send("No queue found on this server")
        return
    if not args:
        await message.channel.reply("You have to pass a song number in queue.")
        return

    length = len(queue.tracks)

    selected = int(args[0])
    selected_second = int(args[1])

    if not selected <= length and selected > 0:
        await message.reply("Well, id is invalid")
        return
    if not selected_second <= length and selected_second > 0:
        await message.reply("Well, second id is invalid")
        return
    if queue.tracks[selected-1] and queue.tracks[selected_second-1]:
        track = queue.tracks.pop(selected-1)
        queue.tracks.insert(selected_second-1, track)
    else:
        await message.channel.reply("This id is invalid")
