from __future__ import unicode_literals
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import os
from tags import tag_finder
import logging

from operator import itemgetter, attrgetter, methodcaller

def path_leaf(path):
    """
    It gets the path final leaf
    """
    head, tail = os.path.split(path)
    return tail or os.path.basename(head)


class MusicDir:
    """
    The MusicDir class indexes the Music directory and provides a
    find_number(index) method
    """

    def __init__(self, path):
        # TODO
        """

        """
        self.path = os.path.join(os.path.dirname(__file__), path)
        os.chdir(self.path)
        files = glob.glob("*")
        # Music objects list
        self.musics = []
        # Music index list (A12, B1, ...)
        self.indexes = []
        for music_file in files:
            # noinspection PyBroadException
            try:
                self.musics.append(Music(music_file))
                l = len(self.musics)
                self.indexes.append(self.musics[l - 1].index)
                logging.info("Successfully added %s to library" % music_file)
            except:
                logging.warning("Unable to load %s to library" % music_file)
        self._sort()

    def _sort(self):
        self.musics = sorted(self.musics, key=attrgetter('index.letter', 'index.number'))
        self.indexes = sorted(self.indexes, key=attrgetter('letter', 'number'))

    def print_music_dir(self):
        # TODO
        """

        """
        for music in self.musics:
            music.print_music()
        return

    def find_index(self, index):
        # TODO
        """
        Returns the Music corresponding to the index
        """
        l = len(self.musics)
        for i in range(0, l):
            condition = index.__eq__(self.musics[i].index)
            if condition:
                return self.musics[i]

        return None

    def filled_slots(self):
        # TODO
        """

        """

        dic = dict([(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D')])
        result = [[], [], [], []]
        letter = 1
        while letter <= 4:
            number = 0
            while number < 20:
                number += 1
                if self.find_index(Index(dic[letter], number)) != None:
                    # noinspection PyTypeChecker
                    result[letter - 1].append(True)
                else:
                    # noinspection PyTypeChecker
                    result[letter - 1].append(False)
            letter += 1
        return result


class Music:
    # TODO
    """

    """

    def __init__(self, path):
        #TODO
        """

        """
        #file named : CODE-Name-Artist.format
        self.path = path
        self.file_name = path_leaf(self.path)
        self.index, self.artist, self.name, self.format = self.find_tags()

    def __str__(self):
        return self.index.__str__() + "  - " + self.name + " - " + self.artist + " - "+ self.format

    def __repr__(self):
        return self.__str__()

    def find_tags(self):
        #TODO
        """

        """
        logging.debug("Executing tag_finder() method")
        tags = tag_finder(self.path)
        #Audio file mode
        #index
        index = self.file_name.split("-")[0]
        index = Index(index[:1], int(index[1:]))
        logging.debug(index)
        #artiste
        try:
            artist = tags['artist']
        except KeyError:
            artist = "unknown"
        #nom
        logging.debug("Artist:" + artist)
        try:
            name = tags['title']
        except KeyError:
            name = "unknown"
        #format
        logging.debug("Title:" + name)
        extension = self.file_name.split(".")[-1]
        return index, artist, name, extension

    def print_music(self):
        #TODO
        """

        """
        print self.index.__str__() + " - " + self.name + " - " + self.artist + " - " + self.format

    def display(self):
        #TODO
        """

        """
        return "%s%s : %s by %s" % (self.index, self.name, self.artist)


class Index(object):
    def __init__(self, letter, number):
        self.letter = letter
        self.number = number

    def __str__(self):
        return self.letter + unicode(self.number)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.letter == other.letter and self.number == other.number
