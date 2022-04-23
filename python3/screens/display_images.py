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
        image_x, image_y = image.get_size()
        origin_x, origin_y = 0,0
        if image_x < self.size[0]:
            origin_x = int((self.size[0] - image_x)/2)
        if image_y < self.size[1]:
            origin_y = int((self.size[1] - image_y)/2)
        self.screen.fill((0,0,0))
        self.screen.blit(image, (origin_x, origin_y))
        pygame.display.flip()
        
    def scale_image(self, image):
        image = pygame.image.load(image)
        image_x, image_y = image.get_size()
        if image_y > image_x:
            size_y = self.size[1]
            size_x = (size_y / image_y) * image_x
            if size_x > self.size[0]:
                size_x = self.size[0]
                size_y = (size_x / image_x) * image_y
        else:
            size_x = self.size[0]
            size_y = (size_x / image_x) * image_y
            if size_y > self.size[1]:
                size_y = self.size[1]
                size_x = (size_y / image_y) * image_x
        size_x, size_y = int(size_x), int(size_y)
        return pygame.transform.scale(image, (size_x, size_y))

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
    rounded_minutes = int((n.minute / 20) * 20)
    last_checked = datetime(n.year, n.month, n.day, n.hour, rounded_minutes, 0, 0)
    print('Started @ ' + last_checked.strftime('%Y-%m-%d %H:%M:%S'))

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
            print('Refreshing images @ ' + current_time.strftime('%Y-%m-%d %H:%M:%S'))
            refresh_screens.check_files(path, current_time.strftime('%Y-%m-%d'))
            # last_checked rounds to the minute to keep the timing of 
            # the refreshed deterministic
            rounded_minutes = int((current_time.minute / 20) * 20)
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
                time.sleep(5)
