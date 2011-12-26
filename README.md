Time-Lapse console application written in Python
================================================

Creates a Time-Lapse desktop screensharing to automatically
create a video that runs at 24fps in MPEG4.

You specify the total time of the Time-Lapse and the resulting
time for the result. It will automatically start and create
the video for you within the desired frames per second

Prerequisistes
--------------

This script depends on the following software to be installed.

 * Python 2.7
 * PIL Extensions
 * MEncoder

Examples
--------
**Example (on Windows):**

    python time-lapse.py --base 86400 --to 60 --mencoder C:/Sandbox/Software/MPlayer-athlon-svn-34401/mencoder.exe

**Example (on Linux):**

    python time-lapse.py --base 86400 --to 60

**Example (skip to encoding):**

    python time-lapse.py --base 86400 --to 60  --skip-captures

**Example (skip encoding just capture):**

    python time-lapse.py --base 86400 --to 60  --skip-encode

**Help**

    python time-lapse.py -h
    usage: time-lapse.py [-h] --base BASE --to TO [--mencoder MENCODER] [--encode]
    
    Process some integers.
    
    optional arguments:
      -h, --help           show this help message and exit
      --base BASE          The total number of seconds to time lapse.
      --to TO              The total number of seconds the resulting video is.
      --mencoder MENCODER  The mencoder executable location.
      --encode             Skip screen grabbing and directly encode the images.

