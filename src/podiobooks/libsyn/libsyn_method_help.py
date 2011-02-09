"""Dumps out the list of Methods from the LibSyn API"""

import xmlrpclib

def main():
    """MAIN FUNCTION TO RUN IF THIS SCRIPT IS CALLED ALONE"""
    
    SERVER_URL = 'http://api.libsyn.com/xmlrpc'
    SERVER = xmlrpclib.Server(SERVER_URL)
    
    RESULT = SERVER.system.methodHelp('producer.publishing.getItemInfo')
    
    print "Help for producer.publishing.getItemInfo"
    print RESULT
    
if __name__ == "__main__":
    main()  # pragma: no cover