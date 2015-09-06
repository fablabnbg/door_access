class Status_manager:
	ACCESS_WITH_OTHERS=5
	ACCESS_ALONE=10

	NOTHING_SPECIAL=0
	LEAVE_WITHOUT_ENTER=1
	NO_MORE_TRUSTED=2
	EMPTY=3

	def __init__(self):
		self.persons=dict()

	def enter(self, ident, access_level):
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
		return len(self.persons)==0
