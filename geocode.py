import urllib.request
import json

from urllib.parse import urlparse

"""
Class Geocode is used to contact the primary third party geocoding service. In our case it is
Google's geocoding service.
"""
class Geocode:

	"""
	Constructor for the primary Geocode service library. Initializes this url to the primary
	geocoding service URL.
	"""
	def __init__(self):
		self.url = "http://maps.googleapis.com/maps/api/geocode/json?"

	"""
	getQueryParams accepts an address and returns a dict as accepted by our primary geocoding
	service.
	@param address A human readable string containing an address. ex: "1600 Pennsylvania Ave NW"
	"""
	def getQueryParams(self, address):
		return {
			"address": address
		}

	"""
	Given the data returned by the geocoding service, returns an object only including lat and lng.
	@param data (byte) object that contains coordinates
	@returns (byte) object containing properties lat and lng
	"""
	def parseCoords(self, data):
		data = json.loads(data.decode('utf-8'))
		coords = data['results'][0]['geometry']['location']
		return json.dumps(coords).encode('utf-8')

	# Makes a request as appropriate for the provided address. Returns a byte obj
	# param address Should be a plain address string, for example: "1600 Pennsylvania Ave NW"
	def request(self, address):

		# Get the expected query params
		query_string = self.getQueryParams(address)

		# Encode the object
		encoded_qs = urllib.parse.urlencode(query_string)

		# Request the url
		with urllib.request.urlopen(self.url + encoded_qs) as response:
			resp = response.read()

		return self.parseCoords(resp)

class BackupGeocode(Geocode):
	def __init__(self):
		self.url = 'https://geocoder.cit.api.here.com/6.2/geocode.json?'

	def getQueryParams(self, address):
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

