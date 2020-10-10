module.exports = {
    name: 'eval',
    aliases:['hack'],
    run(message,args,client)
    {
        if (message.author.id === '341290281624141824') {
            message.channel.send(eval(args.join(' ')));
        }
    }
}
