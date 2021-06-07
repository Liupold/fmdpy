"""api for fetching song metadata and url."""
import requests
from fmdpy import headers, ART
from fmdpy.song import Song


def parse_query(query_json):
    """Set metadata and return Song obj list."""
    song_list = []
    for sng_raw in query_json['results']:
        song_id = sng_raw['id']
        song_title = sng_raw['title']
        song_year = sng_raw['year']
        song_album = sng_raw['more_info']['album']
        song_copyright = sng_raw['more_info']['copyright_text']
        if len(sng_raw['more_info']['artistMap']['primary_artists']) != 0:
            song_artist = sng_raw['more_info']['artistMap']['primary_artists'][0]['name']
        else:
            song_artist = "Unknown"
        song_ = Song(songid=song_id,
                     title=song_title, artist=song_artist, year=song_year,
                     album=song_album, copyright=song_copyright)
        song_list.append(song_)
    return song_list


def query(query_text, max_results=5):
    """Fetch songs from query."""
    if ("fmd" in query_text) or ("liupold" in query_text):
        print(ART)

    req = requests.get(
        headers=headers,
        url=f"https://www.jiosaavn.com/api.php?p=1&q={query_text.replace(' ', '+')}\
            &_format=json&_marker=0&api_version=4&ctx=wap6dot0\
            &n={max_results}&__call=search.getResults")
    return parse_query(req.json())


def get_song_urls(song_obj):
    """Fetch song download url."""
    req = requests.get(headers=headers,
                       url=f"https://www.jiosaavn.com/api.php?__call=song.getDetails&cc=in\
        &_marker=0%3F_marker%3D0&_format=json&pids={song_obj.songid}")
    raw_json = req.json()[song_obj.songid]
    if 'media_preview_url' in raw_json.keys():
        song_obj.url = raw_json['media_preview_url'].\
            replace('https://preview.saavncdn.com/', 'https://aac.saavncdn.com/').\
            replace('_96_p.mp4', '_320.mp4')
        song_obj.thumb_url = raw_json['image'].replace(
            '-150x150.jpg', '-500x500.jpg')
