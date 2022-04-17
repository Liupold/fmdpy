import subprocess
from fmdpy import config
import ast

def player(sng):
    print('Playing:', sng.title + ' [' + sng.artist + '] ...')
    player_cmd = ast.literal_eval(config['STREAM']['player_cmd'])
    for i, string in enumerate(player_cmd):
        player_cmd[i] = player_cmd[i].replace('$audio', sng.url)
        player_cmd[i] = player_cmd[i].replace('$cover', sng.thumb_url)
        player_cmd[i] = player_cmd[i].replace('$title', sng.title + ' [' + sng.artist + ']')
    subprocess.run(player_cmd)
