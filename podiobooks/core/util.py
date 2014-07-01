import os
import urllib
from PIL import Image

from noodles.util import AssetsFromImageHandler

from django.conf import settings


def download_cover(title, upload_path=''):
    raw_cover_url = "http://asset-server.libsyn.com/show/%s/" % title.libsyn_show_id

    if not upload_path:
        upload_path = title.cover.field.upload_to

    destination_dir = os.path.join(settings.MEDIA_ROOT, upload_path)

    if not os.path.isdir(destination_dir):
        os.makedirs(destination_dir)

    image_file = "%s.jpg" % title.libsyn_show_id
    destination = os.path.join(destination_dir, image_file)
    upload_path = "%s/%s" % (upload_path, image_file)

    try:
        if not os.path.isfile(destination):
            filename, httpresponse = urllib.urlretrieve(raw_cover_url)
            img = Image.open(filename)
            if img.mode != "RGB":
                img = img.convert("RGB")
            img.save(destination, "JPEG", quality=100)

        if not title.cover:
            title.cover = upload_path
            title.save()
    except IOError:
        pass

    return title.cover


def get_cover_url_at_width(title, width):
    """
    Returns the URL for a title.cover at a particular width

    Will download the cover lazily if needed.

    returns None if it fails all attempts
    """
    attr = "cover_%s" % width
    try:
        return getattr(title, attr).url
    except AttributeError:
        download_cover(title)
        if title.cover:
            try:
                return getattr(title, attr).url
            except AttributeError:
                return title.cover
    return None


def get_libsyn_cover_url(title, height, width):
    """Pulls the final libsyn URL for a title from libsyn"""
    return "http://asset-server.libsyn.com/show/{0}/height/{1}/width/{2}".format(title.libsyn_show_id, height, width)
