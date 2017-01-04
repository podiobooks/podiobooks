"""General Podiobooks Utilities"""
import requests
import logging
import os
from future.backports.html.parser import HTMLParser

from xml.etree import ElementTree
from PIL import Image

from django.conf import settings

# pylint: disable=C0325
from six import BytesIO

LOGGER = logging.getLogger(name='podiobooks.util')


def download_cover_from_libsyn(title):
    """Download cover image from Libsyn"""

    # If no libsyn slug or cover, return "None"
    # Later in the chain, this will result in a placeholder image
    if not title.libsyn_slug and (title.cover is None or title.cover == ""):
        return None
    elif not title.libsyn_slug and (title.cover is not None and title.cover != ""):
        return title.cover

    upload_path = title.cover.field.upload_to

    absolute_upload_dir = os.path.join(settings.MEDIA_ROOT, upload_path)
    if not os.path.isdir(absolute_upload_dir):
        os.makedirs(absolute_upload_dir)

    image_file_name = "{0}.jpg".format(title.slug)
    upload_file_path = os.path.join(absolute_upload_dir, image_file_name)
    cover_image_url = "{0}/{1}".format(upload_path, image_file_name)

    try:
        LOGGER.info("Downloading new cover for %s...", title.name)

        rss_feed_url = "http://{0}.podiobooks.libsynpro.com/rss".format(title.libsyn_slug)
        feed = requests.get(rss_feed_url)
        feed_tree = ElementTree.fromstring(feed.content)
        title.libsyn_cover_image_url = feed_tree.find('channel').find('image').find('url').text

        response = requests.get(title.libsyn_cover_image_url)  # pylint: disable=W0612

        img = Image.open(BytesIO(response.content))
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(upload_file_path, "JPEG", quality=100)

        # try:
        #     os.remove(filename)
        # except OSError:
        #     pass

        LOGGER.info("Saving new cover in model for %s...", title.name)
        title.cover = cover_image_url
        title.save(always_create_assets=True)

    except Exception as e:
        LOGGER.error("Error Getting Cover for %s, %s", title.name, e)
        raise

    return title.cover


def get_cover_url_at_width(title, width):
    """
    Returns the URL for a title.cover at a particular width

    Will download the cover lazily if needed.

    returns None if it fails all attempts
    """
    try:
        if settings.USE_COVER_PLACEHOLDERS_ONLY:
            return settings.LOCALIZED_COVER_PLACEHOLDER
    except AttributeError:
        pass

    attr = "cover_%s" % width
    try:
        cover_url = getattr(title, attr).url
        if settings.MEDIA_URL in cover_url:
            return cover_url
        else:
            return settings.MEDIA_URL + cover_url
    except AttributeError:
        download_cover_from_libsyn(title)

    if title.cover:
        try:
            return getattr(title, attr).url
        except AttributeError:
            return title.cover.url

    return settings.LOCALIZED_COVER_PLACEHOLDER


class MLStripper(HTMLParser):
    """Hard-Core HTML Tag Stripper Class"""

    def __init__(self):
        """Initialize"""
        self.reset()
        self.fed = []
        self.strict = False
        object.__init__(self)

    def handle_data(self, d):
        """Append the stripped data"""
        self.fed.append(d)

    def get_data(self):
        """Get the stripped data"""
        return ''.join(self.fed)


def strip_tags(html):
    """Strip all HTML Tags and Entities"""
    stripper = MLStripper()

    if not html:
        html = ''

    stripper.feed(html)
    return stripper.get_data()
