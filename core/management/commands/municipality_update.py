from django.core.management.base import BaseCommand

import pandas as pd

from core.models import Municipality

from django.contrib.gis.geos import GEOSGeometry


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        print("Wait Data is being Loaded")

        municipalities = Municipality.objects.all()

        for municipality in municipalities:
            province = municipality.district.province
            municipality.province = province
            municipality.save()

        print('Successfully updated municipality')



