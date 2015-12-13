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

