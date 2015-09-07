class Door:
	"""The Door class can check the status of the door.

	Door(IO_door)
	IO_door : IOctrl.gpio class controlling the pin the door sensor is connected to
	"""
	def __init__(self,IO_door):
		self.gpio=IO_door
		self.gpio.set_dir('in')
	
	def is_open(self):
		"Returns True if door is open"
		return self.gpio.get()==1

	def is_closed(self):
		"Returns True if door is closed"
		return self.gpio.get()==0
