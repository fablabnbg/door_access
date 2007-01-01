import threading
import time

class Edge_detect(threading.Thread):
	"""Class to do software edge detection on a gpio pin.

	Edge_detect(pin)
	pin : gpio instance

	properties:
	edgecount : number of rising edges since last reset
	lastwidth : duration of the last 'high' pulse
	abort : stop counting thread

	methods:
	start : start counting thread
	reset : reset counter
	"""
	def __init__(self,pin,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.pin=pin
		self.pin.set_dir('in')
		self.pin.set_interrupt('both')
		self.abort=False
		self.mutex=threading.Lock()
		self.reset()

	def reset(self):
		"""reset counters"""
		with self.mutex:
			self.edgecount=0
			self.lastwidth=0
			self.lasttime=0

	def run(self):
		while not self.abort:
			self.pin.wait()
			with self.mutex:
				if self.pin.get()==1:
					# edge was rising
					self.lasttime=time.time()
					self.edgecount+=1
				else:
					# edge was falling
					self.lastwidth=time.time()-self.lasttime
