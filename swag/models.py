from django.db import models

# Create your models here.
class DownloadedSongs(models.Model):
    url = models.URLField()
