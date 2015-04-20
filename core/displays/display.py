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
            try:
                from lib.displays.display_LCDd_2x40 import DisplayLCDd2x40
                logging.debug("Imported display_LCDd_2x40 library, initializing")
                self.display = DisplayLCDd2x40(loaded_config)
                return
            except:
                logging.warning("2x40 display cannot be initialized, switching to dummy")

        from lib.displays.display_dummy import DisplayDummy
        logging.debug("Imported DisplayDummy library, initializing")
        self.display = DisplayDummy()