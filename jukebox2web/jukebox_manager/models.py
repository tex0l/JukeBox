from django.db import models
from library_manager.models import Music
from django.conf import settings
# Create your models here.
class PlayList(models.Model):
    name = models.CharField(name='name', max_length='100', default='My Playlist')
    is_current = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True, editable=False)

    @staticmethod
    def get_or_create_current():
        current_playlist = PlayList.objects.filter(is_current=True)
        if current_playlist:
            return current_playlist
        current_playlist = PlayList(is_current=True)
        current_playlist.save()
        return current_playlist

class Index(models.Model):
    letter = models.IntegerField(name='letter')
    number = models.IntegerField(name='number')
    music = models.ForeignKey('library_manager.Music', null=True, blank=True)
    date_added = models.DateTimeField(auto_now=True, editable=False)

    def __eq__(self, other):
        return other.letter == self.letter and other.number == self.number


