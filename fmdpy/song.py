"""song class for fmdpy."""
from dataclasses import dataclass

# needed to store metadata
#pylint: disable=too-many-instance-attributes


@dataclass
class Song:
    """Song class to hold metadata."""
    songid: str
    title: str = "Unknown"
    album: str = "Unknown"
    artist: str = "Unknown"
    year: str = "Unknown"
    copyright: str = "Unknown"
    url: str = ""
    thumb_url: str = ""
    raw_json = {}
