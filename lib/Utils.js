const soundcloud = require("soundcloud-scraper");
const ytpl = require("ytpl");
const ytsr = require("youtube-sr");
//const ytdl = require("discord-ytdl-core");
require("dotenv").config();

const youtubeVideoRegex = /(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/;
const spotifySongRegex = /https?:\/\/(?:embed\.|open\.)(?:spotify\.com\/)(?:track\/|\?uri=spotify:track:)((\w|-){22})/;
const spotifyPlaylistRegex = /https?:\/\/(?:embed\.|open\.)(?:spotify\.com\/)(?:playlist\/|\?uri=spotify:playlist:)((\w|-){22})/;

module.exports = {
  isSoundcloudLink(query) {
    return soundcloud.validateURL(query);
  },

  isSpotifySong(query) {
    return spotifySongRegex.test(query);
  },

  isSpotifyPlaylist(query) {
    return spotifyPlaylistRegex.test(query);
  },

  isYTPlaylistLink(query) {
    return ytpl.validateID(query);
  },

  isYTVideoLink(query) {
    return youtubeVideoRegex.test(query);
  },
  async fetchYoutube(query) {
    query = encodeURIComponent(query);
    const data = await ytsr.search(query, { type: "video" });
    data[0].url = `https://www.youtube.com/watch?v=${data[0].id}`;
    return data[0];
  },
};
