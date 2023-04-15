"""fmdpy."""
from . import conf

VERSION = "0.6.3"
install_requires = ['click', 'music-tag>=0.4.3', 'requests', 'pillow',
                    'lyricsgenius', 'dataclasses', 'spotipy', 'tqdm', 'pydub',
                    'pycryptodome']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' +
    '(KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}

ART = fr'''
 .o88o.                         .o8
 888 `"                        "888
o888oo  ooo. .oo.  .oo.    .oooo888  oo.ooooo.  oooo    ooo
 888    `888P"Y88bP"Y88b  d88' `888   888' `88b  `88.  .8'
 888     888   888   888  888   888   888   888   `88..8'
 888     888   888   888  888   888   888   888    `888'
o888o   o888o o888o o888o `Y8bod88P"  888bod8P'     .8'
                                      888       .o..P'
                                     o888o      `Y8P   ({VERSION})
'''

config = conf.load()
