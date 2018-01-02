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
			
			address = query_params['address'][0]

			p = geocode.Geocode();
			data = p.request(address)

			if data:
				return self.respond(200, data)
			else:
				# fall to backup
				q = geocode.BackupGeocode()
				data = q.request(address)
				if data:
					return self.respond(200, data)
				else:
					return self.respond(400, json.dumps({"error": "all geocode services failed"}).encode('utf-8'))

		else:
			return self.respond(400, json.dumps({ "error": "No address query parameter specified." }).encode('utf-8'))

	def respond(self, code, data):
		self.send_response(code)
		self.send_header('Content-Type', 'application/json')
		self.end_headers()
		self.wfile.write(data)
		return


server = HTTPServer(('localhost', 8000), MyHandler)

while True:
	server.handle_request()