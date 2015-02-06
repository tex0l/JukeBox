from __future__ import unicode_literals
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging


class DisplayChooser():
    #TODO
    """

    """
    def __init__(self, loaded_config):
        #TODO
        """

        """
        if loaded_config.lcd['type'] == '2x40':
            from display_LCDd_2x40 import Display_LCDd_2x40
            logging.debug("Imported Display_LCDd_2x40 library, initializing")
            self.display = Display_LCDd_2x40(loaded_config)
        else:
            from display_LCD_dummy import Display_LCDd_dummy
            logging.debug("Imported Display_LCDd_dummy library, initializing")
            self.display = Display_LCDd_dummy()