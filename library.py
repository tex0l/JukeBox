from __future__ import unicode_literals
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
import json


def path_leaf(path):
    """
    It gets the path final leaf
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
            'title':'titre de la musique A1',
            'artist': 'artiste de la musique A1',
            'path': 'chemin du fichier correspondant a la musique A1'
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
        self.library = self.raw_library.clean()

    def read(self):
        with open(self.json_file, 'r') as f:
            return json.load(f)

    def write(self, dict):
        with open(self.json_file, 'w') as f:
            json.dump(dict, f)

    def clean(self):
        """
        clean() method takes the json, parses it and put its elements in suitable objects
        """
        letters = ['A', 'B', 'C', 'D']
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11',
                       '12', '13', '14', '15', '16', '17', '18', '19', '20']
        result = {}
        for letter in letters:
            for number in numbers:
                index = Index(letter,number)
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
        Returns the Music corresponding to the index
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
        self.file_name = path_leaf(self.path) # TODO: useful ?
        self.index = index
        self.title = title
        self.artist = artist

    def __str__(self):
        return self.index.__str__() + "  - " + self.title + " - " + self.artist + " - " + self.file_name

    def __repr__(self):
        return self.__str__()

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
