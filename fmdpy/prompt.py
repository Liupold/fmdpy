import sys
from concurrent.futures import ThreadPoolExecutor
from fmdpy import config, stream
from fmdpy.api import query, get_song_urls
from fmdpy.download import main_dl, get_lyric
from fmdpy.splist import pl_spotify_dl
from tqdm import tqdm

def list_songs(song_list):
    for i, sng in enumerate(song_list):
        print(f'{i}) {sng.title} [{sng.artist}] ({sng.year})')

def find_songs(search_str, count):
    song_list = query(search_str, count)
    list_songs(song_list)
    return song_list

def run_prompt(prompt_input, song_list, multiple, count,
               fmt, bitrate, lyrics, directory, filename):
        download_pool = []
        stream_pool = []

        if "" == prompt_input:
            return song_list

        if prompt_input in ('.q', '.exit', '.quit'):
            sys.exit()

        if not prompt_input[0].isdigit():
            return find_songs(prompt_input, count)

        if ('.' not in prompt_input or
            prompt_input[-2:] == ".p"):

            for indx in prompt_input.replace(' ', '').split(','):
                if indx[-2:] == '.p':
                    c_pool = stream_pool
                    indx = indx[:-2]
                else:
                    c_pool = download_pool

                if ':' in indx:
                    [lower, upper] = indx.split(':')
                    c_pool += [*range(int(lower), int(upper)+1)]
                elif '-' in indx:
                    [lower, upper] = indx.split('-')
                    c_pool += [*range(int(lower), int(upper)+1)]
                else:
                    c_pool.append(int(indx))

        if prompt_input[-2:] == '.a':
            return find_songs(\
                    f"{song_list[int(prompt_input[:-2])].album_url}", count)

        if prompt_input[-2:] == '.l':
            print(get_lyric(song_list[int(prompt_input[:-2])]))


        def download(i):
            sng = song_list[i]
            get_song_urls(sng)
            status = main_dl(sng, dlformat=fmt, bitrate=bitrate,
                             addlyrics=lyrics, directory=directory,
                             filename=filename, silent=False)
            return status

        with ThreadPoolExecutor(max_workers=multiple,
                initializer=tqdm.set_lock, initargs=(tqdm.get_lock(),)) as exe:
            exe.map(download, download_pool)

        for i in stream_pool:
            sng = song_list[i]
            get_song_urls(sng)
            stream.player(sng)

        return song_list
