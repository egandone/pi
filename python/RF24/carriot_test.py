#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Client paho-mqtt CarriotsMqttServer
# main.py
import paho.mqtt.publish as publish
from json import dumps

class CarriotsMqttClient():
    host = 'mqtt.carriots.com'
    port = '1883'
    auth = {}
    topic = '%s/streams'

    def __init__(self, auth):
        self.auth = auth
        self.topic = '%s/streams' % auth['username']

    def publish(self, msg):
        try:
            publish.single(topic=self.topic, payload=msg, hostname=self.host, auth=self.auth, port=self.port)
        except Exception, ex:
            print ex


if __name__ == '__main__':
    auth = {'username': '8d2818491e3c69fbd65138abe3da9c2b39e232de3a38bf261f99549de2178c3d', 'password': ''}
    msg_dict = {'protocol': 'v2', 'device': 'defaultDevice@egandone.egandone', 'at': 'now', 'data': {'temp': 21, 'hum':58}}
    client_mqtt = CarriotsMqttClient(auth=auth)  
    client_mqtt.publish(dumps(msg_dict))
    
