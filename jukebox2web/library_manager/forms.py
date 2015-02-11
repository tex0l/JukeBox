# -*- coding: utf-8 -*-
from django import forms
from . import models
from . import fields

class MusicForm(forms.Form):
    file_field = fields.RestrictedFileField(content_types=['audio'], help_text="Select a file", label="Upload a music")
    class Meta:
        model = models.Music
        fields = ['file_field']