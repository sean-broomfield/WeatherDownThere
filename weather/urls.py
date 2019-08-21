from django.urls import path
from . import views

urlpatterns = [
    path('detail', views.detail, name="detail"),
    path('artist/<str:artist_id>', views.artistdetails, name="artistdetails"),
    path('search', views.search, name="search"),
]
