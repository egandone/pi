#!/usr/bin/env python

from __future__ import print_function
import time
from RF24 import *
import RPi.GPIO as GPIO

irq_gpio_pin = None

# Setup for GPIO 22 CE and CE0 CSN with SPI Speed @ 8Mhz
radio = RF24(RPI_V2_GPIO_P1_15, BCM2835_SPI_CS0, BCM2835_SPI_SPEED_8MHZ)

def try_read_data():
    if radio.available():
        while radio.available():
            len = radio.getDynamicPayloadSize()
            receive_payload = radio.read(len)
            print('Got payload size={} value="{}"'.format(len, receive_payload.decode('utf-8')))

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
    try_read_data()

