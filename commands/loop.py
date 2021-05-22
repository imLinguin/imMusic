from lib import utils
from discord import Embed, Color


async def run(message):
    if not await utils.check_voice_channel(message):
        await message.reply("You have to be in a voice channel")
        return

    if not utils.check_for_existing_queue(message):
        await message.reply("Nothing is playing")
        return

    queue = utils.get_queue(message.guild.id)

    queue.loop += 1

    if queue.loop > 2:
        queue.loop = 0

    mode = ""
    if queue.loop == 0:
        mode = "None"
    elif queue.loop == 1:
        mode = "Queue"
    elif queue.loop == 2:
        mode = "Song"
    await message.channel.send(embed=Embed(description="Now looping {0}".format(mode), colour=Color.from_rgb(141, 41, 255)), delete_after=5)
