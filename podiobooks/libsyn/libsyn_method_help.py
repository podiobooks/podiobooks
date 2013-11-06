"""Dumps out the list of Methods from the LibSyn API"""

import xmlrpclib


def main():
    """MAIN FUNCTION TO RUN IF THIS SCRIPT IS CALLED ALONE"""
    
    server_url = 'http://api.libsyn.com/xmlrpc'
    server = xmlrpclib.Server(server_url)
    
    result = server.system.methodHelp('producer.publishing.getItemInfo')
    
    print "Help for producer.publishing.getItemInfo"
    print result
    
if __name__ == "__main__":
    main()  # pragma: no cover
