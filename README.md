# FMDPY

[![PIP-PYVERSION](https://img.shields.io/pypi/pyversions/fmdpy)](https://pypi.org/project/fmdpy/)
[![CI-STATUS](https://github.com/Liupold/fmdpy/workflows/CI/badge.svg)](https://github.com/Liupold/fmdpy/actions?query=workflow%3A%22CI%22)
[![CD-STATUS](https://github.com/Liupold/fmdpy/workflows/CD/badge.svg)](https://github.com/Liupold/fmdpy/actions?query=workflow%3A%22CD%22)
[![license](https://img.shields.io/github/license/liupold/fmdpy.svg)](https://github.com/liupold/fmdpy/blob/master/LICENSE)
[![PIP-VERSION](https://img.shields.io/pypi/v/fmdpy.svg)](https://pypi.org/project/fmdpy/)
[![Downloads](https://pepy.tech/badge/fmdpy/month)](https://pepy.tech/project/fmdpy)
[![PIP-STATUS](https://img.shields.io/pypi/status/fmdpy)](https://pypi.org/project/fmdpy/)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/95456cb6f9484d7fafb70ea3e43e9322)](https://www.codacy.com/gh/Liupold/fmdpy/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Liupold/fmdpy&amp;utm_campaign=Badge_Grade)

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
From github: (after clone)
```
python ./install.py
```
## UPDATE:
```
fmdpy -u
```

## USEAGE
```text
Usage: fmdpy [OPTIONS] [SEARCH]...

  FMDPY.

  Download music with metadata

  For multiple download you can use something like:

  "Download: 1, 2, 3, 5:8", (This will download 1, 2, 3, 5, 6, 7, 8)

  -f native: save to native container [Default](ffmpeg not req.) (-b is
  ignored)

Options:
  -c, --count INTEGER    Max Number of results
  -f, --fmt TEXT         Format of the audio file.
  -b, --bitrate INTEGER  Bitrate in kb, (250k is default)
  -d, --directory PATH   Specify the folder.
  -l, --lyrics           Add lyrics
  -V, --Version          display version
  -u, --update           Update: (for pip only)
  --help                 Show this message and exit.
```

## EXAMPLE

![example.gif](example.gif)
