from django.urls import path
from . import views

urlpatterns = [
    path('venue/<str:venue_id>', views.venuedetails, name="venuedetails"),
    path('artist/<str:artist_id>', views.artistdetails, name="artistdetails"),
    path('<str:event_id>', views.eventdetails, name="eventdetails"),
    path('search', views.search, name="search"),
]
