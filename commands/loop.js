module.exports = {
    name: 'loop',
    aliases:['lp'],
    run(message,args,client)
    {
        const repeatMode = client.player.getQueue(message).repeatMode;
                if (repeatMode) {

                    client.player.setRepeatMode(message, false);
                    return message.channel.send(`🔁 Repeat mode disabled`);
                } else {
                    client.player.setRepeatMode(message, true);
                    return message.channel.send(`🔁 Repeat mode enabled`);

                }
    }
}