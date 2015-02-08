from __future__ import unicode_literals
from django.db import models

# Create your models here.
class Index(models.Model):
    letter = models.CharField('letter', max_length=1)
    number = models.IntegerField('number')

class Music(models.Model):
    index = models.ForeignKey(Index, name='index')
    title = models.CharField('title', max_length=100)
    artist = models.CharField('artist', max_length=100)
    directory = models.ForeignKey(MusicDirectory, name='directory', help_text="directory of the jukebox")
    file = models.FileField('file', max_length=100)
    date_added = models.DateTimeField('date_added')

class MusicDirectory(models.Model):
    path = models.FilePathField(path="/Users/timotheerebours/Documents/Python_Projects/JukeBox")
