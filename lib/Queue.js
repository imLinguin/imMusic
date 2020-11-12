class Queue {
  constructor(message) {
    this.guildID = message.guild.id;

    this.dispatcher = null;
    this.voiceConnection = null;

    this.tracks = [];

    this.stream = null;

    this.volume = 100;

    this.isPlaying = false;

    this.paused =
      this.voiceConnection &&
      this.voiceConnection.dispatcher &&
      this.voiceConnection.dispatcher.paused;

    this.firstMessage = message;
  }
  get playing() {
    return this.tracks[0];
  }
}
module.exports = Queue;
