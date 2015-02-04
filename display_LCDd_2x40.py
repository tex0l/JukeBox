from __future__ import unicode_literals
import pyLCDd
import threading
import time
import music_player


class UpdateThread(threading.Thread):
    def __init__(self, display, CONF):
        threading.Thread.__init__(self)
        self.alive = threading.Event()
        self.alive.set()
        self.display = display
        self.player = music_player.Player(False)
        self.playing = ""
        self.CONF = CONF

    def run(self):
        print("Starting Update Thread")
        while self.alive.isSet():
            time.sleep(0.1)
            self.display.setQueue(self.player.queue_count())
            self.display.waitingEntry()
            if self.player.isPlaying():
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
        self.display = pyLCDd.pyLCDd(self.CONF.lcd['LCDd_host'], self.CONF.lcd['LCDd_port'], "jukeboX")
        self.entryString = self.display.addScroller(1, 1, 28, 4).setText("Choose song")
        self.queueString = self.display.addString(30, 1).setText("Queue : 0")
        self.icon = self.display.addIcon(1, 2).setIcon("STOP")
        self.line2 = self.display.addScroller(3, 2, 38, 4)
        self.UT = UpdateThread(self, CONF)
        self.UT.start()
        self.timer = None
        self.entryInProgress = False
        self.lastAdded = time.time()
        self.queue = 0


    def setQueue(self, q):  # Change the length of the queue displayed
        self.queue = q
        self.queueString.setText("Queue : %d" % q)

    def waiting(self):
        self.icon.setIcon("STOP")
        self.line2.setText("Nothing in the playlist. Add a song ?")

    def playingSong(self, number, title, artist):
        self.icon.setIcon("PLAY")
        self.line2.setText("%s - %s - %s"%(number, title, artist))

    def removeEntry(self):
        self.entryInProgress = False
        self.waitingEntry()

    def waitingEntry(self):
        if self.entryInProgress is False:
            if (self.queue < self.CONF.variables['nb_music']) or (time.time()-self.lastAdded > self.CONF.variables['timeout']):
                self.entryString.setText("Choose song")
            else:
                self.entryString.setText("Wait %s seconds" % (int(self.CONF.variables['timeout']+1-time.time()+self.lastAdded)))

    def entry(self, letter, number="_", song=None):
        self.entryInProgress = True
        text = "Entry : %s%s" % (letter.upper(), number)
        if self.timer is not None:
            self.timer.cancel()
        if song is not None:
            text += " - %s - %s" % (song.name, song.artist)
            self.lastAdded = time.time()
            self.timer = threading.Timer(5, self.removeEntry)
            self.timer.start()
        self.entryString.setText(text)
