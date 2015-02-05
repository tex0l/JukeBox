from __future__ import unicode_literals
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lcdproc.server import Server
import threading
import time
import music_player


class UpdateThread(threading.Thread):
    """

    """
    def __init__(self, display, CONF):
        threading.Thread.__init__(self)
        self.alive = threading.Event()
        self.alive.set()
        self.display = display
        self.player = music_player.Player(CONF, launch=False)
        self.playing = ""
        self.CONF = CONF

    def run(self):
        print("Starting Update Thread")
        while self.alive.isSet():
            time.sleep(0.1)
            self.display.setQueue(self.player.queue_count())
            self.display.waitingEntry()
            if self.player.is_playing():
                if self.player.number() != self.playing:
                    self.display.playingSong(self.player.number(), self.player.title(), self.player.artist())
            else:
                self.display.waiting()
                self.playing = ""

    def join(self, timeout=None):
        self.alive.clear()
        threading.Thread.join(self, timeout)


class displayLCDd2x40:
# a class to handle all the display functions of the jukebox and actually display them on a 40x2 display through pyLCDd
    def __init__(self, CONF):
        self.CONF = CONF

        lcd = Server(hostname=self.CONF.lcd['lcdd_host'], port=self.CONF.lcd['lcdd_port'])
        lcd.start_session()
        screen = lcd.add_screen("jukeboX".encode('ascii', 'ignore'))
        screen.set_heartbeat("off".encode('ascii', 'ignore'))
        screen.set_priority("foreground".encode('ascii', 'ignore'))

        self.entryString = screen.add_scroller_widget("entry".encode('ascii', 'ignore'),
                                                      text="Choose song".encode('ascii', 'ignore'), left=1, top=1,
                                                      right=28, bottom=1, speed=4)
        self.queueString = screen.add_string_widget("queue".encode('ascii', 'ignore'),
                                                    text="Queue : 0".encode('ascii', 'ignore'), x=30, y=1)
        self.icon = screen.add_icon_widget("playIcon".encode('ascii', 'ignore'), x=1, y=2,
                                           name="STOP".encode('ascii', 'ignore'))
        self.playingString = screen.add_scroller_widget("playing".encode('ascii', 'ignore'),
                                                        text="Nothing in the playlist. Add a song ?"
                                                        .encode('ascii', 'ignore'),
                                                        left=3, top=2, right=40, bottom=2, speed=4)
        #self.display.addScroller(3, 2, 38, 4)
        self.UT = UpdateThread(self, CONF)
        self.UT.start()
        self.timer = None
        self.entryInProgress = False
        self.lastAdded = time.time()
        self.queue = 0


    def setQueue(self, q):  # Change the length of the queue displayed
        self.queue = q
        self.queueString.set_text("Queue : %d".encode('ascii', 'ignore') % q)

    def waiting(self):
        self.icon.set_name("STOP".encode('ascii', 'ignore'))
        self.playingString.set_text("Nothing in the playlist. Add a song ?".encode('ascii', 'ignore'))

    def playingSong(self, number, title, artist):
        self.icon.set_name("PLAY".encode('ascii', 'ignore'))
        text = "%s - %s - %s"%(number, title, artist)
        self.playingString.set_text(text.encode('ascii', 'ignore'))

    def removeEntry(self):
        self.entryInProgress = False
        self.waitingEntry()

    def waitingEntry(self):
        if self.entryInProgress is False:
            if (self.queue < self.CONF.variables['nb_music']) \
                    or (time.time()-self.lastAdded > self.CONF.variables['add_timeout']):
                self.entryString.set_text("Choose song".encode('ascii', 'ignore'))
            else:
                text = "Wait %s seconds" % (int(self.CONF.variables['add_timeout']+1-time.time()+self.lastAdded))
                self.entryString.set_text(text.encode('ascii', 'ignore'))

    def entry(self, entry, song=None):
        self.entryInProgress = True
        text = "Entry : %s" % entry
        if self.timer is not None:
            self.timer.cancel()
        if song is not None:
            text += " - %s - %s" % (song.name, song.artist)
            self.lastAdded = time.time()
            self.timer = threading.Timer(5, self.removeEntry)
            self.timer.start()
        self.entryString.set_text(text.encode('ascii', 'ignore'))
