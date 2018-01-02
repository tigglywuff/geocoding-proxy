from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

import json
import urllib.request

class Geocode:

	# Makes a request as appropriate for the provided address. Returns a byte obj
	# param address Should be a plain address string, for example: "1600 Pennsylvania Ave NW"
	def request(self, address):

		# Call a function that should be overridden by the other classes
		query_string = self.getQueryString(address)

		# Encode the object
		encoded_qs = urllib.parse.urlencode(query_string)

		# Request the url
		with urllib.request.urlopen(self.url + encoded_qs) as response:
			resp = response.read()

		return self.parseCoords(resp)

class GeocodeHere(Geocode):
	def __init__(self):
		self.url = 'https://geocoder.cit.api.here.com/6.2/geocode.json?'

	def getQueryString(self, address):
		return {
			"app_id": "ARwHKNHdZvDjncf5oqgZ",
			"app_code": "yhe7sdIYlh7hJKNZ8ADf3g",
			"searchtext": address
		}

	def parseCoords(self, data):
		data = json.loads(data.decode('utf-8'))
		coords = data['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']
		coords = {
			"lat": coords['Latitude'],
			"lng": coords['Longitude']
		}
		return json.dumps(coords).encode('utf-8')

class GeocodeGoogle(Geocode):
	def __init__(self):
		self.url = "http://maps.googleapis.com/maps/api/geocode/json?"

	# Returns a JSON
	def getQueryString(self, address):
		return { "address": address }

	def parseCoords(self, data):
		# data is a bytes object
		# cast bytes to json so we can work with it

		data = json.loads(data.decode('utf-8'))

		# return the data as bytes again
		coords = data['results'][0]['geometry']['location']

		return json.dumps(coords).encode('utf-8')


class MyHandler(BaseHTTPRequestHandler):

	def do_GET(self):

		query_params = urllib.parse.parse_qs(urlparse(self.path).query)

		if 'address' in query_params:
			response_code = 200
			
			# p = GeocodeGoogle();
			p = GeocodeHere()
			
			address = query_params['address'][0]
			data = p.request(address)


		else:
			response_code = 400
			data = json.dumps({ "code": response_code, "message": "No query parameters specified" }).encode('utf-8')


		self.send_response(response_code)
		self.send_header('Content-Type', 'application/json')
		self.end_headers()

		self.wfile.write(data)
		return



server = HTTPServer(('localhost', 8000), MyHandler)

while True:
	server.handle_request()