# FMDPY

[![PIP-PYVERSION](https://img.shields.io/pypi/pyversions/fmdpy)](https://pypi.org/project/fmdpy/)
[![license](https://img.shields.io/github/license/liupold/fmdpy.svg)](https://github.com/liupold/fmdpy/blob/master/LICENSE)
[![PIP-VERSION](https://img.shields.io/pypi/v/fmdpy.svg)](https://pypi.org/project/fmdpy/)
[![PIP-STATUS](https://img.shields.io/pypi/status/fmdpy)](https://pypi.org/project/fmdpy/)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/95456cb6f9484d7fafb70ea3e43e9322)](https://www.codacy.com/gh/Liupold/fmdpy/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Liupold/fmdpy&amp;utm_campaign=Badge_Grade)

[![CI-STATUS](https://github.com/Liupold/fmdpy/workflows/CI/badge.svg)](https://github.com/Liupold/fmdpy/actions?query=workflow%3A%22CI%22)
[![CD-STATUS](https://github.com/Liupold/fmdpy/workflows/CD/badge.svg)](https://github.com/Liupold/fmdpy/actions?query=workflow%3A%22CD%22)

[![Downloads](https://pepy.tech/badge/fmdpy)](https://pepy.tech/project/fmdpy)

```text

 ,dPYb,                            8I
 IP'`Yb                            8I
 I8  8I                            8I
 I8  8'                            8I
 I8 dP   ,ggg,,ggg,,ggg,     ,gggg,8I  gg,gggg,    gg     gg
 I8dP   ,8" "8P" "8P" "8,   dP"  "Y8I  I8P"  "Yb   I8     8I
 I8P    I8   8I   8I   8I  i8'    ,8I  I8'    ,8i  I8,   ,8I
,d8b,_ ,dP   8I   8I   Yb,,d8,   ,d8b,,I8 _  ,d8' ,d8b, ,d8I
PI8"8888P'   8I   8I   `Y8P"Y8888P"`Y8PI8 YY88888PP""Y88P"888
 I8 `8,                                I8               ,d8I'
 I8  `8,                               I8             ,dP'8I
 I8   8I                               I8            ,8"  8I
 I8   8I                               I8            I8   8I
 I8, ,8'                               I8            `8, ,8I
  "Y8P'                                I8             `Y8P"
```

## INSTALL
From PIP:
```shell
python -m pip install --upgrade fmdpy
```
From github:

```shell
python -m pip install git+https://github.com/Liupold/fmdpy
```
## UPDATE

```shell
fmdpy -u
```

## USAGE
```text
Usage: fmdpy [OPTIONS] [SEARCH]...

  FMDPY.

  Download music with metadata

  For multiple download you can use something like:

  "fmdpy: 1, 2, 3, 5:8", (This will download 1, 2, 3, 5, 6, 7, 8)

  "fmdpy: >1, >2", (This will play (stream) 1, 2) (using player_cmd)

  "fmdpy: }5", (This will find lyric of 5)

  "fmdpy: ?<KEYWORD>", (This will search songs based on <KEYWORD>).

  Streaming, downloading can also be mixed. If done so downloading will be
  done prior to streaming.

  -f native: save to native container [Default](ffmpeg not req.) (-b is
  ignored)

Options:
  -c, --count INTEGER     Max Number of results
  -f, --fmt TEXT          Format of the audio file.
  -b, --bitrate INTEGER   Bitrate in kb, (250 is default)
  -m, --multiple INTEGER  number of concurrent downloads.
  -d, --directory PATH    Specify the folder.
  -l, --lyrics            Add lyrics
  -V, --Version           display version
  -g, --gen               generate the config file.
  -u, --update            Update: (for pip only)
  --help                  Show this message and exit.
```

## CONFIG
The default location of config file is `~/.fmdpy.ini` and can be set
using env var `FMDPY_CONFIG_FILE`

The sample file is available in repo. `example.ini`
This is by no means necessary for the operation.

To generate the config file use `fmdpy -g`

## SPOTIFY support

It can download playlist from spotify given the following is set in
config file.
```ini
[API_KEYS]
spotify_client_id =
spotify_client_secret =
```
## Lyrics from lyrics genius
It can also add lyrics from lyricsgenius into the meta data given the following is set in config file.
```ini
[API_KEYS]
lyricsgenius =
```

## Streaming
For Streaming (version: 0.5+) is required and
the following must be set.

```ini
[STREAM]
player_cmd =
```
(The default `player_cmd` uses mpv)
in `player_cmd` The following strings will be replaced:

| Strings  | Replaced By                           |
|----------|---------------------------------------|
| `$audio` | The URL of the music file.            |
| `$cover` | The URL of the cover art file. (JPEG) |
| `$title` | SONG_NAME \[ARTIST_NAME\]               |

### vlc example
`player_cmd = ['vlc', '$audio']`

## EXAMPLE

![example.gif](example.gif)
