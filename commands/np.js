module.exports = {
  name: "nowplaying",
  aliases: ["np", "now-playing"],
  async run(message, args, client) {
    let song = await client.player.nowPlaying(message);

    const progress = client.player.createProgressBar(message, {
      timecodes: true,
    });
    const embed = {
      color: 0xe41ee8,
      image: {
        url: song.thumbnail,
      },
      description: `▶ Now playing [${song.title}](${song.url} 'YT link bro!')`,
      fields: [
        {
          name: `Requested by`,
          value: `<@${song.requestedBy.id}>`,
        },
      ],
    };

    progress
      ? embed.fields.push({
          name: "Progress:",
          value: progress,
        })
      : null;

    message.channel.send({
      embed: embed,
    });
  },
};
