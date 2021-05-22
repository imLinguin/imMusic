import math
import spotipy
import os
import re
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
load_dotenv()
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                                                           client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")))


def is_track(url):
    return re.match("https:\/\/(open.spotify.com)(\/track\/)(\d|\w){22}", url)


def is_playlist(url):
    return re.match("https:\/\/(open.spotify.com)(\/playlist\/)(\d|\w){22}", url)


def get_track(url):
    track = sp.track(url)
    title = track.get("name")
    author = track.get("album").get("artists")[0]["name"]
    cover = track.get("album").get("images")[0].get("url")
    duration = track.get("duration_ms")
    return {"title": title, "creator": author, "cover": cover, "duration": duration}


def get_playlist(url):
    playlist = []
    playlist_data = sp.playlist(url)
    total = playlist_data.get("tracks").get("total")
    repeat_times = math.ceil(total / 100)
    for i in range(repeat_times):
        tracks = sp.playlist_tracks(url, limit=100, offset=(i*100)+1)
        for track in tracks["items"][:]:
            name = track["track"]["name"]
            artist = track["track"]["artists"][0]["name"]
            duration = track["track"]["duration_ms"]
            cover = None
            if track["track"]["album"]["images"]:
                cover = track["track"]["album"]["images"][0]["url"]

            playlist.append(
                {"title": name, "creator": artist, "cover": cover, "duration": duration})

    return playlist
