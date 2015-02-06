from __future__ import unicode_literals
# !/usr/bin/env python
# -*- coding: utf-8 -*-

from config import Config
from logger import Logger
from jukebox import Jukebox
import logging

loaded_config = Config()
# Initialilizing the logger with the correct settings
logger = Logger(log_format=loaded_config.log['format'],
                path=loaded_config.log['path'],
                level=loaded_config.log['level']).root_logger


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
    main(loaded_config)