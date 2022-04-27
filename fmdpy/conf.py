"""Config Module for fmpdy."""
import os
import configparser


def load():
    """Loader of config (.ini) files for fmdpy."""
    config = configparser.ConfigParser()

    config['DEFAULT'] = {}

    config['UI'] = {
            'max_result_count': "10",
    }

    config['DL_OPTIONS'] = {
            'fmt': "native",
            'lyrics': "False",
            'bitrate': '250',
            'default_directory': "./",
            'multiple': '1',
    }

    config['API_KEYS'] = {
            'spotify_client_id': "",
            'spotify_client_secret': "",
            'lyricsgenius': "",
    }

    config['STREAM'] = {
            'player_cmd': ['setsid', '-f', 'mpv', '$audio',
                '--cover-art-file=$cover',
                '--force-media-title=$title',
                '--really-quiet',
                '--oset-metadata-set=comment="a"', '--no-terminal'],
    }

    file_path = os.getenv('FMDPY_CONFIG_FILE') or \
        os.path.expanduser('~/.fmdpy.ini')

    if os.path.isfile(file_path):
        config.read(file_path)

    return config
