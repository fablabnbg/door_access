import threading
import time

class Lock_ctrl:
	def __init__(self,IO_open,IO_close,IO_latch):
		self.opener=IO_open
		self.opener.set_dir('out')
		self.closer=IO_close
		self.closer.set_dir('out')
		self.latcher=IO_latch
		self.latcher.set_dir('out')
		self.opener.set(0)
		self.closer.set(0)
		self.latcher.set(0)
		self.state=None

	def is_locked(self):
		return self.state=='locked'

	def close(self):
		def runthread():
			print('lock')
			self.closer.set(1)
			time.sleep(0.1)
			self.closer.set(0)
			self.state='locked'
		threading.Thread(target=runthread).start()


	def open(self):
		def runthread():
			print('open')
			self.opener.set(1)
			time.sleep(0.1)
			self.opener.set(0)
			self.state='open'
		threading.Thread(target=runthread).start()

	def latch(self):
		def runthread():
			print('latch')
			self.latcher.set(1)
			time.sleep(5)
			self.latcher.set(0)
		threading.Thread(target=runthread).start()
