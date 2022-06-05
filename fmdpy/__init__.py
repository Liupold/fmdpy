"""fmdpy."""
from . import conf

VERSION = "0.5.2"
install_requires = ['ffmpeg-python', 'click', 'music-tag>=0.4.3', 'requests',
                    'pillow', 'lyricsgenius', 'dataclasses', 'spotipy', 'tqdm']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1;' +
    ' WOW64; rv:39.0) Gecko/20100101 Firefox/75.0',
}

ART = r'''  _| |_ |  \ /  |   /\  (   _   ) || || |
 /     \|   v   |  /  \  | | | || \| |/ |
( (| |) ) |\_/| | / /\ \ | | | | \_   _/
 \_   _/| |   | |/ /__\ \| | | |   | |
   |_|  |_|   |_/________\_| |_|   |_|
                                         '''
config = conf.load()
