from lib import utils


async def run(message):
    queue = utils.get_queue(message)
    output = ""
    if not queue:
        await message.channel.send("No queue found on this server")
        return
    counter = 1
    if len(queue.tracks) >= 1:
        for i in queue.tracks:
            if queue.now_playing_index + 1 == counter:
                output += "🔴 "
            output = output + "{0}. {1}\n".format(counter, i.title)
            counter += 1
    await message.channel.send("```{0}```".format(output))
