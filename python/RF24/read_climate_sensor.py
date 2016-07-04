#!/usr/bin/env python

from __future__ import print_function
import time
import sys
from RF24 import *
import RPi.GPIO as GPIO
import dweepy

irq_gpio_pin = None

# Setup for GPIO 22 CE and CE0 CSN with SPI Speed @ 8Mhz
radio = RF24(RPI_V2_GPIO_P1_15, BCM2835_SPI_CS0, BCM2835_SPI_SPEED_8MHZ)
thing_name = 'd5299e5a8688832804c2f51ecaf5192e'

def try_read_data():
    if radio.available():
        len = radio.getDynamicPayloadSize()
        receive_payload = radio.read(len)
        print('Got payload size={} value="{}"'.format(len, receive_payload.decode('utf-8')))
        values = receive_payload.split('|')
        dweet = {'temp1': float(values[0].decode()), 'temp2': float(values[1].decode()), 'pressure': float(values[2].decode()), 'humidity': float(values[3].decode())}
        print(dweet)
        dweepy.dweet_for(thing_name, dweet)
            

pipes = [0xF0F0F0F0E1, 0xF0F0F0F0D2]
#min_payload_size = 4
#max_payload_size = 32

print('Running ...')
radio.begin()
radio.enableDynamicPayloads()
radio.setRetries(5, 15)
radio.printDetails()

print('... awaiting transmission')

radio.openReadingPipe(1, pipes[0])
radio.startListening()

# forever loop
while 1:
    try:
        try_read_data()
    except:
        e = sys.exc_info()[0]
        print(e)
    time.sleep(60)

