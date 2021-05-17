from discord import Client, Activity, ActivityType
import logging
# Bot modules
import commandHandler
import os
from dotenv import load_dotenv
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

client.run(os.getenv("TOKEN"))
