from django.core.management.base import BaseCommand

import pandas as pd

from core.models import HouseHold, GenderList, OwnershipList, EthnicityList, ReligionList, MotherTongueList, \
    EducationList, Occupation, OccupationList, BusinessList, FoodChoice, FoodEaten, InsuranceList, Insurance, \
    Vehicle, VehicleList, FacilityList, Facilities , FuelTypeList, Fuel, WhoseOwnershipData, WhoseOwnershipList, \
    HouseType, HouseTypeList, WorkDoneOnFlood, WorkDoneOnFloodList, TechnicalField, TechnicalFieldList, RoadType, \
    RoadCapacity, RoadCapacityType, DrinkingWater, DrinkingWaterList, Latrine, LatrineList, DisasterList, \
    DisasterProne, InformationMedium, InformationMediumList, WarningMediumList, WarningMediumSuitableForDisaster, \
    MaterialsInNearestMarket, MaterialsInNearestMarketList, CopingMechanism, CopingMechanismList, \
    DisasterPreparednessMechanism, DisasterPreparednessMechanismList, InvolvedInSimulation, GuideLine, GuideLineList, \
    WardFallingProneArea, DamageType, DamageList, HouseDamageList

from django.contrib.gis.geos import Point


class Command(BaseCommand):
    help = 'load province data from province.xlsx file'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        df = pd.read_csv(path).fillna('')
        upper_range = len(df)

        print("Wait Data is being Loaded")

        for row in range(0, upper_range):
            try:

                gender = GenderList.objects.get(name=df['Sex_houseowner'][row])
                ownership = OwnershipList.objects.get(name=df['status_owner'][row])
                ethnicity = EthnicityList.objects.get(name=df['Caste_owner'][row])
                religion = ReligionList.objects.get(name=df['Religion'][row])
                mother_tongue = MotherTongueList.objects.get(name=df['Mother_tongue'][row])
                education_level = EducationList.objects.get(name=df['Education_owner'][row])
                responder_gender = GenderList.objects.get(name=df['Resp_Sex'][row])
                road_type = RoadType.objects.get(name=df['Road_type'][row])

                house_hold = HouseHold.objects.create(
                    index=df['index'][row],
                    start_date=df['start'][row],
                    end_date=df['start'][row],
                    surveyor_name=df['Name_surveyor'][row],
                    name_of_place=df['Place_name'][row],
                    ward_no=df['ward'][row],
                    location=Point(float(df['__6_GPS_coordinates_longitude'][row]), float(df['__6_GPS_coordinates_latitude'][row])),
                    altitude=df['__6_GPS_coordinates_altitude'][row],
                    precision=df['__6_GPS_coordinates_precision'][row],
                    household_no=df['Household_number'][row],
                    house_holder_name=df['Name_owner'][row],
                    age_of_owner=df['Age_owner'][row],
                    gender_of_house_owner=gender,
                    status_of_owner=ownership,
                    if_other_owner_status=df['_If_other_please_state_here'][row],
                    ethnicity=ethnicity,
                    other_ethnicity=df['caste_other'][row],
                    religion=religion,
                    religion_other=df['Religion_other'][row],
                    mother_tongue=mother_tongue,
                    other_mother_tongue=df['MT_other'][row],
                    contact_num=df['Contact'][row],
                    education_level=education_level,
                    owner_citizenship_number=df['Citizenship_no'][row],
                    responder_name=df['Responder_Name'][row],
                    responder_gender=responder_gender,
                    responder_age=df['Resp_Age'][row],
                    responder_contact=df['Resp_Contact'][row],
                    other_family_member=df['other_family'][row],
                    foods_eaten_in_last7_day=df['Food_type'][row],
                    monthly_expanses=df['Monthly_Expenses'][row],
                    monthly_income=df['Monthly_fam_income'][row],
                    if_loan_amount=df['Loan_amount'][row],
                    loan_time=df['_If_yes_for_how_long'][row],
                    have_livestock=df['Animal_detail_presence'][row],

                    # complete till here

                    date_of_establishment=df['Established_year'][row],
                    number_of_storey=df['House_storey'][row],
                    number_of_rooms=df['Room_number'][row],
                    # received_building_permit=df['Household_number'][row],
                    # building_completion_certificate=df['Household_number'][row],
                    is_house_earthquake_resilience=df['Earthquake_resistance'][row],
                    # is_house_landslide_resilience=df['Household_number'][row],
                    how_much_land_ownership=df['Land_ownership'][row],
                    does_land_lies_near_river_flood_plain=df['_Does_the_land_und'][row],
                    land_near_river_flood_plain=df['_If_is_near_to_the_river'][row],
                    # image_with_landscape=df['Household_number'][row],
                    time_for_nearest_road=df['Main_road_distance'][row],
                    road_type=road_type,
                    road_width=df['_98_Wh_o_your_house_In_ft'][row],
                    time_to_nearest_school=df['School_distance'][row],
                    time_to_nearest_health_institution=df['Health_institution_distance'][row],
                    time_to_nearest_security_force=df['Security_distance'][row],
                    does_ward_have_identified_risk_area=df['Risk_Area'][row],
                    do_you_know_about_warning_system=df['EWS'][row],
                    is_there_waning_system=df['EWS_detail'][row],
                    did_you_got_early_information_in_disaster=df['Disaster_EWS'][row],
                    if_yes_which_medium_was_used=df['EWS_medium'][row],
                    does_ward_have_evacuation_shelter=df['evacuation_centre'][row],
                    distance_to_evacuation_shelter=df['Evac_shelter_distance'][row],
                    capacity_of_evacuation_shelter=df['_What_is_t_acity_of_the_shelter'][row],
                    distance_to_nearest_openspace=df['Openspace_distance'][row],
                    how_far_nearest_market=df['Market_distance'][row],
                    was_nearest_market_operating_in_disaster=df['Market_operation'][row],
                    was_material_easily_available=df['easy_access'][row],
                    if_not_material_how_you_managed=df['Material _management'][row],
                    how_far_is_alternative_market=df['Alternative_market'][row],
                    name_of_alternative_market=df['Market_name'][row],
                    is_there_warehouse_in_your_ward=df['_Does_your_house'][row],
                    how_often_replace_material_in_emergency_kit=df['_als_in_emergency_kit'][row],
                    contingency_plan_involvement=df['Household_number'][row],
                    ward_has_safe_place=df['_Safe_spac'][row],
                    distance_to_safe_place=df['_If_s_it_from_your_house'][row],
                )

                # occupation

                # occupation lists
                agriculture = OccupationList.objects.get(name='Agriculture')
                agriculture_wages = OccupationList.objects.get(name='Agricultural wages')
                daily_wages = OccupationList.objects.get(name='Daily wages')
                gov_service = OccupationList.objects.get(name='Government service')
                non_gov_service = OccupationList.objects.get(name='Non-government service')
                foreign_emp = OccupationList.objects.get(name='Foreign employment')
                entrepreneur = OccupationList.objects.get(name='Entrepreneur')
                business = OccupationList.objects.get(name='Business')
                labour_india = OccupationList.objects.get(name='Seasonal labor, India')
                labour_nepal = OccupationList.objects.get(name='Seasonal labor, Nepal')
                student = OccupationList.objects.get(name='Student')
                other = OccupationList.objects.get(name='Other')

                occupation = Occupation.objects.create(
                    occupation=agriculture,
                    if_occupation=df['Main_occupation/Agriculture'][row],
                    house_hold=house_hold
                )

                occupation = Occupation.objects.create(
                    occupation=agriculture_wages,
                    if_occupation=df['Main_occupation/Agriculture_Labour'][row],
                    house_hold=house_hold
                )

                occupation = Occupation.objects.create(
                    occupation=daily_wages,
                    if_occupation=df['Main_occupation/Daily_Labour'][row],
                    house_hold=house_hold
                )

                occupation = Occupation.objects.create(
                    occupation=gov_service,
                    if_occupation=df['Main_occupation/Government_Job'][row],
                    house_hold=house_hold
                )

                occupation = Occupation.objects.create(
                    occupation=non_gov_service,
                    if_occupation=df['Main_occupation/Non-Government_Job'][row],
                    house_hold=house_hold
                )

                occupation = Occupation.objects.create(
                    occupation=foreign_emp,
                    if_occupation=df['Main_occupation/Foreign_Employment'][row],
                    house_hold=house_hold
                )

                occupation = Occupation.objects.create(
                    occupation=entrepreneur,
                    if_occupation=df['Main_occupation/Self-Employment'][row],
                    house_hold=house_hold
                )

                shop = BusinessList.objects.get(name='shop')
                pharmacy = BusinessList.objects.get(name='Pharmacy')
                stationery = BusinessList.objects.get(name='Stationery')
                hard_shop = BusinessList.objects.get(name='Hardware shop')
                hotel = BusinessList.objects.get(name='Hotel/Restaurant')
                poultry = BusinessList.objects.get(name='Poultry farming')
                livestock = BusinessList.objects.get(name='Livestock farming')
                cattle = BusinessList.objects.get(name='Cattle farming')
                agriculture_bus = BusinessList.objects.get(name='Other agricultural business')
                small_bus = BusinessList.objects.get(name='Other small business')
                other_bus = BusinessList.objects.get(name='Other')

                occupation = Occupation.objects.create(
                    occupation=business,
                    if_occupation=df['Main_occupation/business'][row],
                    house_hold=house_hold
                )

                # business
                occupation = Occupation.objects.create(
                    occupation=business,
                    if_occupation=df['Main_occupation/business'][row],
                    if_business_its_type=shop,
                    if_business=df['Business/Kirana_Pasal'][row],
                    house_hold=house_hold
                )

                occupation = Occupation.objects.create(
                    occupation=business,
                    if_occupation=df['Main_occupation/business'][row],
                    if_business_its_type=pharmacy,
                    if_business=df['Business/Medical_Shop'][row],
                    house_hold=house_hold
                )

                occupation = Occupation.objects.create(
                    occupation=business,
                    if_occupation=df['Main_occupation/business'][row],
                    if_business_its_type=stationery,
                    if_business=df['Business/Stationery_Shop'][row],
                    house_hold=house_hold
                )

                occupation = Occupation.objects.create(
                    occupation=business,
                    if_occupation=df['Main_occupation/business'][row],
                    if_business_its_type=hard_shop,
                    if_business=df['Business/Hardware_Shop'][row],
                    house_hold=house_hold
                )

                occupation = Occupation.objects.create(
                    occupation=business,
                    if_occupation=df['Main_occupation/business'][row],
                    if_business_its_type=hotel,
                    if_business=df['Business/Hotel_Business'][row],
                    house_hold=house_hold
                )

                occupation = Occupation.objects.create(
                    occupation=business,
                    if_occupation=df['Main_occupation/business'][row],
                    if_business_its_type=poultry,
                    if_business=df['Business/Poultry Farm'][row],
                    house_hold=house_hold
                )

                occupation = Occupation.objects.create(
                    occupation=business,
                    if_occupation=df['Main_occupation/business'][row],
                    if_business_its_type=livestock,
                    if_business=df['Business/Goat Farm'][row],
                    house_hold=house_hold
                )

                occupation = Occupation.objects.create(
                    occupation=business,
                    if_occupation=df['Main_occupation/business'][row],
                    if_business_its_type=cattle,
                    if_business=df['Business/Cow Farm'][row],
                    house_hold=house_hold
                )

                occupation = Occupation.objects.create(
                    occupation=business,
                    if_occupation=df['Main_occupation/business'][row],
                    if_business_its_type=agriculture_bus,
                    if_other_agriculture_business=df['Other_business'][row],
                    if_agriculture_business_harvest_sufficient=df['Crop_sufficiency'][row],
                    if_business=df['Business/Others_Agriculture'][row],
                    house_hold=house_hold
                )

                occupation = Occupation.objects.create(
                    occupation=business,
                    if_occupation=df['Main_occupation/business'][row],
                    if_business_its_type=small_bus,
                    if_business=df['Business/Others_Small Business'][row],
                    if_other_small_business=df['Business/Others_Small Business'][row],
                    house_hold=house_hold
                )

                occupation = Occupation.objects.create(
                    occupation=business,
                    if_occupation=df['Main_occupation/business'][row],
                    if_business_its_type=other_bus,
                    if_business=df['Business/Others'][row],
                    if_other_occupation=df['_If_ot_s_please_state_here'][row],
                    house_hold=house_hold
                )

                # business completed

                occupation = Occupation.objects.create(
                    occupation=labour_india,
                    if_occupation=df['Main_occupation/labour_india'][row],
                    house_hold=house_hold
                )

                occupation = Occupation.objects.create(
                    occupation=labour_nepal,
                    if_occupation=df['Main_occupation/labour_nepal'][row],
                    house_hold=house_hold
                )

                # occupation = Occupation.objects.create(
                #     occupation=student,
                #     if_occupation=df['Household_number'][row],
                #     house_hold=house_hold
                # )

                occupation = Occupation.objects.create(
                    occupation=other,
                    if_occupation=df['Main_occupation/Others'][row],
                    house_hold=house_hold,
                    if_other_occupation=df['Other_occupation'][row]
                )

                # food eaten

                food_choice = FoodChoice.objects.all()

                food_eaten = FoodEaten.objects.create(
                    food=food_choice[0],
                    no_of_days_food_eaten=df['Main_staple'][row],
                    house_hold=house_hold
                )

                food_eaten = FoodEaten.objects.create(
                    food=food_choice[1],
                    no_of_days_food_eaten=df['Pulses'][row],
                    house_hold=house_hold
                )

                food_eaten = FoodEaten.objects.create(
                    food=food_choice[2],
                    no_of_days_food_eaten=df['Vegetables'][row],
                    house_hold=house_hold
                )

                food_eaten = FoodEaten.objects.create(
                    food=food_choice[3],
                    no_of_days_food_eaten=df['Fruits'][row],
                    house_hold=house_hold
                )

                food_eaten = FoodEaten.objects.create(
                    food=food_choice[4],
                    no_of_days_food_eaten=df['Meat_and_fish'][row],
                    house_hold=house_hold
                )

                food_eaten = FoodEaten.objects.create(
                    food=food_choice[5],
                    no_of_days_food_eaten=df['Milk_and_Products'][row],
                    house_hold=house_hold
                )

                food_eaten = FoodEaten.objects.create(
                    food=food_choice[6],
                    no_of_days_food_eaten=df['Sugar_products'][row],
                    house_hold=house_hold
                )

                food_eaten = FoodEaten.objects.create(
                    food=food_choice[7],
                    no_of_days_food_eaten=df['Oil_products'][row],
                    house_hold=house_hold
                )

                food_eaten = FoodEaten.objects.create(
                    food=food_choice[8],
                    no_of_days_food_eaten=df['Condiments'][row],
                    house_hold=house_hold
                )

                # insurance

                insurance_list = InsuranceList.objects.all()

                insurance = Insurance.objects.create(
                    insurance=insurance_list[0],
                    have_insurance=df['Insurance_type/Life_Insurance'][row],
                    house_hold=house_hold
                )

                insurance = Insurance.objects.create(
                    insurance=insurance_list[1],
                    have_insurance=df['Insurance_type/Animal_Insurance'][row],
                    house_hold=house_hold
                )

                insurance = Insurance.objects.create(
                    insurance=insurance_list[2],
                    have_insurance=df['Insurance_type/Farm_Insurance'][row],
                    house_hold=house_hold
                )

                insurance = Insurance.objects.create(
                    insurance=insurance_list[3],
                    have_insurance=df['Insurance_type/crop'][row],
                    house_hold=house_hold
                )

                insurance = Insurance.objects.create(
                    insurance=insurance_list[4],
                    have_insurance=df['Insurance_type/other'][row],
                    if_other_insurance_choice=df['other_insurance'][row],
                    house_hold=house_hold
                )
                # vehicle

                vehicle_list = VehicleList.objects.all()

                vehicle = Vehicle.objects.create(
                    vehicle=vehicle_list[0],
                    have_vehicle=df['Vehicles/Car/Jeep/Van_personal'][row],
                    house_hold=house_hold
                )

                vehicle = Vehicle.objects.create(
                    vehicle=vehicle_list[1],
                    have_vehicle=df['Vehicles/Car/Jeep/Van_Commercial'][row],
                    house_hold=house_hold
                )

                vehicle = Vehicle.objects.create(
                    vehicle=vehicle_list[2],
                    have_vehicle=df['Vehicles/Minibus/Minitruck'][row],
                    house_hold=house_hold
                )

                vehicle = Vehicle.objects.create(
                    vehicle=vehicle_list[3],
                    have_vehicle=df['Vehicles/Cycle'][row],
                    house_hold=house_hold
                )

                vehicle = Vehicle.objects.create(
                    vehicle=vehicle_list[4],
                    have_vehicle=df['Vehicles/Bus/Triper/Big_Vehicle'][row],
                    house_hold=house_hold
                )

                vehicle = Vehicle.objects.create(
                    vehicle=vehicle_list[5],
                    have_vehicle=df['Vehicles/Tractor/Power'][row],
                    house_hold=house_hold
                )

                vehicle = Vehicle.objects.create(
                    vehicle=vehicle_list[6],
                    have_vehicle=df['Vehicles/Others_Heavy_Equipment'][row],
                    if_other_heavy_equipment=df['Heavy_equipment'][row],
                    house_hold=house_hold
                )

                vehicle = Vehicle.objects.create(
                    vehicle=vehicle_list[7],
                    have_vehicle=df['Vehicles/If_No_Vehicle'][row],
                    house_hold=house_hold
                )

                # facility

                facility_list = FacilityList.objects.all()

                facility = Facilities.objects.create(
                    facility=vehicle_list[0],
                    have_facility=df['Facilities_type/Radio'][row],
                    house_hold=house_hold
                )

                facility = Facilities.objects.create(
                    facility=vehicle_list[1],
                    have_facility=df['Facilities_type/Television'][row],
                    house_hold=house_hold
                )

                facility = Facilities.objects.create(
                    facility=vehicle_list[2],
                    have_facility=df['Facilities_type/Fridge'][row],
                    house_hold=house_hold
                )

                facility = Facilities.objects.create(
                    facility=vehicle_list[3],
                    have_facility=df['Facilities_type/oven'][row],
                    house_hold=house_hold
                )

                facility = Facilities.objects.create(
                    facility=vehicle_list[4],
                    have_facility=df['Facilities_type/Mobile/Telephone'][row],
                    house_hold=house_hold
                )

                facility = Facilities.objects.create(
                    facility=vehicle_list[5],
                    have_facility=df['Facilities_type/Washing_Machine'][row],
                    house_hold=house_hold
                )

                facility = Facilities.objects.create(
                    facility=vehicle_list[6],
                    have_facility=df['Facilities_type/Others'][row],
                    if_other_facility=df['other_facilities'],
                    house_hold=house_hold
                )

                facility = Facilities.objects.create(
                    facility=vehicle_list[7],
                    have_facility=df['Facilities_type/Internet'][row],
                    house_hold=house_hold
                )

                # fuel
                fuel_list = FuelTypeList.objects.all()

                fuel = Fuel.objects.create(
                    fuel=fuel_list[0],
                    have_fuel=df['Fuel_type/Kerosene'][row],
                    house_hold=house_hold
                )
                fuel = Fuel.objects.create(
                    fuel=fuel_list[1],
                    have_fuel=df['Fuel_type/L.P Gas'][row],
                    house_hold=house_hold
                )
                fuel = Fuel.objects.create(
                    fuel=fuel_list[2],
                    have_fuel=df['Fuel_type/Dung'][row],
                    house_hold=house_hold
                )

                fuel = Fuel.objects.create(
                    fuel=fuel_list[3],
                    have_fuel=df['Fuel_type/Bio Gas'][row],
                    house_hold=house_hold
                )

                fuel = Fuel.objects.create(
                    fuel=fuel_list[4],
                    have_fuel=df['Fuel_type/Electrical Appliances'][row],
                    house_hold=house_hold
                )

                fuel = Fuel.objects.create(
                    fuel=fuel_list[5],
                    have_fuel=df['Fuel_type/Firewood/Coal'][row],
                    house_hold=house_hold
                )

                fuel = Fuel.objects.create(
                    fuel=fuel_list[6],
                    have_fuel=df['Fuel_type/Others'][row],
                    if_other_fuel=df['Other_fueltype'][row],
                    house_hold=house_hold
                )

                # whose Ownership

                whose_ownership = WhoseOwnershipList.objects.all()

                ownership = WhoseOwnershipData.objects.create(
                    ownership=whose_ownership[0],
                    have_ownership=df['Ownership_detail/Male'][row],
                    house_hold=house_hold
                )

                ownership = WhoseOwnershipData.objects.create(
                    ownership=whose_ownership[1],
                    have_ownership=df['Ownership_detail/Female'][row],
                    house_hold=house_hold
                )

                ownership = WhoseOwnershipData.objects.create(
                    ownership=whose_ownership[3],
                    have_ownership=df['Ownership_detail/Both'][row],
                    house_hold=house_hold
                )

                # house type
                house_type_list = HouseTypeList.objects.all()

                house_type = HouseType.objects.create(
                    ownership=house_type_list[0],
                    have_house=df['House_type/R.C.C. '][row],
                    house_hold=house_hold

                )

                house_type = HouseType.objects.create(
                    ownership=house_type_list[1],
                    have_house=df['House_type/C.G.I'][row],
                    house_hold=house_hold

                )

                house_type = HouseType.objects.create(
                    ownership=house_type_list[2],
                    have_house=df['House_type/Slate/Stone'][row],
                    house_hold=house_hold

                )

                house_type = HouseType.objects.create(
                    ownership=house_type_list[3],
                    have_house=df['House_type/Semi_Permanent_House'][row],
                    house_hold=house_hold

                )

                house_type = HouseType.objects.create(
                    ownership=house_type_list[4],
                    have_house=df['House_type/C.G.I_temporary'][row],
                    house_hold=house_hold

                )

                house_type = HouseType.objects.create(
                    ownership=house_type_list[5],
                    have_house=df['House_type/Bhus /Khar/Mud'][row],
                    house_hold=house_hold

                )

                house_type = HouseType.objects.create(
                    ownership=house_type_list[6],
                    have_house=df['House_type/Others_(Other)'][row],
                    if_other=df['_If_other_please_state_here_001'][row],
                    house_hold=house_hold

                )

                # work done on flood

                work_done = WorkDoneOnFloodList.obejcts.all()

                work = WorkDoneOnFlood.objects.create(
                    work_done=work_done[0],
                    if_work_done=df['Activities_detail/Basement Construction'][row],
                    house_hold=house_hold

                )

                work = WorkDoneOnFlood.objects.create(
                    work_done=work_done[1],
                    if_work_done=df['Activities_detail/Strong_Wall'][row],
                    house_hold=house_hold

                )

                work = WorkDoneOnFlood.objects.create(
                    work_done=work_done[2],
                    if_work_done=df['Activities_detail/Effective_Dhal_Outlet'][row],
                    house_hold=house_hold

                )

                work = WorkDoneOnFlood.objects.create(
                    work_done=work_done[3],
                    if_work_done=df['Activities_detail/Others'][row],
                    if_other_work=df['Other_Activities'][row],
                    house_hold=house_hold
                )

                # Technical Field List

                technical_list = TechnicalFieldList.objects.all()

                technical = TechnicalField.objects.create(
                    technical=technical_list[0],
                    if_technical=df['Manpower_type/Doctor'][row],
                    female_num=df['Doc_female_number'][row],
                    male_num=df['Doc_male_number'][row],
                    if_sex_female=df['Doctor_sex/Female'][row],
                    if_sex_male=df['Doctor_sex/Male'][row],
                    house_hold=house_hold

                )

                technical = TechnicalField.objects.create(
                    technical=technical_list[0],
                    if_technical=df['Manpower_type/Engineer'][row],
                    female_num=df['Eng_female'][row],
                    male_num=df['Eng_Male'][row],
                    if_sex_female=df['Eng_sex/female'][row],
                    if_sex_male=df['Eng_sex/male'][row],
                    house_hold=house_hold

                )

                technical = TechnicalField.objects.create(
                    technical=technical_list[0],
                    if_technical=df['Manpower_type/Sub-engineer'][row],
                    female_num=df['Subeng_female'][row],
                    male_num=df['Subeng_male'][row],
                    if_sex_female=df['Subeng_sex/female'][row],
                    if_sex_male=df['Subeng_sex/male'][row],
                    house_hold=house_hold

                )

                technical = TechnicalField.objects.create(
                    technical=technical_list[0],
                    if_technical=df['Manpower_type/Nurse'][row],
                    female_num=df['Nurse_number'][row],
                    male_num=df['_If_male_nurse_their_number'][row],
                    if_sex_female=df['_If_nurse/Female_(female)'][row],
                    if_sex_male=df['_If_nurse/Male_(male)'][row],
                    house_hold=house_hold

                )

                technical = TechnicalField.objects.create(
                    technical=technical_list[0],
                    if_technical=df['Manpower_type/H.A/Lab Assistant/Radiologist/Pharmacist'][row],
                    female_num=df['HA_LAB_sex/female'][row],
                    male_num=df['HA_LAB_sex/male'][row],
                    if_sex_female=df['HA_LAB_female'][row],
                    if_sex_male=df['HA_LAB_male'][row],
                    house_hold=house_hold

                )

                technical = TechnicalField.objects.create(
                    technical=technical_list[0],
                    if_technical=df['Manpower_type/Veterinary'][row],
                    female_num=df['Vet_Sex/female'][row],
                    male_num=df['Vet_Sex/male'][row],
                    if_sex_female=df['Vet_female'][row],
                    if_sex_male=df['Vet_male'][row],
                    house_hold=house_hold

                )

                technical = TechnicalField.objects.create(
                    technical=technical_list[0],
                    if_technical=df['Manpower_type/Carpenter'][row],
                    female_num=df['Dakarmi_female'][row],
                    male_num=df['Dakarmi_male'][row],
                    if_sex_female=df['Dakarmi_sex/female'][row],
                    if_sex_male=df['Dakarmi_sex/male'][row],
                    house_hold=house_hold

                )

                technical = TechnicalField.objects.create(
                    technical=technical_list[0],
                    if_technical=df['Manpower_type/Electrician'][row],
                    female_num=df['Electrician_female'][row],
                    male_num=df['Electrician_male'][row],
                    if_sex_female=df['Electrician_sex/female'][row],
                    if_sex_male=df['Electrician_sex/male'][row],
                    house_hold=house_hold

                )

                technical = TechnicalField.objects.create(
                    technical=technical_list[0],
                    if_technical=df['Manpower_type/Plumber'][row],
                    female_num=df['Plumber_female'][row],
                    male_num=df['Plumber_male'][row],
                    if_sex_female=df['Manpower_type/Doctor'][row],
                    if_sex_male=df['Plumber_sex/female'][row],
                    house_hold=house_hold

                )

                technical = TechnicalField.objects.create(
                    technical=technical_list[0],
                    if_technical=df['Manpower_type/J.T/J.T.A'][row],
                    female_num=df['JT_female'][row],
                    male_num=df['JT_male'][row],
                    if_sex_female=df['JT_Sex/female'][row],
                    if_sex_male=df['JT_Sex/male'][row],
                    house_hold=house_hold

                )

                technical = TechnicalField.objects.create(
                    technical=technical_list[0],
                    if_technical=df['Manpower_type/Others'][row],
                    female_num=df['Other_tech_female'][row],
                    male_num=df['Other_tech_male'][row],
                    if_sex_female=df['Other_technical_femal'][row],
                    if_sex_male=df['Other_tech_sex'][row],
                    house_hold=house_hold
                )

                # road capacity

                road_capacity = RoadCapacity.objects.all()

                road_type = RoadCapacityType.objects.create(
                    road=road_capacity[0],
                    have_road=df['Road_capacity/Crane/Dozer/Ace'][row],
                    house_hold=house_hold
                )

                road_type = RoadCapacityType.objects.create(
                    road=road_capacity[1],
                    have_road=df['Road_capacity/Minibus/Mini Truck'][row],
                    house_hold = house_hold,

                )

                road_type = RoadCapacityType.objects.create(
                    road=road_capacity[2],
                    have_road=df['Road_capacity/Tractor_Power'][row],
                    house_hold=house_hold,

                )

                road_type = RoadCapacityType.objects.create(
                    road=road_capacity[3],
                    have_road=df['Road_capacity/Pumpset Runnable_Fir'][row],
                    house_hold=house_hold,

                )

                road_type = RoadCapacityType.objects.create(
                    road=road_capacity[4],
                    have_road=df['Road_capacity/Bus/Pickup/Car_Cha'][row],
                    house_hold=house_hold,

                )

                road_type = RoadCapacityType.objects.create(
                    road=road_capacity[5],
                    have_road=df['Road_capacity/Motorcycle_Mat'][row],
                    house_hold=house_hold,

                )

                # Water sources

                drinking_list = DrinkingWaterList.objects.all()

                drinking_water = DrinkingWater.objects.create(
                    drinking_water=road_capacity[0],
                    if_drinking_water=df['Water_sources/Public_Tap'][row],
                    house_hold=house_hold,
                )

                drinking_water = DrinkingWater.objects.create(
                    drinking_water=road_capacity[0],
                    if_drinking_water=df['Water_sources/Private_Tap'][row],
                    house_hold=house_hold,
                )

                drinking_water = DrinkingWater.objects.create(
                    drinking_water=road_capacity[0],
                    if_drinking_water=df['Water_sources/Pond or Stream'][row],
                    house_hold=house_hold,
                )

                drinking_water = DrinkingWater.objects.create(
                    drinking_water=road_capacity[0],
                    if_drinking_water=df['Water_sources/River'][row],
                    house_hold=house_hold,
                )

                drinking_water = DrinkingWater.objects.create(
                    drinking_water=road_capacity[0],
                    if_drinking_water=df['Water_sources/Tubewell'][row],
                    status=df['_What_is_the_status_of_tube_well'][row],
                    number_of_house_using_source=df['_How_many_house_use_it'][row],
                    house_hold=house_hold,
                )

                drinking_water = DrinkingWater.objects.create(
                    drinking_water=road_capacity[0],
                    if_drinking_water=df['Water_sources/Others'][row],
                    if_other_drinking_water=df['Other_Watersources'][row],
                    house_hold=house_hold,
                )

                # latrines

                latrine_list = LatrineList.objects.all()

                latrine = Latrine.objects.create(
                    latrine=latrine_list[0],
                    have_latrine=df['Toilet_type/Dhal'][row],
                    house_hold=house_hold,
                )
                latrine = Latrine.objects.create(
                    latrine=latrine_list[1],
                    have_latrine=df['Toilet_type/Hole'][row],
                    house_hold=house_hold,
                )
                latrine = Latrine.objects.create(
                    latrine=latrine_list[2],
                    have_latrine=df['Toilet_type/Bio Gas'][row],
                    house_hold=house_hold,
                )
                latrine = Latrine.objects.create(
                    latrine=latrine_list[3],
                    have_latrine=df['Toilet_type/Safety Tank'][row],
                    house_hold=house_hold,
                )

                latrine = Latrine.objects.create(
                    latrine=latrine_list[4],
                    have_latrine=df['Toilet_type/Having Ring '][row],
                    house_hold=house_hold,
                )
                latrine = Latrine.objects.create(
                    latrine=latrine_list[5],
                    have_latrine=df['Toilet_type/Others'][row],
                    if_other_latrine=df['Toilet_type/Others'][row],
                    house_hold=house_hold
                )

                # disaster

                disaster_list = DisasterList.objects.all()

                disaster = DisasterProne.objects.create(
                    name=disaster_list[4],
                    is_disaster_prone=df['Disaster_Detail/Volcano'][row],
                    house_hold=house_hold,
                )

                disaster = DisasterProne.objects.create(
                    name=disaster_list[4],
                    is_disaster_prone=df['Disaster_Detail/Fire '][row],
                    house_hold=house_hold,
                )

                disaster = DisasterProne.objects.create(
                    name=disaster_list[4],
                    is_disaster_prone=df['Disaster_Detail/Landslide'][row],
                    house_hold=house_hold,
                )

                disaster = DisasterProne.objects.create(
                    name=disaster_list[4],
                    is_disaster_prone=df['Disaster_Detail/Flood'][row],
                    house_hold=house_hold,
                )

                disaster = DisasterProne.objects.create(
                    name=disaster_list[4],
                    is_disaster_prone=df['Disaster_Detail/Thundering'][row],
                    house_hold=house_hold,
                )

                disaster = DisasterProne.objects.create(
                    name=disaster_list[4],
                    is_disaster_prone=df['Disaster_Detail/Drought/Dry'][row],
                    house_hold=house_hold,
                )

                disaster = DisasterProne.objects.create(
                    name=disaster_list[4],
                    is_disaster_prone=df['Disaster_Detail/Wind'][row],
                    house_hold=house_hold,
                )

                disaster = DisasterProne.objects.create(
                    name=disaster_list[4],
                    is_disaster_prone=df['Disaster_Detail/Epidemics'][row],
                    house_hold=house_hold,
                )

                disaster = DisasterProne.objects.create(
                    name=disaster_list[4],
                    is_disaster_prone=df['Disaster_Detail/Wildlife_Attack'][row],
                    house_hold=house_hold,
                )

                disaster = DisasterProne.objects.create(
                    name=disaster_list[4],
                    is_disaster_prone=df['Disaster_Detail/Road_Accident'][row],
                    house_hold=house_hold,
                )

                disaster = DisasterProne.objects.create(
                    name=disaster_list[4],
                    is_disaster_prone=df['Disaster_Detail/Snake_Bite'][row],
                    house_hold=house_hold,
                )

                disaster = DisasterProne.objects.create(
                    name=disaster_list[4],
                    is_disaster_prone=df['Disaster_Detail/Others'][row],
                    disaster_other=df['Other_disaster'][row],
                    house_hold=house_hold,
                )

                # Information Medium

                information_list = InformationMediumList.objects.all()

                information = InformationMedium.objects.create(
                    info_medium=information_list[4],
                    have_information=df['Information_medium/Radio/Television'][row],
                    house_hold=house_hold,
                )


                information = InformationMedium.objects.create(
                    info_medium=information_list[4],
                    have_information=df['Information_medium/Local Resident'][row],
                    house_hold=house_hold,
                )


                information = InformationMedium.objects.create(
                    info_medium=information_list[4],
                    have_information=df['Information_medium/Newspaper'][row],
                    house_hold=house_hold,
                )


                information = InformationMedium.objects.create(
                    info_medium=information_list[4],
                    have_information=df['Information_medium/Concerned Authority'][row],
                    house_hold=house_hold,
                )


                information = InformationMedium.objects.create(
                    info_medium=information_list[4],
                    have_information=df['Information_medium/Received'][row],
                    house_hold=house_hold,
                )


                information = InformationMedium.objects.create(
                    info_medium=information_list[4],
                    have_information=df['Information_medium/Hoading Board'][row],
                    house_hold=house_hold,
                )


                information = InformationMedium.objects.create(
                    info_medium=information_list[4],
                    have_information=df['Information_medium/Others'][row],
                    if_other_medium=df['Other_medium'][row],
                    house_hold=house_hold,
                )

                # suitable warning medium

                warning_list = WarningMediumList.objects.all()

                warning_medium = WarningMediumSuitableForDisaster.objects.create(
                    warning_medium=warning_list[4],
                    if_warning_medium=df['Suitable_medium/Radio'][row],
                    house_hold=house_hold,
                )


                warning_medium = WarningMediumSuitableForDisaster.objects.create(
                    warning_medium=warning_list[4],
                    if_warning_medium=df['Suitable_medium/Television'][row],
                    house_hold=house_hold,
                )


                warning_medium = WarningMediumSuitableForDisaster.objects.create(
                    warning_medium=information_list[4],
                    if_warning_medium=df['Suitable_medium/Micking'][row],
                    house_hold=house_hold,
                )


                warning_medium = WarningMediumSuitableForDisaster.objects.create(
                    warning_medium=warning_list[4],
                    if_warning_medium=df['Suitable_medium/Sairen'][row],
                    house_hold=house_hold,
                )


                warning_medium = WarningMediumSuitableForDisaster.objects.create(
                    warning_medium=warning_list[4],
                    if_warning_medium=df['Suitable_medium/SMS'][row],
                    house_hold=house_hold,
                )


                warning_medium = WarningMediumSuitableForDisaster.objects.create(
                    warning_medium=warning_list[4],
                    if_warning_medium=df['Suitable_medium/Others'][row],
                    if_other_medium=df['Other_suitable_medium'][row],
                    house_hold=house_hold,
                )

                # material list

                material_list = MaterialsInNearestMarketList.objects.all()

                material = MaterialsInNearestMarket.objects.create(
                    material_in_market=material_list[4],
                    is_material_available=df['Market_availability/Grain'][row],
                    house_hold=house_hold,
                )

                material = MaterialsInNearestMarket.objects.create(
                    material_in_market=material_list[4],
                    is_material_available=df['Market_availability/Dalhan/Dalhiya '][row],
                    house_hold=house_hold,
                )

                material = MaterialsInNearestMarket.objects.create(
                    material_in_market=material_list[4],
                    is_material_available=df['Market_availability/Vegetables'][row],
                    house_hold=house_hold,
                )

                material = MaterialsInNearestMarket.objects.create(
                    material_in_market=material_list[4],
                    is_material_available=df['Market_availability/Fruits'][row],
                    house_hold=house_hold,
                )

                material = MaterialsInNearestMarket.objects.create(
                    material_in_market=material_list[4],
                    is_material_available=df['Market_availability/Edible Oil'][row],
                    house_hold=house_hold,
                )

                material = MaterialsInNearestMarket.objects.create(
                    material_in_market=material_list[4],
                    is_material_available=df['Market_availability/Fish/Meat,Egg'][row],
                    house_hold=house_hold,
                )

                material = MaterialsInNearestMarket.objects.create(
                    material_in_market=material_list[4],
                    is_material_available=df['Market_availability/Agriculture_Material '][row],
                    house_hold=house_hold,
                )

                material = MaterialsInNearestMarket.objects.create(
                    material_in_market=material_list[4],
                    is_material_available=df['Market_availability/Others_Inedible item'][row],
                    house_hold=house_hold,
                )

                material = MaterialsInNearestMarket.objects.create(
                    material_in_market=material_list[4],
                    is_material_available=df['Market_availability/Construction Material'][row],
                    house_hold=house_hold,
                )

                material = MaterialsInNearestMarket.objects.create(
                    material_in_market=material_list[4],
                    is_material_available=df['Market_availability/Clothes'][row],
                    house_hold=house_hold,
                )

                material = MaterialsInNearestMarket.objects.create(
                    material_in_market=material_list[4],
                    if_other_material=df['Other_availability'][row],
                    is_material_available=df['Market_availability/Others'][row],
                    house_hold=house_hold,
                )

                # coping mechanism
                coping_list = CopingMechanismList.objects.all()

                coping = CopingMechanism.objects.create(
                    coping_medium=coping_list[4],
                    is_coping_medium=df['Market_availability/Clothes'][row],
                    house_hold=house_hold,
                )

                coping = CopingMechanism.objects.create(
                    coping_medium=coping_list[4],
                    is_coping_medium=df['Market_availability/Clothes'][row],
                    house_hold=house_hold,
                )

                coping = CopingMechanism.objects.create(
                    coping_medium=coping_list[4],
                    is_coping_medium=df['Market_availability/Clothes'][row],
                    house_hold=house_hold,
                )

                coping = CopingMechanism.objects.create(
                    coping_medium=coping_list[4],
                    is_coping_medium=df['Market_availability/Clothes'][row],
                    house_hold=house_hold,
                )

                coping = CopingMechanism.objects.create(
                    coping_medium=coping_list[4],
                    is_coping_medium=df['Market_availability/Clothes'][row],
                    house_hold=house_hold,
                )

                coping = CopingMechanism.objects.create(
                    coping_medium=coping_list[4],
                    is_coping_medium=df['Market_availability/Clothes'][row],
                    house_hold=house_hold,
                )

                coping = CopingMechanism.objects.create(
                    coping_medium=coping_list[4],
                    is_coping_medium=df['Market_availability/Clothes'][row],
                    house_hold=house_hold,
                )

                coping = CopingMechanism.objects.create(
                    coping_medium=coping_list[4],
                    is_coping_medium=df['Market_availability/Clothes'][row],
                    house_hold=house_hold,
                )

                coping = CopingMechanism.objects.create(
                    coping_medium=coping_list[4],
                    is_coping_medium=df['Market_availability/Clothes'][row],
                    house_hold=house_hold,
                )

                coping = CopingMechanism.objects.create(
                    coping_medium=coping_list[4],
                    is_coping_medium=df['Market_availability/Clothes'][row],
                    if_other_medium=df['Market_availability/Clothes'][row],
                    house_hold=house_hold,
                )

                # Disaster preparedness mechanism

                disaster_prepare_list = DisasterPreparednessMechanismList.objects.all()

                preparedness = DisasterPreparednessMechanism.objects.create(
                    preparedness=disaster_prepare_list[4],
                    involved_in_disaster_preparedness=df['disaster_risk_management'][row],
                    house_hold=house_hold,
                )

                preparedness = DisasterPreparednessMechanism.objects.create(
                    preparedness=disaster_prepare_list[4],
                    involved_in_disaster_preparedness=df['first_aid'][row],
                    house_hold=house_hold,
                )

                preparedness = DisasterPreparednessMechanism.objects.create(
                    preparedness=disaster_prepare_list[4],
                    involved_in_disaster_preparedness=df['search_and_rescue'][row],
                    house_hold=house_hold,
                )

                preparedness = DisasterPreparednessMechanism.objects.create(
                    preparedness=disaster_prepare_list[4],
                    involved_in_disaster_preparedness=df['Psycho-Socio'][row],
                    house_hold=house_hold,
                )

                preparedness = DisasterPreparednessMechanism.objects.create(
                    preparedness=disaster_prepare_list[4],
                    involved_in_disaster_preparedness=df['WASH'][row],
                    house_hold=house_hold,
                )

                preparedness = DisasterPreparednessMechanism.objects.create(
                    preparedness=disaster_prepare_list[4],
                    involved_in_disaster_preparedness=df['VCA'][row],
                    house_hold=house_hold,
                )

                preparedness = DisasterPreparednessMechanism.objects.create(
                    preparedness=disaster_prepare_list[4],
                    involved_in_disaster_preparedness=df['Nothing'][row],
                    house_hold=house_hold,
                )

                preparedness = DisasterPreparednessMechanism.objects.create(
                    preparedness=disaster_prepare_list[4],
                    involved_in_disaster_preparedness=df['Others'][row],
                    house_hold=house_hold,
                )

                # Involvement in simulation

                simulation = InvolvedInSimulation.objects.create(
                    simulation=disaster_list[4],
                    involved_in_f_simulation=df['Volcano'][row],
                    house_hold=house_hold,
                )

                simulation = InvolvedInSimulation.objects.create(
                    simulation=disaster_list[4],
                    involved_in_f_simulation=df['Flood'][row],
                    house_hold=house_hold,
                )

                simulation = InvolvedInSimulation.objects.create(
                    simulation=disaster_list[4],
                    involved_in_f_simulation=df['Fire'][row],
                    house_hold=house_hold,
                )

                simulation = InvolvedInSimulation.objects.create(
                    simulation=disaster_list[4],
                    involved_in_f_simulation=df['Landslide'][row],
                    house_hold=house_hold,
                )

                simulation = InvolvedInSimulation.objects.create(
                    simulation=disaster_list[4],
                    involved_in_f_simulation=df['Others'][row],
                    if_other_simulation=df['_If_othe_d_please_state_here'][row],
                    house_hold=house_hold,
                )


                # simulation = InvolvedInSimulation.objects.create(
                #     simulation=disaster_list[4],
                #     involved_in_f_simulation=df['Nothing'][row],
                #     house_hold=house_hold,
                # )

                #Guideline

                guideline_list = GuideLineList.objects.all()

                guideline = GuideLine.objects.create(
                    guideline=disaster_list[4],
                    know_about_guideline=df['_LDCRP_'][row],
                    involved_in_development_process=df['_ent_process_of_LDCRP'][row],
                    house_hold=house_hold,
                )

                guideline = GuideLine.objects.create(
                    guideline=disaster_list[4],
                    know_about_guideline=df['_DPRP_'][row],
                    involved_in_development_process=df['_ment_process_of_DPRP'][row],
                    house_hold=house_hold,
                )

                # ward falling prone area

                ward_falling = WardFallingProneArea.objects.create(
                    prone_area=disaster_list[4],
                    is_prone_area=df['Flood'][row],
                    # house_hold=house_hold,
                )

                ward_falling = WardFallingProneArea.objects.create(
                    prone_area=disaster_list[4],
                    is_prone_area=df['__057/Volcano'][row],
                    # house_hold=house_hold,
                )

                ward_falling = WardFallingProneArea.objects.create(
                    prone_area=disaster_list[4],
                    is_prone_area=df['__057/Landslide'][row],
                    # house_hold=house_hold,
                )

                ward_falling = WardFallingProneArea.objects.create(
                    prone_area=disaster_list[4],
                    is_prone_area=df['__057/Fire'][row],
                    # house_hold=house_hold,
                )

                ward_falling = WardFallingProneArea.objects.create(
                    prone_area=disaster_list[4],
                    is_prone_area=df['__057/Nothing from above'][row],
                    # house_hold=house_hold,
                )

                # Flood Damage Type
                damage_list = DamageList.objects.all()
                house_damage_list = HouseDamageList.objects.all()

                damage_type1 = DamageType.objects.create(
                    damage_type=damage_list[4],
                    damages=df['__054/Family Member'][row],
                )

                damage_type1 = DamageType.objects.create(
                    damage_type=damage_list[4],
                    damages=df['__054/House'][row],
                )

                #if house has been damaged type of damage
                house_damage_type1 = DamageType.objects.create(
                    damage_type=damage_list[4],
                    if_house_damage_type=house_damage_list[4],
                    damages=df['__055/Damage in Basement'][row],
                )
                house_damage_type1 = DamageType.objects.create(
                    damage_type=damage_list[4],
                    if_house_damage_type=house_damage_list[4],
                    damages=df['__055/Damage in Roof'][row],
                )
                house_damage_type1 = DamageType.objects.create(
                    damage_type=damage_list[4],
                    if_house_damage_type=house_damage_list[4],
                    damages=df['__055/Material in Wall'][row],
                )
                house_damage_type1 = DamageType.objects.create(
                    damage_type=damage_list[4],
                    if_house_damage_type=house_damage_list[4],
                    damages=df['__055/House_Flooded'][row],
                )
                house_damage_type1 = DamageType.objects.create(
                    damage_type=damage_list[4],
                    if_house_damage_type=house_damage_list[4],
                    damages=df['__055/Without Damage'][row],
                )

                house_damage_type1 = DamageType.objects.create(
                    damage_type=damage_list[4],
                    if_house_damage_type=house_damage_list[4],
                    if_house_other_damage=df['_If_othe_e_please_state_here'][row],
                    damages=df['__055/Others'][row],
                )



                damage_type1 = DamageType.objects.create(
                    damage_type=damage_list[4],
                    damages=df['__054/Furniture'][row],
                )

                damage_type1 = DamageType.objects.create(
                    damage_type=damage_list[4],
                    damages=df['__054/Land'][row],
                )

                damage_type1 = DamageType.objects.create(
                    damage_type=damage_list[4],
                    damages=df['__054/Family Member'][row],
                )

                damage_type1 = DamageType.objects.create(
                    damage_type=damage_list[4],
                    damages=df['__054/Cattle'][row],
                )


                damage_type1 = DamageType.objects.create(
                    damage_type=damage_list[4],
                    damages=df['__054/Edible crops'][row],
                )


                damage_type1 = DamageType.objects.create(
                    damage_type=damage_list[4],
                    damages=df['__054/Machinery'][row],
                )


                damage_type1 = DamageType.objects.create(
                    damage_type=damage_list[4],
                    damages=df['__054/Crops'][row],
                )


                damage_type1 = DamageType.objects.create(
                    damage_type=damage_list[4],
                    damages=df['__054/Others'][row],
                )


                damage_type1 = DamageType.objects.create(
                    damage_type=damage_list[4],
                    damages=df['__054/Private_Documents'][row],
                    damage_other=df['_If_othe_s_please_state_here'][row]
                )


                # Disaster prone Damage caused by disaster


                #flood
                disaster_prone = DisasterProne.objects.create(
                    name=disaster_list[4],
                    damage_type=damage_list[4],
                    if_damage=df['__054/Family Member'][row],
                    house_hold=house_hold,
                )

                disaster_prone = DisasterProne.objects.create(
                    name=disaster_list[4],
                    damage_type=damage_list[4],
                    if_damage=df['__054/House'][row],
                    house_hold=house_hold,
                )

                disaster_prone = DisasterProne.objects.create(
                    name=disaster_list[4],
                    damage_type=damage_list[4],
                    if_damage=df['__054/Furniture'][row],
                    house_hold=house_hold,
                )

                disaster_prone = DisasterProne.objects.create(
                    name=disaster_list[4],
                    damage_type=damage_list[4],
                    if_damage=df['__054/Land'][row],
                    house_hold=house_hold,
                )

                disaster_prone = DisasterProne.objects.create(
                    name=disaster_list[4],
                    damage_type=damage_list[4],
                    if_damage=df['__054/Cattle'][row],
                    house_hold=house_hold,
                )

                disaster_prone = DisasterProne.objects.create(
                    name=disaster_list[4],
                    damage_type=damage_list[4],
                    if_damage=df['__054/Edible crops'][row],
                    house_hold=house_hold,
                )

                disaster_prone = DisasterProne.objects.create(
                    name=disaster_list[4],
                    damage_type=damage_list[4],
                    if_damage=df['__054/Machinery'][row],
                    house_hold=house_hold,
                )


                disaster_prone = DisasterProne.objects.create(
                    name=disaster_list[4],
                    damage_type=damage_list[4],
                    if_damage=df['__054/Private_Documents'][row],
                    house_hold=house_hold,
                )


                disaster_prone = DisasterProne.objects.create(
                    name=disaster_list[4],
                    damage_type=damage_list[4],
                    if_damage=df['__054/Crops'][row],
                    house_hold=house_hold,
                )








            except Exception as e:
                    print(e)
