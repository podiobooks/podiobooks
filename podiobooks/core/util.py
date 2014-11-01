"""General Podiobooks Utilities"""
import urllib
import logging
from xml.etree import ElementTree

import os
import re
from PIL import Image
from django.conf import settings


# pylint: disable=C0325

LOGGER = logging.getLogger(name='podiobooks.util')


def use_placeholder_cover_for_title(title, upload_path=''):
    """If an image isn't loaded, use a placeholder cover"""
    if not upload_path:
        upload_path = title.cover.field.upload_to

    destination_dir = os.path.join(settings.MEDIA_ROOT, upload_path)
    if not os.path.isdir(destination_dir):
        os.makedirs(destination_dir)

    image_file = "%s-placeholder.jpg" % title.slug
    destination = os.path.join(destination_dir, image_file)
    upload_path = "%s/%s" % (upload_path, image_file)

    try:
        if not os.path.isfile(destination):
            img = Image.open(os.path.join(settings.STATIC_ROOT, settings.LOCALIZED_COVER_PLACEHOLDER))
            if img.mode != "RGB":
                img = img.convert("RGB")
            img.save(destination, "JPEG", quality=100)

        if not title.cover:
            title.cover = upload_path
            title.save()
    except IOError:
        pass

    return title.cover


def download_cover_from_libsyn(title):
    """Download cover image from Libsyn"""

    if not title.libsyn_slug:  # If no libsyn slug, exit
        return None

    upload_path = title.cover.field.upload_to

    absolute_upload_dir = os.path.join(settings.MEDIA_ROOT, upload_path)
    if not os.path.isdir(absolute_upload_dir):
        os.makedirs(absolute_upload_dir)

    image_file_name = "{0}.jpg".format(title.slug)
    upload_file_path = os.path.join(absolute_upload_dir, image_file_name)
    cover_image_url = "{0}/{1}".format(upload_path, image_file_name)

    try:
        LOGGER.info("Downloading new cover for {0}...", title.name)

        # Make sure we have a fresh filename so that asset generation is triggered
        append = 0
        while os.path.isfile(upload_file_path):
            append += 1
            image_file_name = "%s_%s.jpg" % (title.slug, append)
            upload_file_path = os.path.join(absolute_upload_dir, image_file_name)
            cover_image_url = "%s/%s" % (upload_path, image_file_name)

        rss_feed_url = "http://{0}.podiobooks.libsynpro.com/rss".format(title.libsyn_slug)
        feed = urllib.urlopen(rss_feed_url)
        feed_tree = ElementTree.parse(feed).getroot()
        title.libsyn_cover_image_url = feed_tree.find('channel').find('image').find('url').text

        filename, httpresponse = urllib.urlretrieve(title.libsyn_cover_image_url)  # pylint: disable=W0612

        img = Image.open(filename)
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(upload_file_path, "JPEG", quality=100)

        LOGGER.info("Saving new cover in model for {0}...", title.name)
        title.cover = cover_image_url
        title.save()

    except Exception as e:
        LOGGER.error("Error Getting Cover for {0}, {1}", title.name, e)
        raise

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
        download_cover_from_libsyn(title)

    if title.cover:
        try:
            return getattr(title, attr).url
        except AttributeError:
            return title.cover.url

    return None