# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',
    (r'^', include('library_manager.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)
