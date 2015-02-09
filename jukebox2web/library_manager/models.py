from __future__ import unicode_literals
from django.db import models
import os


class Music(models.Model):
    title = models.CharField('title', max_length=100)
    artist = models.CharField('artist', max_length=100)
    file_field = models.FileField(unique=True)


class Index(models.Model):
    letter = models.IntegerField('letter')
    number = models.IntegerField('number')

    def __eq__(self, other):
        return other.letter == letter and other.number == number

