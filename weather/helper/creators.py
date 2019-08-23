from django.shortcuts import render
from weather.models import Artist, Event, Venue
import time


def createArtist(request, result):
    if result['page']['totalElements'] == 0:
        return render(result, 'weather/home.html', {'error': 'No search results found!'})
    elif result['page']['totalElements'] == 1:
        # Create artist, Grab Events, Create Venues
        result = result['_embedded']['attractions'][0]
        obj, created = Artist.objects.get_or_create(
            name=result['name'],
            artistId=result['id'],
            genre=result['classifications'][0]['genre']['name'],
            image=result['images'][0]['url']
        )
        time.sleep(1)
    else:
        return render(request, 'weather/search.html', {'searchResults': result['_embedded']['attractions'],
                                                       'searchType': request.POST['options'],
                                                       'searchQuery': request.POST['searchQuery']})
