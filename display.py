from __future__ import unicode_literals
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import logging


class DisplayChooser():
    """
    Chooses the display according to the config file
    """

    def __init__(self, loaded_config):
        if loaded_config.lcd['type'] == '2x40':
            from display_LCDd_2x40 import DisplayLCDd2x40

            logging.debug("Imported Display_LCDd_2x40 library, initializing")
            self.display = DisplayLCDd2x40(loaded_config)
        else:
            from display_dummy import DisplayDummy

            logging.debug("Imported Display_dummy library, initializing")
            self.display = DisplayDummy()