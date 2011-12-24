Time-Lapse console application written in Python
================================================

Creates a Time-Lapse desktop screensharing to automatically
create a video that runs at 24fps in MPEG4.

You specify the total time of the Time-Lapse and the resulting
time for the result. It will automatically start and create
the video for you within the desired frames per second

**Example (on Windows):**

    python time-lapse.py --base 86400 --to 60 --mencoder C:/Sandbox/Software/MPlayer-athlon-svn-34401/mencoder.exe

**Example (on Linux):**

    python time-lapse.py --base 86400 --to 60

**Example (skip to encoding):**

    python time-lapse.py --base 86400 --to 60  --encode 