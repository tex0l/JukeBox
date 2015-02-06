from __future__ import unicode_literals
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import getch
import keyboard_map
import parser
from raw_input_timout import nonBlockingRawInput
import music_player
import time
import logging
from display import DisplayChooser
import threading


class Jukebox:
    """
    Implements the Jukebox class aka "the core"
    It links the user interface with the rest of the program
    """

    def __init__(self, loaded_config):
        """
        Initializes the jukebox:
        First it retrieves the dictionnary,
        Then it initializes the player, the display and the library,
        And it asks if an import is necessary, and completes the library automatically,
        Finally it switches into using mode aka the "normal mode"
        """
        # initialisation du dictionnaire
        logging.info("Initializing dictionnary")
        self.dictionary = keyboard_map.Map()
        # initialisation du lecteur
        logging.info("Initializing player")
        self.player = music_player.Player(loaded_config)
        logging.info("Initializing display")
        self.display = DisplayChooser(self.player, loaded_config).display
        logging.info("Initializing library")
        self.music_index = parser.MusicDir(loaded_config.paths['music_dir'])
        if loaded_config.variables['index']:
            user_input = nonBlockingRawInput(
                "To update music directory from import directory\nType 'y' or 'yes', %s secs then skipped: " %
                loaded_config.variables['index_timeout'], timeout=loaded_config.variables['index_timeout'])
            if user_input == "y" or user_input == "yes":
                self.generate(loaded_config)
        self.print_help()
        self.main(loaded_config)

    def generate(self, loaded_config):
        """
        The generate() method first parses the import directory with Player().generatelibrary() method,
        Then it updates the library by totally overwriting it with the new one
        """
        logging.info("Parsing import directory")
        self.player.generate_library(loaded_config.paths['index_dir'], loaded_config.paths['music_dir'],
                                     self.music_index.filled_slots())
        logging.info("Updating music library")
        self.music_index = parser.MusicDir(loaded_config.paths['music_dir'])

    def exit(self):
        #TODO
        """

        """
        logging.debug("Waiting for the end of the display thread update")
        self.display.UT.join()  # Attend que le thread d'update du display soit termine
        logging.debug("Exiting the player")
        self.player.exit()
        # display.display.RT.join()
        print ("Goodbye !")
        logging.info("Exiting program")
        exit()

    def list(self):
        #TODO
        """

        """
        print ("List of songs :")
        self.music_index.printmusicdir()

    def main(self, loaded_config, entry=""):
        """
        The main() method is the user interface
        The argument entry is "" by default,
        It asks the choice then it processes it to the dictionary and the as it follows:
        If it is "quit", then it exits the program           # Those two functions are allowed only
        If it is "list", the it prints the lis of the musics # with another keyboard than the 24 keys
        Else it calls itself with the entry argument given by self.musicpicker() method:
        It is the precedent choice, if you've chosen a letter)
        Hence, entry equals choice in all cases except when you've picked a letter on the last round,
        Then it will equals this letter concatenated with the current choice when you pick a number
        """
        logging.debug("Entering main() loop (once) again")
        sys.stdout.write('Enter your choice : ')
        sys.stdout.flush()
        # Recuperation de la frappe clavier
        choice = getch.getch()
        logging.debug("Got choice %s through getch" % choice)
        # Conversion avec le dictionnaire
        logging.debug("Mapping choice throughout the dictionary")
        choice = self.dictionary.find(choice)
        if choice == 'quit':
            self.exit()
        elif choice == 'list':
            self.list()
            self.main(loaded_config)
        elif choice == '':
            print("Invalid Entry")
            logging.debug("Invalid entry")
            self.main(loaded_config)
        else:
            self.main(loaded_config, self.music_picker(loaded_config, choice, entry))

    def is_letter_updater(self, string):
        """
        Returns the string if it's a letter, and sends it to the screen
        Else it returns ""
        """
        if (str(string)).isalpha():
            entry = string.upper()
            self.display.entry(entry + "_")
            return entry
        return ""

    def add_song(self, song, entry):
        """
        Adds a song to the jukebox queue, and displays the corresponding info on the screen
        """
        print("Song chosen : " + song.artist + "'s " + song.name)
        logging.debug("Song %s picked from entry %s" % (song.name, entry))
        #ajout a la playlist
        self.player.enqueue(song)
        queue_count = self.player.queue_count()
        print("Songs queued :" + str(queue_count))
        self.display.entry(entry, song)
        self.display.setQueue(queue_count)

    def is_digit_updater(self, choice, entry):
        """
        Tests if the choice is a number,
        Then tries to find the song,
        If found, it plays it, updates the screen
        It returns "" as an entry anyway
        """

        old_entry = entry
        if (str(choice)).isdigit():
            entry += choice
            song = self.music_index.find_number(entry)
            if song != "":
                self.add_song(song, entry)
                logging.debug("is_digit_updater(%s,%s) returns " % (choice, old_entry))
                return ''
            print("This song does not exist")
            logging.debug("No song found for entry %s" % entry)
            logging.debug("is_digit_updater(%s,%s) returns " % (choice, old_entry))
            return ""
        logging.debug("is_digit_updater(%s,%s) returns is_letter_updater(''+%s)" % (choice,
                                                                                    old_entry,
                                                                                    choice))
        return self.is_letter_updater("" + choice)

    def music_picker(self, loaded_config, choice, entry):
        """
        The music_picker() method is the main part to processing the entry the user
        It implements the waiting condition : if the queue length > nb_music and if you added a song
        less than timeout secs, then you'll have to wait the remaining time and type a key again
        Then only,
        If you haven't picked a letter the last round,
        Then it processes the choice throughout is_letter_updater() method and returns the result,
        If it fails, it raises an "Invalid input" error,
        Else it processes the choice throughout is_digit_updater()  method and returns the result.
        """

        time_elapsed = time.time() - self.player.last_added
        if self.player.queue_count() < loaded_config.variables['nb_music'] \
                or time_elapsed > loaded_config.variables['add_timeout']:
            # Si on n'a pas deja choisi une lettre
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
            remaining_time = loaded_config.variables['add_timeout'] - time_elapsed
            logging.debug("Waiting for timeout, still %s secs to wait" % remaining_time)

    @staticmethod
    def print_help():
        """
        Just some distracting letters
        """
        print (30 * '-')
        print ("   j u k e b o X")
        print (30 * '-')
        print ("A-D + 1-20. Select Song")
        print ("Q. Quit")
        print ("L. List songs")
        print (30 * '-')