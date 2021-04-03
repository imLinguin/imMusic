class Queue:
    def __init__(self,message,connection):
        self.guildID = message.guild.id
        self.voiceConnection = connection
        self.tracks = []

        self.volume = 100
        self.isPlaying = False

        self.firstMessage = message