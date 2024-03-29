from weather.models import Artist, Event, Venue, Weather
from weather import api
from weather.helper import baseUrls
import requests
import time


######### Artist Functions ########### ###################################### ######################################

def search_artist_by_keyword(artist_query):
    time.sleep(1)
    return requests.get(f"{baseUrls.TM_ARTIST}"
                        f"&keyword={artist_query}"
                        f"&apikey={api.tmaccess()}").json()


def search_artist_by_id(art_id):
    time.sleep(1)
    return requests.get(f"{baseUrls.TM_ARTIST}"
                        f"&id={art_id}"
                        f"&apikey={api.tmaccess()}").json()


def create_artist(result):
    print(f"Create! {result['name']}"
          f"{result['id']}"
          f"{result['classifications'][0]['genre']['name']}"
          f"{result['images'][0]['url']}")
    obj, created = Artist.objects.get_or_create(
        name=result['name'],
        artistId=result['id'],
        genre=result['classifications'][0]['genre']['name'],
        image=result['images'][0]['url']
    )
    return obj, created


######### Venue Functions ########### ###################################### ######################################

def search_venue_by_keyword(venue_query):
    time.sleep(1)
    return requests.get(f"{baseUrls.TM_VENUE}"
                        f"&keyword={venue_query}"
                        f"&apikey={api.tmaccess()}").json()


def search_venue_by_id(venue_id):
    time.sleep(1)
    return requests.get(f"{baseUrls.TM_VENUE}"
                        f"&id={venue_id}"
                        f"&apikey={api.tmaccess()}").json()


def create_venue(result):
    obj, created = Venue.objects.get_or_create(
        VenueName=result['name'],
        VenueId=result['id'],
        city=result['city']['name'],
        state=result['state']['name'],
        address=result['address']['line1'],
        # image=result['images'][0]['url'],
        image='',
        latitude=result['location']['latitude'],
        longitude=result['location']['longitude']
    )
    return obj, created


def search_venue_from_details(venue_id):
    time.sleep(1)
    return requests.get(f"{baseUrls.NEW_VEN}"
                        f"{venue_id}?locale=en-us"
                        f"&countrycode=us"
                        f"&apikey={api.tmaccess()}").json()


######### Event Functions ########### ###################################### ######################################

def search_event_by_artist(artist_id, size):
    time.sleep(1)
    return requests.get(f"{baseUrls.TM_EVENT}"
                        f"{artist_id}"
                        f"&size={size}"
                        f"&apikey={api.tmaccess()}").json()


def search_event_by_venue(venue_id):
    time.sleep(1)
    return requests.get(f"{baseUrls.TM_EVENT_2}"
                        f"&size=5"
                        f"&venueId={venue_id}"
                        f"&apikey={api.tmaccess()}").json()


def create_event(result, artist_id):
    print("Creating Event!")
    print(f"Artist id is {artist_id}")
    obj, created = Event.objects.get_or_create(
        performer=Artist.objects.get(artistId=artist_id),
        venueLoc=result['_embedded']['venues'][0]['name'],
        venueId=result['_embedded']['venues'][0]['id'],
        eventId=result['id'],
        date=result['dates']['start']['dateTime'],
        url=result['url'],
        # seatMap=result['seatmap']['staticUrl']
    )
    print("Done Creating!")
    return obj, created


######### Weather Functions ########### ###################################### ######################################

def search_weather_by_coordinates(venue):
    time.sleep(1)
    return requests.get(f"{baseUrls.OW_API}"
                        f"&lat={venue.latitude}"
                        f"&lon={venue.longitude}"
                        f"&appid={api.owaccess()}").json()


def update_or_create_weather(result, event):
    obj, created = Weather.objects.update_or_create(
        concert=event,
        eventId=event.eventId,
        weatherId=f"{event.eventId}"f"{event.performer.artistId}",
        defaults={'description': result['weather'][0]['description'],
                  'temphi': result['main']['temp_max'],
                  'templow': result['main']['temp_min'],
                  'icon': f"http://openweathermap.org/img/wn/"f"{result['weather'][0]['icon']}"f"@2x.png"}
    )
    return obj, created
