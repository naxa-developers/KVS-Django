from django.core.management.base import BaseCommand

import pandas as pd

from core.models import Province, District, HouseHoldData

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

        try:
            house = [
                HouseHoldData(
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
                    deviceid=df['deviceid'][row],
                    date=df['date'][row],
                    surveyor_name=df['surveyor_name'][row],
                    place_name=df['place_name'][row],
                    # province=df['province'][row],
                    # district=df['province'][row],
                    # municipality=df['municipality'][row],


                    # boundary=GEOSGeometry(df['geom'][row]),
                    # p_code=df['ADMIN2P_CODE'][row],
                    ward=df['ward'][row],
                    house_number=df['house_number'][row],
                    latitude=df['latitude'][row],
                    longitude=df['longitude'][row],
                    altitude=df['altitude'][row],
                    gps_precision=df['gps_precision'][row],
                    household_number=df['household_number'][row],
                    owner_name=df['owner_name'][row],
                    owner_age=df['owner_age'][row],
                    owner_sex=df['owner_sex'][row],
                    owner_status=df['owner_status'][row],
                    owner_status_other=df['owner_status_other'][row],
                    owner_caste=df['owner_caste'][row],
                    owner_caste_other=df['owner_caste_other'][row],
                    religion=df['religion'][row],
                    religion_other=df['religion_other'][row],
                    mother_tongue=df['mother_tongue'][row],
                    mother_tongue_other=df['mother_tongue_other'][row],
                    contact_no=df['contact_no'][row],
                    owner_education=df['owner_education'][row],
                    owner_citizenship_no=df['owner_citizenship_no'][row],
                    responder_name=df['responder_name'][row],
                    responder_sex=df['responder_age'][row],
                    responder_contact=df['responder_contact'][row],
                    other_family_living=df['other_family_living'][row],
                    main_occupation=df['main_occupation'][row],
                    other_occupation=df['other_occupation'][row],
                    business=df['business'][row],
                    other_business=df['other_business'][row],
                    other_small_business=df['other_small_business'][row],
                    crop_sufficiency=df['crop_sufficiency'][row],
                    food_type=df['food_type'][row],
                    main_staple=df['main_staple'][row],
                    pulses=df['pulses'][row],
                    vegetables=df['vegetables'][row],
                    fruits=df['fruits'][row],
                    meat_and_fish=df['meat_and_fish'][row],
                    milk_and_products=df['milk_and_products'][row],
                    sugar_products=df['sugar_products'][row],
                    oil_products=df['oil_products'][row],
                    condiments=df['condiments'][row],
                    monthly_expenses=df['monthly_expenses'][row],
                    monthly_income=df['monthly_income'][row],
                    loan=df['loan'][row],
                    loan_amount=df['loan_amount'][row],
                    loan_duration=df['loan_duration'][row],
                    animal_presence=df['animal_presence'][row],
                    insurance=df['insurance'][row],
                    other_insurance=df['other_insurance'][row],
                    vehicle=df['vehicle'][row],
                    vehicles_other=df['vehicles_other'][row],
                    facilities_type=df['facilities_type'][row],
                    other_facilities=df['other_facilities'][row],
                    fuel_type=df['fuel_type'][row],
                    other_fuel_type=df['other_fuel_type'][row],
                    land_ownership=df['land_ownership'][row],
                    house_type=df['house_type'][row],
                    house_type_other=df['house_type_other'][row],
                    house_built_year=df['house_built_year'][row],
                    house_stories=df['house_stories'][row],
                    no_of_rooms=df['no_of_rooms'][row],
                    house_map_registered=df['house_map_registered'][row],
                    building_standard_code=df['building_standard_code'][row],
                    earthquake_resistance=df['earthquake_resistance'][row],
                    flood_prone=df['flood_prone'][row],
                    flood_resilience_activities=df['flood_resilience_activities'][row],
                    flood_activities_resilience_other=df['flood_activities_resilience_other'][row],
                    owned_land_area=df['owned_land_area'][row],
                    owned_land_near_river=df['owned_land_near_river'][row],
                    owned_land_area_near_river=df['owned_land_area_near_river'][row],
                    owned_land_image=df['owned_land_image'][row],
                    technical_manpower_presence=df['technical_manpower_presence'][row],
                    manpower_type=df['manpower_type'][row],
                    doctor_sex=df['doctor_sex'][row],
                    doctor_male_number=df['doctor_male_number'][row],
                    doctor_female_number=df['doctor_female_number'][row],
                    engineer_sex=df['engineer_sex'][row],
                    engineer_male_number=df['engineer_male_number'][row],
                    engineer_female_number=df['engineer_female_number'][row],

                ) for row in range(0, upper_range)

            ]

            district_data = HouseHoldData.objects.bulk_create(house)

            if district_data:
                self.stdout.write('Successfully  updated data ..')

        except Exception as e:
            print(e)

