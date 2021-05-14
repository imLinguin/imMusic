from commands import ping, play, skip, queue, filter
from lib import utils
import logging

logging.Logger("commands")
logger = logging.getLogger("commands")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename='logs/commands.log', encoding='utf-8', mode='w')
logger.addHandler(handler)


async def do_stuff(message, client):

    msg = message.content[1:]
    splited = msg.split(" ")
    cmd = splited[0]
    splited.pop(0)
    args = splited
    print("CMD: {0}; ARGS: {1}; GUILD: {2}".format(
        cmd, args, message.guild.name))
    logger.log(logging.INFO, "CMD: {0}; ARGS: {1}; GUILD: {2}".format(
        cmd, args, message.guild.name),)
    if cmd.lower() == "ping":
        await ping.run(message)
    elif cmd.lower() == "play":
        await play.run(message, args)
    elif cmd.lower() == "disconnect":
        await utils.destroy_queue(message)
    elif cmd.lower() == "pause":
        utils.pause(message)
    elif cmd.lower() == "skip":
        await skip.run(message)
    elif cmd.lower() == "queue":
        await queue.run(message)
    elif cmd.lower() == "filter":
        await filter.run(message, args)
