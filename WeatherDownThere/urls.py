from django.contrib import admin
from django.urls import path, include
from weather import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('event/', include('weather.urls')),
]
