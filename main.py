import discord
import logging

# Bot modules
import commandHandler


client = discord.Client()

# Logging utility
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@client.event
async def on_ready():
    print('Zalogowano jako {0.user}'.format(client))
    print('------')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('*'):
        await commandHandler.doStuff(message,client)

client.run('NzQ1NjIxNzY3ODE2NzQwOTM2.Xz0cYg.d-z453AGk0Nk55wrPrt_0jk9jcE')
