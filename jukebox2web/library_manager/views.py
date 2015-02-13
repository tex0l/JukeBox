# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.template import RequestContext
from forms import MusicForm

from models import Music
class Upload(View):


    def get(self, request):

        form = MusicForm() # A empty, unbound form
        musics = Music.objects.all()
        for music in musics:
            print music.file_field.name
        # Render list page with the documents and the form
        return render_to_response(
            'upload.html',
            {'musics': musics, 'form': form},
            context_instance=RequestContext(request)
        )


    def post(self, request):
        form = MusicForm(request.POST, request.FILES)
        print request.FILES
        print form.is_valid()
        if form.is_valid():
            new_music = Music(file_field=request.FILES['file_field'])
            new_music.save()
            new_music.clean()
            # Redirect to the document list after POST
            return HttpResponseRedirect('upload')
        else:
            return self.get(request)

class Main(View):

    def get(self, request):
        library = Music.objects.all()

