"""__main__ for module fmdpy (cli is handled here)."""

import sys
import subprocess
from fmdpy import VERSION, install_requires

if (len(sys.argv) > 1) and (sys.argv[1] in {'-u', '--update'}):
    subprocess.check_call([sys.executable, '-m', 'pip',
                          'install', '--upgrade', *install_requires])
    sys.exit(0)

try:
    import click
    from fmdpy.api import query, get_song_urls
    from fmdpy.download import main_dl
    from fmdpy.splist import pl_spotify_dl
except ModuleNotFoundError:
    print("Requirements missing, possible fix:\n\tfmdpy -u")
    print("Report to: https://github.com/liupold/fmdpy/issues")
    sys.exit(2)
# This is needed for cli (too-many-arguments and too-many-locals)
# pylint: disable=too-many-arguments disable=too-many-locals


@click.command()
@click.option('-c', "--count", default=10, help="Max Number of results")
@click.option('-f', "--fmt", default='native',
              help="Format of the audio file.")
@click.option('-b', "--bitrate", default=250,
              help="Bitrate in kb, (250k is default)")
@click.option('-d', "--directory", default='./',
              help="Specify the folder.", type=click.Path(exists=True))
@click.option('-l', "--lyrics", help="Add lyrics", is_flag=True)
@click.option('-V', "--Version", help="display version", is_flag=True)
@click.option('-u', "--update", help="Update: (for pip only)", is_flag=True)
@click.argument('search', nargs=-1)
def fmdpy(count, search, fmt, bitrate, version, lyrics, update, directory):
    """FMDPY.

    Download music with metadata\n
    For multiple download you can use something like:\n
    "Download: 1, 2, 3, 5:8", (This will download 1, 2, 3, 5, 6, 7, 8)

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

    search = ' '.join(search)
    if 'spotify.com/playlist' in search:
        pl_spotify_dl(search, dlformat=fmt, bitrate=bitrate,
                      addlyrics=lyrics)
        sys.exit(0)

    song_list = query(search, count)
    for i, sng in enumerate(song_list):
        print(f'{i+1}) {sng.title} [{sng.artist}] ({sng.year})')

    if len(song_list) > 0:
        download_pool = []
        to_download = input("\nDownload: ")
        for indx in to_download.replace(' ', '').split(','):
            if ':' in indx:
                [lower, upper] = indx.split(':')
                download_pool += [*range(int(lower) - 1, int(upper))]
            elif '-' in indx:
                [lower, upper] = indx.split('-')
                download_pool += [*range(int(lower) - 1, int(upper))]
            else:
                download_pool.append(int(indx)-1)

        for i in download_pool:
            sng = song_list[i]
            print(f'{i+1}) {sng.title} [{sng.artist}] ({sng.year})')
            get_song_urls(sng)
            if not main_dl(sng, dlformat=fmt, bitrate=bitrate,
                           addlyrics=lyrics, directory=directory):
                print(f'Unable to download: {i+1})' +
                      f'{sng.title} [{sng.artist}] ({sng.year})')
            print("\n")
    else:
        print(f"No result for: {search}")


if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    fmdpy()
