"""General Utilities for working with the LibSyn API"""

import xmlrpclib
import hashlib
from django.conf import settings

def get_show_info(libsyn_slug):
    """ Returns info from LibSyn about a certain show """
    
    # network slug (network_id can be substituted) is to ensure the authenticated user
    # has proper permission features on the network. show slug (show_id can be substituted)
    # is the show we're looking for
    params = {  'network_slug'    : settings.LIBSYN_NETWORK_SLUG,         
                'show_slug'       : libsyn_slug    }
    
    # api string is usually a secret - similar to a password
    user = User(settings.LIBSYN_USER, settings.LIBSYN_KEY)
    
    try:
        show_info = make_api_call(user, 'producer.publishing.getShowInfo', params)
    except xmlrpclib.Error:  # pragma: no cover
        show_info = ""
        print "LIBSYN API CALL ERROR!"
    
    return show_info
    

def make_api_call(user, method, params):
    """Make an XMLRPC call to the main API - Returns mixed
    Expects a User object as the user argument"""

    api_params = _build_params(user, params)
    
    server = xmlrpclib.Server(settings.LIBSYN_API_SERVER_URL, verbose=True) #@UnusedVariable # pylint: disable=W0612

    # better way to call a string as a method?
    method = "server.%s" % (method)
    print method

    try:
        return eval(method)(api_params)
    except xmlrpclib.Fault, f:   # pragma: no cover
        print server
        raise f

def _build_params(user, params):
    """Builds up the parameter dict for the API call"""
    return {'user'      : user.email ,
            'params'    : params ,
            'hash'      : _sign_params(user, params) }

def _sign_params(user, params):
    """Signs the params with user's api key"""
    hash_str = user.api_key  # start string with api key (kinda a salt)

    keys = params.keys()
    keys.sort()
    for key in keys:
        if(_is_scalar(params[key])):  # pragma: no cover
            temp_str = "%s%s" % (key, params[key])
            hash_str += temp_str

    sha1 = hashlib.sha1(hash_str).hexdigest() #@UndefinedVariable # pylint: disable=F0401
    return sha1

def _is_scalar(x):
    """Determines if a particular var is a scalar value"""
    return isinstance(x, basestring) or isinstance(x, int)

class User:
    """Just a simple user class to hold basic information """
    def __init__(self, email, api_key):
        self.email = email
        self.api_key = api_key