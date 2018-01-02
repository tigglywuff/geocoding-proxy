from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

import configparser
import json
import geocode
import urllib.request

config = configparser.ConfigParser()
config.read('config.ini')

class MyHandler(BaseHTTPRequestHandler):

	"""
	Override the do_GET function to accept an address parameter and perform the geocoding proxy service
	"""
	def do_GET(self):

		# Retrieve the query parameters for this request, returned as a dict
		query_params = urllib.parse.parse_qs(urlparse(self.path).query)

		# Require the user to pass in query parameter "address" with string value containing a human
		# readable address
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
					return self.respond(400, json.dumps({"error": "No data returned from geocoding services"}).encode('utf-8'))

		# Respond with an error if no query param was specified
		else:
			return self.respond(400, json.dumps({ "error": "No address query parameter specified" }).encode('utf-8'))

	"""
	Sends a response based on the provided error code and data object
	"""
	def respond(self, code, data):
		self.send_response(code)
		self.send_header('Content-Type', 'application/json')
		self.end_headers()
		self.wfile.write(data)
		return

# Read server information from config
host = (config['BASE']['host'])
port = int(config['BASE']['port'])

server = HTTPServer((host, port), MyHandler)

# Run the server
while True:
	server.handle_request()