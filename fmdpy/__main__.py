import click
from fmdpy.api import query, getSongURLs
from fmdpy.download import *
from fmdpy import VERSION
import sys

@click.command()
@click.option('-c', "--count", default=30, help="Max Number of results")
@click.option('-f', "--fmt", default='opus', help="Format of the audio file. (opus is default)")
@click.option('-b', "--bitrate", default=250, help="Bitrate in kb, (250k is default)")
@click.option('-d', "--directory", default='./', help="Specify the folder.", type=click.Path(exists=True))
@click.option('-l', "--lyrics", help="Add lyrics", is_flag=True)
@click.option('-V', "--Version", help="display version", is_flag=True)
@click.argument('search', nargs=-1)
def fmdpy(count, search, fmt, bitrate, version, lyrics, directory):
    if version:
        print("fmdpy:", VERSION)
        sys.exit(0)
    search=' '.join(search)
    song_list = query(search, count)
    for i, s in enumerate(song_list):
        print(f'{i+1}) {s.title} [{s.artist}] ({s.year})')

    download_pool = [];
    to_download = input("\nDownload: ")

    for indx in to_download.replace(' ', '').split(','):
        if ':' in indx:
            [l, u] = indx.split(':')
            [ download_pool.append(i - 1) for i in range(int(l), int(u)+1) ]
        elif '-' in indx:
            [l, u] = indx.split('-')
            [ download_pool.append(i - 1) for i in range(int(l), int(u)+1) ]
        else:
            download_pool.append(int(indx) - 1)

    for i in download_pool:
        s = song_list[i]
        print(f'{i+1}) {s.title} [{s.artist}] ({s.year})')
        getSongURLs(s)
        if not Dl(s, dlformat=fmt, bitrate=bitrate, addlyrics=lyrics, directory=directory):
            print(f'Unable to download: {i+1}) {s.title} [{s.artist}] ({s.year})')
        print("\n")

if __name__ == '__main__':
    fmdpy()
