# -*- coding: utf-8 -*-
from django.db import models
import time
from tags import tag_finder


class Artist(models.Model):
    name = models.CharField(name='name', max_length='100', default='unknown')
    date_added = models.DateTimeField(auto_now=True, editable=False)


class Album(models.Model):
    name = models.CharField(name='name', max_length='100', default='unknown')
    year = models.IntegerField(name='year', default=None)
    artist = models.ForeignKey('Artist', null=True, blank=True)
    date_added = models.DateTimeField(auto_now=True, editable=False)
    number_of_tracks = models.IntegerField(name='number_of_tracks', null=True, blank=True)
    number_of_discs = models.IntegerField(name='number_of_discs', null=True, blank=True)

class Music(models.Model):
    title = models.CharField('title', max_length=100)
    artist = models.ForeignKey('Artist', null=True, blank=True)
    album = models.ForeignKey('Album', null=True, blank=True)
    file_field = models.FileField(upload_to="Library")
    date_added = models.DateTimeField(auto_now=True, editable=False)
    track_number = models.IntegerField(name='track_number', null=True, blank=True)
    disc_number = models.IntegerField(name='disc_number', null=True, blank=True)

    def clean(self):
        file_path = self.file_field.path
        tags = tag_finder(file_path)







