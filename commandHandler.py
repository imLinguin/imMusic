from commands import ping, play, skip, queue, filter, remove, back, move
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

    cmd = cmd.lower()

    if cmd == "ping":
        await ping.run(message)
    elif cmd == "play" or cmd == "p":
        await play.run(message, args)
    elif cmd == "disconnect" or cmd == "fuckoff":
        await utils.destroy_queue(message.guild.id)
        await message.add_reaction("👋")
    elif cmd == "pause":
        utils.pause(message)
        await message.add_reaction("⏸")
    elif cmd == "skip" or cmd == "s":
        await skip.run(message)
        await message.add_reaction("⏭")
    elif cmd == "back":
        await back.run(message)
        await message.add_reaction("⏮")
    elif cmd == "queue" or cmd == "q":
        await queue.run(message)
    elif cmd == "filter":
        await filter.run(message, args)
    elif cmd == "remove" or cmd == "rm":
        await remove.run(message, args)
        await message.add_reaction("🗑")
    elif cmd == "move" or cmd == "mv":
        await move.run(message, args)
