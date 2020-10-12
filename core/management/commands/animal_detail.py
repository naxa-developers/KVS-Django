from django.core.management.base import BaseCommand

import pandas as pd

from core.models import Province, District, HouseHoldData, OwnerFamilyData, AnimalDetailData

from django.contrib.gis.geos import GEOSGeometry


class Command(BaseCommand):
    help = 'load AnimalDetail data from .xlsx file'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        df = pd.read_excel(path, sheet_name=2)
        upper_range = len(df)

        print("Wait Data is being Loaded")

        for row in range(0, upper_range):
            try:
                animal = AnimalDetailData.objects.create(
                    index=df['index'][row],
                    parent_index=df['parent_index'][row],
                    animal_type=df['animal_type'][row],
                    animal_number=df['animal_number'][row],
                    is_it_for_commercial_purpose=df['is_it_for_commercial_purpose'][row],
                    survey=HouseHoldData.objects.filter(index=df['parent_index'][row])[0],

                )

                print(row, 'Data was successfully updated')

            except Exception as e:
                print(e)




