#!/usr/bin/env python3

import time

from RadioReceiver import RadioReceiver
from Dweeter import Dweeter
from CarriotsMqttClient import CarriotsMqttClient

print('Running ...')

# Create a receiver to get the data from the arduino
receiver = RadioReceiver()

# To send data to dweet.io
dweeter = Dweeter()

# To send data to carriots.com
auth = {'username': '8d2818491e3c69fbd65138abe3da9c2b39e232de3a38bf261f99549de2178c3d', 'password': ''}
client_mqtt = CarriotsMqttClient(auth)

# All initialized
print('... awaiting transmission')

# Start up the radio receiver
receiver.start();

# Loop forever reading data from the radio and then publishing it
#    There is a 60 seconds wait between each iteration 
#    assuming the radio is returning data.  This keeps us from
#    flooding the IoT services and exceeding my "free" account
#    limit(s)
#
#    If no data it received from then it waits only 2 seconds and 
#    tries again.  This speeds up startup since it takes a second
#    or two for the radio receiver to initialize
#
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

