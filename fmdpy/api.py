"""api for fetching song metadata and url."""
import base64 as bs64
import requests
from Crypto.Cipher import DES
from fmdpy import headers, ART
from fmdpy.song import Song
from fmdpy.splist import get_songs_splist

def get_song_urls(song_obj):
    """Fetch song download url."""
    req = requests.get(headers=headers,
                       url="https://www.jiosaavn.com/api.php?__call=song.getDetails" \
                               + f"&ctx=web6dot0&_marker=0&_format=json&pids={song_obj.songid}")

    raw_json = req.json()['songs'][0]
    if 'encrypted_media_url' in raw_json.keys():
        key = '38346591'.encode('utf-8')
        dciper = DES.new(key, DES.MODE_ECB)
        decrypted = dciper.decrypt(bs64.b64decode(raw_json['encrypted_media_url']))
        song_obj.url = decrypted.replace(b'\x05', b'').decode().replace('_96', '_320')
        song_obj.thumb_url = raw_json['image'].replace(
            '-150x150.jpg', '-500x500.jpg')

def parse_query(query_json):
    song_list = []
    r_key = 'results'
    if 'songs' in query_json:
        r_key = 'songs'
    for sng_raw in query_json[r_key]:
        song_id = sng_raw['id']
        song_title = sng_raw['song']
        song_year = sng_raw['year']
        song_album = sng_raw['album']
        song_copyright = sng_raw['copyright_text']
        if len(sng_raw['primary_artists']) != 0:
            song_artist = sng_raw['primary_artists']
        else:
            song_artist = "Unknown"
        song_album_url = sng_raw['album_url']
        song_ = Song(songid=song_id,
                     title=song_title, artist=song_artist, year=song_year,
                     album=song_album, copyright=song_copyright,
                     album_url=song_album_url)
        song_list.append(song_)
    return song_list


def query_songs_search(query_text, max_results=5):
    """Search Songs using text."""
    if ("fmd" in query_text) or ("liupold" in query_text):
        print(ART)

    req = requests.get(
        headers=headers,
        url=f"https://www.jiosaavn.com/api.php?p=1&q={query_text.replace(' ', '+')}" \
            + "&_format=json&_marker=0&ctx=wap6dot0" \
            + f"&n={max_results}&__call=search.getResults")
    return parse_query(req.json())


def query_song_from_url(query_url):
    """Fetch album from url"""

    token = query_url.split('/')[-1]
    req = requests.get(
        headers=headers,
        url=f"https://www.jiosaavn.com/api.php?__call=webapi.get&token={token}&" \
                + "type=song&includeMetaTags=0&ctx=web6dot0&_format=json&_marker=0")
    #print(json.dumps(query_json, indent = 1))
    return parse_query(req.json())


def query_album_from_url(query_url):
    """Fetch album from url"""

    token = query_url.split('/')[-1]
    req = requests.get(
        headers=headers,
        url=f"https://www.jiosaavn.com/api.php?__call=webapi.get&token={token}" \
                + "&type=album&includeMetaTags=0&ctx=web6dot0&_format=json&_marker=0")
    song_list = parse_query(req.json())
    print(f"Album:\t\"{song_list[0].album}\"\n")
    return song_list


def query(query_string, max_results=5):
    "This is whrere the text from the prompt comes!"
    if query_string[:30] == "https://www.jiosaavn.com/song/":
        return query_song_from_url(query_string)
    elif query_string[:31] == "https://www.jiosaavn.com/album/":
        return query_album_from_url(query_string)
    if query_string == "":
        return []
    if 'spotify.com/playlist' in query_string:
        return get_songs_splist(query_string)
    return query_songs_search(query_string, max_results)
