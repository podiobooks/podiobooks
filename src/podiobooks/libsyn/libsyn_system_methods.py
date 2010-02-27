"""Dumps out the list of System Methods from the LibSyn API"""

import xmlrpclib

SERVER_URL = 'http://api.libsyn.com/xmlrpc'
SERVER = xmlrpclib.Server(SERVER_URL)

RESULT = SERVER.system.listMethods()

for r in RESULT:
    print r
