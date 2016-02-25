# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from views import *
from ajax_views import *
from . import views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'jukebox2web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^playlist_manager', PlaylistManager.as_view(), name='PlaylistManager'),
    url(r'^ajax/library', Library.as_view(), name='library'),
    url(r'^ajax/upload', AjaxUpload.as_view(), name='library'),
    url(r'^ajax/artwork_upload', ArtworkUpload.as_view(), name='ArtworkUpload'),
    url(r'^ajax/artwork', Artworks.as_view(), name='artwork'),
    url(r'^tag.pdf', views.pdf_view, name='tag'),

)
