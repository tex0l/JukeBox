# -*- coding: utf-8 -*-
from django.views.generic import View
import json
from django.http import HttpResponse

from models import *


class Library(View):

    def get(self, request):
        artists_request = Artist.objects.all()
        artists = []
        autocomplete_artists = []
        autocomplete_albums = []
        for artist in artists_request:
            autocomplete_artists.append(artist.name)
            artist_albums = []
            artist_albums_request = Album.objects.filter(album_artist=artist)
            for album in artist_albums_request:
                autocomplete_albums.append(album.name)
                album_musics = []
                album_musics_request = Music.objects.filter(album=album)
                for music in album_musics_request:
                    album_musics.append({"pk": music.pk, "title": music.title, "artist": music.artist.name,
                                         "album": music.album.name, "album_artist": album.album_artist.name,
                                         "number": music.track_number, "disc_nb": music.disc_number,
                                         "artwork": music.artwork.url})
                if album_musics:
                    album_musics.sort(key=lambda m: (m['disc_nb'] if m['disc_nb'] else 0)*1000 +
                                                    (m['number'] if m['number'] else 0))
                    artist_albums.append({"pk": album.pk, "title": album.name, "artist": album.album_artist.name,
                                          "musics": album_musics, "artwork": album_musics[0]['artwork'],
                                          "year": album.year})
            if artist_albums:
                artist_albums.sort(key=lambda a: str(a["year"]) + a["title"])
                artists.append({"pk": artist.pk, "name": artist.name, "albums": artist_albums,
                                "artwork": artist_albums[0]['artwork']})

        artists.sort(key=lambda a: a["name"])
        return HttpResponse(json.dumps({'artists': artists, 'autocomplete_artists': autocomplete_artists,
                                        'autocomplete_albums': autocomplete_albums}), content_type='application/json')
