from __future__ import unicode_literals
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mpd import MPDClient, ConnectionError
import os
import time
import logging
from tags import tag_finder
from slugify import slugify
import socket

#class MyError(socket.error, ConnectionError):


class Player():
    #TODO
    """

    """
    def __init__(self, loaded_config, launch=True):
        #TODO
        """

        """
        if launch:
            logging.info("Killing MPD")
            os.system("killall mpd")
            command = unicode("mpd %s" % loaded_config.paths['mpd_conf_file'])
            #lancement de mpd
            logging.info("Starting MPD")
            os.system(command)
        #connexion
        self.client = MPDClient()
        self.client.timeout = None
        self.client.idletimeout = None
        self.loaded_config = loaded_config
        logging.info("Connecting to MPD")
        self.connect()
        self.last_added = time.time()
        self.client.consume(1)
        self.client.crossfade(1)
        self.dic = dict([(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D')])

    def connect(self):
        #TODO
        """

        """
        try:
            self.client.connect(self.loaded_config.network['mpd_host'], self.loaded_config.network['mpd_port'])
            logging.info("Updating MPD client")
            self.client.update()
            self.update()
        except ConnectionError, socket.error:
            logging.warning("Unable to contact daemon, reconnecting and retry")
            self.connect()

    def update(self):
        #TODO
        """

        """
        logging.info("Updating the library")
        try:
            self.client.update(1)
        except ConnectionError, socket.error:
            logging.warning("Unable to contact daemon, reconnecting and retry")
            self.connect()

    def enqueue(self, music):
        #TODO
        """

        """
        try:
            logging.info("Adding music %s to queue" % music.path)
            self.client.add(music.path)
            self.client.play()
            self.last_added = time.time()
        except KeyboardInterrupt:
            raise
        except ConnectionError, socket.error:
            logging.warning("Unable to contact daemon, reconnecting and retry")
            self.connect()
            self.enqueue(music)

    def is_playing(self):
        #TODO
        """

        """
        try:
            status = self.client.status()
            return status['state'] == 'play'
        except ConnectionError, socket.error:
            logging.warning("Unable to contact daemon, reconnecting and retry")
            self.connect()
            return self.is_playing()

    def title(self):
        #TODO
        """

        """
        try:
            return self.client.currentsong()['title']
        except ConnectionError, socket.error:
            logging.warning("Unable to contact daemon, reconnecting and retry")
            self.connect()
            return self.title()
        except:
            logging.error("Unable to get the title index of the song")
            return ""

    def artist(self):
        #TODO
        """

        """
        try:
            return self.client.currentsong()['artist']
        except ConnectionError, socket.error:
            logging.warning("Unable to contact daemon, reconnecting and retry")
            self.connect()
            return self.artist()
        except:
            logging.error("Unable to get the artist of the song")
            return ""

    def number(self):
        #TODO
        """

        """
        try:
            return self.client.currentsong()['file'].split("-")[0]
        except ConnectionError, socket.error:
            logging.warning("Unable to contact daemon, reconnecting and retry")
            self.connect()
            return self.number()
        except:
            logging.error("Unable to get the index of the song")
            return ""

    def queue_count(self):
        #TODO
        """

        """
        try:
            playlist = self.client.playlist()
            return len(playlist)
        except ConnectionError, socket.error:
            logging.warning("Unable to contact daemon, reconnecting and retry")
            self.connect()
            return self.queue_count()

    def exit(self):
        #TODO
        """

        """
        try:
            logging.info("Disconnecting client")
            self.client.disconnect()
        except ConnectionError, socket.error:
            logging.warning("Unable to contact daemon, reconnecting and retry")
            self.connect()
            self.exit()
            return
        logging.info('Killing MPD')
        os.system("killall mpd")

    def generate_library(self, extraction_path, final_path, filled_slots=None):
        #TODO
        """

        """
        if not filled_slots: filled_slots = []
        logging.debug("Getting current path")
        current_path = os.getcwd()
        import_path = self.get_absolute_path(extraction_path)
        export_path = self.get_absolute_path(final_path)
        logging.debug("Changing directory to %s" % import_path)
        os.chdir(import_path)
        logging.debug("Listing directory")
        ls_info = os.listdir(".")
        result = {}
        logging.debug("Browsing directory")
        for file_path in ls_info:
            logging.info("Currently working on %s ..." % file_path)
            tags = tag_finder(file_path)
            if tags == {}:
                logging.debug("No tags received, must be a system file")
                continue
            try:
                logging.debug("Executing index_picker() method")
                result = self.index_picker(self.dic, filled_slots=filled_slots,
                                           letter=result['letter'], number=result['number'])
            except KeyError:
                logging.warning("Letter and number are not defined, if you see this often, there might be a problem")
                result = self.index_picker(self.dic, filled_slots=filled_slots)

            from_path = self.get_from_path(import_path, file_path)
            to_path = self.get_to_path(export_path, result['index'],
                                       slugify(tags['title'], separator=" "),
                                       slugify(tags['artist'], separator=" "),
                                       tags['extension'])
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
    def get_to_path(export_path, index, title, artist, extension):
        #TODO
        """

        """
        return Player.format_path(export_path) + u"/" + index + u"-" + \
               Player.format_file_name(title) + u"-" + \
               Player.format_file_name(artist) + u"." + extension
    
    @staticmethod
    def get_from_path(import_path, file_path):
        #TODO
        """

        """
        return Player.format_path(import_path) + u"/" + Player.format_path(file_path) + u" "
    
    @staticmethod
    def get_absolute_path(path):
        #TODO
        """

        """
        return os.path.join(os.path.dirname(__file__), path)

    @staticmethod
    def format_file_name(path):
        #TODO
        """

        """
        return Player.format_path(path).replace("/", "\ ")

    @staticmethod
    def format_path(path):
        #TODO
        """

        """
        return path.replace(" ", "\ ").replace("'", "\\'").replace("&", "\\&").replace("(", "\(").replace(")", "\)")

    @staticmethod
    def index_picker(dic, filled_slots, letter=1, number=1):
        #TODO
        """

        """
        logging.debug("index_picker() method started with letter:%s and number %s" % (letter, number))
        while filled_slots[letter-1][number-1]:
            number += 1
            if number == 21 and letter < 4:
                number = 1
                letter += 1
            if letter == 5:
                logging.warning("Library is full: empty it ! skipping...")
        index = dic[letter]+str(number)
        filled_slots[letter-1][number-1] = True
        logging.debug("index_picker() method returns index: %s letter %s number %s" % (index, letter, number))
        return {"index": index, "filled_slots": filled_slots, "letter": letter, "number": number}