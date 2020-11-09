module.exports = {
  name: "nowplaying",
  aliases: ["np"],
  run(message, args, client) {
    let song = client.queues.get(message.guild.id)?.tracks[0];
    if (!song) return message.channel.send("No music playing currently!");
    let embed = {
      color: 0x51cab0,
      title: "Current song is",
      description: `[${song.title}](${song.url})`,
    };
    message.channel.send({ embed: embed });
  },
};
