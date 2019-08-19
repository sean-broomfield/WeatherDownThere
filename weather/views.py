from django.shortcuts import render, redirect
import requests
from weather import api
from weather.helper import baseUrls
from weather.models import Artist, Event, Venue


# Returns all music events at the venue id
# https://app.ticketmaster.com/discovery/v2/events.json?classificationName=music&size=5&venueId=KovZpZA7AAEA

# Returns all music events where tyler is a  keyword at the venue id and sorts by date
# https://app.ticketmaster.com/discovery/v2/events.json?classificationName=music&keyword=tyler&sort=date,asc&venueId=KovZpZA7AAEA

# For artist search, if the list > 0 then return events sorted by name, date, with location embedded in view.
# For venue search, display list of venues and allow user to click one which will then take them to a different page
# to see all the events and weather?

# ARTIST
# if 0 elements
# pass error and redirect home.
# if 1 element
# open one element and go to details page
# if more than 1 element
# display search results and allow the user to select one.

def home(request):
    # if 1 and get text then search, then redirect to search results page
    if request.method == 'POST':
        if request.POST['options'] == "1" and request.POST['searchQuery']:
            r = requests.get(f"{baseUrls.TMART}"
                             f"&keyword={request.POST['searchQuery']}"
                             f"&sort=name,date,asc"
                             f"&apikey={api.tmaccess()}").json()
            if r['page']['totalElements'] == 0:
                return render(request, 'weather/home.html', {'error': 'No search results found!'})
            else:
                return render(request, 'weather/detail.html')
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
                print("1")
                result = r['_embedded']['venues'][0]
                obj, created = Venue.objects.get_or_create(
                    VenueName=result['name'],
                    VenueId=result['id'],
                    defaults={'latitude': float(result['location']['latitude']),
                              'longitude': float(result['location']['longitude'])}
                )
                return render(request, 'weather/detail.html', {'venue': Venue.objects.get(VenueId=obj.VenueId)})
            else:
                print("multi")
                return render(request, 'weather/search.html',
                              {'searchResults': r['_embedded']['venues'], 'searchQuery': request.POST['searchQuery']})
    return render(request, 'weather/home.html')


def search(request):
    return render(request, 'weather/search.html')


def detail(request):
    return render(request, 'weather/detail.html')
