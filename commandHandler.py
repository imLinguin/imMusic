from commands import ping,play
from lib import utils

async def doStuff(message,client):
    msg = message.content[1:]
    splited = msg.split(" ")
    cmd = splited[0]
    splited.pop(0);
    args = splited;
    print("CMD: {0}; ARGS: {1}; GUILD: {2}".format(cmd,args,message.guild.name))

    if cmd.lower() == "ping":
        await ping.run(message)
    elif cmd.lower() == "play":
        await play.run(message,args,client)
    elif cmd.lower() == "disconnect":
        await utils.destroyQueue(message)
    elif cmd.lower() == "pause":
        utils.pause(message)