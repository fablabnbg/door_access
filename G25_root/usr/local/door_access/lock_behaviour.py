import threading
import time

class Lock_behaviour:
	"""The Lock_behaviour class defines the exact behaviour of the locking and unlocking of the door

	Lock_behaviour(lock,door,beeper)
	lock : lock_ctrl.Lock_ctrl class
	door : door.Door class
	beeper : callable used for issuing beeps
	"""
	def __init__(self,lock,door,lock_led,beeper):
		self.lock=lock
		self.door=door
		self.lock_led=lock_led
		self.beep=beeper
		self.abort=False
		self.closing=False
		self.open_retry_count=0
		self.open_time=0
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
		# Wait for closing to actually end
		while self.closing:
			time.sleep(0.05)
		t=time.time()
		if self.open_time+30>t:
			# Tried to open door more than once within one half minute
			self.open_retry_count+=1
		else:
			# longer than one minute since trying to open
			self.open_time=t
			self.open_retry_count=1
		if self.lock.is_locked() or self.open_retry_count>=3:
			self.lock.open()
		else:
			self.lock.latch()

	def _close_sequencer(self,timeout):
		print('start close')
		def timed_out(started,duration):
			"""Check if duration seconds have passed since started.
			If duration is zero always return False.
			"""
			return duration and time.time()-started>duration
		# states of the closing sequence
		WAIT_OPEN_DOOR=0
		WAIT_CLOSED_DOOR=1
		WAIT_CERTAIN_CLOSED_DOOR=2
		WAIT_LOCK_TURN_FINISHED=3

		start_time=time.time()
		lastbeep=start_time
		beep_period=2
		self.abort=False
		abortable=True # disables abort when lock is turning

		state=WAIT_OPEN_DOOR
		while not (timed_out(start_time,timeout) or (self.abort and abortable)):
			if state==WAIT_OPEN_DOOR:
				# First wait for the door to be open
				if self.door.is_open():
					state=WAIT_CLOSED_DOOR
			if state==WAIT_CLOSED_DOOR:
				# Wait for door to be closed again
				if self.door.is_closed():
					state=WAIT_CERTAIN_CLOSED_DOOR
					waitstart=time.time() # start timer to make certain the door is closed
			if state==WAIT_CERTAIN_CLOSED_DOOR:
				# wait for the door to be certainly closed
				if self.door.is_open():
					# the door was opened again. Return to waiting for closed door
					state=WAIT_CLOSED_DOOR
				if self.door.is_closed() and timed_out(waitstart,0.5):
					# the door was closed for half a second. Lock door and exit state machine
					self.lock.close()
					abortable=False
					# reset timeout to something large enough to allow the lock to turn
					start_time=time.time()
					timeout=60
					self.lock_led.reset()
					state=WAIT_LOCK_TURN_FINISHED
			if state==WAIT_LOCK_TURN_FINISHED:
				# wait for lock to finish turning
				if self.lock_led.lastwidth>1:
					break
			if timed_out(lastbeep,beep_period):
				# Beep while statemachine is runnning
				self.beep(3)
				lastbeep=time.time()
			time.sleep(0.1)
		time.sleep(1)
		self.abort=False
		self.closing=False
