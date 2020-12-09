const Discord = require("discord.js");
const fs = require("fs");

require("dotenv").config();
const client = new Discord.Client();
client.queues = new Discord.Collection();

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

client.on("ready", () => {
  console.log(`Ready! ${client.user.tag}`);
  client.user.setPresence({
    activity: {
      name: `*help | ${client.guilds.cache.size} servers`,
      type: "LISTENING",
    },
    status: "online",
  });
});

client.on("message", async (message) => {
  if (message.author.bot || !message.guild || !message.content.startsWith("*"))
    return;
  if (!message.member.voice.channel && message.content !== ("*h" || "*help"))
    return message.channel.send("❌ You're not in a voice channel.");

  const args = message.content.slice(1).trim().split(/ +/g);
  const command = args.shift().toLowerCase();
  const cmd =
    client.commands.get(command) ||
    client.commands.find((cmd) => cmd.aliases && cmd.aliases.includes(command));

  if (!cmd) return;
  try {
    cmd.run(message, args, client);
  } catch (error) {
    console.log(error);
  }
});

client.on("voiceStateUpdate", (oldState, newState) => {
  const queue = client.queues.find((g) => g.guildID === oldState.guild.id);
  if (!queue) return;

  if (newState.member.id === client.user.id && !newState.channelID) {
    queue.dispatcher.destroy();
    client.queues.delete(newState.guild.id);
  }
});

client.login(process.env.TOKEN);
