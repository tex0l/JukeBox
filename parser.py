from __future__ import unicode_literals
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import os
from tags import tag_finder
import logging


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
        #TODO
        """

        """
        self.path = os.path.join(os.path.dirname(__file__), path)
        os.chdir(self.path)
        files = glob.glob("*")
        # Music objects list
        self.music = []
        # Music index list (A12, B1, ...)
        self.index = []
        for music_file in files:
            # noinspection PyBroadException
            try:
                self.music.append(Music(music_file))
                l = len(self.music)
                self.index.append(self.music[l - 1].number)
            except:
                logging.warning(music_file + " is incorrectly named. Try updating the database")


    def print_music_dir(self):
        #TODO
        """

        """
        for music in self.music:
            music.print_music()
        return

    def find_number(self, index):
        #TODO
        """
        Returns the Music corresponding to the index
        """
        l = len(self.index)

        for i in range(0, l):
            if self.index[i] == index:
                return self.music[i]

        return ""

    def filled_slots(self):
        #TODO
        """

        """

        dic = dict([(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D')])
        result = [[], [], [], []]
        letter = 1
        while letter <= 4:
            number = 0
            while number < 20:
                number += 1
                if self.find_number(dic[letter] + str(number)) != "":
                    # noinspection PyTypeChecker
                    result[letter - 1].append(True)
                else:
                    # noinspection PyTypeChecker
                    result[letter - 1].append(False)
            letter += 1
        return result


class Music:
    #TODO
    """

    """

    def __init__(self, path):
        #TODO
        """

        """
        #file named : CODE-Name-Artist.format
        self.path = path
        self.file_name = path_leaf(self.path)
        self.number, self.artist, self.name, self.format = self.find_tags()


    def find_tags(self):
        #TODO
        """

        """
        logging.debug("Executing tag_finder() method")
        tags = tag_finder(self.path)
        #Audio file mode
        #index
        index = self.file_name.split("-")[0]
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
        print self.number + " - " + self.name + " - " + self.artist + " - " + self.format

    def display(self):
        #TODO
        """

        """
        return "%s : %s by %s" % (self.number, self.name, self.artist)
