from lib import utils


async def run(message):
    if not await utils.check_voice_channel(message):
        await message.channel.send("You have to be in a voice channel")
        return
    if not utils.get_queue(message.guild.id):
        await message.channel.send("No queue found on this server")
        return
    utils.resume(message)
    await utils.skip(message)
