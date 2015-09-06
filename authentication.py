class Auth_file:
	def __init__(self,filename):
		self.filename=filename
	
	def auth(self,identity):
		with open(self.filename,'rb') as f:
			for l in f:
				lid,access_level,comment=l.strip().split(b';',2)
				if lid==identity:
					return int(access_level)
		return 0
