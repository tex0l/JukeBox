from __future__ import unicode_literals
from mutagen.easyid3 import EasyID3
from mutagen.easymp4 import EasyMP4
import logging

def tag_finder(file_path):
    logging.debug("tag_finder started on %s" % file_path)

    result = {}
    if not file_path.startswith(u'.'):
        result = id3_finder(file_path)
        logging.debug("Tags found : %s" % result)
        try:
            result['artist'] = result[u'artist'][0]
            logging.info("Artist found: %s" % result['artist'])
        except KeyError:
            result['artist'] = "unknown"
            logging.warning("No artist tag found, setting to unknown")

        try:
            result['title'] = result[u'title'][0]
            logging.info("Title found: %s" % result['title'])
        except KeyError:
            result['title'] = u"unknown"
            logging.warning("No title tag found, setting to unknown")
        try:
            result['extension'] = file_path.split(u".")
            result['extension'] = result['extension'].pop(len(result['extension'])-1)
            logging.info("Extension found: %s" % result['extension'])
        except:
            logging.warning("No extension found")
    else:
        logging.info("System file, ignored.")
    return result

def id3_finder(file_path):
    tags = {}
    try:
        tags = EasyID3(file_path)
        logging.info("ID3 tags found")
        return tags
    except:
        logging.info("no ID3 tags found")
    try:
        tags = EasyMP4(file_path)
        logging.info("MP4 tags found")
        return tags
    except:
        logging.info("no MP4 tags found")
    return tags


