#!/usr/bin/python
# Example using a character LCD plate.
import time

import Adafruit_CharLCD as LCD


# Initialize the LCD using the pins 
lcd = LCD.Adafruit_CharLCDPlate()

# Show some basic colors.
lcd.set_color(1.0, 1.0, 1.0)
while True:
   lcd.clear()
   current_time = time.localtime(time.time())
   timefmt = "%a, %b. %d%n        %H:%M:%S"
   lcd.message(time.strftime(timefmt, current_time))
   now = time.localtime(time.time())
   while (now.tm_sec == current_time.tm_sec):
      time.sleep(0.1)
      now = time.localtime(time.time())
