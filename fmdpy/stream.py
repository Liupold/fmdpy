"The following module helps in fmdpy streaming."
import subprocess
from fmdpy import config
import ast

def player(sng):
    """Player based on player_cmd, which can play sng
    sng being the song object.
    retuns: CompletedProces
    """
    print('Playing:', sng.title + ' [' + sng.artist + '] ...')
    player_cmd = ast.literal_eval(config['STREAM']['player_cmd'])
    for i in range(len(player_cmd)):
        player_cmd[i] = player_cmd[i].replace('$audio', sng.url)
        player_cmd[i] = player_cmd[i].replace('$cover', sng.thumb_url)
        player_cmd[i] = player_cmd[i].replace('$title', sng.title + ' [' + sng.artist + ']')
    return subprocess.run(player_cmd)
