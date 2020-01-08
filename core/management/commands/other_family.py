from django.core.management.base import BaseCommand

import pandas as pd

from core.models import Province, District, HouseHoldData, OwnerFamilyData, OtherFamilyMember

from django.contrib.gis.geos import GEOSGeometry


class Command(BaseCommand):
    help = 'load province data from province.xlsx file'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        df = pd.read_csv(path)
        upper_range = len(df)

        print("Wait Data is being Loaded")

        for row in range(0, upper_range):
            try:
                animal = OtherFamilyMember.objects.create(
                    index=df['index'][row],
                    parent_index=df['parent_index'][row],
                    other_family_numbers=df['other_family_numbers'][row],
                    females_less_then_5_years=df['females_less_than_5_years'][row],
                    males_less_then_5_years=df['males_less_than_5_years'][row],
                    females_between_5_to_15_years=df['females_between_5_to_15_years'][row],
                    males_between_5_to_15_years=df['males_between_5_to_15_years'][row],
                    females_between_16_to_59_years=df['females_between_16_to_59_years'][row],
                    males_between_16_to_59_years=df['males_between_16_to_59_years'][row],
                    females_between_60_to_70_years=df['females_between_60_to_70_years'][row],
                    males_between_60_to_70_years=df['males_between_60_to_70_years'][row],
                    females_above_70_years=df['females_above_70_years'][row],
                    males_above70_years=df['males_above_70_years'][row],
                    total_persons=df['total_persons'][row],
                    pregnant_number=df['pregnant_number'][row],
                    disabled=df['disabled'][row],
                    disablility_type=df['disability_type'][row],
                    disablility_type_other=df['disability_type_other'][row],
                    survey=HouseHoldData.objects.get(index=df['parent_index'][row]),

                )

                print(row, 'Data was successfully updated')

            except Exception as e:
                print(e)

