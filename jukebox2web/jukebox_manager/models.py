from django.db import models
from django.conf import settings
from library_manager.models import *
import logging
# Create your models here.


class SlotPair(models.Model):
    slot1_nb = models.IntegerField(name='slot1_nb', help_text='is the number of the final index. Ex: id 1 for index A1 ')
    slot2_nb = models.IntegerField(name='slot2_nb', help_text='is the number of the final index. Ex: id 2 for index A2 ')
    music1 = models.ForeignKey('library_manager.Music', null=True, blank=True, related_name='+')
    music2 = models.ForeignKey('library_manager.Music', null=True, blank=True, related_name='+')
    artwork = models.ImageField(upload_to='Artwork')
    artwork_pk = models.IntegerField(name='artwork_pk', default=0)

    def dict(self):
        if self.artwork:
            artwork = self.artwork.url
        elif self.music1 and self.music1.album.artwork:
            artwork = self.music1.album.artwork.url()
        elif self.music2 and self.music2.album.artwork:
            artwork = self.music2.album.artwork.url()
        else:
            artwork = 'static/default_artwork.png'

        return {'slot1_nb': self.slot1_nb, 'slot2_nb': self.slot2_nb,
                'music1': self.music1.dict() if self.music1 else {},
                'music2': self.music2.dict() if self.music2 else {},
                'artwork': artwork, 'pk': self.pk}

    def dictify(self):
        return {
            self.slot1_nb: {
                'artist': Artist.objects.get(pk=Music.objects.get(pk=self.music1_id).artist_id).name,
                'title': Music.objects.get(pk=self.music1_id).title,
                'path': Music.objects.get(pk=self.music1_id).file_field.path
            },
            self.slot2_nb: {
                'artist': Artist.objects.get(pk=Music.objects.get(pk=self.music2_id).artist_id).name,
                'title': Music.objects.get(pk=self.music2_id).title,
                'path': Music.objects.get(pk=self.music2_id).file_field.path
            }
        }


class MusicSet(models.Model):
    selection = models.CharField(name='selection', max_length=1, help_text="if not blank, then it's the current musicset for letter id here")
    name = models.CharField(name='name', max_length=100)
    s0 = models.ForeignKey('jukebox_manager.SlotPair', related_name='+')
    s1 = models.ForeignKey('jukebox_manager.SlotPair', related_name='+')
    s2 = models.ForeignKey('jukebox_manager.SlotPair', related_name='+')
    s3 = models.ForeignKey('jukebox_manager.SlotPair', related_name='+')
    s4 = models.ForeignKey('jukebox_manager.SlotPair', related_name='+')
    s5 = models.ForeignKey('jukebox_manager.SlotPair', related_name='+')
    s6 = models.ForeignKey('jukebox_manager.SlotPair', related_name='+')
    s7 = models.ForeignKey('jukebox_manager.SlotPair', related_name='+')
    s8 = models.ForeignKey('jukebox_manager.SlotPair', related_name='+')
    s9 = models.ForeignKey('jukebox_manager.SlotPair', related_name='+')

    @classmethod
    def create(cls, name):
        S = []
        for i in range(0,10):
            S.append(SlotPair(slot1_nb=2*i+1, slot2_nb=2*(i+1)))
            S[i].save()
        return MusicSet(name=name, s0=S[0], s1=S[1], s2=S[2], s3=S[3], s4=S[4], s5=S[5], s6=S[6], s7=S[7], s8=S[8], s9=S[9])

    def save(self, *args, **kwargs):
        list = [self.s0, self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7, self.s8, self.s9]
        for slot_pair in list:
            slot_pair.save()
        super(MusicSet, self).save(*args, **kwargs)  # Call the "real" save() method.

    def dict(self):
        return {
            'pk': self.pk, 'name': self.name, 'selection': self.selection,
            'slot_pairs': [self.s0.dict(), self.s1.dict(), self.s2.dict(), self.s3.dict(), self.s4.dict(),
                           self.s5.dict(), self.s6.dict(), self.s7.dict(), self.s8.dict(), self.s9.dict()]
        }

    def dictify(self):
        list = [self.s0, self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7, self.s8, self.s9]
        dict = {}
        for slot_pair in list:
            dict.update(slot_pair.dictify())
        return dict

    def get_selected_dictified_MusicSet(selection):
        try:
            return MusicSet.objects.get(selection=selection).dictify()
        except KeyError:
            logging.error("MusicSet %s not found, ignored")
            return {}

    @staticmethod
    def get_selected_MusicSets():
        return {
            'A': MusicSet.get_selected_dictified_MusicSet('A'),
            'B': MusicSet.get_selected_dictified_MusicSet('B'),
            'C': MusicSet.get_selected_dictified_MusicSet('C'),
            'D': MusicSet.get_selected_dictified_MusicSet('D'),
                }
