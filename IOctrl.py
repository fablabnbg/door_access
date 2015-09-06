import os

portmap={
	'A':{a:a for a in range(22,32)},
	'C':{64:0,65:1,66:2,67:3,68:4,95:31},
	}

class gpio:
	def __init__(self,num,direction):
		port='A' if num<64 else 'C'
		self.devname='/sys/class/gpio/pio'+port+str(portmap[port][num])
		if not os.path.exists(self.devname):
			with open('/sys/class/gpio/export','w') as f:
				f.write(str(num))
		self.set_dir(direction)

	def set_dir(self,direction):
		if not direction in ('in','out'):
			raise ValueError('direction must be "in" or "out" not "{}"'.format(direction))
		self.direction=direction
		with open(os.path.join(self.devname,'direction'),'w') as f:
			f.write(self.direction)

	def set(self,value,change=False):
		if not self.direction=='out':
			if change:
				self.direction('out')
			else:
				raise ValueError('Port is set to input and function not asked to change')
		if not value in (0,1):
			raise ValueError('Can only set value to one or zero not "{}"'.format(value))
		with open(os.path.join(self.devname,'value'),'w') as f:
			f.write(str(value))

	def get(self,change=False):
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
