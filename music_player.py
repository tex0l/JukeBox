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