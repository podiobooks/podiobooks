"""
Core Utility Functions
"""


def get_libsyn_cover_url(title, height, width):
    """Pulls the final libsyn URL for a title from libsyn"""
    scale_url = "http://asset-server.libsyn.com/show/{0}/height/{1}/width/{2}".format(title.libsyn_show_id, height,
        width)
    # Removed Lookup logic with caching and such - was not improving overall site performance.
    return scale_url