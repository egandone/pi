import pygame
import time
import os
import glob
import ftplib
import sys
import subprocess
import re
import refresh_screens
from datetime import datetime, timedelta

class Display:
    def __init__(self):
        self.open()

    def show_image(self, image):
        image = self.scale_image(image)
        self.screen.blit(image, (0, 0))
        pygame.display.flip()
        
    def scale_image(self, image):
        return pygame.transform.scale(pygame.image.load(image), self.size)

    def open(self):
        pygame.display.init()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.size = self.screen.get_size()

    def close(self):
        pygame.display.quit()

if __name__ == "__main__":
    # Download images every 20 minutes
    check_interval = timedelta(minutes=20)
    
    # Set the initial value for las_checked to the
    # nearest 20 minute boundary not past the current time
    #
    # This makes the refresh time deterministic rather
    # then being impacted by when the program first
    # ran.  Effectively this means the images are freshed
    # 3 times an hour @ 00, 20, and 40
    n = datetime.now()
    rounded_minutes = (n.minute / 20) * 20
    last_checked = datetime(n.year, n.month, n.day, n.hour, rounded_minutes, 0, 0)
    print 'Started @ ' + last_checked.strftime('%Y-%m-%d %H:%M:%S')

    # Initialize infiles to an empty list to
    # force an image download on initial startup
    infiles = []
    display = Display()
    display.open()
    path = '/home/pi/screens'
    while True:
	current_time = datetime.now()
	elapsed_time = current_time - last_checked
	if (elapsed_time > check_interval) or (len(infiles) == 0):
            print 'Refreshing images @ ' + current_time.strftime('%Y-%m-%d %H:%M:%S')
            refresh_screens.check_files(path, current_time.strftime('%Y-%m-%d'))
            # last_checked rounds to the minute to keep the timing of 
            # the refreshed deterministic
            rounded_minutes = (current_time.minute / 20) * 20
            last_checked = datetime(current_time.year, current_time.month, current_time.day, current_time.hour, rounded_minutes, 0, 0)

        infiles = glob.glob(os.path.join(path, '*.[Jj][Pp][Gg]'))
        infiles.extend(glob.glob(os.path.join(path, '*.[Pp][Nn][Gg]')))
        infiles.extend(glob.glob(os.path.join(path, '*.[Mm][Pp]4')))
        infiles.sort()
        for infile in infiles:
            # print 'Show file ' + infile
            video_file = re.search('[Mm][Pp]4$', infile)
            if  (video_file != None):
                a = subprocess.call(["omxplayer", "-o", "hdmi", infile])
            else:
            	display.show_image(infile)
            	# Show each image for 10 seconds
            	time.sleep(10)
