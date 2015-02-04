from __future__ import unicode_literals
from mpd import MPDClient, ConnectionError
import config
import os
import time
from mutagen.easyid3 import EasyID3
import mutagen
from slugify import slugify

class Player():
    def __init__(self, CONF, launch=True):
        if launch:
            os.system("killall mpd")
            command = unicode("mpd %s" % CONF.paths['mpd_conf_file'])
            #lancement de mpd
            os.system(command)
        #connexion
        self.client = None
        self.CONF = CONF
        self.connect()
        self.lastAdded = time.time()


    def connect(self):
        #creation du client MPD
        self.client = MPDClient()
        self.client.timeout = None
        self.client.idletimeout = None
        self.client.connect(self.CONF.network['host'], self.CONF.network['port'])
        self.client.update()
        self.client.consume(1)
        self.client.crossfade(1)

    def enqueue(self, music):
        try:
            self.client.add(music.path)
            self.client.play()
            self.lastAdded = time.time()
        except KeyboardInterrupt:
            raise
        except ConnectionError:
            self.connect()
            self.enqueue(music)

    def isPlaying(self):
        try:
            status = self.client.status()
            return status['state']=='play'
        except ConnectionError:
            self.connect()
            return (self.isPlaying())

    def title(self):
        try :
            return self.client.currentsong()['title']
        except ConnectionError:
            self.connect()
            return (self.title())
        except:
            return ""

    def artist(self):
        try:
            return self.client.currentsong()['artist']
        except ConnectionError:
            self.connect()
            return (self.artist())
        except:
            return ""

    def number(self):
        try:
            return self.client.currentsong()['file'].split("-")[0]
        except ConnectionError:
            self.connect()
            return (self.isPlaying())
        except:
            return ""

    def queue_count(self):
        try:
            playlist = self.client.playlist()
            return len(playlist)
        except ConnectionError:
            self.connect()
            return (self.queue_count())

    def exit(self):
        try:
            self.client.disconnect()
        except ConnectionError:
            self.connect()
            self.exit()
            return
        os.system("killall mpd")

    def cleanFileName(self,path):
        return self.cleanPath(path).replace("/","\ ")

    def cleanPath(self,path):
        return path.replace(" ","\ ").replace("'","\\'").replace("&", "\\&").replace("(","\(").replace(")","\)")
    
    def generate_library(self, extraction_path, final_path, filledslots=[]):
        current_path = os.getcwd()
        import_path = os.path.join(os.path.dirname(__file__), extraction_path)
        export_path = os.path.join(os.path.dirname(__file__), final_path)
        os.chdir(import_path)
        lsinfo = os.listdir(".")
        letter = 1
        number = 1
        dic = dict([(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D')])
        #os.system("mkdir "+final_path)
        for file in lsinfo:
            #file = repr(file)
            if not file.startswith(u'.'):
                try:
                    id3 = EasyID3(file)
                    print id3
                    try:
                        artist = slugify(id3[u'artist'][0], separator=" ")
                    except KeyError:
                        artist = u"unknown"
                    try:
                        title = slugify(id3[u'title'][0], separator=" ")
                        print title
                    except KeyError:
                        title = u"unknown"
                    extension = file.split(u".")
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
                    filledslots[letter-1][number-1] = True
                    from_path = self.cleanPath(import_path) + u"/" + \
                                self.cleanPath(file) + u" "
                    to_path = self.cleanPath(export_path) + u"/" + index + u"-" + \
                              self.cleanFileName(title) + u"-" + \
                              self.cleanFileName(artist) + u"." + extension

                    cp_command = "mv " + from_path + " " + to_path
                    print "\nmoved" + from_path + "\nto" + to_path
                    #print(cp_command)
                    os.system(cp_command)
                except mutagen.id3._util.ID3NoHeaderError:
                    print "no id3 tags found, ignored"
            else:
                print "system file, ignored"
        os.chdir(current_path)


#player =Player()
#path = raw_input("Entrez le chemin du repertoire a analyser : ")
#os.system("mkdir ./Music")
#player.listinfo(path,"./Music")