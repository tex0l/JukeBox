from __future__ import unicode_literals
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

#TODO Put it in config !
class Map():
    def __init__(self, loaded_config):
        self.map = loaded_config.map
        logging.debug("Map retrieved : %s" % self.map)

    def find(self, char):
        try:
            return self.map[char]
        except KeyError:
            return ""