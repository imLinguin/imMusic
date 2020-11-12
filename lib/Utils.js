const soundcloud = require("soundcloud-scraper");
const ytpl = require("ytfps");
const ytsr = require("youtube-sr");
const moment = require("moment");
require("dotenv").config();

const youtubeVideoRegex = /(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/;
const spotifySongRegex = /https?:\/\/(?:embed\.|open\.)(?:spotify\.com\/)(?:track\/|\?uri=spotify:track:)((\w|-){22})/;
const spotifyPlaylistRegex = /https?:\/\/(?:embed\.|open\.)(?:spotify\.com\/)(?:playlist\/|\?uri=spotify:playlist:)((\w|-){22})/;
const spotifyAlbumRegex = /https?:\/\/(?:embed\.|open\.)(?:spotify\.com\/)(?:album\/|\?uri=spotify:album:)((\w|-){22})/;
const youtubePlaylistRegex = /https?:\/\/(www.youtube.com\/)(watch|playlist)\?(v=|list=)((\w|-){11})/;

module.exports = {
  isSoundcloudLink(query) {
    return soundcloud.validateURL(query);
  },

  isSpotifySong(query) {
    return spotifySongRegex.test(query);
  },

  isSpotifyPlaylist(query) {
    return spotifyPlaylistRegex.test(query) || spotifyAlbumRegex.test(query);
  },

  isYTPlaylistLink(query) {
    return youtubePlaylistRegex.test(query);
  },

  isYTVideoLink(query) {
    return youtubeVideoRegex.test(query);
  },
  async fetchYoutube(query) {
    // query = encodeURIComponent(query);
    const data = await ytsr.search(query, { type: "video" });
    if (!data || !data[0] || data === []) return null;
    data[0].url = `https://www.youtube.com/watch?v=${await data[0].id}`;
    return data[0];
  },
  getProgressBar(queue) {
    if (!queue) return;
    const currentStreamTime = queue.voiceConnection.dispatcher
      ? queue.voiceConnection.dispatcher.streamTime
      : 0;
    const totalTime = queue.tracks[0].getDuration;
    const index = Math.round((currentStreamTime / totalTime) * 15);

    if (index >= 1 && index <= 15) {
      const bar = "░░░░░░░░░░░░░░░".split("");
      const fill = "█";
      bar.splice(0, index, fill);
      const roznica = 15 - bar.length;
      for (j = 0; j < roznica; j++) {
        bar.unshift(fill);
      }
      const currentTimecode =
        currentStreamTime >= 3600000
          ? moment(currentStreamTime).format("H:mm:ss")
          : moment(currentStreamTime).format("m:ss") ||
            moment(currentStreamTime).format("m:s");
      return `${currentTimecode} ┃ ${bar.join("")} ┃ ${queue.playing.duration}`;
    } else {
      const currentTimecode =
        currentStreamTime >= 3600000
          ? moment(currentStreamTime).format("H:mm:ss")
          : moment(currentStreamTime).format("m:ss");
      return `${
        currentTimecode ? currentStreamTime : "0:00"
      } ┃ ░░░░░░░░░░░░░░░░ ┃ ${queue.playing.duration}`;
    }
  },
  separatePlaylistID(query) {
    query = query.split("=");
    query = query[query.length - 1];
    return query;
  },
};
