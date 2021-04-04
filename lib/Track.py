class Track:
    def __init__(self,url,data,message):
        self.url = url
        self.title = data.get("track")
        self.author = data.get("artist")
        self.duration = data.get("duration")
        self.requestedBy = message.author
    

    def getEmbed(self):
        return {
            "title":self.title,
            "description":"Requested by {0}".format(self.requestedBy.name),
            "footer":"cool"
        }