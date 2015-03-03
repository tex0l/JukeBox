# -*- coding: utf-8 -*-
from django.views.generic import View
import json
from django.http import HttpResponse
from urllib import unquote

from models import *
from library_manager.models import *
import threading


def sets_list():
    sets_request = MusicSet.objects.all()
    sets = []
    for s in sets_request:
        sets.append(s.dict())

    return sets


class MusicSets(View):

    @staticmethod
    def get(request):
        return HttpResponse(json.dumps(sets_list()), content_type='application/json')

    @staticmethod
    def post(request):
        edit = request.POST
        sets = edit.get('sets')
        if edit.get('type') == 'save':
            MusicSets.save_sets(sets)
            print "Sets saved"
            return HttpResponse('')
        elif edit.get('type') == 'add':
            m = MusicSet(name=edit.get('name'))
            m.save()
            return HttpResponse(json.dumps(sets_list()), content_type='application/json')

    @staticmethod
    def save_sets(sets):
        for music_set in sets:
            s = MusicSet.objects.get(pk=music_set.get('pk'))

            s.name = music_set.get('name')

            s.s0.music1 = Music.objects.get(pk=music_set.get('s01'))
            s.s0.music2 = Music.objects.get(pk=music_set.get('s02'))

            s.s1.music1 = Music.objects.get(pk=music_set.get('s03'))
            s.s1.music2 = Music.objects.get(pk=music_set.get('s04'))

            s.s2.music1 = Music.objects.get(pk=music_set.get('s05'))
            s.s2.music2 = Music.objects.get(pk=music_set.get('s06'))

            s.s3.music1 = Music.objects.get(pk=music_set.get('s07'))
            s.s3.music2 = Music.objects.get(pk=music_set.get('s08'))

            s.s4.music1 = Music.objects.get(pk=music_set.get('s09'))
            s.s4.music2 = Music.objects.get(pk=music_set.get('s10'))

            s.s5.music1 = Music.objects.get(pk=music_set.get('s11'))
            s.s5.music2 = Music.objects.get(pk=music_set.get('s12'))

            s.s6.music1 = Music.objects.get(pk=music_set.get('s13'))
            s.s6.music2 = Music.objects.get(pk=music_set.get('s14'))

            s.s7.music1 = Music.objects.get(pk=music_set.get('s15'))
            s.s7.music2 = Music.objects.get(pk=music_set.get('s16'))

            s.s8.music1 = Music.objects.get(pk=music_set.get('s17'))
            s.s8.music2 = Music.objects.get(pk=music_set.get('s18'))

            s.s9.music1 = Music.objects.get(pk=music_set.get('s19'))
            s.s9.music2 = Music.objects.get(pk=music_set.get('s20'))

            s.save()