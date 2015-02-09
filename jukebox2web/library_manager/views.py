from __future__ import unicode_literals
from django.shortcuts import render, render_to_response
from django.views.generic import View
from django.http import HttpResponse

class Library(View):


    def get(self, request):

        return render_to_response('index.html', {'title': 'Hello World !','message':'This is home page test'})

