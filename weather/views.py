from django.shortcuts import render
from django.utils import timezone
import requests
from weather import api
from weather.helper import baseUrls
from weather.models import Artist, Event, Venue


# Returns all music events at the venue id
# https://app.ticketmaster.com/discovery/v2/events.json?classificationName=music&size=5&venueId=KovZpZA7AAEA

# Returns all music events where tyler is a  keyword at the venue id and sorts by date
# https://app.ticketmaster.com/discovery/v2/events.json?classificationName=music&keyword=tyler&sort=date,asc&venueId=KovZpZA7AAEA

def home(request):
    if request.method == 'POST':
        if request.POST['options'] == "1" and request.POST['searchQuery']:
            r = requests.get(f"{baseUrls.TMART}"
                             f"&keyword={request.POST['searchQuery']}"
                             f"&apikey={api.tmaccess()}").json()
            if r['page']['totalElements'] == 0:
                return render(request, 'weather/home.html', {'error': 'No search results found!'})
            elif r['page']['totalElements'] == 1:
                result = r['_embedded']['attractions'][0]
                obj, created = Artist.objects.get_or_create(
                    name=result['name'],
                    artistId=result['id'],
                    genre=result['classifications'][0]['genre']['name'],
                    image=result['images'][0]['url']
                )
                return artistdetails(request, obj.artistId)
            else:
                return render(request, 'weather/search.html',
                              {'searchResults': r['_embedded']['attractions'],
                               'searchType': request.POST['options'],
                               'searchQuery': request.POST['searchQuery']})
            ######################################################
        elif request.POST['options'] == "2" and request.POST['searchQuery']:
            print(request.POST['options'])
            r = requests.get(f"{baseUrls.TMVEN}"
                             f"&keyword={request.POST['searchQuery']}"
                             f"&apikey={api.tmaccess()}").json()
            if r['page']['totalElements'] == 0:
                print("0")
                return render(request, 'weather/home.html', {'error': 'No search results found!'})
            #######################################################
            elif r['page']['totalElements'] == 1:
                result = r['_embedded']['venues'][0]
                obj, created = Venue.objects.get_or_create(
                    VenueName=result['name'],
                    VenueId=result['id'],
                    city=result['city']['name'],
                    state=result['state']['name'],
                    address=result['address']['line1'],
                    image=result['images'][0]['url'],
                    latitude=result['location']['latitude'],
                    longitude=result['location']['longitude']
                )
                return render(request, 'weather/venuedetails.html', {'venue': Venue.objects.get(VenueId=obj.VenueId)})
            else:
                return render(request, 'weather/search.html',
                              {'searchResults': r['_embedded']['venues'],
                               'searchType': request.POST['options'],
                               'searchQuery': request.POST['searchQuery']})
    return render(request, 'weather/home.html')


def search(request):
    return render(request, 'weather/search.html')


def artistdetails(request, artist_id):
    if request.method == "POST":
        # get date, check db for those after date, api request for
        time = timezone.now()
        
    if Artist.objects.filter(artistId=artist_id).exists():
        return render(request, 'weather/artistdetails.html',
                      {'artist': Artist.objects.get(artistId=artist_id),
                       'events': Event.objects.filter(performer__artistId__exact=artist_id)})
    r = requests.get(f"{baseUrls.TMART}"
                     f"&id={artist_id}"
                     f"&apikey={api.tmaccess()}").json()
    result = r['_embedded']['attractions'][0]
    newArtist = Artist.objects.create(
        name=result['name'],
        artistId=result['id'],
        genre=result['classifications'][0]['genre']['name'],
        image=result['images'][0]['url']
    )
    return render(request, 'weather/artistdetails.html',
                  {'artist': newArtist, 'events': Event.objects.filter(performer__artistId__exact=artist_id)})


def eventdetails(request, event_id):
    event = Event.objects.get(eventId=event_id)
    return render(request, 'weather/eventdetails.html', {'event': event})


def venuedetails(request, venue_id):
    if Venue.objects.filter(VenueId__exact=venue_id).exists():
        return render(request, 'weather/venuedetails.html',
                      {'events': Event.objects.filter(venueId=venue_id),
                       'venue': Venue.objects.get(VenueId__exact=venue_id)})
    r = requests.get(f"{baseUrls.TMVEN}"
                     f"&id={venue_id}"
                     f"&apikey={api.tmaccess()}").json()
    result = r['_embedded']['venues'][0]
    newVenue = Venue.objects.create(
        VenueName=result['name'],
        VenueId=result['id'],
        city=result['city']['name'],
        state=result['state']['name'],
        address=result['address']['line1'],
        image=result['images'][0]['url'],
        latitude=result['location']['latitude'],
        longitude=result['location']['longitude']
    )
    return render(request, 'weather/venuedetails.html', {'events': Event.objects.filter(venueId__exact=venue_id),
                                                         'venue': newVenue})
