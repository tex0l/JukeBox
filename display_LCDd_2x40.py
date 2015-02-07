from __future__ import unicode_literals
# !/usr/bin/env python
# -*- coding: utf-8 -*-
from lcdproc.server import Server
from threading import Thread, Event, Timer, Lock
import time
import logging


class LockableServer(Server):
    """
    A subclass of lcdproc Server to make it thread-safe
    """

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
    """
    A thread to update the display regularly
    """

    def __init__(self, display, player, loaded_config):
        Thread.__init__(self)
        self.alive = Event()
        self.alive.set()
        self.display = display
        self.player = player
        self.playing = ""
        self.loaded_config = loaded_config

    def run(self):
        logging.debug("Starting updating thread ")
        while self.alive.isSet():
            time.sleep(0.25)
            self.display.set_queue(self.player.queue_count())
            self.display.waiting_entry()
            if self.player.is_playing():
                if self.player.number() != self.playing:
                    self.display.playing_song(self.player.number(), self.player.title(), self.player.artist())
            else:
                self.display.waiting()
                self.playing = ""

    def join(self, timeout=None):
        self.alive.clear()
        return super(UpdateThread, self).join(timeout)


class DisplayLCDd2x40:
    """
    A class to handle all the display functions of the jukebox and actually display them on a 40x2 
    display through the python lcdproc module
    """
    
    def __init__(self, player, loaded_config):
        self.loaded_config = loaded_config

        self.lcd = LockableServer(hostname=self.loaded_config.lcd['lcdd_host'], port=self.loaded_config.lcd['lcdd_port'])
        with self.lcd:
            self.lcd.start_session()
            self.screen = self.lcd.add_screen("jukebox".encode('ascii', 'replace'))
            self.screen.set_heartbeat("off".encode('ascii', 'replace'))
            self.screen.set_priority("foreground".encode('ascii', 'replace'))
            self.entry_string = self.screen.add_scroller_widget("entry".encode('ascii', 'replace'),
                                                       text="Choose song".encode('ascii', 'replace'), left=1, top=1,
                                                       right=28, bottom=1, speed=4)
            self.queue_string = self.screen.add_string_widget("queue".encode('ascii', 'replace'),
                                                     text="Queue : 0".encode('ascii', 'replace'), x=30, y=1)
            self.icon = self.screen.add_icon_widget("playIcon".encode('ascii', 'replace'), x=1, y=2,
                                           name="STOP".encode('ascii', 'replace'))
            self.playing_string = self.screen.add_scroller_widget("playing".encode('ascii', 'replace'),
                                                         text="Nothing in the playlist. Add a song ?"
                                                         .encode('ascii', 'replace'),
                                                         left=3, top=2, right=40, bottom=2, speed=4)
        self.UT = UpdateThread(self, player, loaded_config)
        self.UT.start()
        self.timer = None
        self.entryInProgress = False
        self.lastAdded = time.time()
        self.queue = 0


    def set_queue(self, q): 
        """
        Change the length of the queue displayed on the LCD
        """
        self.queue = q
        with self.lcd:
            self.queue_string.set_text("Queue : %d".encode('ascii', 'replace') % q)

    def waiting(self):
        """
        Tell the display that no song is playing
        """
        with self.lcd:
            self.icon.set_name("STOP".encode('ascii', 'replace'))
            self.playing_string.set_text("Nothing in the playlist. Add a song ?".encode('ascii', 'replace'))

    def playing_song(self, number, title, artist):
        """
        Tell the display which song is playing
        """
        with self.lcd:
            self.icon.set_name("PLAY".encode('ascii', 'replace'))
            text = "%s - %s - %s" % (number, title, artist)
            self.playing_string.set_text(text.encode('ascii', 'replace'))

    def remove_entry(self):
        """
        Tell the display that there is no entry
        """
        self.entryInProgress = False
        self.waiting_entry()

    def waiting_entry(self):
        """
        The display waits for an entry
        """
        if self.entryInProgress is False:
            if (self.queue < self.loaded_config.variables['nb_music']) \
                    or (time.time() - self.lastAdded > self.loaded_config.variables['add_timeout']):
                with self.lcd:
                    self.entry_string.set_text("Choose song".encode('ascii', 'replace'))
            else:
                text = "Wait %s seconds" % (
                int(self.loaded_config.variables['add_timeout'] + 1 - time.time() + self.lastAdded))
                with self.lcd:
                    self.entry_string.set_text(text.encode('ascii', 'replace'))

    def entry(self, entry, song=None):
        """
        The display shows the current entry
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
            self.entry_string.set_text(text.encode('ascii', 'replace'))
