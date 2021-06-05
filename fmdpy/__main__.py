import click
from fmdpy.api import query, getSongURLs
from fmdpy.download import *

@click.command()
@click.option('-c', "--count", default=30, help="Max Number of results")
@click.option('-f', "--fmt", default='opus', help="Format of the audio file.")
@click.argument('search', nargs=-1)
def fmdpy(count, search, fmt):
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
        Dl(s, fmt)

if __name__ == '__main__':
    fmdpy()
