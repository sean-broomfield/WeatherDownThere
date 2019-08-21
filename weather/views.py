from django.shortcuts import render, redirect
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
            # ZERO RESULT
            if r['page']['totalElements'] == 0:
                return render(request, 'weather/home.html', {'error': 'No search results found!'})
            # ONE RESULT
            elif r['page']['totalElements'] == 1:
                result = r['_embedded']['attractions'][0]
                obj, created = Artist.objects.get_or_create(
                    name=result['name'],
                    artistId=result['id'],
                    genre=result['classifications'][0]['genre']['name'],
                    image=result['images'][0]['url']
                )
                return artistdetails(request, obj.artistId)
            # MULTIPLE RESULTS
            else:
                print("Multi")
                return render(request, 'weather/search.html',
                              {'searchResults': r['_embedded']['attractions'],
                               'searchQuery': request.POST['searchQuery']})
            ######################################################
        elif request.POST['options'] == "2" and request.POST['searchQuery']:
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
                    defaults={'latitude': float(result['location']['latitude']),
                              'longitude': float(result['location']['longitude'])}
                )
                return render(request, 'weather/detail.html', {'venue': Venue.objects.get(VenueId=obj.VenueId)})
            else:
                return render(request, 'weather/search.html',
                              {'searchResults': r['_embedded']['venues'], 'searchQuery': request.POST['searchQuery']})
    return render(request, 'weather/home.html')


def search(request):
    return render(request, 'weather/search.html')


def artistdetails(request, artist_id):
    return render(request, 'weather/artistdetails.html',
                  {'artist': Artist.objects.get(artistId=artist_id),
                   'events': Event.objects.filter(performer__artistId__exact=artist_id)})


def detail(request):
    return render(request, 'weather/detail.html')
