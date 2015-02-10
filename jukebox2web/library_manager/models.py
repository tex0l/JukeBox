# -*- coding: utf-8 -*-
from django.db import models
import os


class Music(models.Model):
    title = models.CharField('title', max_length=100)
    artist = models.CharField('artist', max_length=100)
    file_field = models.FileField(upload_to="Library", storage="media")


class Index(models.Model):
    letter = models.IntegerField('letter')
    number = models.IntegerField('number')

    def __eq__(self, other):
        return other.letter == self.letter and other.number == self.number