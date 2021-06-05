import requests
from fmdpy import headers, art
from fmdpy.song import Song


def parse_query(query_json):
    song_list = []
    for s in query_json['results']:
        song_id = s['id']
        song_title = s['title']
        song_year = s['year']
        song_album = s['more_info']['album']
        song_copyright = s['more_info']['copyright_text']
        if len(s['more_info']['artistMap']['primary_artists']) != 0:
            song_artist = s['more_info']['artistMap']['primary_artists'][0]['name']
        else:
            song_artist = "Unknown"
        song_ = Song(songid=song_id, \
                title=song_title, artist=song_artist, year=song_year, album=song_album, copyright=song_copyright)
        song_list.append(song_)
    return song_list

def query(query_text, max_results=5):
    if ("fmd" in query_text) or ("liupold" in query_text):
        print(art)

    r = requests.get(headers=headers, \
            url=f"https://www.jiosaavn.com/api.php?p=1&q={query_text.replace(' ', '+')}\
            &_format=json&_marker=0&api_version=4&ctx=wap6dot0\
            &n={max_results}&__call=search.getResults")
    return parse_query(r.json())

def getSongURLs(song_obj):
    r = requests.get(headers=headers, \
            url=f"https://www.jiosaavn.com/api.php?__call=song.getDetails&cc=in&_marker=0%3F_marker%3D0&_format=json&pids={song_obj.songid}")
    raw_json = r.json()[song_obj.songid]
    song_obj.url = raw_json['media_preview_url'].\
            replace('https://preview.saavncdn.com/', 'https://aac.saavncdn.com/').\
            replace('_96_p.mp4', '_320.mp4')
    song_obj.thumb_url = raw_json['image'].replace('-150x150.jpg', '-500x500.jpg')

