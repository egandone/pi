import time
import os
import glob
import ftplib
import sys
import re
import refresh_screens
from datetime import datetime, timedelta

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
    
        time.sleep(60)
