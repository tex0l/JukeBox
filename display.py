from __future__ import unicode_literals
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from display_LCD_dummy import displayLCDddummy
from display_LCDd_2x40 import displayLCDd2x40


class DisplayChooser():

    def __init__(self, CONF):
        if CONF.lcd['type'] == '2x40':
            self.display = displayLCDd2x40(CONF)
        else:
            self.display = displayLCDddummy()