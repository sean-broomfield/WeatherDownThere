from django.shortcuts import render
from django.utils import timezone
import requests
import time
from weather import api
from weather.helper import baseUrls
from weather.helper import creators
from weather.models import Artist, Event, Venue, Weather


# ARTIST TO EVENTS TO VENUES

def home(request):
    if request.method == 'POST':
        ########## ARTIST SEARCH #############
        if request.POST['options'] == "1" and request.POST['searchQuery']:
            r = creators.search_artist_by_keyword(request.POST['searchQuery'])
            if r['page']['totalElements'] == 0:
                return render(request, 'weather/home.html', {'error': 'No search results found!'})
            elif r['page']['totalElements'] == 1:
                artist, artist_created = creators.create_artist(r['_embedded']['attractions'][0])
                search_result = creators.search_event_by_artist(artist.artistId, 5)
                if search_result['page']['totalElements'] > 0:
                    for result in search_result['_embedded']['events']:
                        event, event_created = creators.create_event(result, artist.artistId)
                        venue, venue_created = creators.create_venue(result['_embedded']['venues'][0])
                return render(request, 'weather/artistdetails.html',
                              {'artist': artist,
                               'events': Event.objects.filter(performer__artistId__exact=artist.artistId)})
            else:
                return render(request, 'weather/search.html',
                              {'searchResults': r['_embedded']['attractions'],
                               'searchType': request.POST['options'],
                               'searchQuery': request.POST['searchQuery']})
        ########## VENUE SEARCH #############
        elif request.POST['options'] == "2" and request.POST['searchQuery']:
            r = creators.search_venue_by_keyword(request.POST['searchQuery'])
            if r['page']['totalElements'] == 0:
                return render(request, 'weather/home.html', {'error': 'No search results found!'})
            elif r['page']['totalElements'] == 1:
                venue, venue_created = creators.create_venue(r['_embedded']['venues'][0])
                search_result = creators.search_event_by_venue(venue.VenueId)
                if search_result['page']['totalElements'] > 0:
                    for result in search_result['_embedded']['events']:
                        artist, artist_created = creators.create_artist(result['_embedded']['attractions'][0])
                        event, event_created = creators.create_event(result, artist.artistId)
                return render(request, 'weather/venuedetails.html',
                              {'venue': venue, 'events': Event.objects.filter(venueId__exact=venue.VenueId)})
            else:
                return render(request, 'weather/search.html',
                              {'searchResults': r['_embedded']['venues'],
                               'searchType': request.POST['options'],
                               'searchQuery': request.POST['searchQuery']})
    return render(request, 'weather/home.html', {'events': Event.objects.all()[:6]})


def search(request):
    return render(request, 'weather/search.html')


def artistdetails(request, artist_id):
    if Artist.objects.filter(artistId=artist_id).exists():
        num = Event.objects.filter(performer__artistId__exact=artist_id).count()
        if num == 5:
            return render(request, 'weather/artistdetails.html',
                          {'artist': Artist.objects.get(artistId=artist_id),
                           'events': Event.objects.filter(performer__artistId__exact=artist_id)})
        else:
            left = 5 - num
            r = creators.search_event_by_artist(artist_id, left)
            if r['page']['totalElements'] > 0:
                for result in r['_embedded']['events']:
                    event, event_created = creators.create_event(result, artist_id)
                    venue, venue_created = creators.create_venue(result['_embedded']['venues'][0])
            return render(request, 'weather/artistdetails.html', {'artist': Artist.objects.get(artistId=artist_id),
                                                                  'events': Event.objects.filter(
                                                                      performer__artistId__exact=artist_id)})
    elif not Artist.objects.filter(artistId=artist_id).exists():
        r = creators.search_artist_by_id(artist_id)
        new_artist, created = creators.create_artist(r['_embedded']['attractions'][0])
        # Grab events
        num = Event.objects.filter(performer__artistId__exact=artist_id).count()
        r = creators.search_event_by_artist(artist_id, 5 - num)
        if r['page']['totalElements'] > 0:
            for result in r['_embedded']['events']:
                event, event_created = creators.create_event(result, artist_id)
                venue, venue_created = creators.create_venue(result['_embedded']['venues'][0])
        return render(request, 'weather/artistdetails.html',
                      {'artist': new_artist, 'events': Event.objects.filter(performer__artistId__exact=artist_id)})


def eventdetails(request, event_id):
    event = Event.objects.get(eventId=event_id)
    # Venue doesn't exist in database so search for and create the data.
    if not Venue.objects.filter(VenueId__exact=event.venueId).exists():
        r = creators.search_venue_by_id(event.venueId)
        venue, venue_created = creators.create_venue(r['_embedded']['venues'][0])

    # Venue exists, so request weather data based on venue. #
    r = creators.search_weather_by_coordinates(Venue.objects.get(VenueId__exact=event.venueId))
    weather, weather_created = creators.update_or_create_weather(r, event)
    return render(request, 'weather/eventdetails.html',
                  {'event': event, 'weather': weather})


def venuedetails(request, venue_id):
    # Venue exists in DB
    if Venue.objects.filter(VenueId__exact=venue_id).exists():
        return render(request, 'weather/venuedetails.html',
                      {'events': Event.objects.filter(venueId=venue_id),
                       'venue': Venue.objects.get(VenueId__exact=venue_id)})

    # Venue does NOT exist in DB
    r = creators.search_venue_from_details(venue_id)
    venue, venue_created = creators.create_venue(r)

    # Get venue events
    r = creators.search_event_by_venue(venue.VenueId)
    if r['page']['totalElements'] > 0:
        for result in r['_embedded']['events']:
            artist, artist_created = creators.create_artist(result['_embedded']['attractions'][0])
            event, event_created = creators.create_event(result, artist.artistId)
    return render(request, 'weather/venuedetails.html', {'events': Event.objects.filter(venueId=venue.VenueId),
                                                         'venue': venue})
