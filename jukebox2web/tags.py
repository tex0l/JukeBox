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

    if not file_path.startswith('.'):
        result = {}
        tags = id3_finder(file_path)
        KEYS = [
            'artist',
            'title',
            'album',
            'date',
            'tracknumber',
            'discnumber'
        ]
        for key in KEYS:
            result = add_key(tags, result, key)
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

def add_key(import_dict, result_dict, key):
    if import_dict.has_key(key):
        result_dict[key] = import_dict[key][0]
        logging.debug("Tag %s found: %s" % (key, result_dict[key]))
    else:
        logging.warning("No %s tag found" % key)
    return result_dict

def id3_finder(file_path):
    # TODO
    """

    """
    # noinspection PyBroadException
    try:
        tags = EasyID3(file_path)
        logging.debug("ID3 tags found")
        return tags
    except Exception as e:
        logging.info('Exception: %s' % e)
        logging.info("no ID3 tags found")
    # noinspection PyBroadException
    try:
        tags = EasyMP4(file_path)
        logging.debug("MP4 tags found")
        return tags
    except Exception as e:
        logging.info('Exception: %s' % e)
        logging.info("no MP4 tags found")
    return {}


def pict_test(audio):
    try:
        x = audio.pictures
        if x:
            return True
    except Exception:
        pass
    if 'covr' in audio or 'APIC:' in audio:
        return True
    return False
