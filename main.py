from __future__ import unicode_literals
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config import Config
import logging
from jukebox import Jukebox
CONF = Config()
logging.basicConfig(filename="/var/log/jukebox.log", format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)


jukebox = Jukebox(CONF)
