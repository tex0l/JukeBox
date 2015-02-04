from __future__ import unicode_literals
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import os
from tags import tag_finder


def path_leaf(path): #recupere le bout d'un chemin systeme
    head, tail = os.path.split(path)
    return tail or os.path.basename(head)

class MusicDir:
    def __init__(self, path):
        #chemin du repertoire
        self.path = os.path.join(os.path.dirname(__file__), path)
        os.chdir(self.path)
        print os.chdir(self.path)
        fichiers = glob.glob("*")
        #listes des objets Music
        self.musique = []
        #listes des index des musiques (type A1, B12, etc.)
        self.codes = []
        #indexation iterative
        for file in fichiers:
            try:
                self.musique.append(Music(file))
                l = len(self.musique)
                self.codes.append(self.musique[l-1].number)
            except:
                print(file+" is incorrectly named. Try updating the database")

    # impression de la liste des musiques
    def printmusicdir(self):
        for music in self.musique:
            music.printmusic()

    # renvoie l'objet Music correspondant a l'index test
    def findnumber(self, test):
        l = len(self.codes)
        
        for i in range(0,l):
            if (self.codes[i] == test):
                return self.musique[i]
            
        return ""

    def filled_slots(self):

        dic = dict([(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D')])
        filledslots = [[],[],[],[]]
        letter = 1
        while letter <= 4:
            number = 0
            while number < 20:
                number += 1
                if self.findnumber(dic[letter]+str(number)) != "":
                    filledslots[letter-1].append(True)
                else:
                    filledslots[letter-1].append(False)
            letter += 1
        return filledslots
    
        
class Music:
    def __init__(self, path):
        #file named : CODE-Name-Artist.format
        #chemin
        self.path = path
        #nom du fichier
        self.file_name = path_leaf(self.path)
        self.find_tags()


    def find_tags(self):
        tags = tag_finder(self.path)
        #Audio file mode
        #index
        self.number = self.file_name.split("-")[0]
        #artiste
        try:
            self.artist = tags['artist'][0]
        except KeyError:
            self.artist = "unknown"
        #nom
        try:
            self.name = tags['title'][0]
        except KeyError:
            self.name = "unknown"
        #format
        self.format = self.file_name.split(".")[-1]

    def printmusic(self):
        print self.number+" - "+self.name+" - "+self.artist+" - "+self.format
    
    def display(self):
        return "%s : %s by %s" % (self.number, self.name, self.artist)
