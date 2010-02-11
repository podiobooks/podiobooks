#!/usr/bin/python

import xmlrpclib
import hashlib
import pprint
from podiobooks.settings import LIBSYN_USER, LIBSYN_KEY, LIBSYN_NETWORK_SLUG

def getShowInfo(libsyn_slug):
	""" Returns info about a certain show """
	
	# network slug (network_id can be substituted) is to ensure the authenticated user
	# has proper permission features on the network. show slug (show_id can be substituted)
	# is the show we're looking for
	params = {	'network_slug'	: LIBSYN_NETWORK_SLUG, 		
				'show_slug'		: libsyn_slug	}
	
	# api string is usually a secret - similar to a password
	user = User(LIBSYN_USER, LIBSYN_KEY)
	
	try:
		result = Api().makeApiCall(user, 'producer.publishing.getShowInfo', params)
	except:
		result = ""
	
	return result
	

class Api:
	def makeApiCall(self, user, method, params={}, url='http://api.libsyn.com/xmlrpc'):
		"""Make an XMLRPC call to the main API - Returns mixed
		Expects a User object as the user argument"""

		# server = xmlrpclib.ServerProxy(url, allow_none=1)


		api_params = self._buildParams(user, params)

		# better way to call a string as a method?
		method = "server.%s" % (method)

		try:
			return eval(method)(api_params)
		except xmlrpclib.Fault, f:
			raise Exception('xmlrpcerror', f.faultString)

	def _buildParams(self, user, params={}):
		return {'user'      : user.email ,
				'params'    : params ,
				'hash'      : self._signParams(user, params) }

	def _signParams(self, user, params):
		"""Signs the params with user's api key"""
		str = user.api_key  # start string with api key (kinda a salt)

		keys = params.keys()
		keys.sort()
		for key in keys:
			if(self._isScalar(params[key])):
				temp_str = "%s%s" % (key, params[key])
				str += temp_str

		sha1 = hashlib.sha1(str).hexdigest()
		return sha1

	def _isScalar(self, x):
		return isinstance(x, basestring) or isinstance(x, int)

class User:
	"""Just a simple user class to hold basic information """
	def __init__(self, email, api_key):
		self.email = email
		self.api_key = api_key

##### MAIN FUNCTION TO RUN IF THIS SCRIPT IS CALLED ALONE ###
if __name__ == "__main__":
	result = getShowInfo('theflownsky')
	
	# pretty print the result
	pp = pprint.PrettyPrinter(indent=4)
	pp.pprint(result)
