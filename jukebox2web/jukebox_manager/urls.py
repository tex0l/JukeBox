# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from views import *


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'jukebox2web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^ajax/sets', MusicSets.as_view(), name='music_sets')
)
