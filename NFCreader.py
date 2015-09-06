import threading
import serial
import time

class NFCreader(threading.Thread):
	def __init__(self,dev,on_card,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.callback=on_card
		self.s=serial.Serial(dev,9600,timeout=0)
		self.beeptime=0

	def run(self):
		while True:
			if self.beeptime:
				if self.beeptime>100:
					self.beeptime=99
				if self.beeptime<0:
					self.beeptime=0
				self.s.write('b{:02}\n'.format(self.beeptime).encode('ascii'))
				self.beeptime=0
			line=self.s.readline()
			if line:
				self.interpret(line)
			time.sleep(0.1)

	def beep(self,duration):
		self.beeptime=duration

	def interpret(self,line):
		if line.startswith(b'New'):
			try:
				_,ident=line.split(b':',1)
			except ValueError:
				return
			self.callback(ident.strip())



