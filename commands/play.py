from lib import utils


async def run(message, args):
    # Checks
    if not args:
        utils.resume(message)
        return
    if not await utils.check_voice_channel(message):
        await message.reply("You have to be in a voice channel")
        return
    if not await utils.check_channel_perms(message):
        await message.reply("I don't have permissions to join or speak")
        return
    
    # Initialize queue when it's not present
    if not utils.check_for_existing_queue(message):
        await utils.create_queue(message)

    await utils.add_to_queue(message, args)
