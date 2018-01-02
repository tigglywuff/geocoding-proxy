import json

"""
Convert a bytes object to a dict
@param data {bytes}
"""
def byteToDict(data):
	return json.loads(data.decode("utf-8"))

"""
Convert a dict object to bytes
@param data {dict}
"""
def dictToByte(data):
	return json.dumps(data).encode("utf-8")

"""
Abstracted function to log all information
@param data {*} Any information that will be cast to a str and logged
"""
def log(data):
	print("[INFO] " + str(data))