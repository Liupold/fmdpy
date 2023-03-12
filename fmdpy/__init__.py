"""fmdpy."""
from . import conf

VERSION = "0.6"
install_requires = ['ffmpeg-python', 'click', 'music-tag>=0.4.3', 'requests',
                    'pillow', 'lyricsgenius', 'dataclasses', 'spotipy', 'tqdm']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
    '(KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}

ART = r'''  _| |_ |  \ /  |   /\  (   _   ) || || |
 /     \|   v   |  /  \  | | | || \| |/ |
( (| |) ) |\_/| | / /\ \ | | | | \_   _/
 \_   _/| |   | |/ /__\ \| | | |   | |
   |_|  |_|   |_/________\_| |_|   |_|
                                         '''
config = conf.load()
