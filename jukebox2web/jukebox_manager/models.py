from django.db import models
from django.conf import settings
# Create your models here.

class Slot(models.Model):
    id = models.IntegerField(name='id number', help_text='is the number of the final index. Ex: id 1 for index A1 ')
    music1 = models.ForeignKey('library_manager.Music', related_name='+')
    music2 = models.ForeignKey('library_manager.Music', related_name='+')
    artwork = models.ImageField(upload_to='Artwork')


class MusicSet(models.Model):
    id = models.CharField(name='id letter', max_length=1, help_text="if not blank, then it's the current musicset for letter id here")
    name = models.CharField(name='name', max_length=100)
    s0 = models.ForeignKey('jukebox_manager.Slot', related_name='+')
    s1 = models.ForeignKey('jukebox_manager.Slot', related_name='+')
    s2 = models.ForeignKey('jukebox_manager.Slot', related_name='+')
    s3 = models.ForeignKey('jukebox_manager.Slot', related_name='+')
    s4 = models.ForeignKey('jukebox_manager.Slot', related_name='+')
    s5 = models.ForeignKey('jukebox_manager.Slot', related_name='+')
    s6 = models.ForeignKey('jukebox_manager.Slot', related_name='+')
    s7 = models.ForeignKey('jukebox_manager.Slot', related_name='+')
    s8 = models.ForeignKey('jukebox_manager.Slot', related_name='+')
    s9 = models.ForeignKey('jukebox_manager.Slot', related_name='+')

