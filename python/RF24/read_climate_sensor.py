#!/usr/bin/env python3

import time
import sys
from RF24 import *
import RPi.GPIO as GPIO
import dweepy

from RadioReceiver import RadioReceiver
from Dweeter import Dweeter
from CarriotsMqttClient import CarriotsMqttClient

#irq_gpio_pin = None

print('Running ...')

receiver = RadioReceiver()

dweeter = Dweeter()

auth = {'username': '8d2818491e3c69fbd65138abe3da9c2b39e232de3a38bf261f99549de2178c3d', 'password': ''}
client_mqtt = CarriotsMqttClient(auth)

print('... awaiting transmission')

receiver.start();

# forever loop
while 1:
	try:
		climate_data = receiver.read_data()
		if climate_data:
			print(climate_data)
			dweeter.publish(climate_data)
			client_mqtt.publish(climate_data)
			time.sleep(60)
		else:
			print("... waiting ...")
			time.sleep(2)
	except Exception as ex:
		print(ex)

