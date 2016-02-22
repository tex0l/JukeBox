from __future__ import unicode_literals

import logging
import socket
from threading import Lock, Thread, Event
import time
from mpd import MPDClient, ConnectionError


class LockableMPDClient(MPDClient):
    """
    A subclass of MPDClient to make it thread-safe
    """
    def __init__(self, use_unicode=False):
        # TODO: Is the use_unicode kwarg useful ? If yes, explain...
        super(LockableMPDClient, self).__init__(use_unicode=use_unicode)
        self._lock = Lock()

    def acquire(self):
        self._lock.acquire()

    def release(self):
        self._lock.release()

    def __enter__(self):
        self.acquire()

    def __exit__(self, type, value, traceback):
        self.release()


class MPDHandler(Thread):
    """
    A thread to safely communicate with the mpd client
    """
    # TODO: It'd probably be smart to split this class in two blocks -> a private block, and a public block...
    def __init__(self, loaded_config):
        Thread.__init__(self, name="MPDHandler")

        # TODO: Refactor loaded_config into a kwarg, and handle a default value which would work most of the time
        self.loaded_config = loaded_config

        # TODO: Find why the logs and tracebacks of MPDHandler are not always written and when they are why it's messy
        self.logger = logging.getLogger('mpd')

        self._client = LockableMPDClient(use_unicode=True)

        # TODO: What are those timeouts ?
        self._client.timeout = None
        self._client.idletimeout = None

        # TODO: Is it necessary to set this flag ??? When is it modified ???
        self.is_idle = False

        # TODO: Is it really an 'unknown' state here, isn't it an 'initialization' state ? :)
        self.status = {'state': 'unknown'}

        # This is the song/music currently being played
        self.current_song = {}

        # This is the current playlist of musics already added to MPD
        self.playlist = []

        # This is the queue of musics waiting to be added to MPD
        self.queue = []

        # TODO: Explain those three events !
        self._update_or_not = Event()
        self._clear_or_not = Event()
        self._next_or_not = Event()

        # TODO: Why define an 'mpd' logger and not use it... ?
        logging.info("Connecting to MPD")

        # TODO: Timestamp of the last addition of a music to the queue/playlist ?
        # I can't find where it is actually used...
        self.last_added = time.time()

        # Kill flag
        self._stop = Event()

    # TODO: Refactor all those try/except which are quite ugly. Are they useful ? If yes -> use a decorator !!!
    # TODO: Why are there some functions that contain a return void, and some without a return at all ?
    def _connect(self):
        try:
            with self._client:
                self._client.connect(self.loaded_config.network['mpd_host'], self.loaded_config.network['mpd_port'])
            return
        except socket.error, ConnectionError:
            self._connect()

    def _fetch_status(self):
        try:
            with self._client:
                return self._client.status()
        except socket.error:
            return self._fetch_status()
        except ConnectionError:
            self._connect()
            return self._fetch_status()

    def _fetch_current_song(self):
        try:
            with self._client:
                return self._client.currentsong()
        except socket.error:
            return self._fetch_current_song()
        except ConnectionError:
            self._connect()
            return self._fetch_current_song()

    def _fetch_playlist(self):
        try:
            with self._client:
                playlist = self._client.playlist()
                return playlist
        except socket.error:
            return self._fetch_playlist()
        except ConnectionError:
            self._connect()
            return self._fetch_playlist()

    def _update(self):
        try:
            with self._client:
                self._client.update()
                self._update_or_not.clear()
        except socket.error:
            self._update()
        except ConnectionError:
            self._connect()
            self._update()

    def _enqueue(self, music):
        try:
            with self._client:
                # noinspection PyUnresolvedReferences
                self.logger.debug("Adding %s to playlist" % music.title)
                self.logger.info("path : %s" % music.path)
                self._client.add(music.path)
                # noinspection PyUnresolvedReferences
                self._client.play()
                return
        except socket.error:
            return self._enqueue(music)
        except ConnectionError:
            self._connect()
            return self._enqueue(music)

    def _clear(self):
        try:
            with self._client:
                self._client.clear()
                self._clear_or_not.clear()
        except socket.error:
            self._clear()
        except ConnectionError:
            self._connect()
            self._clear()

    def _next(self):
        try:
            with self._client:
                self._client.next()
                self._next_or_not.clear()
        except socket.error:
            self._clear()
        except ConnectionError:
            self._connect()
            self._clear()

    # Handler core
    def run(self):
        self._connect()

        with self._client:
            # noinspection PyUnresolvedReferences
            self._client.consume(1)
            # noinspection PyUnresolvedReferences
            self._client.crossfade(1)
        while not self._stop.isSet():
            if self._update_or_not.isSet():
                self._update()

            if self._clear_or_not.isSet():
                self._clear()

            length = len(self.queue)
            # TODO: Is it possible to add them in the *right order* without defining an iterated variable ?
            for i in range(0, length):
                self._enqueue(self.queue[0])
                self.queue.pop(0)
            self.status = self._fetch_status()
            self.current_song = self._fetch_current_song()
            self.playlist = self._fetch_playlist()

            if self._next_or_not.isSet():
                self._next()

            time.sleep(1)
# Control methods :

    def next(self):
        self._next_or_not.set()

    def clear(self):
        self._clear_or_not.set()
        self.queue = []
        self.playlist = []

    def update(self):
        self._update_or_not.set()

    def enqueue(self, music):
        self.logger.debug("Adding %s to queue" % music.title)
        self.queue.append(music)

    def get_current_song(self):
        return self.current_song

    def get_status(self):
        return self.status

    def get_queue_count(self):
        return len(self.playlist)+len(self.queue)

    def exit(self):
        self._stop.set()
