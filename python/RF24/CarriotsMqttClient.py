from json import dumps
import paho.mqtt.publish as publish

class CarriotsMqttClient:
	host = 'mqtt.carriots.com'
	port = 1883
	auth = {}
	topic = '%s/streams'

	def __init__(self, auth):
		self.auth = auth
		self.topic = '%s/streams' % auth['username']

	def publish(self, climate_data):
		try:
			msg_dict = {'protocol': 'v2', 'device': 'defaultDevice@egandone.egandone', 'at': 'now'}
			msg_dict['data'] = climate_data
			msg = dumps(msg_dict)
			publish.single(topic=self.topic, payload=msg, hostname=self.host, auth=self.auth, port=self.port)
		except Exception as ex:
			print(ex)
