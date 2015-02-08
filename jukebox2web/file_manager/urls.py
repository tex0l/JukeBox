from __future__ import unicode_literals
from django.conf.urls import patterns, include, url

from file_manager import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)