module.exports = {
    name: 'disconnect',
    aliases:['fuckoff','getout'],
    run(message,args,client)
    {
        const query = args.join(' ')
        if (!client.player.isPlaying(message) || query) {
            if (!query) return message.channel.send(`You have to provide a link or query`);
            client.player.play(message, query, message.author);
            message.react('764459481303875584')
        } else {
        client.player.resume(message);
        }
    }
}