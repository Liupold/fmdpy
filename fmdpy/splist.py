"""A."""
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, CacheFileHandler
from fmdpy import config, cache_dir

def get_songs_splist(url):
    """Search spotiy song and download from fmdpy."""
    from fmdpy.api import query
    song_list = []
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        cache_handler=CacheFileHandler(cache_path=f"{cache_dir}/spotipy.cache"),
        client_id=config['API_KEYS']['spotify_client_id'],
        client_secret=config['API_KEYS']['spotify_client_secret'])
    )
    playlist_dict = spotify.playlist(url)
    tol_items = len(playlist_dict['tracks']['items'])

    for i, item in enumerate(playlist_dict['tracks']['items']):
        title = item['track']['name']
        artist = item['track']['album']['artists'][0]['name']
        q_results = query(f'{title} {artist}')
        print(f"Getting songs.....({i}/{tol_items})", end='\r')

        for q_song in q_results:
            if (title in q_song.title) and (q_song.artist == artist):
                song_list.append(q_song)
                break
    print("done\n")
    return song_list
