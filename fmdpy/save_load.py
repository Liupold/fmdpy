import pickle
import os
from fmdpy import cache_dir

def save(obj, name):
    filename = cache_dir + f'/{name}.fmdpy'
    with open(os.path.expanduser(filename), \
            'wb') as f:
        return pickle.dump(obj, f)

def load(name):
    filename = cache_dir + f'/{name}.fmdpy'
    with open(os.path.expanduser(filename), \
            'rb') as f:
        return pickle.load(f)

def list_saves():
    if not os.path.exists(cache_dir):
        return

    print("SAVES:")
    for n in os.listdir(cache_dir):
        if (os.path.isfile(f"{cache_dir}/{n}") \
                and n[-6:] == ".fmdpy"):
            print(f"- {n[:-6]}")
    print("\n")
