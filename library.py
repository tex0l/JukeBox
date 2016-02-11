from __future__ import unicode_literals
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
import json


def path_leaf(path):
    """
    Not so useful function
    :param path: path to split
    :type path: str

    :rtype: str
    """
    head, tail = os.path.split(path)
    return tail or os.path.basename(head)


class Library:
    """
    The Library class takes the output json of Django, reads it, and provides a find_index() method
    The json containing the library is organized as following :
    {'A':
        {'1':
            {
            'title':'title of the A1 song',
            'artist': 'artist of the A1 song',
            'path': 'path of the A1 song file'
            },
        '2':
        ...
        },
    'B':
        ...
    }
    """
    def __init__(self, json_file):
        self.json_file = json_file
        self.raw_library = self.read()
        self.library = self.clean()

    def read(self):
        """
        Reads the config
        :return: the config from disk
        :rtype: dict
        """
        with open(self.json_file, 'r') as f:
            return json.load(f)

    def write(self, conf):
        """
        Writes the config
        :param conf: the config to be written
        :type conf: dict
        """
        with open(self.json_file, 'w') as f:
            json.dump(conf, f)

    def clean(self):
        """
        clean() method takes the json, parses it and puts its elements in suitable objects

        :return: a usable library
        :rtype: dict
        """
        letters = ['A', 'B', 'C', 'D']
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11',
                   '12', '13', '14', '15', '16', '17', '18', '19', '20']
        result = {}
        for letter in letters:
            for number in numbers:
                index = Index(letter, number)
                try:
                    title = self.raw_library[letter][number]['title']
                    artist = self.raw_library[letter][number]['artist']
                    path = self.raw_library[letter][number]['path']
                    result[index] = Music(index, path, artist, title)
                except KeyError:
                    logging.error('Reading from file music at index %s failed' % index.__str__())
        return result

    def find_index(self, index):
        """
        :param index: the index of the music
        :type index: Index

        :return: the music corresponding to the index
        :rtype: Music
        """
        return self.library[index]

    def __str__(self):
        result = ""
        for music in self.library:
            result += music.__str__() + "\n"
        return result


class Music:

    def __init__(self, index, path, artist, title):
        self.path = path
        self.file_name = path_leaf(self.path)  # TODO: useful ?
        self.index = index
        self.title = title
        self.artist = artist

    def __str__(self):
        return self.index.__str__() + "  - " + self.title + " - " + self.artist + " - " + self.file_name

    def __repr__(self):
        return self.__str__()


class Index(object):
    def __init__(self, letter, number):
        self.letter = unicode(letter)
        self.number = int(number)

    def __str__(self):
        return self.letter + str(self.number)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (self.letter, self.number) == (other.letter, other.number)

    def __hash__(self):
        return hash((self.letter, self.number))
