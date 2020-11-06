module.exports = {
    name: 'pause',
    aliases:['ps'],
    async run(message,args,client)
    {
        await client.player.pause(message);
        message.react('⏸️')
    }
}