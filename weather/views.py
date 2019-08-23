from django.shortcuts import render
from django.utils import timezone
import requests
import time
from weather import api
from weather.helper import baseUrls
from weather.models import Artist, Event, Venue, Weather


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
                # FIX THIS - API LIMIT
                time.sleep(1)
                return artistdetails(request, obj.artistId)
            else:
                return render(request, 'weather/search.html',
                              {'searchResults': r['_embedded']['attractions'],
                               'searchType': request.POST['options'],
                               'searchQuery': request.POST['searchQuery']})
            ######################################################
        elif request.POST['options'] == "2" and request.POST['searchQuery']:
            print(request.POST['options'])
            time.sleep(1)
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
    if request.method == "POST" and Artist.objects.filter(artistId=artist_id).exists():
        num = Event.objects.filter(performer__artistId__exact=artist_id).count()
        if num == 5:
            print(5)
            return render(request, 'weather/artistdetails.html',
                          {'artist': Artist.objects.get(artistId=artist_id),
                           'events': Event.objects.filter(performer__artistId__exact=artist_id)})
        else:
            print("Less than 5")
            print(artist_id)
            left = 5 - num
            time.sleep(1)
            r = requests.get(f"{baseUrls.TMEVENT}"
                             f"{artist_id}"
                             f"&size={left}"
                             f"&apikey={api.tmaccess()}").json()
            if r['page']['totalElements'] > 0:
                results = r['_embedded']['events']
                for result in results:
                    Event.objects.create(
                        performer=Artist.objects.get(artistId=artist_id),
                        venueLoc=result['_embedded']['venues'][0]['name'],
                        venueId=result['_embedded']['venues'][0]['id'],
                        eventId=result['id'],
                        date=result['dates']['start']['dateTime'],
                        url=result['url'],
                        # seatMap=result['seatmap']['staticUrl']
                    ).save()
            return render(request, 'weather/artistdetails.html', {'artist': Artist.objects.get(artistId=artist_id),
                                                                  'events': Event.objects.filter(
                                                                      performer__artistId__exact=artist_id)})
    elif not Artist.objects.filter(artistId=artist_id).exists():
        time.sleep(1)
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
        # Grab events
        time.sleep(1)
        num = Event.objects.filter(performer__artistId__exact=artist_id).count()
        r = requests.get(f"{baseUrls.TMEVENT}"
                         f"{artist_id}"
                         f"&size={5 - num}"
                         f"&apikey={api.tmaccess()}").json()
        if r['page']['totalElements'] > 0:
            results = r['_embedded']['events']
            for result in results:
                Event.objects.create(
                    performer=Artist.objects.get(artistId=artist_id),
                    venueLoc=result['_embedded']['venues'][0]['name'],
                    venueId=result['_embedded']['venues'][0]['id'],
                    eventId=result['id'],
                    date=result['dates']['start']['dateTime'],
                    url=result['url'],
                    # seatMap=result['seatmap']['staticUrl']
                ).save()
                time.sleep(1)
                r = requests.get(f"{baseUrls.TMVEN}"
                                 f"&id={result['_embedded']['venues'][0]['id']}"
                                 f"&apikey={api.tmaccess()}").json()
                result = r['_embedded']['venues'][0]
                obj, newVenue = Venue.objects.get_or_create(
                    VenueName=result['name'],
                    VenueId=result['id'],
                    city=result['city']['name'],
                    state=result['state']['name'],
                    address=result['address']['line1'],
                    image=result['images'][0]['url'],
                    latitude=result['location']['latitude'],
                    longitude=result['location']['longitude']
                ).save()
        return render(request, 'weather/artistdetails.html',
                      {'artist': newArtist, 'events': Event.objects.filter(performer__artistId__exact=artist_id)})
    else:
        return render(request, 'weather/artistdetails.html', {'artist': Artist.objects.get(artistId=artist_id),
                                                              'events': Event.objects.filter(
                                                                  performer__artistId=artist_id)})


def eventdetails(request, event_id):
    event = Event.objects.get(eventId=event_id)
    time.sleep(1)
    if not Venue.objects.filter(VenueId__exact=event.venueId).exists():
        r = requests.get(f"{baseUrls.TMVEN}"
                         f"&id={event.venueId}"
                         f"&apikey={api.tmaccess()}").json()
        result = r['_embedded']['venues'][0]
        obj, created = Venue.objects.update_or_create(
            VenueName=result['name'],
            VenueId=result['id'],
            city=result['city']['name'],
            state=result['state']['name'],
            address=result['address']['line1'],
            image='',
            latitude=result['location']['latitude'],
            longitude=result['location']['longitude']
        )

    # request weather data based on venue
    time.sleep(1)
    r = requests.get(f"{baseUrls.OWAPI}"
                     f"&lat={Venue.objects.get(VenueId__exact=event.venueId).latitude}"
                     f"&lon={Venue.objects.get(VenueId__exact=event.venueId).longitude}"
                     f"&appid={api.owaccess()}").json()

    if Weather.objects.filter(weatherId=f"{event.eventId}"f"{event.performer.artistId}").exists():
        Weather.objects.filter(weatherId=f"{event.eventId}"f"{event.performer.artistId}").update(
            description=r['weather'][0]['description'],
            temphi=r['main']['temp_max'],
            templow=r['main']['temp_min'],
            icon=f"http://openweathermap.org/img/wn/"f"{r['weather'][0]['icon']}"f"@2x.png")
    else:
        Weather.objects.create(
            concert=event,
            eventId=event.eventId,
            description=r['weather'][0]['description'],
            weatherId=f"{event.eventId}"f"{event.performer.artistId}",
            temphi=r['main']['temp_max'],
            templow=r['main']['temp_min'],
            icon=f"http://openweathermap.org/img/wn/"f"{r['weather'][0]['icon']}"f"@2x.png"
        ).save()
    return render(request, 'weather/eventdetails.html',
                  {'event': event, 'weather': Weather.objects.get(eventId=event.eventId)})


def venuedetails(request, venue_id):
    # Venue exists in DB
    if Venue.objects.filter(VenueId__exact=venue_id).exists():
        return render(request, 'weather/venuedetails.html',
                      {'events': Event.objects.filter(venueId=venue_id),
                       'venue': Venue.objects.get(VenueId__exact=venue_id)})
    # Venue does NOT exist in DB
    time.sleep(1)
    r = requests.get(f"{baseUrls.TMVEN}"
                     f"&id={venue_id}"
                     f"&apikey={api.tmaccess()}").json()
    result = r['_embedded']['venues'][0]
    venRes = result['id']
    newVenue = Venue.objects.create(
        VenueName=result['name'],
        VenueId=result['id'],
        city=result['city']['name'],
        state=result['state']['name'],
        address=result['address']['line1'],
        image=result['images'][0]['url'],
        latitude=result['location']['latitude'],
        longitude=result['location']['longitude']
    ).save()
    time.sleep(1)
    # get venue events
    r = requests.get(f"{baseUrls.TMEVENT2}"
                     f"&size=5"
                     f"&venueId={result['id']}"
                     f"&apikey={api.tmaccess()}").json()
    if r['page']['totalElements'] > 0:
        results = r['_embedded']['events']
        for event in results:
            # Check if artists exist if not then create, then create Event
            if not Artist.objects.filter(artistId=event['_embedded']['attractions'][0]['id']).exists():
                # Doesnt exist create object
                Artist.objects.create(
                    name=event['_embedded']['attractions'][0]['name'],
                    artistId=event['_embedded']['attractions'][0]['id'],
                    genre=event['_embedded']['attractions'][0]['classifications'][0]['genre'],
                    image=event['_embedded']['attractions'][0]['images'][0]['url']
                ).save()
            # Performer already exists
            obj, created = Event.objects.get_or_create(
                performer=Artist.objects.get(artistId=event['_embedded']['attractions'][0]['id']),
                venueLoc=event['_embedded']['venues'][0]['name'],
                venueId=event['_embedded']['venues'][0]['id'],
                eventId=event['id'],
                date=event['dates']['start']['dateTime'],
                url=event['url'],
                # seatMap=result['seatmap']['staticUrl']
            )
    print(venRes)
    return render(request, 'weather/venuedetails.html', {'events': Event.objects.filter(venueId=venRes),
                                                         'venue': Venue.objects.filter(VenueId=venRes)})
