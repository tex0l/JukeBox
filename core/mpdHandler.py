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
        super(LockableMPDClient, self).__init__()
        self.use_unicode = use_unicode
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
    #Private functions that actually communicate with the client
    def __init__(self, loaded_config):
        Thread.__init__(self,name="MPDHandler")

        self.loaded_config = loaded_config
        self.logger = logging.getLogger('mpd')
        self._client = LockableMPDClient(use_unicode=True)
        self._client.timeout = None
        self._client.idletimeout = None

        self.is_idle = False
        self.status = {'state': 'unknown'}
        self.current_song = {}
        self.playlist = []
        self.queue = []
        self._update_or_not = Event()
        self._clear_or_not = Event()
        self._next_or_not = Event()
        logging.info("Connecting to MPD")

        self.last_added = time.time()
        self._stop = Event()

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
                self.logger.debug("Adding %s to playlist" % music.name)
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
        self.logger.debug("Adding %s to queue" % music.name)
        self.queue.append(music)

    def get_current_song(self):
        return self.current_song

    def get_status(self):
        return self.status

    def get_queue_count(self):
        return len(self.playlist)+len(self.queue)

    def exit(self):
        self._stop.set()