import os
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import threading
import library
from time import sleep


class PipeHandler (threading.Thread):
    def __init__(self, conf, music_index, player):
        threading.Thread.__init__(self)
        self.conf = conf
        self.music_index = music_index
        self.player = player


    def run(self):
        try :
            os.mkfifo(self.conf.paths["fifo_pipe_file"])
        except OSError as err :
            logging.debug('Cannot create pipe, probably already existing')

        pipein = open(self.conf.paths["fifo_pipe_file"], 'r')
        while True :
            line = pipein.readline()
            if line.__contains__('reload') :
                logging.info("Re-initializing library...\n")
                sleep(3)
                self.player.update()
                self.music_index.__init__(self.conf.paths["json_conf_file"])
                logging.info("done\n")

