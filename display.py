from __future__ import unicode_literals
from display_LCD_dummy import displayLCDddummy
from display_LCDd_2x40 import displayLCDd2x40


class DisplayChooser():

    def __init__(self, CONF):
        if CONF.lcd['type'] == '2x40':
            self.display = displayLCDd2x40(CONF=CONF)
        else:
            self.display = displayLCDddummy()