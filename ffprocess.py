#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Simon Erhardt
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import subprocess
import os
import json
import logging
import argparse
import re
import numexpr

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output:
            print(output.strip())
        if process.poll() is not None:
            break

    return process.wait()

parser = argparse.ArgumentParser(description='Batch convert your media library to H264 and AAC.')
parser.add_argument('--quality', required=False, type=int, default=23, help='crf quality of libx264 (default: 23)')
parser.add_argument('--preset', required=False, type=str, default='veryslow', help='encoding preset for libx264 (default: veryslow)')
parser.add_argument('--resolution', required=False, type=int, default=1080, help='maximum resolution in height (default: 1080)')
parser.add_argument('--rate', required=False, type=int, default=25, help='maximum framerate (default: 25)')
parser.add_argument('folder', type=str, help='folder to scan')
args = parser.parse_args()

logFormatter = logging.Formatter('%(asctime)s %(levelname)s:%(name)s %(message)s')
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logging.getLogger().addHandler(consoleHandler)
logging.getLogger().setLevel(logging.DEBUG)

regexp = re.compile('.*\.(mp4|avi|mov|mkv|divx|xvid|flv|webm|m2ts|m1v|m2v|ogm|ogv|wmv)')
regexpTmp = re.compile('.*\.ffprocess_tmp\.mkv')

for root, dirnames, filenames in os.walk(str(args.folder)):
    for filename in filenames:
        # don't touch tmp files
        if regexpTmp.search(filename) is not None:
            continue

        if regexp.search(filename) is not None:
            filepath = os.path.join(root, filename)

            logging.info("Checking file: %s" % filepath)

            cmd = ['ffprobe', '-show_format', '-show_streams', '-loglevel', 'quiet', '-print_format', 'json', filepath]

            ffmpegCmd = ['ffmpeg', '-y', '-i', filepath]
            convertCmd = []
            reconvert = False

            try:
                result = subprocess.check_output(cmd)
                data = json.loads(result.decode("utf-8"))

                bitrateMbps = int(data['format']['bit_rate']) / 1024 / 1024
                logging.info("Bitrate: %d Mbit/s" % bitrateMbps)

                i = 0
                audioStream = 0
                videoStream = 0
                subtitleStream = 0
                for stream in data['streams']:
                    logging.debug("Found stream of type %s" % stream['codec_type'])

                    if stream['codec_type'] == 'video':
                        if videoStream > 0:
                            logging.warning("Only one videostream is supported, continuing...")

                            i += 1
                            continue

                        ffmpegCmd.append("-map")
                        ffmpegCmd.append("0:%d" % i)

                        convertVideo = False
                        videoConvertCmd = []

                        if not stream['codec_name'] == 'h264':
                            logging.info("Video codec is not h264, reconverting...")
                            convertVideo = True

                        try:
                            frameRate = numexpr.evaluate(stream['avg_frame_rate'])
                            if frameRate > args.rate:
                                logging.info("Frame rate is to high, reconverting...")
                                convertVideo = True
                        except ZeroDivisionError:
                            logging.warning("Couldn't get framerate, reconverting...")
                            convertVideo = True

                        if int(stream['height']) > args.resolution:
                            logging.info("Video resolution is to big, reconverting...")

                            # Just scaling
                            videoConvertCmd.append("-vf")
                            videoConvertCmd.append("scale=-1:"+str(args.resolution))
                            videoConvertCmd.append("-sws_flags")
                            videoConvertCmd.append("lanczos")

                            convertVideo = True

                        if convertVideo is True:
                            # reconvert stream
                            convertCmd.append("-c:v")
                            convertCmd.append("libx264")
                            convertCmd.append("-crf")
                            convertCmd.append(str(args.quality))
                            convertCmd.append("-level:v")
                            convertCmd.append("4.1")
                            convertCmd.append("-preset")
                            convertCmd.append(args.preset)
                            convertCmd.append("-bf")
                            convertCmd.append("16")
                            convertCmd.append("-b_strategy")
                            convertCmd.append("2")
                            convertCmd.append("-subq")
                            convertCmd.append("10")
                            convertCmd.append("-refs")
                            convertCmd.append("4")
                            convertCmd.append("-r")
                            convertCmd.append(str(args.rate))
                            convertCmd.append("-pix_fmt")
                            convertCmd.append("yuvj444p")

                            convertCmd += videoConvertCmd
                            reconvert = True
                        else:
                            # copy stream
                            convertCmd.append("-c:v")
                            convertCmd.append("copy")

                        videoStream += 1

                    elif stream['codec_type'] == 'audio':
                        ffmpegCmd.append("-map")
                        ffmpegCmd.append("0:%d" % i)

                        if stream['channel_layout'] == 'stereo' and not stream['codec_name'] == 'aac':
                            logging.info("Audio codec is not aac, reconverting...")

                            convertCmd.append("-c:a:"+str(audioStream))
                            convertCmd.append("libfdk_aac")
                            convertCmd.append("-b:a:"+str(audioStream))
                            convertCmd.append('128k')

                            reconvert = True
                        else:
                            # copy stream
                            convertCmd.append("-c:a:"+str(audioStream))
                            convertCmd.append("copy")

                        audioStream += 1

                    elif stream['codec_type'] == 'subtitle':
                        ffmpegCmd.append("-map")
                        ffmpegCmd.append("0:%d" % i)

                        convertCmd.append("-c:s:"+str(audioStream))
                        convertCmd.append("copy")

                        subtitleStream += 1

                    i += 1

                if reconvert is True:
                    cmd = ffmpegCmd + convertCmd

                    filename, file_extension = os.path.splitext(filepath)
                    filepathTmp = filename + ".ffprocess_tmp.mkv"
                    filepathNew = filename + ".mkv"
                    cmd.append(filepathTmp)

                    logging.debug("Running cmd: %s" % cmd)
                    exitcode = run_command(cmd)

                    if exitcode == 0:
                        logging.info("Converting successfully, removing old stuff...")

                        os.remove(filepath)
                        os.rename(filepathTmp, filepathNew)

                        logging.info("Converting finished...")
                    else:
                        logging.error("Converting failed, continuing...")

                else:
                    logging.info("File is already good, nothing to do...")

            except (subprocess.CalledProcessError, KeyError):
                logging.error("Couldn't check file %s, continuing..." % filepath)
                continue
