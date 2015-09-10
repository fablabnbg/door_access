"""The IOctrl module enables access to the integrated peripherals of 
the Arietta G25.

IOctrl.gpio : read or write gpio pins
IOctrl.adc  : read ADC (not implemented)
"""

import time
import threading
import os

portmap={
	'A':{a:a for a in range(22,32)},
	'C':{a+64:a for a in range(32)},
	}

class gpio:
	"""The gpio class represents one gpio pin.

	gpio(num,direction=None)
	num : number of the controlled pin
	direction : 'in' or 'out'
	"""
	def __init__(self,num,direction=None):
		port='A' if num<64 else 'C'
		self.devname='/sys/class/gpio/pio'+port+str(portmap[port][num])
		if not os.path.exists(self.devname):
			with open('/sys/class/gpio/export','w') as f:
				f.write(str(num))
		if direction:
			self.set_dir(direction)

	def set_dir(self,direction):
		"""Set direction of pin.
		Either 'in' or 'out'
		"""
		if not direction in ('in','out'):
			raise ValueError('direction must be "in" or "out" not "{}"'.format(direction))
		self.direction=direction
		with open(os.path.join(self.devname,'direction'),'w') as f:
			f.write(self.direction)

	def set(self,value,change=False):
		"""Set value on pin to high (1) or low (0).
		set(value,change=False)
		value : either 1 or 0
		change : set to one to automatically change direction to 'out'
		"""
		if not self.direction=='out':
			if change:
				self.direction('out')
			else:
				raise ValueError('Port is set to input and function not asked to change')
		if not value in (0,1):
			raise ValueError('Can only set value to one or zero not "{}"'.format(value))
		with open(os.path.join(self.devname,'value'),'w') as f:
			f.write(str(value))

	def tap(self,duration):
		"""Set value to high for duration and low again afterwards.

		tap(duration)
		duration : time in seconds to keep pin high
		"""
		def runthread():
			self.set(1)
			time.sleep(0.1)
			self.set(0)
		threading.Thread(target=runthread).start()

	def get(self,change=False):
		"""Get current value on pin. Returns 1 or 0.
		get(change=False)
		change : set to True to automatically change direction to 'in'
		"""
		if not self.direction=='in':
			if change:
				self.direction('in')
			else:
				raise ValueError('Port is set to output and function not asked to change')
		with open(os.path.join(self.devname,'value'),'r') as f:
			return int(f.read())

class adc:
	def __init__(self,num):

		pass
