from __future__ import unicode_literals
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import logging
from core.mpdHandler import MPDHandler
import subprocess


class Player:
    thread = None

    def __init__(self, loaded_config=None):
        if not Player.thread:
            Player.killMPD()
            Player.startMPD(loaded_config)

            self.mpd_handler = MPDHandler(loaded_config)
            self.mpd_handler.start()
            Player.thread = self.mpd_handler
        else:
            self.mpd_handler = Player.thread

        self.dic = dict([(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D')])
        self.last_added = time.time()

    @staticmethod
    def killMPD():
        logging.info("Killing MPD")
        subprocess.call(('killall', 'mpd'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    @staticmethod
    def startMPD(loaded_config):
        command = ("mpd", unicode(loaded_config.paths['mpd_conf_file']))
        logging.info("Starting MPD")
        subprocess.call(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
