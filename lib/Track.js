class Track {
  constructor(trackData, author) {
    this.title = trackData.title || trackData.videoDetails.title;

    this.url = trackData.url || null;

    this.author = trackData.author;

    this.requestedBy = author;

    this.author = trackData.channel
      ? trackData.channel.name
      : trackData.artist ||
        trackData.author.name ||
        trackData.videoDetails.author.name;
  }
}
module.exports = Track;
