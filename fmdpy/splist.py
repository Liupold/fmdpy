"""A."""
import os
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from fmdpy.api import query, get_song_urls
from fmdpy.download import main_dl
from fmdpy import config


def get_song_from_sotify_item(item, **options):
    """Search spotiy song and download from fmdpy."""
    title = item['track']['name']
    artist = item['track']['album']['artists'][0]['name']
    q_results = query(f'{title} {artist}')

    for q_song in q_results:
        if (title in q_song.title) and (q_song.artist == artist):
            get_song_urls(q_song)
            try:
                main_dl(q_song, silent=1,  **options)
                print(
                    f"Downloaded: {q_song.title} [{q_song.artist}] ({q_song.year})")
            except Exception as e:
                print(e)
            return True

    print(f"NOT FOUND: {title} [{artist}]")
    return False


def pl_spotify_dl(url, **options):
    """Donwload given url."""
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=config['API_KEYS']['spotify_client_id'],
        client_secret=config['API_KEYS']['spotify_client_secret'])
    )

    playlist_dict = spotify.playlist(url)
    pl_name = playlist_dict['id']
    if not os.path.exists(pl_name):
        os.makedirs(pl_name)
    dl_song = partial(get_song_from_sotify_item, directory=pl_name, **options)
    with ThreadPoolExecutor(max_workers=4) as pool:
        _ = pool.map(dl_song, playlist_dict['tracks']['items'])
