# ffprocess

[![](https://images.microbadger.com/badges/image/rootlogin/ffprocess.svg)](https://microbadger.com/images/rootlogin/ffprocess "Get your own image badge on microbadger.com") [![](https://images.microbadger.com/badges/version/rootlogin/ffprocess.svg)](https://microbadger.com/images/rootlogin/ffprocess "Get your own version badge on microbadger.com") [![](https://images.microbadger.com/badges/commit/rootlogin/ffprocess.svg)](https://microbadger.com/images/rootlogin/ffprocess "Get your own commit badge on microbadger.com")

A small docker container including ffmpeg to batch convert your media library to a defined h264/aac profile.

-> [DockerHub](https://hub.docker.com/r/rootlogin/ffprocess/)

## Features

 * Made for Docker.
 * Converts files only if needed.
 * You can set a maximum framerate and resolution.
 
## Dependencies when used standalone
   
 * FFMpeg with libfdk_aac, libx264 and any codec that you have in your library.

## Usage

**With docker:**

```
usage: docker run -v /my/media/folder:/data rootlogin/ffprocess
                    [-h] [--quality QUALITY] [--preset PRESET]
                    [--resolution RESOLUTION] [--rate RATE]

Batch convert your media library to H264 and AAC.

optional arguments:
  -h, --help            show this help message and exit
  --quality QUALITY     crf quality of libx264 (default: 23)
  --preset PRESET       encoding preset for libx264 (default: veryslow)
  --resolution RESOLUTION
                        maximum resolution in height (default: 1080)
  --rate RATE           maximum framerate (default: 25)
```

**Standalone:**

If you have ffmpeg and python installed on your computer, you can use this script directly, but I recommend to use the docker image, because there are already all needed codecs inside.

Install dependencies with `pip install -r requirements.txt`.

```
usage: ffprocess.py [-h] [--quality QUALITY] [--preset PRESET]
                    [--resolution RESOLUTION] [--rate RATE]
                    folder

Batch convert your media library to H264 and AAC.

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

## Warranty

This software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. It could even start a nuclear war or kill your kittens. ;)

## Donate

If you want to donate for this project, you can send me some coins to the following address.

**Bitcoin**: 1CCzVGMgoEbd5Zn84QnqjNFRj4PZtAoTrC

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.