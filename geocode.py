from urllib.parse import urlparse

import configparser
import urllib.request

import util

# Read config.ini for Geocode configurations
config = configparser.ConfigParser()

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
		config.read('config.ini')

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
		data = util.byteToDict(data)
		coords = data['results'][0]['geometry']['location']
		return util.dictToByte(coords)

	"""
	Performs a request to the geocoding service for the given address. Do not override this function.
	@param address A human readable string containing an address
	"""
	def request(self, address):
		config.read('config.ini')
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
			util.log(self.config_section + " did not return 200")
			return False

		# Return false if the returned data is not formatted as expected
		except IndexError:
			util.log("Object returned from " + self.config_section + " not formatted as expected")
			return False

		except Exception as e:
			util.log(e)
			return False

"""
An extension of Class Geocode where the constructor, getQueryParams(), and parseCoords() have been
overwritten to use a backup geocoding service API.
"""
class BackupGeocode(Geocode):

	def __init__(self):
		self.config_section = 'HERE'

	def parseCoords(self, data):
		data = util.byteToDict(data)
		coords = data['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']

		# Need to rename key names from "Latitude" to "lat" and the same for lng
		coords = {
			"lat": coords['Latitude'],
			"lng": coords['Longitude']
		}
		return util.dictToByte(coords)