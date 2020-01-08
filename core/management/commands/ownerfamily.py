from django.core.management.base import BaseCommand

import pandas as pd

from core.models import Province, District, HouseHoldData, OwnerFamilyData

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
                owner = OwnerFamilyData.objects.create(
                    # province=Province.objects.get(
                    #     code=(df['Province_id'][row])),
                    #
                    # district=District.objects.get(
                    #     district_code=(df['District_id'][row])),
                    #
                    # name=(df['Name'][row]).capitalize().strip(),
                    #
                    # gn_type_en=(df['Type_en'][row]).capitalize().strip(),
                    #
                    # gn_type_np=(df['Type'][row]).capitalize().strip(),
                    index=df['index'][row],
                    parent_index=df['parent_index'][row],
                    name=df['name'][row],
                    age_group=df['age_group'][row],
                    gender=df['gender'][row],
                    citizenship_number=df['citizenship_number'][row],
                    education_level=df['education_level'][row],
                    occupation=df['occupation'][row],
                    occupation_other=df['occupation_other'][row],
                    working_status=df['working_status'][row],
                    monthly_income=df['monthly_income'][row],
                    falling_under_social_security_criteria=df['falling_under_social_security_criteria'][row],
                    social_security_received=df['social_security_received'][row],
                    reasons_for_not_received_social_security=df['reason_for_not_received_social_security'][row],
                    other_reasons_for_not_received_social_security=df['other_reason_for_not_received_social_security'][row],
                    status_of_family_member=df['status_of_family_member'][row],
                    status_of_family_member_other=df['status_of_family_member_other'][row],
                    disability_type=df['disability_type'][row],
                    disability_type_other=df['disability_type_other'][row],
                    chronic_illness=df['chronic_illness'][row],
                    chronic_illness_other=df['chronic_illness_other'][row],
                    survey=HouseHoldData.objects.get(index=df['parent_index'][row]),

                    # boundary=GEOSGeometry(df['geom'][row]),
                    # p_code=df['ADMIN2P_CODE'][row],

                )

                print(row, 'Data was successfully updated')

            except Exception as e:
                print(e)








