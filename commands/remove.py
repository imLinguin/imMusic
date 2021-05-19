from lib import utils


async def run(message, args):
    queue = utils.get_queue(message.guild.id)
    if not queue:
        await message.channel.send("Not queue found for this server")
        return
    if not args:
        await message.channel.reply("You have to pass a song number in queue.")
        return

    length = len(queue.tracks)

    selected = int(args[0])
    if not selected <= length and selected > 0:
        await message.reply("Well, id is invalid")
        return
    if queue.tracks[selected-1]:
        queue.tracks.pop(selected-1)
    else:
        await message.channel.reply("This id is invalid")
