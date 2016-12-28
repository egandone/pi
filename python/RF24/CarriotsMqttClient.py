from json import dumps
import paho.mqtt.publish as publish

class CarriotsMqttClient:
	_host = None
	_port = None
	_auth = None
	_topic = None

	def __init__(self, auth):
		self._host = 'mqtt.carriots.com'
		self._port = 1883
		self._auth = auth
		self._topic = '%s/streams' % auth['username']

	def publish(self, climate_data):
		msg_dict = {'protocol': 'v2', 'device': 'defaultDevice@egandone.egandone', 'at': 'now'}
		msg_dict['data'] = climate_data
		msg = dumps(msg_dict)
		publish.single(topic=self._topic, payload=msg, hostname=self._host, auth=self._auth, port=self._port)
