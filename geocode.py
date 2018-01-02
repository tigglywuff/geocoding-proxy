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
	Constructor for the primary Geocode service library. Initializes config_section so that this
	Geocode object reads from the correct section in config.ini
	"""
	def __init__(self):
		self.config_section = 'GOOGLE'

	"""
	Accepts an address and returns a query params dict as expected by the primary geocoding service
	@param address {str} a human readable address, ex: "1600 Pennsylvania Ave NW"
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
	Parses an object and returns an object that only has lat and lng
	@param data {bytes} object that contains coordinates as returned by primary geocoding service
	@returns {bytes} object containing lat and lng
	"""
	def parseCoords(self, data):
		data = util.byteToDict(data)
		coords = data['results'][0]['geometry']['location']
		return util.dictToByte(coords)

	"""
	Performs a request to the geocoding service for the given address
	@param address {str} a human readable address, ex: "1600 Pennsylvania Ave NW"
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
An extension of Class Geocode where the constructor and parseCoords() have been overriden to use a
backup geocoding service API.
"""
class BackupGeocode(Geocode):

	"""
	Initialize this Geocode to use HERE's configuration
	"""
	def __init__(self):
		self.config_section = 'HERE'

	"""
	Parse lat and lng from HERE's return object
	@param data {bytes} object that contains coordinates as returned by HERE
	"""
	def parseCoords(self, data):
		data = util.byteToDict(data)
		coords = data['Response']['View'][0]['Result'][0]['Location']['DisplayPosition']

		# Need to rename key names from "Latitude" to "lat" and the same for lng
		coords = {
			"lat": coords['Latitude'],
			"lng": coords['Longitude']
		}
		return util.dictToByte(coords)