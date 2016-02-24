# -*- coding: utf-8 -*-
from django.views.generic import View
import json
from django.http import HttpResponse
from urllib import unquote

from jukebox2web.settings import JSON_PATH
from models import *
from library_manager.models import *
import threading
<<<<<<< HEAD
from subprocess import call
=======
import os
>>>>>>> prob_zach1


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
            selected = {}
            for m in sets:
                if m.pk == int(edit.get('A')):
                    m.selection = 'A'
                    selected['A'] = m
                elif m.pk == int(edit.get('B')):
                    m.selection = 'B'
                    selected['B'] = m
                elif m.pk == int(edit.get('C')):
                    m.selection = 'C'
                    selected['C'] = m
                elif m.pk == int(edit.get('D')):
                    m.selection = 'D'
                    selected['D'] = m
                else:
                    m.selection = ''
                m.save()
            #Create the json file for the jukebox
            #TODO : check that playlists are full and that all four playlists are different
            try :
                f = open('../current_playlist.json', 'w')
                json.dump({'A' : selected['A'].dictify(), 'B' : selected['B'].dictify(),
                                  'C' : selected['C'].dictify(), 'D' : selected['D'].dictify()}, f, indent = 4)
            except (KeyError):
                print("All playlists must be different and full")

            pipeName = '../pipe'
            pipe = os.open(pipeName, os.O_WRONLY)
            os.write(pipe, 'reload\n')

            return HttpResponse(json.dumps({'sets': sets_list()}), content_type='application/json')
        elif t == 'tag':
            # read json file
            with open('../current_playlist.json') as data_file:
                data = json.load(data_file)

            #print(data["A"]["1"]["path"])

            # read tex file
            f = open("../latex/tag.tex", "r")
            contents = f.readlines()
            index = 0
            for line in contents:
                index += 1
                if("\\begin{document}" in line):
                    break
            f.close()

            b = True
            letters = ['A', 'B', 'C', 'D']
            numbers = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']

            for letter in letters:
                for number in numbers:
                    # TODO be carefull with other special characters
                    data[letter][number]["title"] = data[letter][number]["title"].replace("&","\&")
                    data[letter][number]["artist"] = data[letter][number]["artist"].replace("&","\&")
                    if(b):
                        line = "\\boite{\content{%s}{%s}{%s}}" % (letter+number,data[letter][number]["title"],data[letter][number]["artist"])
                        b = False

                    else:
                        line += "{\content{%s}{%s}{%s}}\n" % (letter+number,data[letter][number]["title"],data[letter][number]["artist"])
                        b= True
                        contents.insert(index, line)
                        index += 1
            contents.insert(index, "\end{document}\n")
            contents = contents[:index+1]

            f = open("../latex/tag.tex", "w")
            f.writelines(contents)
            f.close()

            # generate pdf file in latex directory: latex/tag.pdf
            call(["pdflatex","-output-directory", "../latex/","../latex/tag.tex"])
            return HttpResponse('OK') # something else?
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