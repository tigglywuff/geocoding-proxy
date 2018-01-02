from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

import configparser
import geocode
import urllib.request
import util

class MyHandler(BaseHTTPRequestHandler):

	"""
	Override the do_GET function to accept an address parameter and perform the geocoding proxy service
	"""
	def do_GET(self):

		# Retrieve the query parameters for this request, returned as a dict
		query_params = urllib.parse.parse_qs(urlparse(self.path).query)

		# Require the user to pass in query parameter "address" with string value containing a human readable address
		if 'address' in query_params:
			address = query_params['address'][0]

			# Initialize constructor for calling primary geocoding service then request lat and lng data
			geo = geocode.Geocode()
			data = geo.request(address)

			# If data exists then send it back
			if data:
				return self.respond(200, data)

			else:

				# Try the backup geocoding service
				geo = geocode.BackupGeocode()
				data = geo.request(address)

				# If there's data now send that back, otherwise respond with an error
				if data:
					return self.respond(200, data)

				else:
					return self.respond(400, {"error": "No data returned from geocoding services"})

		# Respond with an error if no query param was specified
		else:
			return self.respond(400, { "error": "No address query parameter specified" })

	"""
	Send a response based on the provided error code and data object
	@param code {int} A valid HTTP error code ex: 200 or 400
	@param data {bytes/dict} An object to respond with
	"""
	def respond(self, code, data):
		# Cast data to byte if needed
		if isinstance(data, dict):
			data = util.dictToByte(data)

		self.send_response(code)
		self.send_header('Content-Type', 'application/json')
		self.end_headers()
		self.wfile.write(data)
		return

# Read server information from config
config = configparser.ConfigParser()
config.read('config.ini')

server = HTTPServer((config['BASE']['host'], int(config['BASE']['port'])), MyHandler)

# Run the server
while True:
	server.handle_request()