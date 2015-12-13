import threading
import time
from datetime import datetime

class Beeper:
	def __init__(self, beep):
		self.beep=beep
		self.running=True

	def confirm(self):
		self.beep(1)

	def wait_for_user(self,duration):
		def worker():
			if self.running:
				return
			self.running=True
			start=datetime.now()
			while self.running:
				self.beep(3)
				time.sleep(2)
				if duration and (datetime.now()-start).seconds>duration:
					self.running=False

		threading.Thread(target=worker).start()

	def ack(self):
		self.beep(20)

	def nak(self):
		print('nak')
		self.beep(2)
		time.sleep(0.2)
		self.beep(2)
		time.sleep(0.2)
		self.beep(10)


# earlier try, maybe use these times
#import time
#
#class Beeper:
#	def __init__(self,beep_cmd):
#		self.beep=beep_cmd
#
#	def ack(self):
#		self.beep(4)
#
#	def nak(self):
#		self.beep(1)
#		time.sleep(0.15)
#		self.beep(1)
#
#	def feedback(self):
#		self.beep(0)
#
#	def notice(self):
#		self.beep(1)
#		self.sleep(2)
#
#	def notice(self):
#		self.beep(1)
#		self.sleep(0.5)
#
#	def error(self):
#		self.nak()
#		time.sleep(0.2)
#		self.beep(7)
