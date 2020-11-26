const Utils = require("./Utils");

module.exports = {
  YouTubeSongAnnounce(track) {
    return (embed = {
      color: 0xff0000,
      title: "<:yt:775294971275378709> Song added",
      description: `[${track.title}](${track.url})`,
    });
  },
  YouTubePlaylistAnnounce(tracks) {
    return (embed = {
      color: 0xff0000,
      title: `<:yt:775294971275378709> Added ${tracks.length} tracks.`,
    });
  },
  SpotifySongAnnounce(track) {
    return (embed = {
      color: 0x1ed760,
      title: `<:spotify:775294970721992714> Song added [${track.requestedBy}]`,
      description: `[${track.title}](${track.url})`,
    });
  },
  SpotifyListAnnounce(tracks) {
    return (embed = {
      color: 0x1ed760,
      title: `<:spotify:775294970721992714> Added ${tracks.length} tracks. [${tracks[0].requestedBy}]`,
    });
  },
  SoundCloudSongAnnounce(track) {
    return (embed = {
      color: 0xff6d00,
      title: `<:soundcloud:775294969384140811> Song added [${track.requestedBy}]`,
      description: `[${track.title}](${track.url})`,
    });
  },
  CustomSearchAnnounce(track) {
    return (embed = {
      color: 0x5c5c5c,
      title: `<:magnifying:775295981063241738> Song added [${track.requestedBy}]`,
      description: `[${track.title}](${track.url})`,
    });
  },

  NowPlaying(queue, message) {
    let song = queue.tracks[0];
    let embed = {
      color: 0x51cab0,
      title: "Now playing",
      description: `[${song.title}](${song.url})`,
      fields: [
        {
          name: "\u200b",
          value: Utils.getProgressBar(queue),
          inline: true,
        },
        {
          name: `Requested by:`,
          value: `${song.requestedBy.username}`,
          inline: true,
        },
        {
          name: "From playlist:",
          value: `${song.fromPlaylist ? "Yes" : "No"}`,
          inline: true,
        },
      ],
      image: {
        url: song.thumbnail,
      },
    };
    message.channel.send({ embed: embed });
  },
};
