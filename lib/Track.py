class Track:
    def __init__(url,data,message):
        self.url = url
        self.title = data.title
        this.author = data.author
        self.duration = data.duration
        self.requestedBy = message.author
        