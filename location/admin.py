from django.contrib import admin

from location.models import GeoLocation


@admin.register(GeoLocation)
class GeoLocation(admin.ModelAdmin):
    list_display = ('geofile', 'coordinate_file')
