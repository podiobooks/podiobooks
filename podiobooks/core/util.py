import os
import urllib
from PIL import Image

from noodles.util import AssetsFromImageHandler

from django.conf import settings


def download_cover(title, upload_path=''):
    raw_cover_url = "http://asset-server.libsyn.com/show/%s/" % title.libsyn_show_id

    destination_dir = os.path.join(settings.MEDIA_ROOT, upload_path)

    if not os.path.isdir(destination_dir):
        os.makedirs(destination_dir)

    image_file = "%s.jpg" % title.libsyn_show_id
    destination = os.path.join(destination_dir, image_file)
    upload_path = "%s/%s" % (upload_path, image_file)

    if not os.path.isfile(destination):
        filename, httpresponse = urllib.urlretrieve(raw_cover_url)
        img = Image.open(filename)
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(destination, "JPEG", quality=100)

    if not title.cover:
        title.cover = upload_path
        title.save()

    return title.cover
