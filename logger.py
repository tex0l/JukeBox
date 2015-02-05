from __future__ import unicode_literals
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

class Logger:
    def __init__(self, format, path, level):
        self.log_formatter = logging.Formatter(format)
        self.root_logger = logging.getLogger()
        self.root_logger.setLevel(level)
        self.file_handler = logging.FileHandler(path)
        self.file_handler.setFormatter(self.log_formatter)
        self.root_logger.addHandler(self.file_handler)

        self.console_handler = logging.StreamHandler()
        self.console_handler.setFormatter(self.log_formatter)
        self.root_logger.addHandler(self.console_handler)