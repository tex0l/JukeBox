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
        return HttpResponse(json.dumps({'sets': sets_list()}), content_type='application/json')

    @staticmethod
    def post(request):
        edit = request.POST
        t = edit.get('type')
        if t == 'save':
            sets = json.loads(edit.get('sets'))
            MusicSets.save_sets(sets)
            return HttpResponse('OK')
        elif t == 'add':
            m = MusicSet.create(name=edit.get('name'))
            m.save()
            return HttpResponse(json.dumps(m.dict()), content_type='application/json')
        elif t == 'select':
            sets = MusicSet.objects.all()
            for m in sets:
                if m.pk == int(edit.get('A')):
                    m.selection = 'A'
                elif m.pk == int(edit.get('B')):
                    m.selection = 'B'
                elif m.pk == int(edit.get('C')):
                    m.selection = 'C'
                elif m.pk == int(edit.get('D')):
                    m.selection = 'D'
                else:
                    m.selection = ''
                m.save()
            #TODO : Actually pushing to the jukebox
            return HttpResponse(json.dumps({'sets': sets_list()}), content_type='application/json')
        raise Exception('Unexpected music set request')

    @staticmethod
    def save_sets(sets):
        for music_set in sets:
            s = MusicSet.objects.get(pk=music_set.get('pk'))

            s.name = music_set.get('name')

            s.s0.music1 = Music.objects.get(pk=music_set.get('s1')) if music_set.get('s1') else None
            s.s0.music2 = Music.objects.get(pk=music_set.get('s2')) if music_set.get('s2') else None

            s.s1.music1 = Music.objects.get(pk=music_set.get('s3')) if music_set.get('s3') else None
            s.s1.music2 = Music.objects.get(pk=music_set.get('s4')) if music_set.get('s4') else None

            s.s2.music1 = Music.objects.get(pk=music_set.get('s5')) if music_set.get('s5') else None
            s.s2.music2 = Music.objects.get(pk=music_set.get('s6')) if music_set.get('s6') else None

            s.s3.music1 = Music.objects.get(pk=music_set.get('s7')) if music_set.get('s7') else None
            s.s3.music2 = Music.objects.get(pk=music_set.get('s8')) if music_set.get('s8') else None

            s.s4.music1 = Music.objects.get(pk=music_set.get('s9')) if music_set.get('s9') else None
            s.s4.music2 = Music.objects.get(pk=music_set.get('s10')) if music_set.get('s10') else None

            s.s5.music1 = Music.objects.get(pk=music_set.get('s11')) if music_set.get('s11') else None
            s.s5.music2 = Music.objects.get(pk=music_set.get('s12')) if music_set.get('s12') else None

            s.s6.music1 = Music.objects.get(pk=music_set.get('s13')) if music_set.get('s13') else None
            s.s6.music2 = Music.objects.get(pk=music_set.get('s14')) if music_set.get('s14') else None

            s.s7.music1 = Music.objects.get(pk=music_set.get('s15')) if music_set.get('s15') else None
            s.s7.music2 = Music.objects.get(pk=music_set.get('s16')) if music_set.get('s16') else None

            s.s8.music1 = Music.objects.get(pk=music_set.get('s17')) if music_set.get('s17') else None
            s.s8.music2 = Music.objects.get(pk=music_set.get('s18')) if music_set.get('s18') else None

            s.s9.music1 = Music.objects.get(pk=music_set.get('s19')) if music_set.get('s19') else None
            s.s9.music2 = Music.objects.get(pk=music_set.get('s20')) if music_set.get('s20') else None

            s.save()