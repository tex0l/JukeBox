import pyLCDd

class displayLCDd2x40: #a class to handle all the display functions of the jukebox and actually display them on a 40x2 display through pyLCDd
    def __init__(self):
        self.display = pyLCDd.pyLCDd("127.0.0.1",13666,"jukeboX")
        self.creditString = self.display.addString(1,1).setText("Credit : 0")
        self.queueString = self.display.addString(30,1).setText("Queue : 0")
        self.icon = self.display.addIcon(1,2).setIcon("PLAY")
        self.line2 = self.display.addString(3,2).setText("Insert Coin")
        self.mode = "coin"
    
    def setCredit(self,c): #Change the number of credits displayed
        self.creditString.setText("Credits : %d" %c)
    
    def setQueue(self,q): #Change the length of the queue displayed
        self.queueString.setText("Queue : %d" %q)
    
    def setMode(self,mode): #mode is a string. "free" for free play mode, "coin" for normal mode
        if mode == "free" or mode == "coin":
            self.mode = mode
        else:
            print("ERROR : invalid mode set")
    
    def waiting(self):
        if self.mode == "free":
            self.icon.setIcon(None)
            self.line2.remove()
            self.line2 = self.display.addString(1,2).setText("Free Play")
        elif self.mode == "coin":
            self.icon.setIcon(None)
            self.line2.remove()
            self.line2 = self.display.addString(1,2).setText("Insert Coin")
    
    def playingSong(self,song):
        self.icon.setIcon("PLAY")
        self.line2.remove()
        self.line2 = self.display.addScroller(3,2,4)
        self.line2.setText(song.display())
    
    def entry(self,letter,number=0,song=None):
        if number!=0:
            text="Entry : %s%d"%(letter.uppercase(),number)
        else:
            text="Entry : %s_"%letter.uppercase()
        
        if song!=None:
            text+=" - Adding %s by %s"%(song.name,song.artist)

    