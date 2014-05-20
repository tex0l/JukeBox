#!/usr/bin/python
# Version 2


import sys
import os

import getch
import keyboard_map
import music_player
import parser
from display_LCDd_2x40 import *

dic = keyboard_map.Map() # initialisation du dictionnaire
player = music_player.Player(); # initialisation du lecteur
music_dir="/Users/arantes/JukeMusic" # repertoire de musique
music_index = parser.MusicDir(music_dir)
display=displayLCDd2x40()

generate = raw_input("Update music directory ? ((y or yes ) or anything else)")
if (generate=="y" or generate=="yes"):
    #extraction_path = raw_input("Extract from ? : ")
    #final_path = music_dir;
    player.generate_library(music_dir,music_dir,music_index.filled_slots())

print (30 * '-')
print ("   j u k e b o X")
print (30 * '-')
print ("$. Credit")
print ("A-D + 1-20. Select Song")
print ("J. Switch to Jack Input")
print ("Q. Quit")
print ("L. List songs")
print (30 * '-')

credit = 0 # nombre de credits
entry="" # choix de musique, est vide avant le choix d'une lettre A-D, puis est complete par un nombre 1-20 sauf si erreur -> ""

#music_dir="/Users/arantes/JukeMusic" # repertoire de musique
#music_index = parser.MusicDir(music_dir) # indexation des musiques

while 1 :
    sys.stdout.write('Enter your choice : ')
    sys.stdout.flush()
    choice = getch.getch() # Recuperation de la frappe clavier
    choice = dic.find(choice) # Conversion avec le dictionnaire
    if choice == 'credit':
        print ("Adding 1 credit")
        credit+=1
        display.setCredit(credit)
        display.waiting("choose")
        print("Credit = "+`credit`)
    elif choice == 'quit':
        player.exit()
        #display.display.RT.join()
        print ("Goodbye !")
        exit();
    elif choice == 'list':
        print ("List of songs :")
        music_index.printmusicdir()
    else:
        if entry=="": # Si on n'a pas deja choisi une lettre
            if (str(choice)).isalpha(): # Si c'est une lettre
                entry=choice.upper() # L'entree devient la lettre en majuscule
            else:
                print("Invalid input") # Echec
        else:
            if (str(choice)).isdigit(): #si le choix est un nombre
                entry+=choice #on ajoute a l'entree le nombre correspondant
                song = music_index.findnumber(entry) # recherche dans l'index des musiques
                if song=="":
                    print("This song does not exist") #non trouve
                elif credit==0:
                    print("0 credit. Insert coin")#pas de credit
                else:
                    print("Song chosen : " + song.artist+"'s "+song.name)
                    player.enqueue(song); #ajout a la playlist
                    print("songs queued :" + str(player.queue_count()));
                    credit-=1
                    display.setCredit(credit)
                    print("Credits left : " +`credit`)
                    if credit==0:
                        display.waiting("coin")
                    display.setQueue(player.queue_count())
                entry=""
            elif (""+choice).isalpha(): #on ecrase le choix de la lettre precedente
                entry=choice.upper()
            else: #echec
                print("Invalid input")
                entry=""

