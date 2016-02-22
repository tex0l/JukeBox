from __future__ import unicode_literals
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os


class Logger:
    """
    This class is very simple and is of no use in the rest of the program except in main.py,
    when it's initialized.
    To log you must first import logging in the file.
    Then you log messages with debug(), info(), warning, error(), critical() methods
    The level is 10 for debug, ..., 50 for critical)

    """

    def __init__(self, log_format, path, level):
        """
        log_format is the wanted logging format
        path is the path of the log file
        level is the minimum required level for the logged messages,
        if less it's nor stored nor displayed
        """
        self.log_formatter = logging.Formatter(log_format)

        self.root_logger = logging.getLogger()
        self.mpd_logger = logging.getLogger('mpd')
        self.mpd_logger.propagate = False

        self.root_logger.setLevel(level)
        self.mpd_logger.setLevel(level)

        self.file_handler = logging.FileHandler(os.path.join(os.path.dirname(__file__), path), mode='a')
        self.file_handler.setFormatter(self.log_formatter)

        self.root_logger.addHandler(self.file_handler)
        self.mpd_logger.addHandler(self.file_handler)
