import math
from lib import utils
from discord import Embed, Color


async def run(message):
    queue = utils.get_queue(message.guild.id)
    output = ""

    if not queue:
        await message.channel.send("No queue found on this server")
        return
    page = queue.queue_page
    available_pages = len(queue.tracks) / 15
    if page < 0:
        page = 0
    elif page > available_pages:
        page = math.ceil(available_pages)
    counter = (page * 15)+1

    if len(queue.tracks) >= 1:
        for i in get_tracks_from_to(1+(15*page), 14+(15*page), queue):
            if queue.now_playing_index + 1 == counter:
                output += "🔴 "
            output = output + "{0}. {1}\n".format(counter, i.title)
            counter += 1
    if output:
        if not queue.queue_message:
            queue.queue_message = await message.channel.send("Page {0}```{1}```".format(page+1, output))
            if available_pages > 1:
                await queue.queue_message.add_reaction("⬆")
                await queue.queue_message.add_reaction("⬇")
                await queue.queue_message.add_reaction("❌")
        else:
            await queue.queue_message.edit(content="Page {0}```{1}```".format(page+1, output))
        await queue.queue_message.add_reaction("❌")
    else:
        await message.channel.send(embed=Embed(description="Queue is empty!", colour=Color.from_rgb(237, 19, 19)))


def get_tracks_from_to(from_, to, queue):
    return queue.tracks[from_ - 1:to+1]
