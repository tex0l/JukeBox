from __future__ import unicode_literals
# !/usr/bin/env python
# -*- coding: utf-8 -*-

from config import Config
from logger import Logger
from jukebox import Jukebox
import logging
import sys

config = Config()
# Initializing the logger with the correct settings
logger = Logger(log_format=config.log['format'],
                path=config.log['path'],
                level=config.log['level']).root_logger


def main(loaded_config):
    """
    This method main.main() initializes a jukebox.Jukebox class with loaded_config
    """
    # You may toggle to True when debugging to avoid restarting loops
    debug = True
    try:
        Jukebox(loaded_config)
    except Exception as e:
        logger.critical("Jukebox has crashed with error %s restarting... " % e)
        if not debug:
            main(loaded_config)
        else:
            raise


if __name__ == '__main__':
    # This code executes the following if and only if main.py is first started, not another file.
    logging.warning("Starting...")
    if len(sys.argv) >= 2 and sys.argv[1] == 'dummy':
        config.lcd['type'] = 'dummy'
    main(config)