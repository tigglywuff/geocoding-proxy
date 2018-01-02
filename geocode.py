from urllib.parse import urlparse

import configparser
import urllib.request
import json

# Read config.ini for Geocode configurations
config = configparser.ConfigParser()
config.read('config.ini')

"""
Class Geocode is used to contact the primary third party geocoding service.
"""
class Geocode:

	"""
	Constructor for the primary Geocode service library. Initializes this url to the primary
	geocoding service URL.
	"""
	def __init__(self):
		self.config_section = 'GOOGLE'

	"""
	getQueryParams accepts an address and returns a dict as accepted by our primary geocoding
	service.
	@param address A human readable string containing an address
	"""
	def getQueryParams(self, address):
		# Get the primary address key from the config
		ret = {
			config[self.config_section]['address_key']: address
		}

		# Read any other keys as needed
		for key in config[self.config_section]:
			if not (key == 'url' or key == 'address_key'):
				ret[key] = config[self.config_section][key]

		return ret

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
		self.url = config[self.config_section]['url']

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

		# Return false if the returned data is not formatted as expected
		except IndexError:
			return False

"""
An extension of Class Geocode where the constructor, getQueryParams(), and parseCoords() have been
overwritten to use a backup geocoding service API.
"""
class BackupGeocode(Geocode):

	def __init__(self):
		self.config_section = 'HERE'

	def parseCoords(self, data):
		data = json.loads(data.decode('utf-8'))
		coords = data['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']

		# Need to rename key names from "Latitude" to "lat" and the same for lng
		coords = {
			"lat": coords['Latitude'],
			"lng": coords['Longitude']
		}
		return json.dumps(coords).encode('utf-8')