from __future__ import unicode_literals
# !/usr/bin/env python
# -*- coding: utf-8 -*-
from mutagen.easyid3 import EasyID3
from mutagen.easymp4 import EasyMP4
import logging


def tag_finder(file_path):
    # TODO
    """

    """
    logging.debug("tag_finder started on %s" % file_path)

    if not file_path.startswith(u'.'):
        result = {}
        tags = id3_finder(file_path)
        try:
            result['artist'] = tags['artist'][0]
            logging.debug("Artist found: %s" % result['artist'])
        except KeyError:
            result['artist'] = "unknown"
            logging.warning("No artist tag found, setting to unknown")

        try:
            result['title'] = tags['title'][0]
            logging.debug("Title found: %s" % result['title'])
        except KeyError:
            result['title'] = "unknown"
            logging.warning("No title tag found, setting to unknown")
        # noinspection PyBroadException
        try:
            result['extension'] = file_path.split(u".")
            result['extension'] = result['extension'].pop(len(result['extension']) - 1)
            logging.debug("Extension found: %s" % result['extension'])
        except:
            logging.warning("No extension found")
        return result
    else:
        logging.debug("System file, ignored.")
    return {}


def id3_finder(file_path):
    # TODO
    """

    """
    # noinspection PyBroadException
    try:
        tags = EasyID3(file_path)
        logging.debug("ID3 tags found")
        return tags
    except:
        logging.info("no ID3 tags found")
    # noinspection PyBroadException
    try:
        tags = EasyMP4(file_path)
        logging.debug("MP4 tags found")
        return tags
    except:
        logging.info("no MP4 tags found")
    return {}


