import threading
import serial
import time

class NFCreader(threading.Thread):
	"""The NFCreader class controls an NFC reader on a serial port.
	To actually start communication the "start"-method has to be called.

	NFCreader(dev, on_card)
	dev : path to serial device
	on_card : callback executed when the reader signals a new card
	"""

	def __init__(self,dev,on_card,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.callback=on_card
		self.s=serial.Serial(dev,9600,timeout=0)
		self.beeptime=0

	def run(self):
		"""Executed on new thread by "start"."""
		while True:
			if self.beeptime:
				if self.beeptime>=100:
					self.beeptime=99
				if self.beeptime<0:
					self.beeptime=0
				beepcmd='B{:02}\n\r'.format(self.beeptime).encode('ascii')
				self.s.write(beepcmd)
				self.beeptime=0
			line=self.s.readline()
			if line:
				self._interpret(line)
			else:
				time.sleep(0.1)

	def beep(self,duration):
		"""Instruct NFCreader emit a beep of given duration,

		beep(duration)
		duration : integer from 0 to 99. Higher means longer
		"""
		self.beeptime=duration

	def _interpret(self,line):
		if line.startswith(b'New'): # Lines signifying a new supported card start with "New something card" and contain the uid after a colon
			try:
				_,ident=line.split(b':',1)
			except ValueError:
				return
			self.callback(ident.strip())
