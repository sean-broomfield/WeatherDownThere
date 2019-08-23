from django.db import models
from django.utils import timezone


# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=255, default='')
    artistId = models.CharField(max_length=255, unique=True)
    genre = models.CharField(max_length=255, default='')
    image = models.URLField(default='')

    def __str__(self):
        return self.name


class Event(models.Model):
    performer = models.ForeignKey(Artist, on_delete=models.CASCADE)
    venueLoc = models.CharField(max_length=255)
    venueId = models.CharField(max_length=255, default='')
    eventId = models.CharField(max_length=255, default='')
    date = models.DateTimeField(default=timezone.now())
    url = models.URLField(default='')
    seatMap = models.URLField(default='')

    def __str__(self):
        return f"{self.performer} @ {self.venueLoc}"


class Venue(models.Model):
    VenueName = models.CharField(max_length=255)
    VenueId = models.CharField(max_length=255, unique=True)
    Event = models.ManyToManyField(Event)
    city = models.CharField(max_length=255, default='')
    state = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=255, default='')
    image = models.URLField(default='')
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    def __str__(self):
        return self.VenueName


class Weather(models.Model):
    concert = models.ForeignKey(Event, on_delete=models.CASCADE)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    def __str__(self):
        return f"{self.concert.performer.name} @ {self.concert.venueLoc}"
