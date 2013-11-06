"""Dumps out the list of System Methods from the LibSyn API"""

import xmlrpclib


def main():  # pragma: no cover
    """MAIN FUNCTION TO RUN IF THIS SCRIPT IS CALLED ALONE"""

    server_url = 'http://api.libsyn.com/xmlrpc'
    server = xmlrpclib.Server(server_url)

    result = server.system.listMethods()

    for r in result:
        print r


if __name__ == "__main__":
    main()  # pragma: no cover
