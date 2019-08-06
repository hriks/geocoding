from rest_framework import serializers

from location.models import GeoLocation


class GeoLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = GeoLocation
        fields = ('geofile',)

    @property
    def data(self):
        return dict(
            data=self.instance.create_coordinate_file(),
            filepath=self.instance.coordinate_file.url)
