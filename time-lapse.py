#!/usr/bin/python
'''
  Creates a Time-Lapse video for your entire desktop at the time
  you specify. This will take screen grabs at an interval that matches
  your desired video length.

  Example (on Windows):
    python time-lapse.py --base 86400 --to 60 --mencoder C:/Sandbox/Software/MPlayer-athlon-svn-34401/mencoder.exe
  
  Example (on Linux):
    python time-lapse.py --base 86400 --to 60

  Example (skip to encoding):
    python time-lapse.py --base 86400 --to 60  --encode

  License under the LGPL
  
  Mohamed Mansour (http://mohamedmansour.com)
'''
import os
import sys
import time
import Image
import ImageGrab
import threading
import argparse

__output__ = '../time-lapse.avi'
__image_path__ = 'images'

class ScreenGrabber(threading.Thread):
  '''
    Uses the Python Imaging Library to take screenshots at every interval.
  '''

  def __init__(self):
    ''' Initializes the threads to start screen grabbing '''
    threading.Thread.__init__(self)
    self.event = threading.Event()
    if not os.path.exists(__image_path__):
      os.mkdir(__image_path__)

  def run(self, total_frames, callback):
    ''' Runs the screen grabbing tool until the intervals completed '''
    sys.stdout.write('  Start screen grabbing in ... ')
    self.event.wait(1)
    sys.stdout.write(' 3')
    self.event.wait(1)
    sys.stdout.write(', 2')
    self.event.wait(1)
    sys.stdout.write(', 1')
    self.event.wait(1)
    sys.stdout.write('. Capturing!\n')

    seconds_per_interval = total_frames / 24
    print '    Total frames to record: %d, each frame every %d seconds' \
        % (total_frames, seconds_per_interval)

    while total_frames > 0:
      self.execute()
      total_frames -= 1
      self.event.wait(seconds_per_interval)

    print '  Done screen grabbing!'
    callback()

  def execute(self):
    ''' Initiates a screengrab and saves it to the images folder '''
    img = ImageGrab.grab()
    path = 'images/ScreenShot_' + time.strftime('%Y_%m_%d_%H_%M_%S') + '.jpg'
    img.save(path)


class MultipleImageEncoder:
  '''
    Encodes a bunch of images into an MPEG-4 video.
  '''
  def __init__(self, mencoder):
    self.mencoder = mencoder

  def run(self):
    ''' Runs mencoder to join the images into a video '''
    print '  Start video encoding ...'
    if not os.listdir(__image_path__):
      print '    There are no images to encode.'
    else:
      os.chdir(__image_path__)
      os.system('%s mf://*.jpg -mf type=jpg -ovc lavc ' \
                '-lavcopts vcodec=mpeg4:mbd=2:trell -oac copy -o %s' \
                 % (self.mencoder.name, __output__))
    print '  Done video encoding!'


class TimeLapse:
  '''
    Manages the time-lapse routine to take screen grabs and encodes after it
    has been completed.
  '''

  def __init__(self):
    ''' Initializes the services and command line arguments '''
    self.args = self.parse_args()
    self.screen_grabber = ScreenGrabber()
    mencoder = 'mencoder'
    if self.args.mencoder:
      mencoder = self.args.mencoder
    self.image_encoder = MultipleImageEncoder(mencoder)

  def parse_args(self):
    ''' Parse arguments command line arguments '''
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--base', dest='base', type=int, required=True,
        help='The total number of seconds to time lapse.')
    parser.add_argument('--to', dest='to', type=int, required=True,
        help='The total number of seconds the resulting video is.')
    parser.add_argument('--mencoder', dest='mencoder', type=file,
        help='The mencoder executable location.')
    parser.add_argument('--skip_capture', action='store_true',
        help='Skip screen captures.')
    parser.add_argument('--skip_encode', action='store_true',
        help='Skip image encoding.')
    return parser.parse_args()

  def start(self):
    ''' Calculates the number of frames to capture within the time lapse '''
    if not self.args.skip_capture and self.args.base < self.args.to:
      print 'Error: Your base must be greater than the to, since we are ' \
            'doing a time lapse.'
      sys.exit(1)

    print 'Start time-lapse ...'
    
    if self.args.skip_capture:
      self.on_screen_grabber_done()
    else:
      total_frames = self.args.base * 24
      total_to_frames = total_frames * self.args.to / self.args.base
      self.screen_grabber.run(total_to_frames,
                              self.on_screen_grabber_done)

  def on_screen_grabber_done(self):
    ''' Callback when screen grab thread has completed, then the encoding will run '''
    if not self.args.skip_encode:
      self.image_encoder.run()
    print 'Done time-lapse!'


if __name__ == "__main__":
  time_lapse = TimeLapse()
  time_lapse.start()
