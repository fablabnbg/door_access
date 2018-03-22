import threading
import time

class Lock_behaviour:
	"""The Lock_behaviour class defines the exact behaviour of the locking and unlocking of the door

	Lock_behaviour(lock,door,beeper)
	lock : lock_ctrl.Lock_ctrl class
	door : door.Door class
	lock_led : Edge_detect.edge_detect class. Used to check if lock is turning
	beeper : callable used for issuing beeps
	"""
	def __init__(self,lock,door,lock_led,beeper):
		self.lock=lock
		self.door=door
		self.lock_led=lock_led
		self.beep=beeper
		self.abort=False
		self.opening=False
		self.closing=False
		self.open_retry_count=0
		self.open_time=0
		self.expected_lastwidth=1
		if door.is_closed():
			self.lock.close()
		else:
			threading.Thread(target=lambda timeout=0:self._close_sequencer(timeout)).start()

	def close(self,callback=None):
		"""start door locking sequence. Starts a new thread"""
		if not self.closing:
			self.closing=True
			threading.Thread(target=lambda timeout=60:self._close_sequencer(timeout,callback)).start()

	def open(self,callback=None):
		"""Open the door. Use the latch if it's unlocked.
		Aborts the closing sequence if it's running.
		"""
		self.abort=True
		t=time.time()
		if self.open_time+10>t:
			# Tried to open door more than once within ten seconds
			self.open_retry_count+=1
		else:
			# longer than ten seconds since trying to open
			self.open_time=t
			self.open_retry_count=1
		if self.open_retry_count>=3:
			# Tried to open three times within ten seconds. Open without sequencing
			print("unconditional open")
			self.lock.open()
		if self.lock.is_locked():
			if not self.opening:
				self.opening=True
				threading.Thread(target=lambda:self._open_sequencer(callback)).start()
		else:
			self.lock.latch()

	def _open_sequencer(self,callback):
		print('start open')
		def timed_out(started,duration):
			"""Check if duration seconds have passed since started.
			If duration is zero always return False.
			"""
			return duration and time.time()-started>duration
		# states of the opening sequence
		WAIT_CLOSE_FINISH=0
		DO_OPEN=1
		state=WAIT_CLOSE_FINISH

		while True:
			if state==WAIT_CLOSE_FINISH:
				if not self.closing:
					state=DO_OPEN
					start=time.time()
					self.lock_led.reset()
					self.lock.open()
			if state==DO_OPEN:
				if timed_out(start,1.5) and self.lock_led.edgecount==0:
					state=WAIT_CLOSE_FINISH
				if self.lock_led.edgecount>40 or timed_out(start,10):
					break
			time.sleep(0.1)
		if callback:
			callback()
		time.sleep(1)
		self.opening=False

	def _close_sequencer(self,timeout,callback=None):
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
		self.abort=False
		abortable=True # disables abort when lock is turning

		state=WAIT_OPEN_DOOR
		self.beep.wait_for_user(0)
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
				if self.lock_led.lastwidth>self.expected_lastwidth:
					if callback:
						callback()
					break
				# check if lock actually startet turning
				if timed_out(start_time,1.5):
					if self.lock_led.edgecount>3:
						# lock has turned after 1.5 seconds but last led-light was not detected. edgecount should be about 10. retry
						self.expected_lastwidth-=0.1 # expect smaller last_width
					state=WAIT_CERTAIN_CLOSED_DOOR
						
			time.sleep(0.1)
		time.sleep(1)
		self.abort=False
		self.closing=False
		self.beep.running=False
