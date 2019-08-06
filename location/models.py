from django.db import models


class GeoLocation(models.Model):
    geofile = models.FileField()
    coordinate_file = models.FileField(null=True, blank=True)

    def read_geofile(self):
        import xlrd
        workbook = xlrd.open_workbook(self.geofile.file.name)
        worksheet = workbook.sheet_by_index(0)
        first_row = list()
        for col in range(worksheet.ncols):
            first_row.append(worksheet.cell_value(0, col))
        data = list()
        for row in range(1, worksheet.nrows):
            elm = dict()
            for col in range(worksheet.ncols):
                elm[first_row[col]] = worksheet.cell_value(row, col)
            data.append(elm)
            elm.update(self.get_coordinates(elm['address']))
        return data

    def get_coordinates(self, address):
        import requests
        from geocoding.settings import GMAPS_API_KEY
        endpoint = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' % (address, GMAPS_API_KEY) # noqa
        r = requests.get(endpoint).json()
        return r['results'][0]['geometry']['location']

    def create_coordinate_file(self):
        import xlsxwriter
        filename = 'media/%s_coordinate.xlsx' % self.geofile.name.split('.')[0]
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()
        col = 0
        worksheet.write(0, col, "Address")
        worksheet.write(0, col + 1, "Lat")
        worksheet.write(0, col + 2, "Lng")
        row = 1
        data = self.read_geofile()
        for _ in data:
            worksheet.write(row, col, _['address'])
            worksheet.write(row, col + 1, _['lat'])
            worksheet.write(row, col + 2, _['lng'])
            row += 1
        workbook.close()
        self.coordinate_file.name = '%s_coordinate.xlsx' % (
            self.geofile.name.split('.')[0])
        self.save()
        return data
