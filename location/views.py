from django.views import View
from django.shortcuts import render

from rest_framework import generics, permissions, exceptions

from location.serializer import GeoLocationSerializer
from django.db import transaction


class Location(View):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        pass


class UploadGeoFile(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = GeoLocationSerializer

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                serializer.save()
        except Exception as e:
            print(e)
            raise exceptions.APIException(
                'Error while reading file. Please verify uploaded file')
