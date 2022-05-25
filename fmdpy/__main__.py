"""__main__ for module fmdpy (cli is handled here)."""
import os
import sys
import ast
import subprocess
from concurrent.futures import ThreadPoolExecutor
from fmdpy import VERSION, install_requires, config, stream

if (len(sys.argv) > 1) and (sys.argv[1] in {'-u', '--update'}):
    subprocess.check_call([sys.executable, '-m', 'pip',
                          'install', '--upgrade', *install_requires])
    sys.exit(0)

try:
    import click
    from fmdpy.api import query, get_song_urls
    from fmdpy.download import main_dl, get_lyric
    from fmdpy.splist import pl_spotify_dl
except ModuleNotFoundError:
    print("Requirements missing, possible fix:\n\tfmdpy -u")
    print("Report to: https://github.com/liupold/fmdpy/issues")
    sys.exit(2)


# This is needed for cli (too-many-arguments and too-many-locals)
# pylint: disable=too-many-arguments disable=too-many-locals
@click.command()
@click.option('-c', "--count", default=int(config['UI']['max_result_count']),
              help="Max Number of results")
@click.option('-f', "--fmt", default=config['DL_OPTIONS']['fmt'],
              help="Format of the audio file.")
@click.option('-b', "--bitrate", default=int(config['DL_OPTIONS']['bitrate']),
              help="Bitrate in kb, (250 is default)")
@click.option('-m', "--multiple",
              default=int(config['DL_OPTIONS']['multiple']),
              help="number of concurrent downloads.")
@click.option('-d', "--directory",
              default=config['DL_OPTIONS']['default_directory'],
              help="Specify the folder.", type=click.Path(exists=True))
@click.option('-l', "--lyrics", help="Add lyrics",
              default=ast.literal_eval(config['DL_OPTIONS']['lyrics']),
              is_flag=True)
@click.option('-V', "--Version", help="display version", is_flag=True)
@click.option('-g', "--gen", help="generate the config file.", is_flag=True)
@click.option('-u', "--update", help="Update: (for pip only)", is_flag=True)
@click.argument('search', nargs=-1)
def fmdpy(count, search, fmt, bitrate, multiple,
          version, lyrics, update, directory, gen):
    """FMDPY.

    Download music with metadata\n
    For multiple download you can use something like:\n

    "fmdpy: 1, 2, 3, 5:8", (This will download 1, 2, 3, 5, 6, 7, 8)\n
    "fmdpy: >1, >2", (This will play (stream) 1, 2) (using player_cmd)\n
    "fmdpy: }5", (This will find lyric of 5)\n
    "fmdpy: ?<KEYWORD>", (This will search songs based on <KEYWORD>).\n

    Streaming, downloading can also be mixed. If done so downloading
    will be done prior to streaming.

    -f native: save to native container [Default](ffmpeg not req.)
    (-b is ignored)
    """
    if update:
        subprocess.check_call([sys.executable, '-m', 'pip',
                              'install', '--upgrade', *install_requires])
        sys.exit(0)

    if version:
        print("fmdpy:", VERSION, f'({sys.executable})')
        sys.exit(0)

    if gen:
        file_path = os.getenv('FMDPY_CONFIG_FILE') or \
            os.path.expanduser('~/.fmdpy.ini')
        with open(file_path, 'w', encoding='utf8') as configfile:
            config.write(configfile)
        sys.exit(0)

    search = ' '.join(search)
    if 'spotify.com/playlist' in search:
        pl_spotify_dl(search, dlformat=fmt, bitrate=bitrate,
                      addlyrics=lyrics)
        sys.exit(0)

    song_list = query(search, count)
    for i, sng in enumerate(song_list):
        print(f'{i+1}) {sng.title} [{sng.artist}] ({sng.year})')

    while True:
        if len(song_list) > 0:
            download_pool = []
            stream_pool = []

            prompt_input = input("\nfmdpy: ")

            if prompt_input in ('quit', 'exit'):
                break

            if prompt_input[0] == '?':
                search = prompt_input[1:]
                song_list = query(search, count)
                for i, sng in enumerate(song_list):
                    print(f'{i+1}) {sng.title} [{sng.artist}] ({sng.year})')
                continue

            if prompt_input[0] == '}':
                print(get_lyric(song_list[int(prompt_input[1:]) - 1]))
                continue

            for indx in prompt_input.replace(' ', '').split(','):
                if indx[0] == '>':
                    c_pool = stream_pool
                    indx = indx[1:]
                else:
                    c_pool = download_pool

                if ':' in indx:
                    [lower, upper] = indx.split(':')
                    c_pool += [*range(int(lower) - 1, int(upper))]
                elif '-' in indx:
                    [lower, upper] = indx.split('-')
                    c_pool += [*range(int(lower) - 1, int(upper))]
                else:
                    c_pool.append(int(indx)-1)

            def download(i):
                sng = song_list[i]
                get_song_urls(sng)

                if multiple <= 1:
                    print(f'{i+1}) {sng.title} [{sng.artist}] ({sng.year})')

                status = main_dl(sng, dlformat=fmt, bitrate=bitrate,
                                 addlyrics=lyrics, directory=directory,
                                 silent=(multiple > 1))

                if status and (multiple > 1):
                    print(f'Downloaded: \
                          {i+1}) {sng.title} [{sng.artist}] ({sng.year})')

                if not status:
                    print(f'Unable to download: {i+1})' +
                          f'{sng.title} [{sng.artist}] ({sng.year})')
                return status

            if multiple > 1:
                with ThreadPoolExecutor(max_workers=multiple) as exe:
                    exe.map(download, download_pool)
            else:
                for i in download_pool:
                    download(i)

            for i in stream_pool:
                sng = song_list[i]
                get_song_urls(sng)
                stream.player(sng)
        else:
            print(f"No result for: {search}")


if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    fmdpy()
