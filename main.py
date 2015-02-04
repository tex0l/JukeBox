from __future__ import unicode_literals
#!/usr/bin/python
# Version 2


import sys

import getch
import keyboard_map
import parser
from config import Config
from raw_input_timout import nonBlockingRawInput
import music_player
import time

CONF = Config()

from display import DisplayChooser


# initialisation du dictionnaire
print "Initializing dictionnary..."
dic = keyboard_map.Map()
# initialisation du lecteur
print "Initializing player..."
player = music_player.Player(CONF, launch=True)
print "Initializing display"
display = DisplayChooser(CONF=CONF).display
print "Initializing library"
music_index = parser.MusicDir(CONF.paths['music_dir'])
if CONF.variables['index']:
    generate = nonBlockingRawInput("To update music directory, type 'y' or 'yes', %s secs then skipped \n" %
                                   CONF.variables['index_timeout'], timeout=CONF.variables['index_timeout'])
    if generate == "y" or generate == "yes":
        #extraction_path = raw_input("Extract from ? : ")
        #final_path = config.MUSIC_DIR;
        print "Parsing import directory"
        player.generate_library(CONF.paths['index_dir'], CONF.paths['music_dir'], music_index.filled_slots())
        print "Updating music library"
        music_index = parser.MusicDir(CONF.paths['music_dir'])

print (30 * '-')
print ("   j u k e b o X")
print (30 * '-')
print ("A-D + 1-20. Select Song")
print ("Q. Quit")
print ("L. List songs")
print (30 * '-')
# choix de musique, est vide avant le choix d'une lettre A-D, puis est complete par un nombre 1-20 sauf si erreur -> ""
entry = ""
# indexation des musiques


while 1:
    sys.stdout.write('Enter your choice : ')
    sys.stdout.flush()
    # Recuperation de la frappe clavier
    choice = getch.getch()
    # Conversion avec le dictionnaire
    choice = dic.find(choice)
    if choice == 'quit':
        display.UT.join()
        player.exit()
        #display.display.RT.join()
        print ("Goodbye !")
        exit();
    elif choice == 'list':
        print ("List of songs :")
        music_index.printmusicdir()
    else:
        #On test le timer
        if ((player.queue_count() < CONF.variables['nb_music']) or (time.time()-player.lastAdded > CONF.variables['timeout'])) :
            # Si on n'a pas deja choisi une lettre
            if entry == "":
                # Si c'est une lettre
                if (str(choice)).isalpha():
                    # L'entree devient la lettre en majuscule
                    entry = choice.upper()
                    display.entry(entry)
                # Echec
                else:
                    print("Invalid input")
            else:
                #si le choix est un nombre
                if (str(choice)).isdigit():
                    oldEntry=entry
                    #on ajoute a l'entree le nombre correspondant
                    entry += choice
                    # recherche dans l'index des musiques
                    song = music_index.findnumber(entry)
                    #non trouvee
                    if song == "":
                        print("This song does not exist")
                    #trouvee
                    else:
                        print("Song chosen : " + song.artist+"'s "+song.name)
                        #ajout a la playlist
                        player.enqueue(song)
                        print("songs queued :" + str(player.queue_count()))
                        display.entry(oldEntry, choice, song)
                        display.setQueue(player.queue_count())
                    entry = ""
                #on ecrase le choix de la lettre precedente
                elif (""+choice).isalpha():
                    entry = choice.upper()
                    display.entry(entry)
                else:  #echec
                    print("Invalid input")
                    entry = ""
        else :
            print("Wait !")
            #display.wait()
