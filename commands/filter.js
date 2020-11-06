const filters = require("../config/filters.json");
module.exports = {
    name: 'filter',
    aliases:['fil'],
    run(message,args,client)
    {
        if(!client.player.isPlaying(message)) return message.channel.send(`No music playing on this server ${emotes.error}`);
        const filter = args[0];
        if(!filter) return message.channel.send(`Please specify a valid filter to enable or disable ❌`);

        const filterToUpdate = Object.values(filters).find((f) => f.toLowerCase() === filter.toLowerCase());

    //If he can't find the filter
        if(!filterToUpdate) return message.channel.send(`This filter doesn't exist ❌`);

        const filterRealName = Object.keys(filters).find((f) => filters[f] === filterToUpdate);

        const queueFilters = client.player.getQueue(message).filters
        const filtersUpdated = {};
        filtersUpdated[filterRealName] = queueFilters[filterRealName] ? false : true;
        client.player.setFilters(message, filtersUpdated);

        if(filtersUpdated[filterRealName]) {

        //The bot adds the filter on the music
        message.channel.send(`I'm adding the filter to the music, please wait... Note: the longer the music is, the longer this will take <a:pepeFastJam:764456068138795008>`);

        } else {

        //The bot removes the filter from the music
        message.channel.send(`I'm disabling the filter on the music, please wait... Note: the longer the music is playing, the longer this will take <a:pepeSadJam:764456069274664960>`);

    }
    }
}