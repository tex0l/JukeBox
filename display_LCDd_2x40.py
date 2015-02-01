import pyLCDd
import threading
import time
import music_player


class UpdateThread(threading.Thread):
    def __init__(self, display):
        threading.Thread.__init__(self)
        self.alive = threading.Event()
        self.alive.set()
        self.display = display
        self.player = music_player.Player(False)
        self.playing = ""
        self.entry = False

    def run(self):
        print("Starting Update Thread")
        while self.alive.isSet():
            time.sleep(0.1)
            self.display.setQueue(self.player.queue_count())
            if not self.entry:
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
    def __init__(self):
        self.display = pyLCDd.pyLCDd("localhost", 13666, "jukeboX")
        self.creditString = self.display.addString(1, 1).setText("Credits : 0")
        self.queueString = self.display.addString(30, 1).setText("Queue : 0")
        self.icon = self.display.addIcon(1, 2).setIcon("STOP")
        self.line2 = self.display.addString(3, 2).setText("Insert Coin")
        self.mode = "coin" # coin or free
        self.credit = 0
        self.UT = UpdateThread(self)
        self.UT.start()
        self.timer = None

    def setCredit(self, c):  # Change the number of credits displayed
        self.credit = c
        if self.credit < 0:
            self.creditString.setText("Free Play")
        else:
            self.creditString.setText("Credits : %d" % c)

    def setQueue(self, q):  # Change the length of the queue displayed
        self.queueString.setText("Queue : %d" % q)

    def waiting(self):
        if self.mode=="free" or self.credit>0:
            self.icon.setIcon("STOP")
            self.line2.remove()
            self.line2 = self.display.addString(3, 2).setText("Choose song")
        elif self.mode == "coin" and self.credit==0:
            self.icon.setIcon("STOP")
            self.line2.remove()
            self.line2 = self.display.addString(3, 2).setText("Insert Coin")

    def playingSong(self, number, title, artist):
        self.icon.setIcon("PLAY")
        self.line2.remove()
        self.line2 = self.display.addScroller(3, 2, 4)
        self.line2.setText("%s - %s by %s"%(number, title, artist))

    def removeEntry(self):
        self.UT.entry=False

    def entry(self, letter, number="_", song=None):
        text = "Entry : %s%s" % (letter.upper(), number)
        if self.timer is not None:
            self.timer.cancel()
        self.UT.entry = True
        if song is not None:
            text += " - %s by %s" % (song.name, song.artist)
            self.timer=threading.Timer(5,self.removeEntry)
            self.timer.start()
        self.line2.remove()
        self.line2 = self.display.addString(3, 2).setText(text)
