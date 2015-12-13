from urllib.request import urlopen, HTTPError
import json

class Decider_http:
	def __init__(self,addr,opener,closer,ack=None,nak=None):
		self.addr=addr
		self.opener=opener
		self.closer=closer
		self.ack=ack
		self.nak=nak

	def do(self,cmd,uid):
		if cmd=='open':
			if self.ack:
				self.ack()
			return self.opener()
		elif cmd=='close':
			return self.closer(lambda:self.log_close(uid))
		elif cmd=='require_pin':
			if self.nak:
				self.nak()
			return 'pin'
		if self.nak:
			self.nak()


	def log_close(self,uid):
		try:
			addr=self.addr+'close'
			data=json.dumps({'card':uid,'write_log':True})
			response=urlopen(addr,data=data.encode('UTF-8'))
		except HTTPError:
			return 0


	def execute(self,command,identity,pin=None):
		uid=identity.decode('ascii').replace(' ','')
		try:
			addr=self.addr+command
			data=json.dumps({'card':uid,'pin':pin})
			response=urlopen(addr,data=data.encode('UTF-8'))
		except HTTPError:
			return 0
		result=json.loads(response.readall().decode('ascii'))
		return self.do(result,uid)

