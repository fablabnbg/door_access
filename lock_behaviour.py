import threading
import time

class Lock_behaviour:
	"""The Lock_behaviour class defines the exact beahviour of the locking and unlocking of the door

	Lock_behaviour(lock,door,beeper)
	lock : lock_ctrl.Lock_ctrl class
	door : door.Door class
	beeper : callable used for issuing beeps
	"""
	def __init__(self,lock,door,beeper):
		self.lock=lock
		self.door=door
		self.beep=beeper
		self.abort=False
		self.closing=False
		if door.is_closed():
			self.lock.close()
		else:
			threading.Thread(target=lambda timeout=0:self._close_sequencer(timeout)).start()

	def close(self):
		"""start door locking sequence. Starts a new thread"""
		if not self.closing:
			self.closing=True
			threading.Thread(target=lambda timeout=60:self._close_sequencer(timeout)).start()

	def open(self):
		"""Open the door. Use the latch if it's unlocked.
		Aborts the closing sequence if it's running.
		"""
		self.abort=True
		if self.lock.is_locked():
			self.lock.open()
		else:
			self.lock.latch()

	def _close_sequencer(self,timeout):
		print('start close')
		def timed_out(started,duration):
			return duration and time.time()-started>duration
		WAIT_OPEN_DOOR=0
		WAIT_CLOSED_DOOR=1
		WAIT_CERTAIN_CLOSED_DOOR=2

		start_time=time.time()
		lastbeep=start_time
		beep_period=2
		self.abort=False

		state=WAIT_OPEN_DOOR
		while not (timed_out(start_time,timeout) or self.abort):
			if state==WAIT_OPEN_DOOR:
				if self.door.is_open():
					state=WAIT_CLOSED_DOOR
			if state==WAIT_CLOSED_DOOR:
				if self.door.is_closed():
					state=WAIT_CERTAIN_CLOSED_DOOR
					waitstart=time.time()
			if state==WAIT_CERTAIN_CLOSED_DOOR:
				if self.door.is_open():
					state=WAIT_CLOSED_DOOR
				if self.door.is_closed() and timed_out(waitstart,0.5):
					self.lock.close()
					break
			if timed_out(lastbeep,beep_period):
				self.beep(3)
				lastbeep=time.time()
			time.sleep(0.1)
		self.abort=False
		self.closing=False
