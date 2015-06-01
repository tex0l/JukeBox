# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.template import RequestContext

from forms import MusicForm
from models import Music

import logging


class PlaylistManager(View):

    def get(self, request):
        print "Playlist Manager Chosen"
        letters = ['A', ]
        numbers = range(1, 21)
        slots = []
        for letter in letters:
            for number in numbers:
                slots.append(letter + str(number))

        return render_to_response(
            'playlist_manager.html',
            {'slots': slots,
             'rows': 10,
             'cols': 2},
            context_instance=RequestContext(request)
        )
