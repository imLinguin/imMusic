module.exports = {
  name: "queue",
  aliases: ["q"],
  async run(message, args, client) {
    const { tracks } = client.player.getQueue(message);
    let songs = "```";
    let num = 1;
    tracks.forEach((track) => {
      songs += `${num}. ${track.title} ${track.duration}\n`;
      num++;
    });
    songs += "```";
    const embed = {
      color: 0xe41ee8,
      title: `Queue for ${message.guild.name}`,
      description: songs,
      footer: {
        text: `Invoked by: ${message.author.tag}`,
      },
    };
    message.channel.send({ embed: embed });
  },
};
