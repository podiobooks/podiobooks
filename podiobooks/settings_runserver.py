import os


def add_path_places():
    """
    Really silly script to add some stuff to the python path
    """
    DDD = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    
    os.sys.path.insert(0, DDD)
    os.sys.path.insert(0, os.path.join(DDD, "eggs"))
    os.sys.path.insert(0, os.path.join(DDD, "eggs-local"))
    os.sys.path.insert(0, os.path.join(DDD, "src"))
    os.sys.path.insert(0, os.path.join(DDD, "src/contrib"))
    os.sys.path.insert(0, os.path.join(DDD, "src/podiobooks"))
    os.sys.path.insert(0, "/Users/brant/Dropbox/repos/django-sodes/sodes/contrib")
    
    for root, dirs, files in os.walk(os.path.join(DDD, "eggs")):
        for dir in dirs:
            if dir.endswith(".egg"):
                os.sys.path.insert(0, os.path.join(DDD, "eggs/%s" % dir))