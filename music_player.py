from mpd import MPDClient
import os
class Player():
    def __init__(self):
        os.system("mpd /etc/mpd.conf")#lancement de mpd
        self.connect();#connexion
    def connect(self):
        self.client = MPDClient();#creation du client MPD
        self.client.timeout = None;
        self.client.idletimout = None;
        self.client.connect("localhost",6600)
        self.client.update();
        self.client.consume(1);
        self.client.crossfade(1);
    def enqueue(self, music):
        try:
            self.client.add(music.path);
            self.client.play();
        except KeyboardInterrupt:
            raise
        except:
            self.connect()
            self.enqueue(music)
    def isPlaying(self):
        status = self.client.status();
        return status['state']=='play';
    def queue_count(self):
        playlist = self.client.playlist();
        return len(playlist);
    def exit(self):
        self.client.disconnect()
        os.system("killall mpd")
    def cleanFileName(self,path):
        return self.cleanPath(path).replace("/","\ ")
    def cleanPath(self,path):
        return path.replace(" ","\ ").replace("'","\\'").replace("&", "\\&")
    
    def generate_library(self,extraction_path,final_path,filledslots=[]):
        current_path=os.path.abspath(os.path.curdir)
        os.system("cd "+extraction_path)
        lsinfo = self.client.lsinfo()
        print(lsinfo)
        letter = 1;
        number = 1;
        dic=dict([(1,'A'),(2,'B'),(3,'C'),(4,'D')])
        os.system("cd "+current_path)
        #os.system("mkdir "+final_path)
        for e in lsinfo:
            try:
                artist = e['artist']
            except KeyError:
                artist = "unknown"
            try:
                title = e['title']
            except KeyError:
                title = "unknown"
            file_name = e['file']
            extension = file_name.split(".")
            extension = extension.pop(len(extension)-1)
            if letter <= 4:
                if number == 21:
                    number =1
                    letter+=1
                
                    
                index = dic[letter]+str(number)
                number+=1
            else:
                print("too many musics")
                break;
            cp_command= "mv "+\
            self.cleanPath(extraction_path)+"/"+\
            self.cleanPath(file_name)+" "+\
            self.cleanPath(final_path)+"/"+\
            index+"-"+\
            self.cleanFileName(title)+"-"+\
            self.cleanFileName(artist)+"."+\
            extension
            #print(cp_command)
            os.system(cp_command)

#player =Player()
#path = raw_input("Entrez le chemin du repertoire a analyser : ")
#os.system("mkdir ./Music")
#player.listinfo(path,"./Music")