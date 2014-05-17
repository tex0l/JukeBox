import socket, threading

class pyLCDd:
    
    #class ReceiveThread(threading.Thread): #ugly way to clear the receiving buffer
    #    def __init__(self,socket):
    #        threading.Thread.__init__(self)
    #        self.socket=socket
    #    
    #    def run(self):
    #        print("Starting Receiving Thread")
    #        while self.alive.isSet():
    #            print("Starting Receiving Thread")
    #            print(self.socket.recv(1024))
    
    def __init__(self,server,port,clientName):
        self.server=server
        self.port=port
        self.clientName=clientName
        self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((server,port)) #connecting socket to LCDd server
        #RT=self.ReceiveThread(self.socket)
        #RT.start()
        self.socket.send("hello") #handshake with the LCDd server
        self.socket.send("client_set -name "+clientName) #creating a client in LCDd
        self.socket.send("screen_add 0")
        self.socket.send("screen_set 0 -priority foreground")
        self.widgets=[]
    
    def findFreeId(self):
        i = 0
        while True:
            i+=1
            j=0
            for w in self.widgets:
                if i==w.id:
                    break
                j+=1
            if j==len(self.widgets):
                break
        return i 
    
    class LCDString:
        def __init__(self,id,x,y,LCD):
            self.id=id
            self.x=x
            self.y=y
            self.LCD=LCD
            self.LCD.socket.send("widget_add 0 %d string" %s.id)

        
        def setText(self,text):
            self.LCD.socket.send("widget_set 0 %d %d %d %s"%(self.id,self.x,self.y,text))
            return self

        def remove(self):
            self.LCD.widgets.remove(self)
            self.LCD.socket.send("widget_del 0 %d" %self.id)
    
    def addString(self,x,y):
        s=LCDString(self.findFreeId(),x,y,self) #creating a new LCDString, the ID is equal to the current number of widgets
        self.widgets.append(s)
        return s

    class LCDScroller:
        def __init__(self,id,x,y,width,direction,speed,LCD):
            self.id=id
            self.x=x
            self.y=y
            self.width=width
            self.direction=direction
            self.speed=speed
            self.LCD=LCD
            self.LCD.socket.send("widget_add 0 %d scroller" %s.id)

        
        def setText(self,text):
            self.LCD.socket.send("widget_set 0 %d %d %d %d %d %s %d %s"%(self.id,self.x,self.y,self.x+self.width-1,self.y,self.direction,self.speed,text))
            return self
        
        def remove(self):
            self.LCD.widgets.remove(self)
            self.LCD.socket.send("widget_del 0 %d" %self.id)

    def addScroller(self,x,y,speed): #speed: int. 0 means still. 1 is the fastest
        s=LCDScroller(self.findFreeId(),x,y,38,h,speed,self) #creating a new LCDScroller, the ID is equal to the current number of widgets
        self.widgets.append(s)
        return s
    
    class LCDIcon:
        def __init__(self,id,x,y,LCD):
            self.id=id
            self.x=x
            self.y=y
            self.LCD=LCD
            self.LCD.socket.send("widget_add 0 %d icon" %s.id)
            
        def setIcon(self, iconName): #iconeName MUST be a valid LCDd icon name
            self.LCD.socket.send("widget_set 0 %d %d %d %s"%(self.id,self.x,self.y,iconName))
            return self
            
        def remove():
            self.LCD.socket.send("widget_del 0 %d" %self.id)
    
    def addIcon(self,x,y):
        s=LCDIcon(self.findFreeId(),x,y,self)
        self.widgets.append(s)
        return s
