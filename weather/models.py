from django.db import models


# Create your models here.
class Event(models.Model):
    artist = models.CharField(max_length=255)
    venue = models.CharField(max_length=255)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    def __str__(self):
        return self.artist + ": " + self.venue
