# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from views import Upload


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'jukebox2web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^upload', Upload.as_view(),name='Upload'),
)
