from django.shortcuts import render
import requests
from weather import api


def home(request):
    if request.method == 'POST':
        print(request.POST['searchQuery'])
        print(request.POST['options'])
    # r = requests.get(
    #     f"https://app.ticketmaster.com/discovery/v2/events.json?size=3&radius=2&unit=miles&venueId=KovZpZA7AAEA&apikey="
    #     f"{api.tmaccess()}")
    # response = r.json()
    return render(request, 'weather/home.html')


def detail(request):
    return render(request, 'weather/detail.html')
