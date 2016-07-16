import time
from pubnub import Pubnub

class MessageChannel:
	command_key = 'command'

	def __init__(self, channel):
		self.channel = channel
		publish_key = 'pub-c-8e8bd077-64a9-4b5a-a5dd-a75a1c1118e2'
		subscribe_key = 'sub-c-81d66b4c-4432-11e6-85a4-0619f8945a4f'
		self.pubnub = Pubnub(publish_key = publish_key, subscribe_key = subscribe_key)
		self.pubnub.subscribe(channels = self.channel, callback = self.callback, error = self.callback, connect = self.connect, reconnect = self.reconnect, disconnect = self.disconnect)

	def callback(self, message, channel):
		print('received: {0}'.format(message))

	def error(self, message):
		print('error: {0}'.formmat(message))

	def connect(self, message):
		print('connect: {0}'.format(message))

	def reconnect(self, message):
		print('reconnect: {0}'.format(message))

	def disconnect(self, message):
		print('disconnect: {0}'.format(message))


if __name__ == '__main__':
	message_channel = MessageChannel('temperature')
	while True:
		time.sleep(10)
