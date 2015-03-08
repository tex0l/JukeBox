# -*- coding: utf-8 -*-
from django.db import models
from django.core.files import File
from tempfile import NamedTemporaryFile
import mutagenwrapper
import hashlib


class Artwork(models.Model):
    image = models.ImageField(upload_to="Artwork", null=True, blank=True)
    hash = models.CharField(name='hash', max_length='100', default='')

    def save(self, *args, **kwargs):
        super(Artwork, self).save(*args, **kwargs)  # Call the "real" save() method.

    def url(self):
        return self.image.url

    @classmethod
    def create(cls, data):
        with NamedTemporaryFile(mode="w+b",) as f:
            f.write(data)
            f.flush()
            h = hashlib.sha1(data).hexdigest()
            o, created = cls.objects.get_or_create(hash=h)
            if created:
                o.image.save("%s.jpg" % h, File(f), save=True)
            return o


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
    artwork = models.ForeignKey('Artwork', null=True, blank=True)


class Music(models.Model):
    title = models.CharField('title', max_length=100)
    artist = models.ForeignKey('Artist', null=True, blank=True)
    album = models.ForeignKey('Album', null=True, blank=True)
    year = models.CharField(name='year', max_length='100', null=True, blank=True)
    file_field = models.FileField(upload_to="Library")
    date_added = models.DateTimeField(auto_now=True, editable=False)
    track_number = models.IntegerField(name='track_number', null=True, blank=True)
    disc_number = models.IntegerField(name='disc_number', null=True, blank=True)

    def clean(self):
        file_path = self.file_field.path
        tags = mutagenwrapper.read_tags(file_path)
        self.title = tags.find('title', 'unknown')
        name = tags.find('artist', 'unknown')
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
        album, created = Album.objects.get_or_create(name=tags.find('album', 'unknown'),
                                                     album_artist=album_artist,
                                                     )
        if created:
            album.number_of_tracks = tags.find('tracktotal')
            album.number_of_discs = tags.find('disctotal')
            artwork = tags.find('pictures')
            if artwork:
                album.artwork = Artwork.create(artwork)
            album.save()

        album.save()
        self.album = album
        self.year = tags.find('year','unknown')
        self.track_number = tags.find('tracknumber')
        self.disc_number = tags.find('discnumber')
        self.save()

    def dict(self):
        return {"pk": self.pk, "title": self.title, "artist": self.artist.name, "album": self.album.name,
                "album_artist": self.album.album_artist.name, "number": self.track_number, "disc_nb": self.disc_number,
                "artwork": (self.album.artwork.url() if self.album.artwork else 'static/default_artwork.png'),
                "url": self.file_field.url}
