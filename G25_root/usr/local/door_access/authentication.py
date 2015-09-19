"""The authentication module contains classes for different ways of 
authenticating a NFC uid
"""

class Auth_file:
	"""The Auth_file class authenticates against a local file.

	Auth_file(filename)
	filename : Path to authentication file

	Fileformat
	----------
	One record per line. A record consists of three semi-colon separated fields.
	The first field is the uid in hex bytes separated by spaces.
	The second field is the access level. An integer
	The third field is arbitrary information
	"""

	def __init__(self,filename):
		self.filename=filename
	
	def auth(self,identity):
		"""Get the access level for the given uid. The authentication file is reread with every call.

		auth(identity)
		identity : bytes object with the uid to authenticate. Space separated hex-bytes
		"""
		try:
			with open(self.filename,'rb') as f:
				for l in f:
					try:
						lid,access_level,comment=l.strip().split(b';',2)
						if lid==identity:
							return int(access_level)
					except ValueError:
						pass
		except:
			print('Error in Auth_file')
		return 0
