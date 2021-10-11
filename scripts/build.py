#!/usr/bin/env python3
"""Build fmdpy."""

import sys
import shutil
import subprocess

# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user',
                      '--upgrade', 'wheel', 'twine'])
subprocess.check_call([sys.executable, 'setup.py', 'sdist', 'bdist_wheel'])

# clean up
shutil.rmtree('build')
shutil.rmtree('fmdpy.egg-info')
