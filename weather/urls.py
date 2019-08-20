from django.urls import path
from . import views

urlpatterns = [
    path('detail', views.detail, name="detail"),
    path('detail2/<str:artist_id>', views.detail2, name="detail2"),
    path('search', views.search, name="search"),
]
