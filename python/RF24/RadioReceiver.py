#!/usr/bin/env python3

from RF24 import *
import RPi.GPIO as GPIO

class RadioReceiver:
	_radio = None
	_pipes = None

	def __init__(self):
		# Setup for GPIO 22 CE and CE0 CSN with SPI Speed @ 8Mhz
		self._radio = RF24(RPI_V2_GPIO_P1_15, BCM2835_SPI_CS0, BCM2835_SPI_SPEED_8MHZ)
		self._pipes = [0xF0F0F0F0E1, 0xF0F0F0F0D2]

	def start(self):
		self._radio.begin()
		self._radio.enableDynamicPayloads()
		self._radio.setRetries(5, 15)
		self._radio.openReadingPipe(1, self._pipes[0])
		self._radio.startListening()

	def read_data(self):
		climate_data = None
		if self._radio.available():
			len = self._radio.getDynamicPayloadSize()
			receive_payload = self._radio.read(len)
			receive_payload = receive_payload.decode('utf-8')
			print('Got payload size={} value="{}"'.format(len, receive_payload))
			values = receive_payload.split('|')
			climate_data = {'temp1': float(values[0]), 'temp2': float(values[1]), 'pressure': float(values[2]), 'humidity': float(values[3])}
		return climate_data
