from __future__ import unicode_literals
from mpd import MPDClient, ConnectionError
import os
import time
import logging
from tags import tag_finder

class Player():
    def __init__(self, CONF, launch=True):
        if launch:
            logging.info("Killing MPD")
            os.system("killall mpd")
            command = unicode("mpd %s" % CONF.paths['mpd_conf_file'])
            #lancement de mpd
            logging.info("Starting MPD...")
            os.system(command)
        #connexion
        self.client = None
        self.CONF = CONF
        logging.info("Connecting to MPD")
        self.connect()
        self.last_added = time.time()

    def connect(self):
        #creation du client MPD
        self.client = MPDClient()
        self.client.timeout = None
        self.client.idletimeout = None
        self.client.connect(self.CONF.network['mpd_host'], self.CONF.network['mpd_port'])
        logging.info("Updating MPD client...")
        self.client.update()
        self.client.consume(1)
        self.client.crossfade(1)

    def enqueue(self, music):
        try:
            logging.info("Adding music %s to queue" % music.path)
            self.client.add(music.path)
            self.client.play()
            self.last_added = time.time()
        except KeyboardInterrupt:
            raise
        except ConnectionError:
            logging.warning("Unable to contact daemon, reconnecting and retry")
            self.connect()
            self.enqueue(music)

    def is_playing(self):
        try:
            status = self.client.status()
            return status['state'] == 'play'
        except ConnectionError:
            logging.warning("Unable to contact daemon, reconnecting and retry")
            self.connect()
            return self.is_playing()

    def title(self):
        try :
            return self.client.currentsong()['title']
        except ConnectionError:
            logging.warning("Unable to contact daemon, reconnecting and retry")
            self.connect()
            return self.title()
        except:
            logging.error("Unable to get the title index of the song")
            return ""

    def artist(self):
        try:
            return self.client.currentsong()['artist']
        except ConnectionError:
            logging.warning("Unable to contact daemon, reconnecting and retry")
            self.connect()
            return self.artist()
        except:
            logging.error("Unable to get the artist of the song")
            return ""

    def number(self):
        try:
            return self.client.currentsong()['file'].split("-")[0]
        except ConnectionError:
            logging.warning("Unable to contact daemon, reconnecting and retry")
            self.connect()
            return self.number()
        except:
            logging.error("Unable to get the index of the song")
            return ""

    def queue_count(self):
        try:
            playlist = self.client.playlist()
            return len(playlist)
        except ConnectionError:
            logging.warning("Unable to contact daemon, reconnecting and retry")
            self.connect()
            return self.queue_count()

    def exit(self):
        try:
            logging.info("Disconnecting client")
            self.client.disconnect()
        except ConnectionError:
            logging.warning("Unable to contact daemon, reconnecting and retry")
            self.connect()
            self.exit()
            return
        logging.info('Killing MPD')
        os.system("killall mpd")

    def generate_library(self, extraction_path, final_path, filled_slots=[]):
        logging.debug("Getting current path")
        current_path = os.getcwd()
        import_path = self.get_absolute_path(extraction_path)
        export_path = self.get_absolute_path(final_path)
        logging.debug("Changing directory to %s" % import_path)
        os.chdir(import_path)
        logging.debug("Listing directory")
        ls_info = os.listdir(".")
        dic = dict([(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D')])
        result = {}
        logging.debug("Browsing directory")
        for file_path in ls_info:
            logging.info("Currently working on %s ..." % file_path)
            tags = tag_finder(file_path)
            try:
                result = self.index_picker(dic, filled_slots=filled_slots,
                                           letter=result['letter'], number=result['number'])
            except KeyError:
                if result != {}:
                    logging.debug("Letter and number are not defined, if you see this often, there might be a problem")
                    result = self.index_picker(dic, filled_slots=filled_slots)
                else:
                    logging.debug("No tags received, must be a system file")
                    break

            from_path = self.format_path(import_path) + u"/" + \
                        self.format_path(file_path) + u" "
            to_path = self.format_path(export_path) + u"/" + result['index'] + u"-" + \
                      self.format_file_name(tags['title']) + u"-" + \
                      self.format_file_name(tags['artist']) + u"." + tags['extension']

            cp_command = "mv " + from_path + " " + to_path
            try:
                os.system(cp_command)
                logging.info("Successfully moved %s to %s " % (from_path, to_path))
            except:
                logging.error("Failed to move %s to %s " % (from_path, to_path))

        logging.info("All musics in import directory have been processed.")
        logging.debug("Changing directory to %s." % current_path)
        os.chdir(current_path)
    @staticmethod
    def get_absolute_path(path):
        return os.path.join(os.path.dirname(__file__), path)

    @staticmethod
    def format_file_name(path):
        return Player.format_path(path).replace("/", "\ ")

    @staticmethod
    def format_path(path):
        return path.replace(" ", "\ ").replace("'", "\\'").replace("&", "\\&").replace("(", "\(").replace(")", "\)")

    @staticmethod
    def index_picker(dic, filled_slots, letter=1, number=1):
        while filled_slots[letter-1][number-1]:
            number += 1
            if number == 21 and letter < 4:
                number = 1
                letter += 1
            if letter == 5:
                logging.warning("Library is full: empty it ! skipping...")
                break
        index = dic[letter]+str(number)
        filled_slots[letter-1][number-1] = True
        return {"index": index, "filled_slots": filled_slots, "letter": letter, "number": number}