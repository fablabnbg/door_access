import threading
import serial

class Keypad(threading.Thread):
	def __init__(self,dev,on_key,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.s=serial.Serial(dev,9600)
		self.on_key=on_key
		self.flush()

	def run(self):
		while True:
			c=self.s.read(1).decode('ascii')
			if len(self.buffer)>100:
				self.flush()
			self.buffer+=c
			self.on_key(self.buffer)

	def flush(self):
		self.buffer=""

