from __future__ import unicode_literals
# !/usr/bin/env python
# -*- coding: utf-8 -*-

from mpd import MPDClient, ConnectionError, CommandError
import os
import time
import logging
from tags import tag_finder
# noinspection PyPackageRequirements
from slugify import slugify
import socket
from threading import Lock, Thread, Event


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyShadowingBuiltins
class LockableMPDClient(MPDClient):
    def __init__(self, use_unicode=False):
        super(LockableMPDClient, self).__init__()
        self.use_unicode = use_unicode
        self._lock = Lock()

    def acquire(self):
        self._lock.acquire()

    def release(self):
        self._lock.release()

    def __enter__(self):
        self.acquire()

    def __exit__(self, type, value, traceback):
        self.release()


class MPDHandler(Thread):
    def __init__(self, loaded_config):
        Thread.__init__(self)

        self.loaded_config = loaded_config
        self.logger = logging.getLogger('mpd')
        self.client = LockableMPDClient(use_unicode=True)
        self.client.timeout = None
        self.client.idleTimeout = 1

        self.is_idle = False
        self.status = {'state': 'unknown'}
        self.current_song = {}
        self.playlist = []
        self.queue = []
        logging.info("Connecting to MPD")

        self.last_added = time.time()
        self._stop = Event()

    def __connect(self):
        with self.client:
            self.client.connect(self.loaded_config.network['mpd_host'], self.loaded_config.network['mpd_port'])
            return

    def exit(self):
        self._stop.set()

    def __fetch_status(self):
        try:
            with self.client:
                return self.client.status()
        except socket.error:
            return self.__fetch_status()
        except ConnectionError:
            self.__connect()
            return self.__fetch_status()


    def __fetch_current_song(self):
        try:
            with self.client:
                return self.client.currentsong()
        except socket.error:
            return self.__fetch_current_song()
        except ConnectionError:
            self.__connect()
            return self.__fetch_current_song()

    def __fetch_playlist(self):
        try:
            with self.client:
                return self.client.playlist()
        except socket.error:
            return self.__fetch_playlist()
        except ConnectionError:
            self.__connect()
            return self.__fetch_playlist()

    def __enqueue(self, music):
        try:
            with self.client:
                # noinspection PyUnresolvedReferences
                self.logger.debug("Adding %s to playlist" % music.name)
                self.client.add(music.path)
                # noinspection PyUnresolvedReferences
                self.client.play()
                return
        except socket.error:
            return self.__enqueue(music)
        except ConnectionError:
            self.__connect()
            return self.__enqueue(music)



    # Handler core
    def run(self):
        self.__connect()

        with self.client:
            # noinspection PyUnresolvedReferences
            self.client.consume(1)
            # noinspection PyUnresolvedReferences
            self.client.crossfade(1)
        while not self._stop.isSet():
            length = len(self.queue)
            for i in range(0, length):
                self.__enqueue(self.queue[i])
                self.queue.pop(i)
            self.status = self.__fetch_status()
            self.current_song = self.__fetch_current_song()
            self.playlist = self.__fetch_playlist()
            time.sleep(1)


    # Control methods :
    def update(self):
        with self.client:
            self.client.update()
            return

    def enqueue(self, music):
        self.logger.debug("Adding %s to queue" % music.name)
        self.queue.append(music)

    def get_current_song(self):
        return self.current_song

    def get_status(self):
        return self.status

    def get_playlist(self):
        return self.playlist


class Player():
    # TODO
    """

    """

    def __init__(self, loaded_config):
        #TODO
        """

        """
        logging.info("Killing MPD")
        os.system("killall mpd")
        command = unicode("mpd %s" % loaded_config.paths['mpd_conf_file'])
        #lancement de mpd
        logging.info("Starting MPD")
        os.system(command)
        self.mpd_handler = MPDHandler(loaded_config)
        self.mpd_handler.setDaemon(True)
        self.mpd_handler.start()
        self.mpd_handler.join(1)
        self.dic = dict([(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D')])
        self.last_added = time.time()

    def update(self):
        logging.info("Updating the library")
        return self.mpd_handler.update()

    def enqueue(self, music):
        logging.info("Enqueueing %s to playlist" % music.name)
        self.mpd_handler.enqueue(music)
        self.last_added = time.time()

    def is_playing(self):
        return self.mpd_handler.status['state'] == 'play'

    def title(self):
        return self.mpd_handler.current_song['title']


    def artist(self):
        return self.mpd_handler.current_song['artist']

    def number(self):
        return self.mpd_handler.current_song['file'].split("-")[0]

    def queue_count(self):
        return len(self.mpd_handler.playlist)

    def exit(self):
        logging.info("Disconnecting client")
        self.mpd_handler.exit()
        logging.info('Killing MPD')
        os.system("killall mpd")

    def generate_library(self, extraction_path, final_path, filled_slots=None):
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
            # noinspection PyBroadException
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
        return Player.format_path(export_path) + u"/" + index + u"-" + \
               Player.format_file_name(title) + u"-" + \
               Player.format_file_name(artist) + u"." + extension

    @staticmethod
    def get_from_path(import_path, file_path):
        return Player.format_path(import_path) + u"/" + Player.format_path(file_path) + u" "

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
        #TODO
        """

        """
        logging.debug("index_picker() method started with letter:%s and number %s" % (letter, number))
        while filled_slots[letter - 1][number - 1]:
            number += 1
            if number == 21 and letter < 4:
                number = 1
                letter += 1
            if letter == 5:
                logging.warning("Library is full: empty it ! skipping...")
        index = dic[letter] + str(number)
        filled_slots[letter - 1][number - 1] = True
        logging.debug("index_picker() method returns index: %s letter %s number %s" % (index, letter, number))
        return {"index": index, "filled_slots": filled_slots, "letter": letter, "number": number}