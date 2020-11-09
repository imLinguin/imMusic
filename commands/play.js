const Utils = require("../lib/Utils");
const ytdl = require("discord-ytdl-core");
const ytpl = require("ytpl");
const spotify = require("spotify-url-info");
const soundcloud = require("soundcloud-scraper");
const key = soundcloud.keygen();
const scrapper = new soundcloud.Client(key);
const Track = require("../lib/Track");
const Queue = require("../lib/Queue");
const Embeds = require("../lib/Embeds");

module.exports = {
  name: "play",
  aliases: ["p"],
  async run(message, args, client) {
    const query = args.join(" ");
    const queryType = classifyQuery(query);
    let trackToAdd;
    let tracksToAdd = [];
    let embed;

    if (
      client.queues.has(message.guild.id) &&
      client.queues.get(message.guild.id).voiceConnection &&
      client.queues.get(message.guild.id).voiceConnection.dispatcher &&
      client.queues.get(message.guild.id).voiceConnection.dispatcher.paused
    ) {
      client.queues.get(message.guild.id).dispatcher.resume();
      return message.react("▶");
    }

    switch (queryType) {
      case "youtube-video":
        tracksToAdd = [];
        const videoData = await ytdl.getBasicInfo(query);
        videoData.url = videoData.videoDetails.video_url;
        trackToAdd = new Track(videoData, message.author); // 775294971275378709
        embed = Embeds.YouTubeSongAnnounce(trackToAdd);
        break;
      case "youtube-playlist":
        const { items } = await ytpl(query, { limit: 1000 });
        for (item of items) {
          if (item.duration || item.author)
            tracksToAdd.push(new Track(item, message.author)); // 775294971275378709
        }
        embed = Embeds.YouTubePlaylistAnnounce(items);
        break;
      case "spotify-song":
        let songData = await spotify.getData(query);
        songData = await Utils.fetchYoutube(
          `${songData.artist || songData.artists[0].name} ${songData.name}` // 775294970721992714
        );
        trackToAdd = new Track(songData, message.author);
        embed = Embeds.SpotifySongAnnounce(trackToAdd);
        break;
      case "spotify-playlist":
        tracksToAdd = [];
        let playlistData = await spotify.getData(query);
        let i = 0;
        while (i < playlistData.tracks.items.length) {
          let data = playlistData.tracks.items;
          if (!data[i]) break;
          let itemData = playlistData.tracks.items[i]; // 775294970721992714
          itemData.title = itemData.track.name;
          itemData.author = itemData.track.artists[0];
          tracksToAdd.push(new Track(itemData, message.author));
          i++;
        }
        embed = Embeds.SpotifyListAnnounce(tracksToAdd);
        break;
      case "soundcloud":
        tracksToAdd = [];
        let soundclouData = await scrapper.getSongInfo(query);
        let ytData = await Utils.fetchYoutube(`${soundclouData.title}`); // 775294969384140811
        trackToAdd = new Track(ytData, message.author);
        embed = Embeds.SoundCloudSongAnnounce(trackToAdd);
        break;
      case "search":
        let youtubeSearch = await Utils.fetchYoutube(`${query}`); // 775295981063241738
        trackToAdd = new Track(youtubeSearch, message.author);
        embed = Embeds.CustomSearchAnnounce(trackToAdd);
        break;
    }

    message.channel.send({ embed: embed });

    if (trackToAdd !== undefined) {
      if (!client.queues.has(message.guild.id)) {
        const newQueue = new Queue(message);
        newQueue.tracks.push(trackToAdd);
        client.queues.set(message.guild.id, newQueue);
      } else {
        const queue = client.queues.get(message.guild.id);
        queue.tracks.push(trackToAdd);
        client.queues.set(message.guild.id, queue);
      }
    } else if (tracksToAdd !== []) {
      if (!client.queues.has(message.guild.id)) {
        const newQueue = new Queue(message);
        newQueue.tracks = tracksToAdd;
        client.queues.set(message.guild.id, newQueue);
      } else {
        const queue = client.queues.get(message.guild.id);
        for (track of tracksToAdd) {
          queue.tracks.push(track);
        }
        client.queues.set(message.guild.id, queue);
      }
    }
    if (!client.queues.get(message.guild.id).isPlaying)
      connectAndPlay(message, client);
  },
};

const classifyQuery = (query) => {
  if (Utils.isSoundcloudLink(query)) {
    return "soundcloud";
  } else if (Utils.isSpotifySong(query)) {
    return "spotify-song";
  } else if (Utils.isSpotifyPlaylist(query)) {
    return "spotify-playlist";
  } else if (Utils.isYTPlaylistLink(query)) {
    return "youtube-playlist";
  } else if (Utils.isYTVideoLink(query)) {
    return "youtube-video";
  } else {
    return "search";
  }
};

const connectAndPlay = async (message, client) => {
  let queue = client.queues.get(message.guild.id);
  if (!queue.voiceConnection) {
    queue.voiceConnection = await message.member.voice.channel.join();
  }

  if (queue.tracks[0].url === null) {
    let track = queue.tracks[0];
    let youtubeTrack = await Utils.fetchYoutube(
      `${track.author} ${track.title}`
    );
    queue.tracks[0] = new Track(await youtubeTrack, message.author);
  }
  let dispatcher = queue.dispatcher || null;
  dispatcher = queue.voiceConnection
    .play(
      ytdl(queue.tracks[0].url, {
        filter: "audioonly",
        opusEncoded: true,
        quality: "highestaudio",
      }),
      {
        type: "opus",
      }
    )
    .on("finish", () => {
      queue.tracks.shift();
      if (queue.tracks.length === 0) {
        message.guild.me.voice.channel.leave();
        queue.firstMessage.channel
          .send({
            embed: {
              color: 0x51cab0,
              title: "Queue ended so I'm leaving",
              description: "NAURA",
            },
          })
          .then((m) => m.react("👋"));
        client.queues.delete(message.guild.id);
        return;
      }
      connectAndPlay(message, client);
    });

  queue.isPlaying = true;
  queue.dispatcher = dispatcher;

  client.queues.set(message.guild.id, queue);
};
