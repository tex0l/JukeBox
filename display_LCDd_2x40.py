from __future__ import unicode_literals
# !/usr/bin/env python
# -*- coding: utf-8 -*-
from lcdproc.server import Server
from threading import Thread, Event, Timer, Lock
import time
import logging


class LockableServer(Server):
    def __init__(self, hostname, port):
        super(LockableServer, self).__init__(hostname=hostname, port=port)
        self._lock = Lock()

    def acquire(self):
        self._lock.acquire()

    def release(self):
        self._lock.release()

    def __enter__(self):
        self.acquire()

    # noinspection PyShadowingBuiltins,PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
    def __exit__(self, type, value, traceback):
        self.release()


class UpdateThread(Thread):
    # TODO
    """

    """

    def __init__(self, display, player, loaded_config):
        #TODO
        """

        """
        Thread.__init__(self)
        self.alive = Event()
        self.alive.set()
        self.display = display
        self.player = player
        self.playing = ["",""]
        self.loaded_config = loaded_config

    def run(self):
        #TODO
        """

        """
        logging.debug("Starting updating thread ")
        while self.alive.isSet():
            time.sleep(0.1)
            self.display.set_queue(self.player.queue_count())
            self.display.waiting_entry()
            if self.player.is_playing():
                if self.player.index() != self.playing:
                    self.display.playing_song(self.player.index(), self.player.title(), self.player.artist())
            else:
                self.display.waiting()
                self.playing = ""

    def join(self, timeout=None):
        #TODO
        """

        """
        self.alive.clear()
        Thread.join(self, timeout)


class DisplayLCDd2x40:
    # TODO
    """

    """
    # a class to handle all the display functions of the jukebox and actually display them on a 40x2 display through pyLCDd
    def __init__(self, player, loaded_config):
        #TODO
        """

        """
        self.loaded_config = loaded_config

        self.lcd = LockableServer(hostname=self.loaded_config.lcd['lcdd_host'],
                                  port=self.loaded_config.lcd['lcdd_port'])
        with self.lcd:
            self.lcd.start_session()
            self.screen = self.lcd.add_screen("jukebox".encode('ascii', 'ignore'))
            self.screen.set_heartbeat("off".encode('ascii', 'ignore'))
            self.screen.set_priority("foreground".encode('ascii', 'ignore'))
            self.entry_string = self.screen.add_scroller_widget("entry".encode('ascii', 'ignore'),
                                                                text="Choose song".encode('ascii', 'ignore'), left=1,
                                                                top=1,
                                                                right=28, bottom=1, speed=4)
            self.queue_string = self.screen.add_string_widget("queue".encode('ascii', 'ignore'),
                                                              text="Queue : 0".encode('ascii', 'ignore'), x=30, y=1)
            self.icon = self.screen.add_icon_widget("playIcon".encode('ascii', 'ignore'), x=1, y=2,
                                                    name="STOP".encode('ascii', 'ignore'))
            self.playing_string = self.screen.add_scroller_widget("playing".encode('ascii', 'ignore'),
                                                                  text="Nothing in the playlist. Add a song ?"
                                                                  .encode('ascii', 'ignore'),
                                                                  left=3, top=2, right=40, bottom=2, speed=4)
        self.UT = UpdateThread(self, player, loaded_config)
        self.UT.start()
        self.timer = None
        self.entryInProgress = False
        self.lastAdded = time.time()
        self.queue = 0


    def set_queue(self, q):  # Change the length of the queue displayed
        #TODO
        """

        """
        self.queue = q
        with self.lcd:
            self.queue_string.set_text("Queue : %d".encode('ascii', 'ignore') % q)

    def waiting(self):
        #TODO
        """

        """
        with self.lcd:
            self.icon.set_name("STOP".encode('ascii', 'ignore'))
            self.playing_string.set_text("Nothing in the playlist. Add a song ?".encode('ascii', 'ignore'))

    def playing_song(self, index, title, artist):
        #TODO
        """

        """
        with self.lcd:
            self.icon.set_name("PLAY".encode('ascii', 'ignore'))
            index = unicode(index[0])+unicode(index[1])
            text = "%s - %s - %s" % (index, title, artist)
            self.playing_string.set_text(text.encode('ascii', 'ignore'))

    def remove_entry(self):
        #TODO
        """

        """
        self.entryInProgress = False
        self.waiting_entry()

    def waiting_entry(self):
        #TODO
        """

        """
        if self.entryInProgress is False:
            if (self.queue < self.loaded_config.variables['nb_music']) \
                    or (time.time() - self.lastAdded > self.loaded_config.variables['add_timeout']):
                with self.lcd:
                    self.entry_string.set_text("Choose song".encode('ascii', 'ignore'))
            else:
                text = "Wait %s seconds" % (
                    int(self.loaded_config.variables['add_timeout'] + 1 - time.time() + self.lastAdded))
                with self.lcd:
                    self.entry_string.set_text(text.encode('ascii', 'ignore'))

    def entry(self, entry, song=None):
        #TODO
        """

        """
        self.entryInProgress = True
        text = "Entry : %s" % entry
        if self.timer is not None:
            self.timer.cancel()
        if song is not None:
            text += " - %s - %s" % (song.name, song.artist)
            self.lastAdded = time.time()
            self.timer = Timer(5, self.remove_entry)
            self.timer.start()
        with self.lcd:
            self.entry_string.set_text(text.encode('ascii', 'ignore'))
