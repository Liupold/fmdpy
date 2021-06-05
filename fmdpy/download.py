import requests
import sys
import tempfile
import ffmpeg
import music_tag
import lyricsgenius
from fmdpy import *

# download file
def dlf(url, file_name, dltext=""):
    with open(file_name, "wb") as f:
        response = requests.get(url, headers=headers, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None: # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data); f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r%s[%s%s](%.2f%%)" \
                        % (dltext, '=' * done, ' ' * (50-done), (dl/total_length)*100))
                sys.stdout.flush()
    print("\tdone.")

def getLyric(song_obj):
    genius = lyricsgenius.Genius(mnc(b'U1ZZR1lzTnlzQXNfVWwwVVVZcW1wMkhPT0EzdF9ZSjRILUJfTzA0cVRtekctVW94RUtlZEFVMGhlX3BwVmd5cg==').decode('utf-8'))
    song = genius.search_song(song_obj.title, song_obj.artist)
    if song:
        return song.lyrics


def Dl(song_obj, dlformat='opus', bitrate=250, addlyrics=0):
    tf_song = tempfile.NamedTemporaryFile(suffix='.mp4')
    dlf(song_obj.url, tf_song.name, "SONG:")

    tf_thumb = tempfile.NamedTemporaryFile(suffix='.jpg')
    dlf(song_obj.thumb_url, tf_thumb.name, "ART :")
    output_file=f"{song_obj.artist}-{song_obj.title}({song_obj.year}).{dlformat}"\
            .replace(' ', '_').lower()

    # convert to desired format.
    (
            ffmpeg
            .input(tf_song.name)
            .output(output_file, **{'b:a': f'{bitrate}k'})
            .global_args('-loglevel', 'error', '-vn')
            .run()
    )

    # add music tags
    f = music_tag.load_file(output_file)
    f['year'] = song_obj.year
    f.append_tag('title', song_obj.title)
    f.append_tag('artist', song_obj.artist)
    f.append_tag('album', song_obj.album)
    f.append_tag('comment', song_obj.copyright + ', downloaded using (https://github.com/Liupold/fmdpy)')
    f.append_tag('album', song_obj.album)
    f['artwork'] = tf_thumb.read()
    if addlyrics:
        song_lyric = getLyric(song_obj)
        if song_lyric:
            f['lyrics'] = song_lyric
    f.save()
    print("\n")

