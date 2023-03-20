"""Downloader for fmdpy."""
import os
import tempfile

import lyricsgenius
import music_tag
import requests
from pydub import AudioSegment
from tqdm import tqdm

from fmdpy import config, headers, utils

def convert_audio(input_file_path, output_file_path, bitrate, dlformat):
    try:
        input_audio = AudioSegment.from_file(input_file_path, "mp4")
    except FileNotFoundError:
        print(f"Input file {input_file_path} not found.")
        return
    except Exception as e:
        print(f"Error reading input file {input_file_path}: {e}")
        return
    try:
        input_audio.export(output_file_path, format=dlformat, bitrate=bitrate)
    except FileNotFoundError:
        print(f"Output file path {output_file_path} not found.")
        return
    except Exception as e:
        print(f"Error writing output file {output_file_path}: {e}")
        return

def dlf(url, file_name, silent=0, dltext=""):
    """Download a file to a specified loaction."""
    with open(file_name, "wb") as file_obj:
        response = requests.get(url, headers=headers, stream=True)
        total_length = response.headers.get('content-length')

        if (total_length is None) or (silent):  # no content length header
            file_obj.write(response.content)
        else:
            #dl_length = 0
            total_length = int(total_length)
            with tqdm(desc=dltext, total=total_length, \
                    leave=True, unit_scale=True, unit='B') as pbar:
                for data in response.iter_content(chunk_size=4096):
                    pbar.update(file_obj.write(data))
                # dl_length = len(data)
                #done = int(50 * dl_length / total_length)
                #sys.stdout.write("\r%s[%s%s](%.2f%%)" % (
                #    dltext, '=' * done, ' ' * (50 - done),
                #            (dl_length / total_length) * 100))
                #sys.stdout.flush()

def get_lyric(song_obj):
    """Get lyric."""
    genius = lyricsgenius.Genius(config['API_KEYS']['lyricsgenius'])
    genius.verbose = False
    song = genius.search_song(song_obj.title, song_obj.artist)
    if song:
        return song.lyrics
    return None


def main_dl(
        song_obj,
        dlformat='opus',
        bitrate=250,
        addlyrics=0,
        directory="./",
        filename="$artist-$name-$year",
        silent=0):
    """Main download function for fmdpy."""
    to_delete = []
    if song_obj.url == "":
        return None

    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=not (os.name == 'nt')) as tf_song:
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=not (os.name == 'nt')) as tf_thumb:
            if os.name == 'nt':
                to_delete.append(tf_song.name)
                to_delete.append(tf_thumb.name)

            directory = utils.resolve_string(song_obj, directory)
            os.makedirs(directory, exist_ok=True)
            filename = utils.slugify(utils.resolve_string(song_obj, filename))
            output_file = directory + '/' + filename

            if os.path.isfile(output_file):
                print(f"[WARNING]: File {output_file + '.mp4'} exist, skipping")
                return False
            dlf(song_obj.url, tf_song.name, dltext=f"SONG: ({song_obj.title})", silent=silent)
            dlf(song_obj.thumb_url, tf_thumb.name, dltext=f"ART : ({song_obj.title})", silent=silent)

            if dlformat != 'native':
                output_file += f".{dlformat}"
                # convert to desired format.
                convert_audio(tf_song.name, output_file, f'{bitrate}k', dlformat)
            else:
                output_file += '.mp4'
                if not os.path.isfile(output_file):
                    with open(output_file, 'wb') as file_obj:
                        file_obj.write(tf_song.read())
                else:
                    print(
                        f"[WARNING]: File {output_file + '.mp4'} exist, skipping")
                    return False

            # add music tags
            file_obj = music_tag.load_file(output_file)
            file_obj['year'] = song_obj.year
            file_obj['title'] = song_obj.title
            file_obj['artist'] = song_obj.artist
            file_obj['album'] = song_obj.album
            file_obj['comment'] = song_obj.copyright \
                + ', downloaded using (https://github.com/Liupold/fmdpy)'
            file_obj['album'] = song_obj.album
            file_obj['artwork'] = tf_thumb.read()
            if addlyrics:
                song_lyric = get_lyric(song_obj)
                if song_lyric:
                    file_obj['lyrics'] = song_lyric
            file_obj.save()
    if len(to_delete) > 0:
        _ = [os.unlink(fname) for fname in to_delete]
    return True
