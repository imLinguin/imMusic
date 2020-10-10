module.exports = {
    name: 'pause',
    aliases:['ps'],
    async run(message,args,client)
    {
        const track = await client.player.pause(message);
        message.channel.send(`${track.name} paused!`);
    }
}