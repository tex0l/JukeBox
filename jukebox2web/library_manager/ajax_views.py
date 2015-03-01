# -*- coding: utf-8 -*-
from django.views.generic import View
import json
from django.http import HttpResponse
from urllib import unquote
# from django.views.decorators.csrf import ensure_csrf_cookie

from models import *


class Library(View):

    @staticmethod
    def get(request):
        return Library.return_json()

    @staticmethod
    def return_json():
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

    @staticmethod
    def post(request):
        edit = request.POST
        if edit.get('type') == 'music':
            pk = int(edit.get('pk')) if edit.get('pk') else None
            title = unquote(edit.get('title')) if edit.get('title') else 'unknown'
            artist = unquote(edit.get('artist')) if edit.get('artist') else 'unknown'
            album_artist = unquote(edit.get('album_artist')) if edit.get('album_artist') else artist
            album = unquote(edit.get('album')) if edit.get('album') else 'unknown'
            track_nb = int(unquote(edit.get('track_nb'))) if edit.get('track_nb') else None
            disc_nb = int(unquote(edit.get('disc_nb'))) if edit.get('disc_nb') else None

            music = Music.objects.get(pk=pk)
            music.title = title
            music.artist, created = Artist.objects.get_or_create(name=artist)
            album_artist_model, created = Artist.objects.get_or_create(name=album_artist)
            music.album, created = Album.objects.get_or_create(name=album, album_artist=album_artist_model)
            music.track_number = track_nb
            music.disc_number = disc_nb
            music.save()

        return Library.return_json()
