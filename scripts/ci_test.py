#!/usr/bin/env python3
"""Test to see if everything is working."""
import os
import sys
import glob
import shutil
import subprocess

print("Building....")
subprocess.check_call([sys.executable, './scripts/build.py'])
print("(Done)")

print("Installing...")
wheel_file = glob.glob('./dist/fmdpy-*.whl')[0]
subprocess.check_call([sys.executable, '-m', 'pip', 'install', wheel_file])
print("(Done)")


# test
os.mkdir('./tmp_test')

os.environ['FMDPY_CONFIG_FILE'] = "./tmp_test/FMDPY.ini"
subprocess.check_call([sys.executable, '-m', 'fmdpy', '-g'])
print("##########FMDPY.ini#################")
with open("./tmp_test/FMDPY.ini") as f:
    print(f.read())
print("####################################")

args = [sys.executable, '-m', 'fmdpy', '-c', '10',
        '', '-d', 'tmp_test', '-f']
with subprocess.Popen([*args, 'mp3'],
                      stdin=subprocess.PIPE, stdout=subprocess.PIPE) as cp:
    cp.communicate('3-6,1\n'.encode())
assert len(glob.glob('./tmp_test/*.mp3')) == 5

with subprocess.Popen([*args, 'opus'],
                      stdin=subprocess.PIPE, stdout=subprocess.PIPE) as cp:
    cp.communicate('4:7, 2\n'.encode())
assert len(glob.glob('./tmp_test/*.opus')) == 5

with subprocess.Popen([*args, 'native', '-m', '4'],
                      stdin=subprocess.PIPE, stdout=subprocess.PIPE) as cp:
    cp.communicate('1, 2:5\n'.encode())
assert len(glob.glob('./tmp_test/*.mp4')) == 5

# cleaning
print("Cleaning...")
shutil.rmtree('./dist')
shutil.rmtree('./tmp_test')
print("(Done)")

# uninstall
print("Uninstalling...")
subprocess.check_call([sys.executable, '-m',
                      'pip', 'uninstall', '-y', 'fmdpy'])
print("(Done)")
