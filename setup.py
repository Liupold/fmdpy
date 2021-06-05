import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fmdpy",
    version="0.2",
    author="Rohn Chatterjee",
    author_email="rohn.ch@gmail.com",
    description="Music Downloader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Liupold/fmdpy",
    license='GPLv3',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['ffmpeg-python', 'click', 'music-tag', 'requests', 'pillow', 'lyricsgenius', 'dataclasses'],
    entry_points = {
        'console_scripts': ['fmdpy=fmdpy.__main__:fmdpy'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    python_requires='>=3.6',
)
