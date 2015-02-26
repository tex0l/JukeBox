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
            artist_pk = artist.pk
            artist_name = artist.name
            artist_albums = []
            artist_albums_request = Album.objects.filter(album_artist=artist)
            for album in artist_albums_request:
                album_pk = album.pk
                album_title = album.name
                album_artist = album.album_artist.name
                album_musics = []
                album_musics_request = Music.objects.filter(album=album)
                for music in album_musics_request:
                    music_pk = music.pk
                    music_title = music.title
                    music_artist = music.artist.name
                    music_number = music.track_number
                    album_musics.append({"pk": music_pk, "title": music_title,
                                         "artist": music_artist, "number": music_number})
                artist_albums.append({"pk": album_pk, "title": album_title,
                                      "artist": album_artist, "musics": album_musics})
            artists.append({"pk": artist_pk, "name": artist_name, "albums": artist_albums})

        return HttpResponse(json.dumps({'artists': artists}), content_type='application/json')
