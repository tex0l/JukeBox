# -*- coding: utf-8 -*-
from django.db import models
from django.core.files import File
from tempfile import NamedTemporaryFile
import mutagenwrapper
import hashlib


class Artwork(models.Model):
    image = models.ImageField(upload_to="Artwork", null=True, blank=True)

    def url(self):
        return self.image.url

    @classmethod
    def create(cls, data, name):
        print "Creating new artwork for : " + name
        with NamedTemporaryFile(mode="w+b",) as f:
            f.write(data)
            f.flush()
            o = cls()
            o.image.save("%s.jpg" % name, File(f), save=True)
            return o


class AlbumArtwork(Artwork):
    album = models.ForeignKey('Album', null=True, blank=True, related_name='+')

    @classmethod
    def add(cls, data, album):
        o = cls.create(data, album.name)
        o.album = album
        o.save()
        return o


class ArtistArtwork(Artwork):
    artist = models.ForeignKey('Artist', null=True, blank=True, related_name='+')

    @classmethod
    def add_existing_artwork(cls, data, artist):
        print "Adding existing artwork to " + artist.name
        o = cls()
        o.image = data
        o.artist = artist
        o.save()
        return o

    @classmethod
    def add_new_artwork(cls, data, artist):
        print "Adding new artwork to " + artist.name
        o = cls.create(data, artist.name)
        o.artist = artist
        o.save()
        return o


class SlotArtwork(Artwork):
    pass


class Artist(models.Model):
    name = models.CharField(name='name', max_length='100', default='unknown')
    date_added = models.DateTimeField(auto_now=True, editable=False)
    artwork = models.ForeignKey('ArtistArtwork', null=True, blank=True, related_name='+')

    def get_artwork_dict(self):
        d = []
        artist_artwork_request = ArtistArtwork.objects.filter(artist=self)
        for artist_artwork in artist_artwork_request:
            selected = (artist_artwork == self.artwork)
            d.append({'pk': artist_artwork.pk, 'url': artist_artwork.url(), 'selected': selected})

        artist_albums = []
        artist_albums_request = Album.objects.filter(album_artist=self)
        for album in artist_albums_request:
            artist_albums.append(album.get_artwork_dict())

        return {'pk': self.pk, 'name': self.name, 'artworks': d, 'albums': artist_albums}


class Album(models.Model):
    name = models.CharField(name='name', max_length='100', default='unknown')
    year = models.CharField(name='year', max_length='100', null=True, blank=True)
    album_artist = models.ForeignKey('Artist', null=True, blank=True)
    date_added = models.DateTimeField(auto_now=True, editable=False)
    number_of_tracks = models.IntegerField(name='number_of_tracks', null=True, blank=True)
    number_of_discs = models.IntegerField(name='number_of_discs', null=True, blank=True)
    artwork = models.ForeignKey('AlbumArtwork', null=True, blank=True, related_name='+')

    def get_artwork_dict(self):
        album_artwork_request = AlbumArtwork.objects.filter(album=self)
        d = []
        for album_artwork in album_artwork_request:
            selected = (album_artwork == self.artwork)
            d.append({'pk': album_artwork.pk, 'url': album_artwork.url(), 'selected': selected})
        return {'pk': self.pk, 'title': self.name, 'album_artist': self.album_artist.pk, 'artworks': d}


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

        artist_name = tags.find('artist', 'unknown')
        artist, artist_created = Artist.objects.get_or_create(name=artist_name)

        album_artist_name = tags.find('albumartist', artist_name)
        album_artist, album_artist_created = Artist.objects.get_or_create(name=album_artist_name)

        album, album_created = Album.objects.get_or_create(name=tags.find('album', 'unknown'),
                                                           album_artist=album_artist)

        artwork = tags.find('pictures')

        if album_created:
            album.number_of_tracks = tags.find('tracktotal')
            album.number_of_discs = tags.find('disctotal')
            if artwork:
                album.artwork = AlbumArtwork.add(artwork, album)
            album.save()

        if (not album.artwork) and artwork:
            album.artwork = AlbumArtwork.add(artwork, album)
            album.save()

        if not artist.artwork:
            if album.artwork:
                artist.artwork = ArtistArtwork.add_existing_artwork(album.artwork.image, artist)
            artist.save()

        if not album_artist.artwork:
            if album.artwork:
                album_artist.artwork = ArtistArtwork.add_existing_artwork(album.artwork.image, artist)
            album_artist.save()

        self.artist = artist
        self.album = album
        self.year = tags.find('year', 'unknown')
        self.track_number = tags.find('tracknumber')
        self.disc_number = tags.find('discnumber')
        self.save()

    def dict(self):
        return {"pk": self.pk, "title": self.title, "artist": self.artist.name, "album": self.album.name,
                "album_artist": self.album.album_artist.name, "number": self.track_number, "disc_nb": self.disc_number,
                "artwork": (self.album.artwork.url() if self.album.artwork else 'static/default_artwork.png'),
                "url": self.file_field.url}
