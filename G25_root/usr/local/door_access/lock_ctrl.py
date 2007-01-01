import threading
import time

class Lock_ctrl:
	"""The Lock_ctrl class manages the door lock.

	Lock_ctrl(IO_open,IO_close,IO_latch)
	IO_open : IOctrl.gpio class controlling the pin to open (not merely unlock) the lock
	IO_close : IOctrl.gpio class controlling the pin to lock the lock
	IO_latch : IOctrl.gpio class controlling the doors latch
	"""
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
		"""Returns True if the door is locked."""
		return self.state=='locked'

	def close(self):
		"""Lock the door."""
		print('lock')
		self.state='locked'
		self.closer.tap(0.1)


	def open(self):
		"""unlock and open the door."""
		print('open')
		self.state='open'
		self.opener.tap(0.1)

	def latch(self):
		"""open the latch."""
		print('latch')
		self.latcher.tap(3)
