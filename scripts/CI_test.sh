#!/bin/sh
set -e

# make and install
sudo apt-get install ffmpeg

echo "Building...."
./scripts/build_pip.sh
echo "(Done)"

echo "Installing..."
python -m  pip install ./dist/fmdpy-*.whl
echo "(Done)"

# test
echo "7:8" | fmdpy "new songs" \
        && [ "$(find -name '*.mp3' | wc -l)" -eq 2 ]

echo "1, 4" | fmdpy "new songs" opus \
        && [ "$(find -name '*.opus' | wc -l)" -eq 2 ]


# cleaning
echo "Cleaning..."
rm -rf ./dist
echo "(Done)"

# uninstall
echo "Uninstalling..."
python -m pip uninstall -y fmdpy
echo "(Done)"
