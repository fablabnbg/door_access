from urllib.request import urlopen, HTTPError
import json

class Decider_http:
	def __init__(self,addr,opener,closer):
		self.addr=addr
		self.opener=opener
		self.closer=closer

	def do(self,cmd):
		if cmd=='open':
			self.opener()
		elif cmd=='close':
			self.closer()

	def execute(self,command,identity):
		uid=identity.decode('ascii').replace(' ','')
		try:
			addr=self.addr+command
			data=json.dumps({'card':uid})
			response=urlopen(addr,data=data.encode('UTF-8'))
		except HTTPError:
			return 0
		result=json.loads(response.readall().decode('ascii'))
		self.do(result)

