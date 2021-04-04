class Track:
    def __init__(self,url,data,message):
        self.url = url
        self.title = data.get("title")
        self.author = data.get("author")
        self.duration = data.get("duration")
        self.requestedBy = message.author
        