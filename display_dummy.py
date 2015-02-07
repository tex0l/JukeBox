from __future__ import unicode_literals
# !/usr/bin/env python
# -*- coding: utf-8 -*-


class DisplayDummy:
    """
    A dummy class to use on a computer without any display
    """
    def __init__(self):
        self.UT = UT()
        return

    def set_queue(self, q):
        return

    def waiting(self):
        return

    def playing_song(self, number, title, artist):
        return

    def remove_entry(self):
        return

    def entry(self, letter, number=None, song=None):
        return


class UT:
    def __init__(self):
        return

    def join(self):
        return
