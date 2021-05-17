class Queue:
    def __init__(self, message, connection):
        self.guild_id = message.guild.id
        self.voice_connection = connection
        self.player = None
        self.tracks = []
        self.volume = 50
        self.is_playing = False
        self.filters = []
        self.filters_update = False
        self.first_message = message
        self.now_playing = None
        self.now_playing_index = 0
        self.start_time = 0
