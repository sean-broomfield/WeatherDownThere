from django.db import models
from django.utils import timezone


# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name


class Event(models.Model):
    performer = models.ForeignKey(Artist, on_delete=models.CASCADE)
    venueLoc = models.CharField(max_length=255)
    date = models.DateField(default=timezone.now())

    def __str__(self):
        return f"{self.performer} @ {self.venueLoc}"


class Venue(models.Model):
    VenueName = models.CharField(max_length=255)
    VenueId = models.CharField(max_length=255)
    Event = models.ManyToManyField(Event)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    def __str__(self):
        return self.VenueName
