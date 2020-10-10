module.exports = {
    name: 'nowplaying',
    aliases:['np','now-playing'],
    async run(message,args,client)
    {
        let song = await client.player.nowPlaying(message);
        console.log(client.player.getQueue(message).tracks)
         const embed = {
           color: 0xe41ee8,
            image: {
                url: song.thumbnail,
            },
           description: `▶ Now playing [${song.title}](${song.url} 'YT link bro!')`,
           fields:[{
                name:`Requested by`,
                value: `<@${song.requestedBy.id}>`,
            },
            ],
            
            }
            message.channel.send({
                embed: embed
            })
    }
}