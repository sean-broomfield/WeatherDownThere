from django.contrib import admin
from .models import Event, Artist, Venue

# Register your models here.
admin.site.register(Event)
admin.site.register(Artist)
admin.site.register(Venue)
