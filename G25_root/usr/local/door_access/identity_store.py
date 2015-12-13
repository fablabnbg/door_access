from datetime import datetime

class Identity_store:
	def __init__(self):
		self._uid=None
		self._last_time=datetime.now()
	
	@property
	def uid(self):
		if (datetime.now()-self._last_time).seconds>90:
			self._uid=None
		return self._uid

	@uid.setter
	def uid(self,new_uid):
		self._uid=new_uid
		self._last_time=datetime.now()
