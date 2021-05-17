from lib import utils
import discord

filters = {
    "8D": "apulsator=hz=0.09",
    "bassboost": "bass=g=20",
    "echo": "aecho=in_gain=0.5:out_gain=0.5:delays=500:decays=0.2",
    "mono": 'pan=mono|c0=.5*c0+.5*c1',
    "nightcore": 'aresample=48000,asetrate=48000*1.25',
    "normalizer": "dynaudnorm=g=101",
    "subboost": 'asubboost',
}


async def run(message, args):
    # Shows all available filters if no queue is present
    if not utils.check_for_existing_queue(message):
        msg = ""
        for key in filters.keys():
            msg += key + "\n"
        embed = discord.Embed(
            title="List of available filters", description=msg, colour=discord.Color.from_rgb(35, 219, 201))
        await message.channel.send(embed=embed)
        return
    elif not args:
        queue = utils.get_queue(message)
        msg = ""
        for val in queue.filters:
            for name in filters.keys():
                if filters.get(name) == val:
                    msg += name + "\n"
                    break
        embed = discord.Embed(
            title="List of active filters", description=msg, colour=discord.Color.from_rgb(35, 219, 201))
        await message.channel.send(embed=embed)
        return
    queue = utils.get_queue(message)

    for requested in args:
        found = filters.get(requested.lower())
        deleted = False
        for i in range(len(queue.filters)):
            if queue.filters[i] == found:
                queue.filters.pop(i)
                deleted = True
                break

        if found and not deleted:
            queue.filters.append(found)
        elif not found:
            await message.channel.send("Couldn't match any filter with {0}".format(requested))

    await utils.filters_updated(message)
