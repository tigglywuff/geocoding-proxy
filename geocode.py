from urllib.parse import urlparse

import urllib.request
import json

"""
Class Geocode is used to contact the primary third party geocoding service.
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
	@param address A human readable string containing an address
	"""
	def getQueryParams(self, address):
		return {
			"address": address
		}

	"""
	Given the data returned by the geocoding service, returns an object only including lat and lng.
	@param data bytes object that contains coordinates
	@returns bytes object containing properties lat and lng
	"""
	def parseCoords(self, data):
		data = json.loads(data.decode('utf-8'))
		coords = data['results'][0]['geometry']['location']
		return json.dumps(coords).encode('utf-8')

	"""
	Performs a request to the geocoding service for the given address. Do not override this function.
	@param address A human readable string containing an address
	"""
	def request(self, address):

		# Get the expected query params
		query_string = self.getQueryParams(address)

		# Encode the object
		encoded_qs = urllib.parse.urlencode(query_string)

		# Request the url
		try:
			response = urllib.request.urlopen(self.url + encoded_qs)
			return self.parseCoords(response.read())

		# Returns false if the response is not 200 success
		except urllib.error.HTTPError as e:
			return False

"""
An extension of Class Geocode where the constructor, getQueryParams(), and parseCoords() have been
overwritten to use a backup geocoding service API.
"""
class BackupGeocode(Geocode):

	def __init__(self):
		self.url = 'https://geocoder.cit.api.here.com/6.2/geocode.json?'

	def getQueryParams(self, address):
		# Pass in my particular set of app_id and app_code credentials
		return {
			"app_id": "ARwHKNHdZvDjncf5oqgZ",
			"app_code": "yhe7sdIYlh7hJKNZ8ADf3g",
			"searchtext": address
		}

	def parseCoords(self, data):
		data = json.loads(data.decode('utf-8'))
		coords = data['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']

		# Need to rename key names from "Latitude" to "lat" and the same for lng
		coords = {
			"lat": coords['Latitude'],
			"lng": coords['Longitude']
		}
		return json.dumps(coords).encode('utf-8')