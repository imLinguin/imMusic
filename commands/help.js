module.exports = {
  name: "help",
  aliases: ["h"],
  run(message, args, client) {
    let embed = {
      color: 0x53bc8c,
      title: `Welcome in the help section`,
      fields: [
        {
          name: "👮‍♂️Prefix",
          value: "Prefix for the bot is *. For now you can't change it.",
          inline: false,
        },
        {
          name: "👏Command usage:",
          value: `So you are wondering how to use commands on ${message.guild.name}?\nIts very simple.\`*play\``,
          inline: false,
        },
        {
          name: "👀List of available commands",
          value:
            "play, search, shuffle, skip, nowplaying, move, loop, disconnect",
          inline: false,
        },
        {
          name: "🤫Coming soon",
          value: "Sound effects such as bassboost",
          inline: false,
        },
      ],
    };
    message.channel.send({ embed: embed });
  },
};
