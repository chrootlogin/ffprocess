# ffprocess

A small docker container including ffmpeg to batch convert your media library to a defined h264/aac profile.

## Features

 * Made for Docker.
 * Converts files only if needed.
 * You can set a maximum framerate and resolution.
 
## Dependencies when used standalone
   
 * FFMpeg with libfdk_aac, libx264 and any codec that you have in your library

## Usage

If you have ffmpeg and python installed on your computer, you can use this script directly, but I recommend to use the docker image, because there are already all needed codecs inside.

```
usage: ffprocess.py [-h] [--quality QUALITY] [--preset PRESET]
                    [--resolution RESOLUTION] [--rate RATE]
                    folder

Process your media library.

positional arguments:
  folder                folder to scan

optional arguments:
  -h, --help            show this help message and exit
  --quality QUALITY     crf quality of libx264 (default: 23)
  --preset PRESET       encoding preset for libx264 (default: veryslow)
  --resolution RESOLUTION
                        maximum resolution in height (default: 1080)
  --rate RATE           maximum framerate (default: 25)
```

**With docker:**

```
usage: docker run -v /my/media/folder:/data rootlogin/ffprocess
                    [-h] [--quality QUALITY] [--preset PRESET]
                    [--resolution RESOLUTION] [--rate RATE]

Process your media library.

optional arguments:
  -h, --help            show this help message and exit
  --quality QUALITY     crf quality of libx264 (default: 23)
  --preset PRESET       encoding preset for libx264 (default: veryslow)
  --resolution RESOLUTION
                        maximum resolution in height (default: 1080)
  --rate RATE           maximum framerate (default: 25)
```

## Warranty

This software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. It could even start a nuclear war or kill your kittens. ;)