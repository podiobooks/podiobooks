"""Dumps out the list of Methods from the LibSyn API"""

import xmlrpclib

SERVER_URL = 'http://api.libsyn.com/xmlrpc'
SERVER = xmlrpclib.Server(SERVER_URL)

RESULT = SERVER.system.methodHelp('producer.publishing.getItemInfo')

print RESULT
