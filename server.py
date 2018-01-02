from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

import json
import urllib.request

import geocode

class MyHandler(BaseHTTPRequestHandler):

	def do_GET(self):

		query_params = urllib.parse.parse_qs(urlparse(self.path).query)

		if 'address' in query_params:
			response_code = 200
			
			# p = geocode.Geocode();
			p = geocode.BackupGeocode()
			
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