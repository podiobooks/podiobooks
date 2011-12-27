"""Dumps out the list of System Methods from the LibSyn API"""

import xmlrpclib

def main(): # pragma: no cover
    """MAIN FUNCTION TO RUN IF THIS SCRIPT IS CALLED ALONE"""
    
    SERVER_URL = 'http://api.libsyn.com/xmlrpc'
    SERVER = xmlrpclib.Server(SERVER_URL)
    
    RESULT = SERVER.system.listMethods()
    
    for r in RESULT:
        print r
    
if __name__ == "__main__":
    main()  # pragma: no cover