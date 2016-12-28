#!/usr/bin/env python3

#from __future__ import print_function
import time
import sys
from RF24 import *
import RPi.GPIO as GPIO
import dweepy
import paho.mqtt.publish as publish
from json import dumps

irq_gpio_pin = None

# Setup for GPIO 22 CE and CE0 CSN with SPI Speed @ 8Mhz
radio = RF24(RPI_V2_GPIO_P1_15, BCM2835_SPI_CS0, BCM2835_SPI_SPEED_8MHZ)
thing_name = 'd5299e5a8688832804c2f51ecaf5192e'

class CarriotsMqttClient:
	host = 'mqtt.carriots.com'
	port = 1883
	auth = {}
	topic = '%s/streams'

	def __init__(self, auth):
		self.auth = auth
		self.topic = '%s/streams' % auth['username']

	def publish(self, msg):
		try:
			publish.single(topic=self.topic, payload=msg, hostname=self.host, auth=self.auth, port=self.port)
		except Exception as ex:
			print(ex)

def try_read_data(carriots_client):
	if radio.available():
		len = radio.getDynamicPayloadSize()
		receive_payload = radio.read(len)
		receive_payload = receive_payload.decode('utf-8')
		print('Got payload size={} value="{}"'.format(len, receive_payload))
		values = receive_payload.split('|')
		dweet = {'temp1': float(values[0]), 'temp2': float(values[1]), 'pressure': float(values[2]), 'humidity': float(values[3])}
		print(dweet)
		dweepy.dweet_for(thing_name, dweet)
		msg_dict = {'protocol': 'v2', 'device': 'defaultDevice@egandone.egandone', 'at': 'now'}
		msg_dict['data'] = dweet
		carriots_client.publish(dumps(msg_dict))

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

auth = {'username': '8d2818491e3c69fbd65138abe3da9c2b39e232de3a38bf261f99549de2178c3d', 'password': ''}
client_mqtt = CarriotsMqttClient(auth)

# forever loop
while 1:
	try:
		try_read_data(client_mqtt)
	except:
		e = sys.exc_info()[0]
		print(e)
	time.sleep(60)

