import threading
import time

class Lock_ctrl:
	def __init__(self,door,IO_open,IO_close,IO_latch):
		self.door=door
		self.opener=IO_open
		self.opener.set_dir('out')
		self.closer=IO_close
		self.closer.set_dir('out')
		self.latcher=IO_latch
		self.latcher.set_dir('out')
		self.mutex=threading.Lock()
		self.opener.set(0)
		self.closer.set(0)
		self.latcher.set(0)
		self.abort=False
		self.state=None
		if door.is_closed():
			self._close()
		else:
			self.close(lambda x:None,0)

	def is_locked(self):
		return self.state=='locked'

	def _open(self):
		print('open')
		self.opener.set(1)
		time.sleep(0.1)
		self.opener.set(0)
		self.state='open'

	def open(self):
		def runthread():
			self._open()
			self.mutex.release()
		self.abort=True
		if self.mutex.acquire(False):
			self.abort=False
			t=threading.Thread(target=runthread)
			t.start()
		
	def _close(self):
		print('lock')
		self.closer.set(1)
		time.sleep(0.1)
		self.closer.set(0)
		self.state='locked'

	def close(self,beeper,timeout=60):
		def runthread():
			def check_timeout():
				return timeout and time.time()-starttime>timeout
			starttime=time.time()
			try:
				while self.door.is_closed():
					if self.abort:
						return
					if check_timeout():
						beeper(50)
						return
					beeper(10)
					time.sleep(0.2)
				time.sleep(0.2)
				close_success=False
				while not close_success:
					while not self.door.is_closed():
						if self.abort:
							return
						if check_timeout():
							beeper(50)
							return
						beeper(10)
						time.sleep(0.2)
					time.sleep(0.5)
					if self.door.is_closed():
						close_success=True
				self._close()
			finally:
				self.abort=False
				self.mutex.release()
		if self.mutex.acquire(False):
			t=threading.Thread(target=runthread)
			t.start()

	def latch(self):
		def runthread():
			print('latch')
			self.latcher.set(1)
			time.sleep(5)
			self.latcher.set(0)
			self.mutex.release()
		self.abort=True
		if self.mutex.acquire(False):
			self.abort=False
			t=threading.Thread(target=runthread)
			t.start()
