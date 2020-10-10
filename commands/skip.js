module.exports = {
    name: 'skip',
    aliases:['s'],
    run(message,args,client)
    {
        client.player.skip(message);
    }
}