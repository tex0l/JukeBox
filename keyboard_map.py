from __future__ import unicode_literals
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import logging


class Map:
    """
    Get the keyboard mapping from the config file
    """
    def __init__(self, conf):
        """
        :param conf: the configuration given
        :type conf: config.Config
        """
        self.map = conf.map
        logging.debug("Map retrieved : %s" % self.map)

    def find(self, char):
        """
        :param char: character to map
        :type char: unicode

        :return: the mapped character if found
        :rtype: unicode
        """
        try:
            return self.map[char]
        except KeyError:
            logging.debug("Did not find char %s in map" % char)
            return ""
