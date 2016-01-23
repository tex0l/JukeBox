from __future__ import unicode_literals
# !/usr/bin/env python
# -*- coding: utf-8 -*-

from config import Config
from logger import Logger
from jukebox import Jukebox
import logging
import sys

# TODO: import config with class inheritance
config = Config()

# TODO: reconfigure logger, it's crappy
logger = Logger(log_format=config.log['format'],
                path=config.log['path'],
                level=config.log['level']).root_logger


def main(conf):
    """
    This method main.main() initializes a jukebox.Jukebox class with loaded_config
    :param conf: the config object loaded at the beginning of main.py
    :type conf: Config
    """
    Jukebox(conf)


if __name__ == '__main__':
    # This code executes the following if and only if main.py is first started, not another file.
    logging.warning("Starting...")
    if len(sys.argv) >= 2 and sys.argv[1] == 'dummy':
        config.lcd['type'] = 'dummy'
    main(config)
