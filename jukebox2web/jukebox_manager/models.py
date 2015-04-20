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
                'artist': self.music1.artist,
                'title': self.music1.title,
                'path': self.music1.file_field.path
            },
            self.slot2_nb:{
                'artist': self.music2.artist,
                'title': self.music2.artist,
                'path': self.music2.file_field.path
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
        s0 = SlotPair(slot1_nb=1, slot2_nb=2)
        s1 = SlotPair(slot1_nb=3, slot2_nb=4)
        s2 = SlotPair(slot1_nb=5, slot2_nb=6)
        s3 = SlotPair(slot1_nb=7, slot2_nb=8)
        s4 = SlotPair(slot1_nb=9, slot2_nb=10)
        s5 = SlotPair(slot1_nb=11, slot2_nb=12)
        s6 = SlotPair(slot1_nb=13, slot2_nb=14)
        s7 = SlotPair(slot1_nb=15, slot2_nb=16)
        s8 = SlotPair(slot1_nb=17, slot2_nb=18)
        s9 = SlotPair(slot1_nb=19, slot2_nb=20)
        s0.save()
        s1.save()
        s2.save()
        s3.save()
        s4.save()
        s5.save()
        s6.save()
        s7.save()
        s8.save()
        s9.save()
        return MusicSet(name=name, s0=s0, s1=s1, s2=s2, s3=s3, s4=s4, s5=s5, s6=s6, s7=s7, s8=s8, s9=s9)

    def save(self, *args, **kwargs):
        self.s0.save()
        self.s1.save()
        self.s2.save()
        self.s3.save()
        self.s4.save()
        self.s5.save()
        self.s6.save()
        self.s7.save()
        self.s8.save()
        self.s9.save()
        super(MusicSet, self).save(*args, **kwargs)  # Call the "real" save() method.

    def dict(self):
        return {
            'pk': self.pk, 'name': self.name,
            'slot_pairs': [self.s0.dict(), self.s1.dict(), self.s2.dict(), self.s3.dict(), self.s4.dict(),
                           self.s5.dict(), self.s6.dict(), self.s7.dict(), self.s8.dict(), self.s9.dict()]
        }

    def dictify(self):
        list = [self.s0, self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7, self.s8, self.s9]
        dict = {}
        for slot_pair in list:
            dict.update(slot_pair.dictify())
        return dict

    @staticmethod
    def get_current_MusicSets():
        try:
            a = MusicSet.objects.get(selection='A')
            a_dict = a.dictify()
        except:
            logging.error("No A MusicSet")
            a_dict = {}
            pass
        try:
            b = MusicSet.objects.get(selection='B')
            b_dict = b.dictify()
        except:
            logging.error("No B MusicSet")
            b_dict = {}
            pass
        try:
            c = MusicSet.objects.get(selection='C')
            c_dict = c.dictify()
        except:
            logging.error("No C MusicSet")
            c_dict = {}
            pass
        try:
            d = MusicSet.objects.get(selection='D')
            d_dict = d.dictify()
        except:
            logging.error("No D MusicSet")
            d_dict = {}
            pass
        return {'A': a_dict, 'B': b_dict, 'C': c_dict, 'D': d_dict}
        
