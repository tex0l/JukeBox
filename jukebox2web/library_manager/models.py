# -*- coding: utf-8 -*-
from django.db import models
from tempfile import NamedTemporaryFile
from django.core.files import File
import time
import mutagenwrapper

class Artist(models.Model):
    name = models.CharField(name='name', max_length='100', default='unknown')
    date_added = models.DateTimeField(auto_now=True, editable=False)

class Album(models.Model):
    name = models.CharField(name='name', max_length='100', default='unknown')
    year = models.CharField(name='year', max_length='100', null=True, blank=True)
    album_artist = models.ForeignKey('Artist', null=True, blank=True)
    date_added = models.DateTimeField(auto_now=True, editable=False)
    number_of_tracks = models.IntegerField(name='number_of_tracks', null=True, blank=True)
    number_of_discs = models.IntegerField(name='number_of_discs', null=True, blank=True)

class Music(models.Model):
    title = models.CharField('title', max_length=100)
    artist = models.ForeignKey('Artist', null=True, blank=True)
    album = models.ForeignKey('Album', null=True, blank=True)
    year = models.CharField(name='year', max_length='100', null=True, blank=True)
    file_field = models.FileField(upload_to="Library")
    date_added = models.DateTimeField(auto_now=True, editable=False)
    track_number = models.IntegerField(name='track_number', null=True, blank=True)
    disc_number = models.IntegerField(name='disc_number', null=True, blank=True)
    artwork = models.ImageField(upload_to="Library", null=True, blank=True)

    def clean(self):
        file_path = self.file_field.path
        tags = mutagenwrapper.read_tags(file_path)
        self.title = tags.find('title','unknown')
        name = tags.find('artist','unknown')
        artist, created = Artist.objects.get_or_create(name=name)
        if created:
            artist.save()
        self.artist = artist
        album_artist_name = tags.find('albumartist')
        if not album_artist_name:
            album_artist_name = name
        album_artist, created = Artist.objects.get_or_create(name=album_artist_name)
        if created:
            album_artist.save()
        album, created = Album.objects.get_or_create(name=tags.find('album','unknown'),
                                                 year=tags.find('year','unknown'),
                                                 album_artist=album_artist,
                                                 )
        if created:
            album.number_of_tracks = tags.find('tracktotal')
            album.number_of_discs = tags.find('disctotal')
            album.save()
        album.save()
        self.album = album
        self.year = tags.find('year','unknown')
        self.track_number = tags.find('tracknumber')
        self.disc_number = tags.find('discnumber')
        artwork = tags.find('pictures')
        if artwork:
            with NamedTemporaryFile(mode="w+b",) as f:
                f.write(artwork)
                f.flush()
                self.artwork.save("%s.jpg" % self.title, File(f), save=True)
        self.save()
