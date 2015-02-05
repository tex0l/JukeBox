from __future__ import unicode_literals
#!/usr/bin/env python
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


class Jukebox:
    """
    Implements the Jukebox class aka "the core"
    It links the user interface with the rest of the program
    """
    def __init__(self, CONF):
        """
        Initializes the jukebox:
        First it retrieves the dictionnary,
        Then it initializes the player, the display and the library,
        And it asks if an import is necessary, and completes the library automatically,
        Finally it switches into using mode aka the "normal mode"
        """
        # initialisation du dictionnaire
        logging.info("Initializing dictionnary")
        self.dictionnary = keyboard_map.Map()
        # initialisation du lecteur
        logging.info("Initializing player")
        self.player = music_player.Player(CONF, launch=True)
        logging.info("Initializing display")
        self.display = DisplayChooser(CONF=CONF).display
        logging.info("Initializing library")
        self.music_index = parser.MusicDir(CONF.paths['music_dir'])
        if CONF.variables['index']:
            input = nonBlockingRawInput("To update music directory from import directory\nType 'y' or 'yes', %s secs then skipped: " %
                                   CONF.variables['index_timeout'], timeout=CONF.variables['index_timeout'])
            if input == "y" or input == "yes":
                self.generate(CONF)
        self.print_help()
        self.main(CONF)

    def generate(self, CONF):
        """
        The generate() method first parses the import directory with Player().generatelibrary() method,
        Then it updates the library by totally overwriting it with the new one
        """
        logging.info("Parsing import directory")
        self.player.generate_library(CONF.paths['index_dir'], CONF.paths['music_dir'], self.music_index.filled_slots())
        logging.info("Updating music library")
        self.music_index = parser.MusicDir(CONF.paths['music_dir'])

    def main(self, CONF, entry=""):
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

        sys.stdout.write('Enter your choice : ')
        sys.stdout.flush()
        # Recuperation de la frappe clavier
        choice = getch.getch()
        logging.debug("Got choice %s through getch" % choice)
        # Conversion avec le dictionnaire
        logging.debug("Mapping choice throughout the dictionary")
        choice = self.dictionnary.find(choice)
        if choice == 'quit':
            logging.debug("Waiting for the end of the display thread update")
            self.display.UT.join() #Attend que le thread d'update du display soit termine
            logging.debug("Exiting the player")
            self.player.exit()
            #display.display.RT.join()
            print ("Goodbye !")
            logging.info("Exiting program")
            exit()
        elif choice == 'list':
            print ("List of songs :")
            self.music_index.printmusicdir()
            self.main(CONF, entry)
        elif choice == '':
            print("Invalid Entry")
            self.main(CONF, entry=entry)
        else:
            logging.debug("Entering main() loop (once) again")
            self.main(CONF, self.music_picker(CONF, choice, entry))

    def is_letter_updater(self, string):
        """
        Returns the string if it's a letter, and sends it to the screen
        Else it returns ""
        """
        if (str(string)).isalpha():
            entry = string.upper()
            self.display.entry(entry+"_")
            return entry
        return ""

    def is_digit_updater(self, choice, entry):
        """
        Tests if the choice is a number,
        Then tries to find the song,
        If found, it plays it, updates the screen
        It returns "" as an entry anyway
        """
        if (str(choice)).isdigit():
            entry += choice
            song = self.music_index.findnumber(entry)
            if song != "":
                print("Song chosen : " + song.artist + "'s " + song.name)
                logging.debug("Song %s picked from entry %s" % (song.name, entry))
                #ajout a la playlist
                self.player.enqueue(song)
                print("songs queued :" + str(self.player.queue_count()))
                self.display.entry(entry, song)
                self.display.setQueue(self.player.queue_count())
                return ''
            print("This song does not exist")
            logging.debug("No song found for entry %s" % entry)
            return ""
        return self.is_letter_updater(""+choice)

    def music_picker(self, CONF, choice, entry):
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
        time_elapsed = time.time()-self.player.last_added
        if self.player.queue_count() < CONF.variables['nb_music'] \
            or time_elapsed > CONF.variables['add_timeout']:
                # Si on n'a pas deja choisi une lettre
                if entry == "":
                    result = self.is_letter_updater(choice)
                    if result == "":
                        logging.info("Invalid input")
                    logging.debug("music_picker returns %s" % result)

                    return result
                else:
                    logging.debug(entry)
                    return self.is_digit_updater(choice, entry)
        else:
            remaining_time = CONF.variables['add_timeout'] - time_elapsed
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