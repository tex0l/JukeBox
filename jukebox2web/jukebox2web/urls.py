from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from django.contrib import admin

from library_manager.views import Library


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'jukebox2web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', Library.as_view(),name='Library'),
)
