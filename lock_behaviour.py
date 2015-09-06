import threading
import time

class Lock_behaviour:
	def __init__(self,lock,door,beeper):
		self.lock=lock
		self.door=door
		self.beep=beeper
		self.abort=False
		if door.is_closed():
			self.lock.close()
		else:
			threading.Thread(target=self._close_sequencer(0)).start()

	def close(self):
		threading.Thread(target=self._close_sequencer(60)).start()

	def open(self):
		self.abort=True
		if self.lock.is_locked():
			self.lock.open()
		else:
			self.lock.latch()

	def _close_sequencer(self,timeout):
		def timed_out(self,started,duration):
			return duration and time.time()-started>duration
		WAIT_OPEN_DOOR=0
		WAIT_CLOSED_DOOR=1
		WAIT_CERTAIN_CLOSED_DOOR=2

		start_time=time.time()
		lastbeep=start_time
		beep_period=1

		state=WAIT_OPEN_DOOR
		while not timed_out(start_time,timeout) or self.abort=True:
			if state==WAIT_OPEN_DOOR:
				if self.door.is_open():
					state=WAIT_CLOSED_DOOR
			if state==WAIT_CLOSED_DOOR:
				if self.door.is_closed()():
					state=WAIT_CERTAIN_CLOSED_DOOR
					waitstart=time.time()
			if state==WAIT_CERTAIN_CLOSED_DOOR:
				if self.door.is_open():
					state=WAIT_CLOSED_DOOR
				if self.door.is_closed() and timed_out(waitstart,0.5):
					self.lock.close()
					break
			if timed_out(lastbeep,beep_period):
				self.beep(20)
				lastbeep=time.time()
			time.sleep(0.1)
		self.abort=False
