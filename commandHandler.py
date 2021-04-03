from commands import ping,play

async def doStuff(message,client):
    msg = message.content[1:]
    splited = msg.split(" ")
    cmd = splited[0]
    splited.pop(0);
    args = splited;
    print("CMD: {0} ARGS: {1}".format(cmd,args))

    if cmd.lower() == "ping":
        await ping.run(message)
    elif cmd.lower() == "play":
        await play.run(message,args,client)
    