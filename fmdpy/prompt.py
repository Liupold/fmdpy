import os
import sys
import platform
import ast
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Event
from fmdpy import ART, stream, cache_dir
from fmdpy.api import query, get_song_urls
from fmdpy.download import main_dl, get_lyric
from fmdpy.save_load import save, load, list_saves
from tqdm import tqdm

if platform.system() in ('Linux'):
    import readline

def list_songs(song_list):
    for i, sng in enumerate(song_list):
        print(f'{i+1}) {sng.title} [{sng.artist}] ({sng.year})')
    print("\n")

def find_songs(search_str, count):
    song_list = query(search_str, count)
    list_songs(song_list)
    return song_list

class FmdpyPrompt():
    def __init__(self, prompt, song_list, config):
        self.prompt = prompt
        self.song_list = song_list
        self.config = config
        self.download_pool = []
        self.stream_pool = []
        self.stop_sig = Event()

        if platform.system() in ('Linux'):
            self.histfile =  cache_dir + '/hist'
            if not (os.path.exists(self.histfile)):
                with open(self.histfile, 'w') as _:
                    pass

    def do_exit(self):
        sys.exit()

    def do_find_songs(self, search_str):
        self.song_list = find_songs(search_str,
                                    int(self.config['UI']['max_result_count']))

    def update_pool(self, prompt_str):
        for indx in prompt_str.replace(' ', '').split(','):
            if indx[-2:] == '.p':
                c_pool = self.stream_pool
                indx = indx[:-2]
            else:
                c_pool = self.download_pool
            if ':' in indx:
                [lower, upper] = indx.split(':')
                c_pool += [*range(int(lower), int(upper)+1)]
            elif '-' in indx:
                [lower, upper] = indx.split('-')
                c_pool += [*range(int(lower), int(upper)+1)]
            else:
                c_pool.append(int(indx))

    def do_get_album(self, prompt_str):
        self.song_list = find_songs(\
                f"{self.song_list[int(prompt_str[:-2]) - 1].album_url}",
                                    int(self.config['UI']['max_result_count']))

    def do_get_lyric(self, prompt_str):
        print(get_lyric(self.song_list[int(prompt_str[:-2]) - 1]))

    def DL(self):
        with ThreadPoolExecutor(max_workers=int(self.config['DL_OPTIONS']['multiple']),
                initializer=tqdm.set_lock, initargs=(tqdm.get_lock(),)) as exe:
            futures = []
            for i in self.download_pool:
                future = exe.submit(main_dl, song_obj=self.song_list[i - 1],
                                    dlformat=self.config['DL_OPTIONS']['fmt'],
                                    bitrate=int(self.config['DL_OPTIONS']['bitrate']),
                                    addlyrics=ast.literal_eval(self.config['DL_OPTIONS']['lyrics']),
                                    directory=self.config['DL_OPTIONS']['default_directory'],
                                    filename=self.config['DL_OPTIONS']['filename'],
                                    dltext=f"{i}",
                                    silent=False, stop_sig=self.stop_sig)
                futures.append(future)
            try:
                for future in as_completed(futures):
                    future.result()
            except KeyboardInterrupt:
                self.stop_sig.set()
                exe.shutdown(wait=True, cancel_futures=True)
                sys.stdout.flush()
                print("\n\nAborting Downloads!!!\n")

    def SM(self):
        for i in self.stream_pool:
            sng = self.song_list[i - 1]
            get_song_urls(sng)
            stream.player(sng)

    def do_get_config(self):
        for sect in self.config.sections():
            print(f"[{sect}]")
            for key, val in self.config.items(sect):
                print(f"{key} = {val}")
            print("\n")

    def parse_input(self, prompt_str):
        if prompt_str == '':
            pass
        elif prompt_str == '.help':
            print(
            """
             fmdpy prompt help!
            --------------------
            operator by defination operates on
            song (is identified using index number).
            `{}` stands for the song index.

            Operators:
            {}, {}-{}, {}:{}: Will download the songs from the list.
            {}.p, {}-{}.p, {}:{}.p: Will stream the songs from the list.
            {}.l: will show the lyrics

            Commands:
            .conf : show the config (priority: command line > config file > default)
            .ls: show the current song list.
            .save {name}: save the current song list.
            .lsave: list all the saved song list.
            .load {name}: load the saved song list.

            some commands needs arguments, which are
            shown in curly brackets.
            """)
        elif (not prompt_str[0].isdigit() \
                and '.' != prompt_str[0]):
            self.do_find_songs(prompt_str)
        elif ('.' not in prompt_str or
              prompt_str[-2:] == ".p"):
            self.update_pool(prompt_str)
            self.SM()
            self.DL()
        elif prompt_str[-2:] == '.a':
            self.do_get_album(prompt_str)

        elif prompt_str[-2:] == '.l':
            self.do_get_lyric(prompt_str)

        elif prompt_str in ('.q', '.bye', '.exit', '.quit'):
            readline.write_history_file(self.histfile)
            sys.exit()

        elif prompt_str == ".conf":
            self.do_get_config()

        elif prompt_str == ".art":
            print(ART)
        elif prompt_str == ".ls":
            list_songs(self.song_list)

        elif prompt_str[0:5] == ".load":
            self.song_list = load(prompt_str[5:].strip())
            list_songs(self.song_list)

        elif prompt_str[0:5] == ".save":
            save(self.song_list, \
                    prompt_str[5:].strip())
            print("Saved!")
        elif prompt_str == ".lsave":
            list_saves()
        else:
            if prompt_str[0].isdigit():
                print("Unknown operator: ",
                      prompt_str.split('.')[1])
            else:
                print(f"Unknown . cmd: {prompt_str}")

    def run(self):
        if platform.system() in ('Linux'):
            readline.read_history_file(self.histfile)
        while True:
            try:
                prompt_input = input(self.prompt).strip()
            except KeyboardInterrupt:
                print("\nGoodbye cruel world! :)")
                break

            if platform.system() in ('Linux'):
                readline.write_history_file(self.histfile)

            self.download_pool = []
            self.stream_pool = []
            self.stop_sig.clear()
            self.parse_input(prompt_input)
