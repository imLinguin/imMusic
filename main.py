from discord import Client, Activity, ActivityType, Embed, Color
import os
from dotenv import load_dotenv
import logging
# Bot modules
from handlers import commandHandler, reactionHandler
from lib import utils
load_dotenv()
client = Client()
# Logging utility
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename='logs/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Infinite loop to check every guild where queue ended to disconnect
utils.check_disconnection


@client.event
async def on_ready():
    print('Zalogowano jako {0.user}'.format(client))
    await client.change_presence(activity=Activity(
        name="Top Discord music bots", type=ActivityType.competing))
    print('------')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('*'):
        await commandHandler.do_stuff(message, client)


@client.event
async def on_voice_state_update(member, before, after):
    if member.id == client.user.id:
        if not after.channel:
            queue = utils.get_queue(before.channel.guild.id)
            if not queue:
                return
            await utils.destroy_queue(before.channel.guild.id)
            await queue.first_message.channel.send(embed=Embed(
                description="I got disconnected from the channel.", colour=Color.from_rgb(237, 19, 19)))


@client.event
async def on_reaction_add(reaction, member):
    await reactionHandler.handle(reaction, member)


client.run(os.getenv("TOKEN"))
