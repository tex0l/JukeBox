from __future__ import unicode_literals
# !/usr/bin/env python
# -*- coding: utf-8 -*-
class DisplayLCDdDummy:
    # TODO
    """

    """
    # a dummy class to use on a computer without a lcd screen emulator
    def __init__(self):
        self.UT = UT()
        return

    # noinspection PyMethodMayBeStatic
    def set_queue(self, q):  # Change the length of the queue displayed
        return

    # noinspection PyMethodMayBeStatic
    def waiting(self):
        return

    # noinspection PyMethodMayBeStatic
    def playing_song(self, number, title, artist):
        return

    # noinspection PyMethodMayBeStatic
    def remove_entry(self):
        return

    # noinspection PyMethodMayBeStatic
    def entry(self, letter, number=None, song=None):
        return


class UT:
    def __init__(self):
        return

    # noinspection PyMethodMayBeStatic
    def join(self):
        return
