from dataclasses import dataclass

@dataclass
class Song:
    songid: str
    title: str = "Unknown"
    album: str = "Unknown"
    artist: str = "Unknown"
    year: str = "Unknown"
    copyright: str = "Unknown"
    url: str = ""
    thumb_url: str = ""
    raw_json = {}

    def geturl(self):
        pass

