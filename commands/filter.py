from lib import utils
import discord

filters = {
    "bassboost": "bass=g=20",
    "normalizer": "dynaudnorm=g=101",
    "echo": "aecho=in_gain=0.5:out_gain=0.5:delays=500:decays=0.2",
}


async def run(message, args):
    # Checks
    if not args or not utils.check_for_existing_queue(message):
        msg = ""
        for key in filters.keys():
            msg += key + "\n"
        embed = discord.Embed(
            title="List of available filters", description=msg)
        await message.channel.send(embed=embed)
        return

    requested = args[0]
    found = None
    try:
        found = filters[requested.lower()]
    except:
        await message.channel.send("There is no filter with that name")
        return

    queue = utils.get_queue(message)
    deleted = False
    for i in range(0, len(queue.filters)):
        if queue.filters[i] == found:
            queue.filters.pop(i)
            deleted = True

    if not deleted:
        queue.filters.append(found)

    await utils.filters_updated(message)
