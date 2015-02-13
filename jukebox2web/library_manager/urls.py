# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from views import *


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'jukebox2web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^upload', Upload.as_view(), name='Upload'),
    url(r'^playlist_manager', PlaylistManager.as_view(), name='PlaylistManager'),
)
