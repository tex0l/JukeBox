from __future__ import unicode_literals
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import Config
from logger import Logger
from jukebox import Jukebox
import logging
CONF = Config()
logger = Logger(format=CONF.log['format'],
                path=CONF.log['path'],
                level=CONF.log['level']).root_logger


def main(CONF):
    Jukebox(CONF)

if __name__ == '__main__':
    logging.warning("Starting...")
    main(CONF)