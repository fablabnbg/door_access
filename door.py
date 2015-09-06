class Door:
	def __init__(self,IO_door):
		self.gpio=IO_door
		self.gpio.set_dir('in')
	
	def is_open(self):
		return self.gpio.get()==1

	def is_closed(self):
		return self.gpio.get()==0
