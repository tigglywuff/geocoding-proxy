import json

def byteToDict(data):
	return json.loads(data.decode('utf-8'))

def dictToByte(data):
	return json.dumps(data).encode('utf-8')

def log(data):
	print('[INFO] ' + str(data))