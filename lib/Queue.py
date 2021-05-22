class Queue:
    def __init__(self, message, connection):
        self.guild_id = message.guild.id
        self.voice_connection = connection
        self.player = None

        self.volume = 50
        self.bitrate = int(connection.channel.bitrate / 1000)
        self.is_playing = False
        self.loop = 0

        self.tracks = []
        self.filters = []

        self.filters_update = False
        self.first_message = message

        self.queue_message = None
        self.queue_page = 0

        self.now_playing = None
        self.now_playing_index = 0

        self.start_time = 0
        self.end_time = 0
