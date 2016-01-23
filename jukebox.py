from __future__ import unicode_literals
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from core import getch
import keyboard_map
import library
import music_player
import time
import logging
from core.displays.display import DisplayChooser
from unidecode import unidecode


class Jukebox:
    """
    Implements the Jukebox class aka "the core"
    It links the user interface with the rest of the program
    """

    def __init__(self, conf):
        """
        Initializes the jukebox:
        First it retrieves the dictionary,
        Then it initializes the music_player.Player, the display and the library.Library,

        :param conf: the given config from main
        :type conf: config.Config
        """
        logging.info("Initializing dictionary")
        self.dictionary = keyboard_map.Map(conf)
        logging.info("Initializing player")
        self.player = music_player.Player(conf)
        logging.info("Initializing display")
        self.display = DisplayChooser(conf).display
        logging.info("Initializing library")
        self.music_index = library.Library(conf.paths["json_conf_file"])
        self.print_help()
        self.main(conf)

    def exit(self):
        logging.debug("Waiting for the end of the display thread update")
        self.display.UT.join()  # Waits until UpdateThread() thread dies
        logging.debug("Exiting the player")
        self.player.exit()
        # display.display.RT.join()
        print ("Goodbye !")
        logging.info("Exiting program")
        exit()

    def list(self):
        print ("List of songs :")
        print self.music_index.__str__()

    def main(self, conf):
        """
        main method() is the loop of the user interface

        :param conf: the given configuration
        :type conf: config.Config
        """
        entry = ""
        while 1:
            entry = self.switch_man(conf, entry)

    def switch_man(self, conf, entry):
        """
        The switch_man() method is the user interface
        It asks the choice then it processes it to the dictionary and the as it follows:
        If it is "quit", then it exits the program           # Those two functions are allowed only
        If it is "list", the it prints the lis of the musics # with another keyboard than the 24 keys
        Else it returns the result given by self.music_picker(entry) method:
        It is the precedent choice, if you've chosen a letter
        Hence, entry equals choice in all cases except when you've picked a letter on the last round,
        Then it will equals this letter concatenated with the current choice when you pick a number

        :param conf: the configuration given
        :type conf: config.Config

        :param entry: it's the choice of music, it's either an empty string, a letter or a letter and a number
        :type entry: unicode

        :rtype: unicode
        """
        logging.debug("Entering switch_man()")
        sys.stdout.write(str("Enter your choice : "))
        sys.stdout.flush()
        choice = getch.getch()
        logging.debug(unidecode("Got choice %s through getch") % choice)
        logging.debug("Mapping choice throughout the dictionary")
        choice = self.dictionary.find(choice)
        if choice == 'quit':
            self.exit()
        elif choice == 'list':
            self.list()
            return ''
        elif choice == 'E99':
            self.player.clear()
            return self.music_picker(conf, choice[1:], choice[:1])
        elif choice == 'next':
            self.player.next()
        elif choice == '':
            print("Invalid Entry")
            logging.debug("Invalid entry")
            return ''
        else:
            return self.music_picker(conf, choice, entry)

    def is_letter_updater(self, string):
        """
        Returns the string if it's a letter, and sends it to the screen
        Else it returns ""

        :param string: the entry to be checked and/or updated
        :type string: unicode

        :rtype: unicode
        """
        if (str(string)).isalpha():
            entry = string.upper()
            self.display.entry(entry + "_")
            return entry
        return ""

    def add_song(self, song, entry):
        """
        Adds a song to the jukebox queue, and displays the corresponding info on the screen

        :param song: the song the add to the queue
        :type song: library.Music

        :param entry: the entry to be updated on the screen
        :type entry: unicode
        """
        print("Song chosen : " + song.artist + "'s " + song.title)
        logging.debug("Song %s picked from entry %s" % (song.title, entry))
        # ajout a la playlist
        self.player.enqueue(song)
        queue_count = self.player.queue_count()
        print("Songs queued :" + str(queue_count))
        self.display.entry(entry, song)
        self.display.set_queue(queue_count)

    def is_digit_updater(self, choice, entry):
        """
        Tests if the choice is a number,
        Then tries to find the song,
        If found, it plays it, updates the screen
        It returns "" as an entry anyway

        :param choice: the second half of the entry, might be a letter
        :type choice: int or unicode

        :param entry: the entry to be updated on the screen
        :type entry: unicode

        :rtype: unicode
        """

        old_entry = entry
        if (str(choice)).isdigit():
            entry += choice
            index = library.Index(entry[:1], int(entry[1:]))
            song = self.music_index.find_index(index)
            logging.debug(song)
            if song:
                self.add_song(song, entry)
                logging.debug("is_digit_updater(%s,%s) returns " % (choice, old_entry))
                return ''
            logging.info("No song found for entry %s" % entry)
            logging.debug("is_digit_updater(%s,%s) returns " % (choice, old_entry))
            return ""
        logging.debug("is_digit_updater(%s,%s) returns is_letter_updater(''+%s)" % (choice,
                                                                                    old_entry,
                                                                                    choice))
        return self.is_letter_updater("" + choice)

    def music_picker(self, conf, choice, entry):
        """
        The music_picker() method is the main part to processing the entry the user
        It implements the waiting condition : if the queue length > nb_music and if you added a song
        less than timeout secs, then you'll have to wait the remaining time and type a key again
        Then only,
        If you haven't picked a letter the last round,
        Then it processes the choice throughout is_letter_updater() method and returns the result,
        If it fails, it raises an "Invalid input" error,
        Else it processes the choice throughout is_digit_updater()  method and returns the result.

        :param conf: the configuration given
        :type conf: config.Config

        :param choice: the second half of the entry, might be a letter
        :type choice: int or unicode

        :param entry: the entry to be updated on the screen
        :type entry: unicode
        """

        time_elapsed = time.time() - self.player.last_added

        if self.player.queue_count() < conf.variables['nb_music'] \
                or time_elapsed > conf.variables['add_timeout']:
            # If we didn't already choose a letter
            if entry == "":
                result = self.is_letter_updater(choice)
                if result == "":
                    logging.info("Invalid input")
                logging.debug("music_picker(loaded_config,%s,%s) returns %s" % (choice,
                                                                                entry,
                                                                                result))
                return result
            else:
                result = self.is_digit_updater(choice, entry)
                logging.debug("music_picker(loaded_config,%s,%s) returns %s" % (choice,
                                                                                entry,
                                                                                result))
                return result
        else:
            remaining_time = conf.variables['add_timeout'] - time_elapsed
            logging.info("Waiting for timeout, still %s secs to wait" % remaining_time)
        return ''

    @staticmethod
    def print_help():
        """
        Just some distracting letters
        """
        print (30 * '-')
        print ("      j u k e b o X  2.0")
        print (30 * '-')
        print ("A-D + 1-20. Select Song")
        print ("Q. Quit")
        print ("L. List songs")
        print (30 * '-')
