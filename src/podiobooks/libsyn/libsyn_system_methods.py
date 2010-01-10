#!/usr/bin/python

import xmlrpclib

server_url = 'http://api.libsyn.com/xmlrpc'
server = xmlrpclib.Server(server_url);

result = server.system.listMethods()

for r in result:
	print r
