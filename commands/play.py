from lib import utils
async def run(message,args,client):
    # Checks
    if not args:
        utils.resume(message)
        return
    if not await utils.checkVoiceChannel(message):
        await message.reply("You have to be in a voice channel")
        return
    if not await utils.checkChannelPerms(message):
        await message.reply("I don't have permissions to join or speak")
        return
    
    # Initialize queue when it's not present
    if not utils.checkForExistingQueue(message):
        await utils.createQueue(message)

    await utils.addToQueue(message,args,client.loop)