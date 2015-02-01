import socket, threading


class pyLCDd:
    #class ReceiveThread(threading.Thread): #ugly way to clear the receiving buffer
    #    def __init__(self,socket):
    #        threading.Thread.__init__(self)
    #        self.socket=socket
    #        self.alive = threading.Event()
    #        self.alive.set()
    #
    #    
    #    def run(self):
    #        print("Starting Receiving Thread")
    #        while self.alive.isSet():
    #            print("Starting Receiving Thread")
    #            print(self.socket.recv(1024))
    #    
    #    def join(self, timeout=None):
    #        self.alive.clear()
    #        threading.Thread.join(self, timeout)
    
    def __init__(self, server, port, clientName):
        self.server = server
        self.port = port
        self.clientName = clientName
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #connecting socket to LCDd server
        self.socket.connect((server, port))
        #self.RT=self.ReceiveThread(self.socket)
        #self.RT.start()

        #handshake with the LCDd server
        self.socket.send("hello\n")
        #creating a client in LCDd
        self.socket.send("client_set -name "+clientName + "\n")
        self.socket.send("screen_add 0\n")
        self.socket.send("screen_set 0 -priority foreground\n")
        self.widgets = []
    
    def findFreeId(self):
        i = 0
        while True:
            i += 1
            j = 0
            for w in self.widgets:
                if i == w.id:
                    break
                j += 1
            if j == len(self.widgets):
                break
        return i 
    
    class LCDString:
        def __init__(self, id, x, y, LCD):
            self.id = id
            self.x = x
            self.y = y
            self.LCD = LCD
            self.LCD.socket.send("widget_add 0 %d string\n" % self.id)

        
        def setText(self,text):
            self.LCD.socket.send("widget_set 0 %d %d %d \"%s\"\n" % (self.id, self.x, self.y, text))
            return self

        def remove(self):
            self.LCD.widgets.remove(self)
            self.LCD.socket.send("widget_del 0 %d\n" % self.id)
    
    def addString(self, x, y):
        #creating a new LCDString, the ID is equal to the current number of widgets
        s = self.LCDString(self.findFreeId(), x, y, self)
        self.widgets.append(s)
        return s

    class LCDScroller:
        def __init__(self, id, x, y, width, direction, speed, LCD):
            self.id = id
            self.x = x
            self.y = y
            self.width = width
            self.direction = direction
            self.speed = speed
            self.LCD = LCD
            self.LCD.socket.send("widget_add 0 %d scroller\n" % self.id)

        def setText(self, text):
            self.LCD.socket.send("widget_set 0 %d %d %d %d %d %s %d \"%s\"\n" %
                                 (self.id, self.x, self.y, self.x+self.width-1,
                                  self.y, self.direction, self.speed, text))
            return self
        
        def remove(self):
            self.LCD.widgets.remove(self)
            self.LCD.socket.send("widget_del 0 %d\n" % self.id)

    #speed: int. 0 means still. 1 is the fastest
    def addScroller(self, x, y, width, speed):
        #creating a new LCDScroller, the ID is equal to the current number of widgets
        s = self.LCDScroller(self.findFreeId(), x, y, width, "h", speed, self)
        self.widgets.append(s)
        return s
    
    class LCDIcon:
        def __init__(self, id, x, y, LCD):
            self.id = id
            self.x=x
            self.y=y
            self.LCD=LCD
            self.LCD.socket.send("widget_add 0 %d icon\n" %self.id)
            
        def setIcon(self, iconName): #iconeName MUST be a valid LCDd icon name
            self.LCD.socket.send("widget_set 0 %d %d %d %s\n" % (self.id, self.x, self.y, iconName))
            return self
            
        def remove(self):
            self.LCD.socket.send("widget_del 0 %d\n" % self.id)
    
    def addIcon(self, x, y):
        s = self.LCDIcon(self.findFreeId(), x, y, self)
        self.widgets.append(s)
        return s
