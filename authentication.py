class Auth_file:
	def __init__(self,filename):
		self.filename=filename
	
	def auth(self,identity):
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
