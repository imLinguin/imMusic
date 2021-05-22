from discord import Embed, Color


class Track:
    def __init__(self, url, data, message):
        self.url = url
        self.stream_url = data.get("url") or None
        self.title = data.get("title")
        self.author = data.get("creator")
        self.duration = data.get("duration")
        self.cover = data.get("cover")
        self.requestedBy = message.author

    def get_embed(self):
        embed = Embed(title="Now Playing", description=self.title,
                      colour=Color.from_rgb(35, 219, 201))
        embed.set_footer(text="Requested by {0}".format(self.requestedBy.name))
        return embed
