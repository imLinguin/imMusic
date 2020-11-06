const Discord = require("discord.js");
const client = new Discord.Client();
const fs = require("fs");
const { Player } = require("discord-player");
const player = new Player(client);
client.player = player;
require("dotenv").config();

client.once("ready", () => {
  console.log(`BRUUUUH!`);

  client.commands = new Discord.Collection();
  const commands = fs
    .readdirSync(__dirname + "/commands")
    .filter((file) => file.endsWith(`.js`));
  commands.forEach((command) => {
    const comand = require(__dirname + `/commands/${command}`);
    if (comand.name) {
      client.commands.set(comand.name, comand);
    }
  });
});
client.on("message", async (message) => {
  if (!message.guild || message.author.bot || !message.content.startsWith("*"))
    return;
  if (!message.member.voice.channel)
    return message.channel.send(`You're not in a voice channel ❌`);
  const args = message.content.slice(1).trim().split(/ +/g);
  const command = args.shift().toLowerCase();
  const cmd =
    client.commands.get(command) ||
    client.commands.find((cmd) => cmd.aliases && cmd.aliases.includes(command));
  if(!cmd) return;
    try {
    cmd.run(message, args, client);
  } catch (error) {
    console.log(error);
  }
});

client.player.on(
  "searchInvalidResponse",
  (message, query, tracks, content, collector) =>
    message.channel.send(`You must send a valid number between 1 and 10!`)
);
client.player.on("searchCancel", (message, query, tracks) =>
  message.channel.send(
    "You did not provide a valid response... Please send the command again!"
  )
);
client.player.on("noResults", (message, query) =>
  message.channel.send(`No results found on YouTube for ${query}!`)
);
client.player.on("channelEmpty", (message, queue) =>
  message.channel.send(
    "Music stopped as there is no more member in the voice channel!"
  )
);
client.player.on("trackStart", (message, track) => {
  const embed = {
    color: 0xe41ee8,
    image: {
      url: track.thumbnail,
    },
    description: `▶ Now playing [${track.title}](${track.url} 'YT link bro!')`,
    fields: [
      {
        name: `Requested by`,
        value: `<@${track.requestedBy.id}>`,
      },
    ],
    footer: {
      text: ``,
    },
  };

  message.channel.send({
    embed: embed,
  });
});
client.player.on("botDisconnect", (message, queue) =>
  message.channel.send(
    "Music stopped as I have been disconnected from the channel!"
  )
);
client.player.on("searchResults", (message, query, tracks) => {
  const mappedTracks = tracks.map((t, i) => `${i + 1}. ${t.title}`);
  let temporar = [];
  for (i = 0; i < 10; i++) {
    temporar.push(mappedTracks[i]);
  }
  const embed = new Discord.MessageEmbed()
    .setColor(0xe41ee8)
    .setAuthor(`Here are your search results for ${query}!`)
    .setDescription(temporar.join("\n"))
    .setFooter("Send the number of the song you want to play!");
  message.channel.send(embed);
});

client.player.on("error", (message, error) => {
  switch (error) {
    case "NotPlaying":
      message.channel.send("There is no music being played on this server!");
      break;
    case "NotConnected":
      message.channel.send("You are not connected in any voice channel!");
      break;
    case "UnableToJoin":
      message.channel.send(
        "I am not able to join your voice channel, please check my permissions!"
      );
      break;
    default:
      message.channel.send(`Something went wrong... Error: ${error}`);
  }
});

client.player.on("trackAdd",(message, queue,track)=>{
  const embed = {
    color: 0xe41ee8,
    description: `:OK: Added [${track.title}](${track.url} 'YT link bro!')`,
    fields: [
      {
        name: `Requested by`,
        value: `<@${track.requestedBy.id}>`,
      },
    ],
    footer: {
      text: `that's cool`,
    },
  };

  message.channel.send({
    embed: embed,
  });
})

client.login(process.env.TOKEN);
