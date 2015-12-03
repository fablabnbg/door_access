from urllib.request import urlopen, HTTPError
import json

class Message:
	def __init__(self,addr):
		self.addr=addr

	def send(self,msg):
		try:
			data=json.dumps({'message':msg})
			response=urlopen(self.addr,data=data.encode('UTF-8'))
		except HTTPError as e:
			return e
