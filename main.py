from __future__ import unicode_literals
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import Config
from logger import Logger
from jukebox import Jukebox
import logging

CONF = Config()
#Initialilizing the logger with the correct settings
logger = Logger(format=CONF.log['format'],
                path=CONF.log['path'],
                level=CONF.log['level']).root_logger


def main(CONF):
    """
    This method main.main() initializes a jukebox.Jukebox class with CONF
    """
    Jukebox(CONF)

if __name__ == '__main__':
    #This function executes the following code if and
    #only if main.py is first started, not another file.
    logging.warning("Starting...")
    main(CONF)