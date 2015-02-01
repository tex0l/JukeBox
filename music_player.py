from __future__ import unicode_literals
from mpd import MPDClient
import config
import os
from mutagen.easyid3 import EasyID3
import mutagen


class Player():
    def __init__(self, launch=True):
        if launch:
            command = unicode("mpd %s" % config.MPD_CONF_FILE)
            #lancement de mpd
            os.system(command)
        #connexion
        self.client = None
        self.connect()

    def connect(self):
        #creation du client MPD
        self.client = MPDClient()
        self.client.timeout = None
        self.client.idletimeout = None
        self.client.connect("localhost", 6600)
        #self.client.update()
        #self.client.consume(1)
        #self.client.crossfade(1)

    def enqueue(self, music):
        try:
            self.client.add(music.path)
            self.client.play()
        except KeyboardInterrupt:
            raise
        except:
            self.connect()
            self.enqueue(music)
    def isPlaying(self):
        status = self.client.status()
        return status['state']=='play'
    def title(self):
        try :
            return self.client.currentsong()['title']
        except:
            return ""
    def artist(self):
        try:
            return self.client.currentsong()['artist']
        except:
            return ""
    def number(self):
        try:
            return self.client.currentsong()['file'].split("-")[0]
        except:
            return ""
    def queue_count(self):
        playlist = self.client.playlist()
        return len(playlist)
    def exit(self):
        self.client.disconnect()
        os.system("killall mpd")
    def cleanFileName(self,path):
        return self.cleanPath(path).replace("/","\ ")
    def cleanPath(self,path):
        return path.replace(" ","\ ").replace("'","\\'").replace("&", "\\&").replace("(","\(").replace(")","\)")
    
    def generate_library(self, extraction_path, final_path, filledslots=[]):
        current_path = os.path.abspath(os.path.curdir)
        os.chdir(extraction_path)
        lsinfo = os.listdir(".")
        letter = 1
        number = 1
        dic = dict([(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D')])
        os.system("cd "+current_path)
        #os.system("mkdir "+final_path)
        for file in lsinfo:
            print file
            if not file.startswith('.'):
                try:
                    id3 = EasyID3(file)
                    print id3
                    try:
                        artist = id3['artist'][0]
                        print artist
                    except KeyError:
                        artist = "unknown"
                    try:
                        title = id3['title'][0]
                    except KeyError:
                        title = "unknown"
                    extension = file.split(".")
                    extension = extension.pop(len(extension)-1)
                    while filledslots[letter-1][number-1]:
                        number += 1
                        if number == 21 and letter < 4:
                            number = 1
                            letter += 1
                        if letter == 5:
                            print ("library is full: empty it, skipping")
                            break
                    index = dic[letter]+str(number)
                    from_path = self.cleanPath(extraction_path) + "/" + \
                                self.cleanPath(file) + " "
                    to_path = self.cleanPath(final_path) + "/" + index + "-" + \
                              self.cleanFileName(title) + "-" + \
                              self.cleanFileName(artist) + "." + extension

                    cp_command = "mv " + from_path + " " + to_path
                    #print(cp_command)
                    os.system(cp_command)
                except mutagen.id3._util.ID3NoHeaderError:
                    print "no id3 tags found, ignored"
            else:
                print "system file, ignored"


#player =Player()
#path = raw_input("Entrez le chemin du repertoire a analyser : ")
#os.system("mkdir ./Music")
#player.listinfo(path,"./Music")