from django.urls import path
from . import views

urlpatterns = [
    path('detail', views.detail, name="detail"),
    path('search', views.search, name="search"),
]
