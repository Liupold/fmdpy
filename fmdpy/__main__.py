"""__main__ for module fmdpy (cli is handled here)."""
import os
import sys
import ast
import subprocess
from tqdm import tqdm
from threading import RLock as TRLock
from fmdpy import ART, VERSION, install_requires, config

if (len(sys.argv) > 1) and (sys.argv[1] in {'-u', '--update'}):
    subprocess.check_call([sys.executable, '-m', 'pip',
                          'install', '--upgrade', *install_requires])
    sys.exit(0)

try:
    import click
    from fmdpy.prompt import FmdpyPrompt, find_songs, list_songs
except ModuleNotFoundError:
    print("Requirements missing, possible fix:\n\tfmdpy -u")
    print("Report to: https://github.com/liupold/fmdpy/issues")
    sys.exit(2)


def gen(ctx, _, value):
    if not value:
        return
    else:
        file_path = os.getenv('FMDPY_CONFIG_FILE') or \
            os.path.expanduser('~/.fmdpy.ini')
        with open(file_path, 'w', encoding='utf8') as configfile:
            config.write(configfile)
        click.echo(f"generated config into: {file_path}")
        ctx.exit()

def update(ctx, _, value):
    if not value:
        return
    else:
        subprocess.check_call([sys.executable, '-m', 'pip',
            'install', '--upgrade', *install_requires])
        ctx.exit()

def version(ctx, _, value):
    if not value:
        return
    else:
        click.echo(ART)
        click.echo(f"fmdpy: {VERSION} ({sys.executable})")
        ctx.exit()


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
              help="Specify the folder.", type=click.Path())

@click.option('-F', "--filename", default=config['DL_OPTIONS']['filename'],
              help="filename format.")

@click.option('-l', "--lyrics", help="Add lyrics",
              default=ast.literal_eval(config['DL_OPTIONS']['lyrics']),
              is_flag=True)

@click.option('-g', "--gen", help="generate the config file.", is_flag=True,
        callback=gen, expose_value=False, is_eager=True)

@click.option('-u', "--update", help="Update: (for pip only)", is_flag=True,
        callback=update, expose_value=False, is_eager=True)

@click.option('-v', "--version", help="display version", is_flag=True,
        callback=version, expose_value=False, is_eager=True)

@click.argument('search', nargs=-1)

def fmdpy(count, search, fmt, bitrate, multiple,
        lyrics, directory, filename):
    """FMDPY.

    Download music with metadata\n
    For multiple download you can use something like:\n

    "fmdpy: 1, 2, 3, 5:8", (This will download 1, 2, 3, 5, 6, 7, 8)\n
    "fmdpy: 1.p, 2.p", (This will play (stream) 1, 2) (using player_cmd)\n
    "fmdpy: 5.p", (This will find lyric of 5)\n
    "fmdpy: 3.a", (This will go to album which 3 belongs to)\n
    "fmdpy: <SEARCH/URL>", (This will search songs based on <SEARCH/URL>).\n

    Streaming, downloading can also be mixed. If done so downloading
    will be done prior to streaming.

    -f native: save to native container [Default](ffmpeg not req.)
    (-b is ignored)
    """

    search = ' '.join(search)
    if 'spotify.com/playlist' in search:
        song_list = get_songs_splist(search)
        list_songs(song_list)
    else:
        song_list = find_songs(search, count)

    config['UI']['max_result_count'] = str(count)
    config['DL_OPTIONS']['bitrate'] = str(bitrate)
    config['DL_OPTIONS']['fmt'] = fmt
    config['DL_OPTIONS']['multiple'] = str(multiple)
    config['DL_OPTIONS']['default_directory'] = directory
    config['DL_OPTIONS']['filename'] = filename
    config['DL_OPTIONS']['lyrics'] = str(lyrics)


    fprompt = FmdpyPrompt(f"fmdpy (v{VERSION})-> ", song_list, config)
    fprompt.song_list = song_list
    fprompt.run()


if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    tqdm.set_lock(TRLock())
    fmdpy()
