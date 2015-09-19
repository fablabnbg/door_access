class Status_manager:
	""" The Status_manager class manages the occupational status of the
	protected room. Decides if the access level is high enough to get access.
	"""
	ACCESS_WITH_OTHERS=5 #lvl for latching the door
	ACCESS_ALONE=10 #lvl for locking and unlocking ´

	# return codes for leave
	NOTHING_SPECIAL=0
	LEAVE_WITHOUT_ENTER=1
	NO_MORE_TRUSTED=2
	EMPTY=3

	def __init__(self):
		self.persons=dict()

	def enter(self, ident, access_level):
		"""Check if a person with a given access_level is allowed to enter.

		enter(ident, access_level):
		ident : string to identify the person wanting access
		access_level : access_level of the person wanting access

		Returns True if entering is allowed, False otherwise.
		"""
		if ident in self.persons:
			return True
		if access_level>=self.ACCESS_ALONE:
			self.persons[ident]=access_level
			return True
		if access_level>=self.ACCESS_WITH_OTHERS:
			if len(self.persons)==0:
				return False
			self.persons[ident]=access_level
			return True
		return False

	def leave(self, ident):
		"""The given person leaves the room.
		
		Returns one of several constants:
		NOTHING_SPECIAL : Person left and there are still trusted people in the room
		LEAVE_WITHOUT_ENTER : someone left without properly entering first
		NO_MORE_TRUSTED : Only untrusted people (access_level below ACCESS_ALONE)
		EMPTY : Room is empty
		"""
		if not ident in self.persons:
			return self.LEAVE_WITHOUT_ENTER
		del self.persons[ident]
		if len(self.persons)==0:
			return self.EMPTY
		max_remaining_access=max(self.persons[k] for k in self.persons)
		if max_remaining_access<self.ACCESS_ALONE:
			return self.NO_MORE_TRUSTED
		return self.NOTHING_SPECIAL

	def is_empty(self):
		"""Returns True if no one is in the room"""
		return len(self.persons)==0

	def flush(self):
		"""Set room to empty"""
		self.persons.clear()
