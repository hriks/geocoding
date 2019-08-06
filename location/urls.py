from django.urls import path

from location.views import Location, UploadGeoFile

urlpatterns = [
    path('upload/geofile', UploadGeoFile.as_view()),
    path('', Location.as_view())
]
