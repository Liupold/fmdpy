#!/usr/bin/env python3
"""Test to see if everything is working."""
import os
import sys
import glob
import shutil
import subprocess

# test
os.mkdir('./tmp_test')

os.environ['FMDPY_CONFIG_FILE'] = "./tmp_test/FMDPY.ini"
subprocess.check_call(['fmdpy', '-g'])
print("##########FMDPY.ini#################")
with open("./tmp_test/FMDPY.ini") as f:
    print(f.read())
print("####################################")

args = ['fmdpy', '-c', '10',
        'new', '-d', 'tmp_test', '-f']
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
shutil.rmtree('./tmp_test')
print("(Done)")
