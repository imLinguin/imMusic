from lib import utils


async def run(message):
    utils.resume(message)
    await utils.skip(message)
