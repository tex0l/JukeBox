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
import subprocess

# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyShadowingBuiltins
class LockableMPDClient(MPDClient):
    """
    A subclass of MPDClient to make it thread-safe
    """
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
    """
    A thread to safely communicate with the mpd client
    """
    #Private functions that actually communicate with the client
    def __init__(self, loaded_config):
        Thread.__init__(self,name="MPDHandler")

        self.loaded_config = loaded_config
        self.logger = logging.getLogger('mpd')
        self._client = LockableMPDClient(use_unicode=True)
        self._client.timeout = None
        self._client.idletimeout = None

        self.is_idle = False
        self.status = {'state': 'unknown'}
        self.current_song = {}
        self.playlist = []
        self.queue = []
        self._update_or_not = Event()
        self._clear_or_not = Event()
        self._next_or_not = Event()
        logging.info("Connecting to MPD")

        self.last_added = time.time()
        self._stop = Event()

    def _connect(self):
        try:
            with self._client:
                self._client.connect(self.loaded_config.network['mpd_host'], self.loaded_config.network['mpd_port'])
            return
        except socket.error, ConnectionError:
            self._connect()

    def _fetch_status(self):
        try:
            with self._client:
                return self._client.status()
        except socket.error:
            return self._fetch_status()
        except ConnectionError:
            self._connect()
            return self._fetch_status()

    def _fetch_current_song(self):
        try:
            with self._client:
                return self._client.currentsong()
        except socket.error:
            return self._fetch_current_song()
        except ConnectionError:
            self._connect()
            return self._fetch_current_song()

    def _fetch_playlist(self):
        try:
            with self._client:
                playlist = self._client.playlist()
                return playlist
        except socket.error:
            return self._fetch_playlist()
        except ConnectionError:
            self._connect()
            return self._fetch_playlist()

    def _update(self):
        try:
            with self._client:
                self._client.update()
                self._update_or_not.clear()
        except socket.error:
            self._update()
        except ConnectionError:
            self._connect()
            self._update()

    def _enqueue(self, music):
        try:
            with self._client:
                # noinspection PyUnresolvedReferences
                self.logger.debug("Adding %s to playlist" % music.name)
                self._client.add(music.path)
                # noinspection PyUnresolvedReferences
                self._client.play()
                return
        except socket.error:
            return self._enqueue(music)
        except ConnectionError:
            self._connect()
            return self._enqueue(music)

    def _clear(self):
        try:
            with self._client:
                self._client.clear()
                self._clear_or_not.clear()
        except socket.error:
            self._clear()
        except ConnectionError:
            self._connect()
            self._clear()

    def _next(self):
        try:
            with self._client:
                self._client.next()
                self._next_or_not.clear()
        except socket.error:
            self._clear()
        except ConnectionError:
            self._connect()
            self._clear()

    # Handler core
    def run(self):
        self._connect()

        with self._client:
            # noinspection PyUnresolvedReferences
            self._client.consume(1)
            # noinspection PyUnresolvedReferences
            self._client.crossfade(1)
        while not self._stop.isSet():
            if self._update_or_not.isSet():
                self._update()

            if self._clear_or_not.isSet():
                self._clear()

            if self._next_or_not.isSet():
                self._next()

            length = len(self.queue)
            for i in range(0, length):
                self._enqueue(self.queue[0])
                self.queue.pop(0)
            self.status = self._fetch_status()
            self.current_song = self._fetch_current_song()
            self.playlist = self._fetch_playlist()
            time.sleep(1)
# Control methods :

    def next(self):
        self._next_or_not.set()

    def clear(self):
        self._clear_or_not.set()

    def update(self):
        self._update_or_not.set()

    def enqueue(self, music):
        self.logger.debug("Adding %s to queue" % music.name)
        self.queue.append(music)

    def get_current_song(self):
        return self.current_song

    def get_status(self):
        return self.status

    def get_queue_count(self):
        return len(self.playlist)+len(self.queue)

    def exit(self):
        self._stop.set()


class Player():
    # TODO
    """

    """
    thread = None
    def __init__(self, loaded_config=None):
        #TODO
        """

        """
        if not Player.thread:
            logging.info("Killing MPD")
            subprocess.call(('killall', 'mpd'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            command = ("mpd", unicode(loaded_config.paths['mpd_conf_file']))
            #lancement de mpd
            logging.info("Starting MPD")
            subprocess.call(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.mpd_handler = MPDHandler(loaded_config)
            self.mpd_handler.start()
            self.mpd_handler.join(1)
            Player.thread = self.mpd_handler
        else:
            self.mpd_handler = Player.thread
        self.dic = dict([(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D')])
        self.last_added = time.time()

    def update(self):
        logging.info("Updating the library")
        return self.mpd_handler.update()

    def enqueue(self, music):
        logging.info("Enqueueing %s" % music.index.__str__())
        self.mpd_handler.enqueue(music)
        self.last_added = time.time()

    def is_playing(self):
        return self.mpd_handler.status['state'] == 'play'

    def title(self):
        return self.mpd_handler.get_current_song()['title']


    def artist(self):
        return self.mpd_handler.get_current_song()['artist']

    def index(self):
        index = self.mpd_handler.get_current_song()['file'].split("-")[0]
        return [index[:1], index[1:]]

    def queue_count(self):
        return self.mpd_handler.get_queue_count()

    def clear(self):
        self.mpd_handler.clear()

    def next(self):
        self.mpd_handler.next()

    def exit(self):
        logging.info("Disconnecting client")
        self.mpd_handler.exit()
        logging.info('Killing MPD')
        os.system("killall mpd")

    def generate_library(self, extraction_path, final_path, filled_slots=None):
        """
        An ugly method to import songs in Import directory into the Music directory and name them correctly.
        """
        if not filled_slots:
            filled_slots = []
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
        """
        Picks a free slot
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