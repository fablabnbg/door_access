from urllib.request import urlopen, HTTPError
import json

class Decider_http:
	def __init__(self,addr,opener,closer):
		self.addr=addr
		self.opener=opener
		self.closer=closer

	def do(self,cmd,uid):
		if cmd=='open':
			self.opener()
		elif cmd=='close':
			self.closer(lambda:self.log_close(uid))

	def log_close(self,uid):
		try:
			addr=self.addr+'close'
			data=json.dumps({'card':uid,'write_log':True})
			response=urlopen(addr,data=data.encode('UTF-8'))
		except HTTPError:
			return 0


	def execute(self,command,identity):
		uid=identity.decode('ascii').replace(' ','')
		try:
			addr=self.addr+command
			data=json.dumps({'card':uid})
			response=urlopen(addr,data=data.encode('UTF-8'))
		except HTTPError:
			return 0
		result=json.loads(response.readall().decode('ascii'))
		self.do(result,uid)

