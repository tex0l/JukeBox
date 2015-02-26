# -*- coding: utf-8 -*-
from django.views.generic import View
import json
from django.http import HttpResponse

from models import *


class Library(View):

    def get(self, request):
        artists_request = Artist.objects.all()
        artists = []
        for artist in artists_request:
            artist_albums = []
            artist_albums_request = Album.objects.filter(album_artist=artist)
            for album in artist_albums_request:
                album_musics = []
                album_musics_request = Music.objects.filter(album=album)
                for music in album_musics_request:
                    album_musics.append({"pk": music.pk, "title": music.title, "artist": music.artist.name,
                                         "album": music.album.name, "number": music.track_number,
                                         "artwork": music.artwork.url})
                if album_musics:
                    artist_albums.append({"pk": album.pk, "title": album.name, "artist": album.album_artist.name,
                                          "musics": album_musics, "artwork": album_musics[0]['artwork']})
            if artist_albums:
                artists.append({"pk": artist.pk, "name": artist.name, "albums": artist_albums,
                                "artwork": artist_albums[0]['artwork']})

        return HttpResponse(json.dumps({'artists': artists}), content_type='application/json')
