async def run(message,args,client):
    member = message.author
    me = message.guild.me

    if not me.voice or not me.voice.channel:
        if not message.author.voice or not message.author.voice.channel:
            return await message.reply("You have to be in a voice channel")
        else:
            connection = await message.author.voice.channel.connect();
    
    