import dweepy

class Dweeter:

	_thing_name = None
	
	def __init__(self):
		self._thing_name = 'd5299e5a8688832804c2f51ecaf5192e'

	def publish(self, climate_data):
		dweepy.dweet_for(self._thing_name, climate_data)
