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

class InvalidInputException(Exception):
        pass

class Jukebox:
    def __init__(self, CONF):
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
            input = nonBlockingRawInput("To update music directory, type 'y' or 'yes', %s secs then skipped \n" %
                                   CONF.variables['index_timeout'], timeout=CONF.variables['index_timeout'])
            if input == "y" or input == "yes":
                self.generate(CONF)
        self.print_help()
        self.main(CONF)

    def generate(self, CONF):
        logging.info("Parsing import directory")
        self.player.generate_library(CONF.paths['index_dir'], CONF.paths['music_dir'], self.music_index.filled_slots())
        logging.info("Updating music library")
        self.music_index = parser.MusicDir(CONF.paths['music_dir'])

    def main(self, CONF, entry=""):
        sys.stdout.write('Enter your choice : ')
        sys.stdout.flush()
        # Recuperation de la frappe clavier
        choice = getch.getch()
        # Conversion avec le dictionnaire
        choice = self.dictionnary.find(choice)
        if choice == 'quit':
            self.display.UT.join() #Attend que le thread d'update du display soit termine
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
            self.main(CONF, entry=self.music_picker(CONF, choice, entry))

    def is_letter_updater(self, choice):
        if (str(choice)).isalpha():
            entry = choice.upper()
            self.display.entry(entry+"_")
            return entry
        else:
            raise InvalidInputException("Invalid input")

    def is_digit_updater(self, choice, entry):
        if (str(choice)).isdigit():
            old_entry = entry
            entry += choice
            song = self.music_index.findnumber(entry)
            #non trouvee
            if song == "":
                print("This song does not exist")
            #trouvee
            else:
                print("Song chosen : " + song.artist+"'s "+song.name)
                #ajout a la playlist
                self.player.enqueue(song)
                print("songs queued :" + str(self.player.queue_count()))
                self.display.entry(entry, song)
                self.display.setQueue(self.player.queue_count())
            return ""
        return self.is_letter_updater(""+choice)

    def music_picker(self, CONF, choice, entry):
        if self.player.queue_count() < CONF.variables['nb_music'] \
                or time.time()-self.player.last_added > CONF.variables['add_timeout']:
            # Si on n'a pas deja choisi une lettre
            if entry == "":
                try:
                    return self.is_letter_updater(choice)
                except InvalidInputException as e:
                    print e.message
                    return ""
            else:
                return self.is_digit_updater(choice, entry)
        else:
            print("Wait !")
    @staticmethod
    def print_help():
        print (30 * '-')
        print ("   j u k e b o X")
        print (30 * '-')
        print ("A-D + 1-20. Select Song")
        print ("Q. Quit")
        print ("L. List songs")
        print (30 * '-')