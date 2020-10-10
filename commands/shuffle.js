module.exports = {
    name: 'shuffle',
    aliases:['sh'],
    run(message,args,client)
    {
        client.player.shuffle(message).then(()=>{
            message.channel.send(`🔀Queue shuffled!`);
        })
    }
}