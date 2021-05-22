from lib import utils


async def run(message, args):
    # Checks
    if not args:
        if not utils.resume(message):
            await message.channel.send("What are you trying to resume? WTF")
        else:
            await message.add_reaction("▶")
        return
    if not await utils.check_voice_channel(message):
        await message.channel.send("You have to be in a voice channel")
        return
    if not await utils.check_channel_perms(message):
        await message.channel.send("I don't have permissions to join or speak")
        return
    if len(args) > 1:
        args = " ".join(args)
    else:
        args = args[0]
    is_valid = utils.check_supported(args)
    if not is_valid:
        await message.add_reaction("❌")
        return
    else:
        await message.add_reaction("✅")
    # Initialize queue when it's not present
    if not utils.check_for_existing_queue(message):
        await utils.create_queue(message)

    await utils.add_to_queue(message, args)
