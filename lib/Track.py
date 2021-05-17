import discord


class Track:
    def __init__(self, url, data, message):
        self.url = url
        self.stream_url = data.get("url")
        self.title = data.get("title")
        self.author = data.get("creator")
        self.duration = data.get("duration")
        self.requestedBy = message.author

    def get_embed(self):
        return discord.Embed(title="Now Playing", description=self.title,
                             footer="Requested by {0}".format(self.requestedBy.name), colour=discord.Color.from_rgb(35, 219, 201))
