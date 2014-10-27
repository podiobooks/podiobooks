"""General Podiobooks Utilities"""
import os
import re
import urllib
from PIL import Image

from django.conf import settings
from xml.etree import ElementTree

# pylint: disable=C0325

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


def download_cover_from_libsyn(title, upload_path=''):
    """Download cover image from Libsyn"""
    if not upload_path:
        upload_path = title.cover.field.upload_to

    destination_dir = os.path.join(settings.MEDIA_ROOT, upload_path)
    if not os.path.isdir(destination_dir):
        os.makedirs(destination_dir)

    image_file = "%s.jpg" % title.slug
    destination = os.path.join(destination_dir, image_file)
    upload_path = "%s/%s" % (upload_path, image_file)

    try:
        if not os.path.isfile(destination) or not title.cover or title.cover != upload_path:
            print "Downloading new cover for %s..." % title.name

            # Make sure we have a fresh filename so that asset generation is triggered
            append = 0
            while os.path.isfile(destination):
                append += 1
                image_file = "%s_%s.jpg" % (title.slug, append)
                destination = os.path.join(destination_dir, image_file)
                upload_path = "%s/%s" % (upload_path, image_file)

            if title.libsyn_cover_image_url:
                raw_cover_url = title.libsyn_cover_image_url
            else:
                raw_cover_url = "http://asset-server.libsyn.com/show/%s/" % title.libsyn_show_id

            filename, httpresponse = urllib.urlretrieve(raw_cover_url)  # pylint: disable=W0612

            img = Image.open(filename)
            if img.mode != "RGB":
                img = img.convert("RGB")
            img.save(destination, "JPEG", quality=100)

        if not title.cover or title.cover != upload_path:
            print "Saving new cover in model for %s..." % title.name
            title.cover = upload_path
            title.save()

    except IOError:
        pass

    return title.cover


def download_cover(title, upload_path=''):
    """Wrapper based on whether showID is filled out"""
    if title.libsyn_show_id or title.libsyn_slug:
        return download_cover_from_libsyn(title, upload_path)
    else:
        return use_placeholder_cover_for_title(title, upload_path)


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


def update_libsyn_slug(title):
    """Update the libsyn slug field on the title based on the first episode MP3 path"""
    first_episode = title.episodes.all()[0]
    try:
        title.libsyn_slug = re.search('com/(.*)/', first_episode.url).group(1)
        title.save()
    except:
        print ("{0} not updated.".format(title.slug))


def update_episode_media_url(episode):
    """Update the media url for an episode to use the podiobooks alias"""
    episode.url = episode.url.replace('http://traffic.libsyn.com', 'http://media.podiobooks.com')
    episode.save()


def update_libsyn_cover_image_url(title):
    """Get the libsyn RSS file, pull the image url, and update the title"""
    if title.libsyn_slug:
        try:
            rss_feed_url = "http://{0}.podiobooks.libsynpro.com/rss".format(title.libsyn_slug)
            print rss_feed_url
            feed = urllib.urlopen(rss_feed_url)
            feed_tree = ElementTree.parse(feed).getroot()
            title.libsyn_cover_image_url = feed_tree.find('channel').find('image').find('url').text
            title.save()
        except:
            print ("Not Updating {0}, Error".format(title.slug))
            raise
    else:
        print ("Not Updating {0}, No Libsyn Slug")
