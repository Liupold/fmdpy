"""The following module helps in fmdpy streaming."""
import subprocess
from fmdpy import config
import ast

def player(sng):
    """Player based on player_cmd.

    Input: sng (song object)
    retuns: CompletedProces
    """
    print('Playing:', sng.title + ' [' + sng.artist + '] ...')
    player_cmd = ast.literal_eval(config['STREAM']['player_cmd'])
    for i, string in enumerate(player_cmd):
        string = string.replace('$audio', sng.url)
        string = string.replace('$cover', sng.thumb_url)
        string = string.replace('$title', sng.title + ' [' + sng.artist + ']')
        player_cmd[i] = string
    subprocess.run(player_cmd)
