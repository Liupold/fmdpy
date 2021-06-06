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
echo "5:8, 12" | fmdpy -c 20 "new songs" -f mp3 \
        && [ "$(find -name '*.mp3' | wc -l)" -eq 5 ]

echo "1, 4, 9:11" | fmdpy -c 20 new songs \
        && [ "$(find -name '*.opus' | wc -l)" -eq 5 ]


# cleaning
echo "Cleaning..."
rm -rf ./dist
echo "(Done)"

# uninstall
echo "Uninstalling..."
python -m pip uninstall -y fmdpy
echo "(Done)"
