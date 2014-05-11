import glob,os,sys
import pygame

def path_leaf(path): #recupere le bout d'un chemin systeme
    head, tail = os.path.split(path)
    return tail or os.path.basename(head)

class MusicDir:
    def __init__(self,path):
        self.path = path;#chemin du repertoire
        os.chdir(path);
        fichiers = glob.glob("*");
        self.musique = [];#listes des objets Music
        self.codes=[];#listes des index des musiques (type A1, B12, etc.)
        for file in fichiers :#indexation iterative
            self.musique.append(Music(file));
            l=len(self.musique);
            self.codes.append(self.musique[l-1].number);
    def printmusicdir(self): # impression de la liste des musiques
        for music in self.musique:
            music.printmusic();
    def findnumber(self,test): # renvoie l'objet Music correspondant a l'index test
        l=len(self.codes)
        
        for i in range(0,l):
            if (self.codes[i]==test):
                return self.musique[i];
            
        return "";
        
        
class Music:
    def __init__(self,path):
        #file named : CODE-Name-Artist.format
        self.path = path;#chemin
        self.file_name = path_leaf(self.path);#nom du fichier
        liste = self.file_name.split("-");
        self.number = liste[0];#index
        self.name = liste[1];#nom
        self.artist = liste[2].split(".");#artiste
        l = len(self.artist);
        self.format=self.artist.pop(l-1);#format
        if l>2:
            self.artist= ".".join(self.artist)
        else:
            self.artist=self.artist[0];
        
    def printmusic(self):
        print self.number+" "+self.name+" "+self.artist+" "+self.format;