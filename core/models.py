
from django.db import models
from django.contrib.gis.db.models import PointField, MultiPolygonField
from django.contrib.auth.models import Group, User

# Create your models here.


class Province(models.Model):
    name = models.CharField(max_length=50)
    code = models.IntegerField(null=True, blank=True)
    boundary = MultiPolygonField(null=True, blank=True)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=50)
    code = models.IntegerField(null=True, blank=True)
    province = models.ForeignKey('Province', related_name='district',
                                 on_delete=models.CASCADE)
    boundary = MultiPolygonField(null=True, blank=True)

    def __str__(self):
        return self.name


class Municipality(models.Model):
    name = models.CharField(max_length=50)
    province = models.ForeignKey('Province', related_name='municipality',
                                 on_delete=models.CASCADE, blank=True, null=True)
    district = models.ForeignKey('District', related_name='municipality',
                                 on_delete=models.CASCADE)
    hlcit_code = models.CharField(max_length=1000, blank=True, null=True)
    boundary = MultiPolygonField(null=True, blank=True)

    def __str__(self):
        return self.name


class UserRole(models.Model):
    user = models.ForeignKey(User, related_name='role', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='role',
                              on_delete=models.CASCADE)
    province = models.ForeignKey('Province', related_name='role',
                                 on_delete=models.CASCADE)
    district = models.ForeignKey('District', related_name='role',
                                 on_delete=models.CASCADE)
    municipality = models.ForeignKey('Municipality', related_name='role',
                                     on_delete=models.CASCADE)


class HouseHoldData(models.Model):
    index = models.CharField(max_length=1000, primary_key=True)
    deviceid = models.CharField(max_length=1000, blank=True, null=True)
    date = models.CharField(max_length=1000, blank=True, null=True)
    surveyor_name = models.CharField(max_length=1000, blank=True, null=True)
    place_name = models.CharField(max_length=1000, blank=True, null=True)
    province = models.ForeignKey('Province',on_delete=models.CASCADE,
                                 null=True, blank=True, related_name='house_hold')
    district = models.ForeignKey('District',on_delete=models.CASCADE,
                                 null=True, blank=True, related_name='house_hold')
    municipality = models.ForeignKey('Municipality', on_delete=models.CASCADE,
                                 null=True, blank=True, related_name='house_hold')
    ward = models.CharField(max_length=1000, blank=True, null=True)
    house_number = models.CharField(max_length=1000, blank=True, null=True)
    latitude = models.CharField(max_length=1000, blank=True, null=True)
    longitude = models.CharField(max_length=1000, blank=True, null=True)
    altitude = models.CharField(max_length=1000, blank=True, null=True)
    gps_precision = models.CharField(max_length=1000, blank=True, null=True)
    household_number = models.CharField(max_length=1000, blank=True, null=True)
    owner_name = models.CharField(max_length=1000, blank=True, null=True)
    owner_age = models.CharField(max_length=1000, blank=True, null=True)
    owner_sex = models.CharField(max_length=1000, blank=True, null=True)
    owner_status = models.CharField(max_length=1000, blank=True, null=True)
    owner_status_other = models.CharField(max_length=1000, blank=True, null=True)
    owner_caste = models.CharField(max_length=1000, blank=True, null=True)
    owner_caste_other = models.CharField(max_length=1000, blank=True, null=True)
    religion = models.CharField(max_length=1000, blank=True, null=True)
    religion_other = models.CharField(max_length=1000, blank=True, null=True)
    mother_tongue = models.CharField(max_length=1000, blank=True, null=True)
    mother_tongue_other = models.CharField(max_length=1000, blank=True, null=True)
    contact_no = models.CharField(max_length=1000, blank=True, null=True)
    owner_education = models.CharField(max_length=1000, blank=True, null=True)
    owner_citizenship_no = models.CharField(max_length=1000, blank=True, null=True)
    responder_name = models.CharField(max_length=1000, blank=True, null=True)
    responder_sex = models.CharField(max_length=1000, blank=True, null=True)
    responder_age = models.CharField(max_length=1000, blank=True, null=True)
    responder_contact = models.CharField(max_length=1000, blank=True, null=True)
    other_family_living = models.CharField(max_length=1000, blank=True, null=True)
    main_occupation = models.CharField(max_length=1000, blank=True, null=True)
    # main_occupation_agriculture =  models.BooleanField(default=False)
    # main_occupation_agriculture_wages =  models.BooleanField(default=False)
    # main_occupation_daily_wages =  models.BooleanField(default=False)
    # main_occupation_government_job =  models.BooleanField(default=False)
    # main_occupation_non_government_job =  models.BooleanField(default=False)
    # main_occupation_foreign_employment =  models.BooleanField(default=False)
    # main_occupation_self =  models.BooleanField(default=False)
    # main_occupation_business =  models.BooleanField(default=False)
    # main_occupation_labour_nepal =  models.BooleanField(default=False)
    # main_occupation_labour_india =  models.BooleanField(default=False)
    # main_occupation_other =  models.BooleanField(default=False)
    other_occupation = models.CharField(max_length=1000, blank=True, null=True)
    business = models.CharField(max_length=1000, blank=True, null=True)
    # if_business_grocery_store = models.BooleanField(default=False)
    # if_business_pharmacy = models.BooleanField(default=False)
    # if_business_stationary = models.BooleanField(default=False)
    # if_business_hardware = models.BooleanField(default=False)
    # if_business_hotel = models.BooleanField(default=False)
    # if_business_poultry = models.BooleanField(default=False)
    # if_business_livestock = models.BooleanField(default=False)
    # if_business_cattle = models.BooleanField(default=False)
    # if_business_other_agriculture_business = models.BooleanField(default=False)
    # if_business_other_small_business = models.BooleanField(default=False)
    # if_business_other = models.BooleanField(default=False)
    other_business = models.CharField(max_length=1000, blank=True, null=True)
    other_small_business = models.CharField(max_length=1000, blank=True, null=True)
    crop_sufficiency = models.CharField(max_length=1000, blank=True, null=True)
    food_type = models.CharField(max_length=1000, blank=True, null=True)
    main_staple = models.CharField(max_length=1000, blank=True, null=True)
    pulses = models.CharField(max_length=1000, blank=True, null=True)
    vegetables = models.CharField(max_length=1000, blank=True, null=True)
    fruits = models.CharField(max_length=1000, blank=True, null=True)
    meat_and_fish = models.CharField(max_length=1000, blank=True, null=True)
    milk_and_products = models.CharField(max_length=1000, blank=True, null=True)
    sugar_products = models.CharField(max_length=1000, blank=True, null=True)
    oil_products = models.CharField(max_length=1000, blank=True, null=True)
    condiments = models.CharField(max_length=1000, blank=True, null=True)
    monthly_expenses = models.CharField(max_length=1000, blank=True, null=True)
    monthly_income = models.CharField(max_length=1000, blank=True, null=True)
    loan = models.CharField(max_length=1000, blank=True, null=True)
    loan_amount = models.CharField(max_length=1000, blank=True, null=True)
    loan_duration = models.CharField(max_length=1000, blank=True, null=True)
    animal_presence = models.CharField(max_length=1000, blank=True, null=True)
    insurance = models.CharField(max_length=1000, blank=True, null=True)
    # insurance_life_insurance = models.BooleanField(default=False)
    # insurance_livestock_insurance = models.BooleanField(default=False)
    # insurance_crops_insurance = models.BooleanField(default=False)
    # insurance_house_or_assest_insurance = models.BooleanField(default=False)
    other_insurance = models.CharField(max_length=1000, blank=True, null=True)
    vehicle = models.CharField(max_length=1000, blank=True, null=True)
    # vehicle_motorcycle = models.BooleanField(default=False)
    # vehicle_car_jeep_van_personal = models.BooleanField(default=False)
    # vehicle_car_jeep_van_commercial = models.BooleanField(default=False)
    # vehicle_minibus_minitruck = models.BooleanField(default=False)
    # vehicle_minibus_cycle = models.BooleanField(default=False)
    # vehicle_bus_tipper_big_vehicle = models.BooleanField(default=False)
    # vehicle_bus_tipper_big_vehicle = models.BooleanField(default=False)
    # vehicle_tractor_power_trailer = models.BooleanField(default=False)
    # vehicle_other_heavy_equipment = models.BooleanField(default=False)
    # vehicle_no_any_vehicle = models.BooleanField(default=False)
    vehicles_other = models.CharField(max_length=1000, blank=True, null=True)
    facilities_type = models.CharField(max_length=1000, blank=True, null=True)
    # facility_radio = models.BooleanField(default=False)
    # facility_tv = models.BooleanField(default=False)
    # facility_fridge = models.BooleanField(default=False)
    # facility_oven = models.BooleanField(default=False)
    # facility_telephone_mobile = models.BooleanField(default=False)
    # facility_washing_machine = models.BooleanField(default=False)
    # facility_internet = models.BooleanField(default=False)
    # facility_other = models.BooleanField(default=False)
    other_facilities = models.CharField(max_length=1000, blank=True, null=True)
    fuel_type = models.CharField(max_length=1000, blank=True, null=True)
    # fuel_type_kerosene = models.BooleanField(default=False)
    # fuel_type_lpg = models.BooleanField(default=False)
    # fuel_type_guitha = models.BooleanField(default=False)
    # fuel_type_bio_gas = models.BooleanField(default=False)
    # fuel_type_electrical = models.BooleanField(default=False)
    # fuel_type_firewood_coal = models.BooleanField(default=False)
    # fuel_type_other = models.BooleanField(default=False)
    other_fuel_type = models.CharField(max_length=1000, blank=True, null=True)
    land_ownership = models.CharField(max_length=1000, blank=True, null=True)
    # ownership_detail_male = models.BooleanField(default=False)
    # ownership_detail_female = models.BooleanField(default=False)
    # ownership_detail_other = models.BooleanField(default=False)
    house_type = models.CharField(max_length=1000, blank=True, null=True)
    # house_type_rcc_framework = models.BooleanField(default=False)
    # house_type_cgi_celling = models.BooleanField(default=False)
    # house_type_pallet_ash_soil = models.BooleanField(default=False)
    # house_type_semi_permanent_house = models.BooleanField(default=False)
    # house_type_temporary_cgi_roof = models.BooleanField(default=False)
    # house_type_temporary_thatched_mud_roof = models.BooleanField(default=False)
    # house_type_other = models.BooleanField(default=False)
    house_type_other = models.CharField(max_length=1000, blank=True, null=True)
    house_built_year = models.CharField(max_length=1000, blank=True, null=True)
    house_stories = models.CharField(max_length=1000, blank=True, null=True)
    no_of_rooms = models.CharField(max_length=1000, blank=True, null=True)
    house_map_registered = models.CharField(max_length=1000, blank=True, null=True)
    building_standard_code = models.CharField(max_length=1000, blank=True, null=True)
    earthquake_resistance = models.CharField(max_length=1000, blank=True, null=True)
    flood_prone = models.CharField(max_length=1000, blank=True, null=True)
    flood_resilience_activities = models.CharField(max_length=1000, blank=True, null=True)
    # flood_activities_raised_plinth = models.BooleanField(default=False)
    # flood_activities_strong_wall = models.BooleanField(default=False)
    # flood_activities_proper_drainage = models.BooleanField(default=False)
    # flood_activities_other = models.BooleanField(default=False)
    flood_activities_resilience_other = models.CharField(max_length=1000, blank=True, null=True)
    owned_land_area = models.CharField(max_length=1000, blank=True, null=True)
    owned_land_near_river = models.CharField(max_length=1000, blank=True, null=True)
    owned_land_area_near_river = models.CharField(max_length=1000, blank=True, null=True)
    owned_land_image = models.ImageField(upload_to='house_hold', blank=True, null=True)
    technical_manpower_presence = models.ImageField(upload_to='house_hold', blank=True, null=True)
    manpower_type = models.CharField(max_length=1000, blank=True, null=True)
    # manpower_doctor = models.BooleanField(default=False)
    # manpower_engineer = models.BooleanField(default=False)
    # manpower_sub_engineer = models.BooleanField(default=False)
    # manpower_nurse = models.BooleanField(default=False)
    # manpower_ha_lab_assitant_pharmacist = models.BooleanField(default=False)
    # manpower_veterinary = models.BooleanField(default=False)
    # manpower_carpenter = models.BooleanField(default=False)
    # manpower_plumber = models.BooleanField(default=False)
    # manpower_electrician = models.BooleanField(default=False)
    # manpower_jt_or_jta = models.BooleanField(default=False)
    # manpower_other_ne = models.BooleanField(default=False)
    # manpower_other_en = models.BooleanField(default=False)
    doctor_sex = models.CharField(max_length=1000, blank=True, null=True)
    doctor_male_number = models.CharField(max_length=1000, blank=True, null=True)
    doctor_female_number = models.CharField(max_length=1000, blank=True, null=True)
    engineer_sex = models.CharField(max_length=1000, blank=True, null=True)
    # engineer_sex_male = models.BooleanField(default=False)
    # engineer_sex_female = models.BooleanField(default=False)
    engineer_male_number = models.CharField(max_length=1000, blank=True, null=True)
    engineer_female_number = models.CharField(max_length=1000, blank=True, null=True)
    subengineer_sex = models.CharField(max_length=1000, blank=True, null=True)
    subengineer_male = models.CharField(max_length=1000, blank=True, null=True)
    subengineer_female = models.CharField(max_length=1000, blank=True, null=True)
    nurse_sex = models.CharField(max_length=1000, blank=True, null=True)
    # nurse_sex_male = models.BooleanField(default=False)
    # nurse_sex_female = models.BooleanField(default=False)
    nurse_male_number = models.CharField(max_length=1000, blank=True, null=True)
    nurse_female_number = models.CharField(max_length=1000, blank=True, null=True)
    ha_lab_sex = models.CharField(max_length=1000, blank=True, null=True)
    # ha_lab_sex_male = models.BooleanField(default=False)
    # ha_lab_sex_female = models.BooleanField(default=False)
    ha_lab_male_number = models.CharField(max_length=1000, blank=True, null=True)
    ha_lab_female_number = models.CharField(max_length=1000, blank=True, null=True)
    veterinary_sex = models.CharField(max_length=1000, blank=True, null=True)
    # veterinary_sex_male = models.BooleanField(default=False)
    # veterinary_sex_female = models.BooleanField(default=False)
    veterinary_male_number = models.CharField(max_length=1000, blank=True, null=True)
    veterinary_female_number = models.CharField(max_length=1000, blank=True, null=True)
    dakarmi_sikarmi_sex = models.CharField(max_length=1000, blank=True, null=True)
    # carpenter_sex_male = models.BooleanField(default=False)
    # carpenter_sex_female = models.BooleanField(default=False)
    dakarmi_sikarmi_male_number = models.CharField(max_length=1000, blank=True, null=True)
    dakarmi_sikarmi_female_number = models.CharField(max_length=1000, blank=True, null=True)
    plumber_sex = models.CharField(max_length=1000, blank=True, null=True)
    # plumber_sex_male = models.BooleanField(default=False)
    # plumber_sex_female = models.BooleanField(default=False)
    plumber_male_number = models.CharField(max_length=1000, blank=True, null=True)
    plumber_female_number = models.CharField(max_length=1000, blank=True, null=True)
    electrician_sex = models.CharField(max_length=1000, blank=True, null=True)
    # electrician_sex_male = models.BooleanField(default=False)
    # electrician_sex_female = models.BooleanField(default=False)
    electrician_male_number = models.CharField(max_length=1000, blank=True, null=True)
    electrician_female_number = models.CharField(max_length=1000, blank=True, null=True)
    jt_sex = models.CharField(max_length=1000, blank=True, null=True)
    # jt_or_jta_sex_male = models.BooleanField(default=False)
    # jt_or_jta_sex_female = models.BooleanField(default=False)
    jt_male_number = models.CharField(max_length=1000, blank=True, null=True)
    jt_female_number = models.CharField(max_length=1000, blank=True, null=True)
    other_technical = models.CharField(max_length=1000, blank=True, null=True)
    other_technical_sex = models.CharField(max_length=1000, blank=True, null=True)
    # other_sex_male = models.BooleanField(default=False)
    # other_sex_female = models.BooleanField(default=False)
    other_technical_male_number = models.CharField(max_length=1000, blank=True, null=True)
    other_technical_female_number = models.CharField(max_length=1000, blank=True, null=True)
    distance_from_main_road = models.CharField(max_length=500, blank=True, null= True)
    road_type = models.CharField(max_length=500, blank=True, null= True)
    road_width = models.CharField(max_length=500, blank=True, null= True)
    road_capacity = models.CharField(max_length=500, blank=True, null= True)
    # road_type_crane_dozer = models.BooleanField(default=False)
    # road_type_minibus_minitruck = models.BooleanField(default=False)
    # road_type_tractor_power_tailor = models.BooleanField(default=False)
    # road_type_tractor_fire_brigade = models.BooleanField(default=False)
    # road_type_tractor_bus_pickup_car = models.BooleanField(default=False)
    # road_type_tractor_motorcycle = models.BooleanField(default=False)
    distance_from_nearest_school = models.CharField(max_length=500, blank=True, null= True)
    distance_from_nearest_health_institution = models.CharField(max_length=500, blank=True, null= True)
    distance_from_nearest_security_forces = models.CharField(max_length=500, blank=True, null= True)
    water_sources = models.CharField(max_length=500, blank=True, null= True)
    water_sources_other = models.CharField(max_length=500, blank=True, null= True)
    # water_sources_public_tap_stand = models.BooleanField(default=False)
    # water_sources_private_tap_stand = models.BooleanField(default=False)
    # water_sources_spring = models.BooleanField(default=False)
    # water_sources_river = models.BooleanField(default=False)
    # water_sources_tube_well = models.BooleanField(default=False)
    # water_sources_other = models.BooleanField(default=False)
    tubewell_type = models.CharField(max_length=1000, blank=True, null=True)
    tubewell_status = models.CharField(max_length=1000, blank=True, null=True)
    no_of_houses_using_tubewell = models.CharField(max_length=1000, blank=True, null=True)
    has_flood_effect_tubewell = models.CharField(max_length=1000, blank=True, null=True)
    public_tap_distance = models.CharField(max_length=1000, blank=True, null=True)
    toilet_facility = models.CharField(max_length=1000, blank=True, null=True)
    toilet_type = models.CharField(max_length=1000, blank=True, null=True)
    # toilet_type_Drainage = models.BooleanField(default=False)
    # toilet_type_pit_hole = models.BooleanField(default=False)
    # toilet_type_bio_gas_attached = models.BooleanField(default=False)
    # toilet_type_septic_tank = models.BooleanField(default=False)
    # toilet_type_ring_type = models.BooleanField(default=False)
    # toilet_type_other = models.BooleanField(default=False)
    toilet_type_other = models.CharField(max_length=1000, blank=True, null=True)
    waterborne_disease = models.CharField(max_length=1000, blank=True, null=True)
    disaster_type = models.CharField(max_length=1000, blank=True, null=True)
    # disaster_type_flood = models.BooleanField(default=False)
    # disaster_type_landslide = models.BooleanField(default=False)
    # disaster_type_fire = models.BooleanField(default=False)
    # disaster_type_black_spot = models.BooleanField(default=False)
    # disaster_type_snake_bite = models.BooleanField(default=False)
    # disaster_type_animal_attack = models.BooleanField(default=False)
    # disaster_type_lightening = models.BooleanField(default=False)
    # disaster_type_road_accident = models.BooleanField(default=False)
    # disaster_type_cold_wind = models.BooleanField(default=False)
    # disaster_type_other = models.BooleanField(default=False)
    disaster_type_other = models.CharField(max_length=1000, blank=True, null=True)
    hazard_type = models.CharField(max_length=1000, blank=True, null=True)
    # hazard_type_flood = models.BooleanField(default=False)
    # hazard_type_landslide = models.BooleanField(default=False)
    # hazard_type_fire = models.BooleanField(default=False)
    # hazard_type_black_spot = models.BooleanField(default=False)
    # hazard_type_snake_bite = models.BooleanField(default=False)
    # hazard_type_animal_attack = models.BooleanField(default=False)
    # hazard_type_lightening = models.BooleanField(default=False)
    # hazard_type_road_accident = models.BooleanField(default=False)
    # hazard_type_cold_wind = models.BooleanField(default=False)
    # hazard_type_other = models.BooleanField(default=False)
    hazard_type_other = models.CharField(max_length=1000, blank=True, null=True)
    is_there_identified_risk_areas = models.CharField(max_length=1000, blank=True, null=True)
    disaster_information_medium = models.CharField(max_length=1000, blank=True, null=True)
    # information_medium_radio_or_tv = models.BooleanField(default=False)
    # information_medium_local_resident = models.BooleanField(default=False)
    # information_medium_local_newspaper = models.BooleanField(default=False)
    # information_medium_related_people = models.BooleanField(default=False)
    # information_medium_other = models.BooleanField(default=False)
    disaster_information_medium_other = models.CharField(max_length=1000, blank=True, null=True)
    knowledge_on_early_warning_system = models.CharField(max_length=1000, blank=True, null=True)
    early_warning_system_installed_nearby = models.CharField(max_length=1000, blank=True, null=True)
    got_early_warning_during_disaster = models.CharField(max_length=1000, blank=True, null=True)
    got_early_warning_during_through = models.CharField(max_length=1000, blank=True, null=True)
    medium_suitable_for_early_warning = models.CharField(max_length=1000, blank=True, null=True)
    other_medium_suitable_for_early_warning = models.CharField(max_length=1000, blank=True, null=True)
    # which_medium_suitable_for_ews_radio = models.BooleanField(default=False)
    # which_medium_suitable_for_ews_tv = models.BooleanField(default=False)
    # which_medium_suitable_for_ews_miking = models.BooleanField(default=False)
    # which_medium_suitable_for_ews_siren = models.BooleanField(default=False)
    # which_medium_suitable_for_ews_sms = models.BooleanField(default=False)
    # which_medium_suitable_for_ews_other = models.BooleanField(default=False)
    evacuation_shelter_availability = models.CharField(max_length=1000, blank=True, null=True)
    distance_to_evacuation_shelter = models.CharField(max_length=1000, blank=True, null=True)
    capacity_of_evacuation_shelter = models.CharField(max_length=1000, blank=True, null=True)
    distance_to_nearest_open_space = models.CharField(max_length=1000, blank=True, null=True)
    distance_to_nearest_market = models.CharField(max_length=1000, blank=True, null=True)
    goods_available_in_nearest_market = models.CharField(max_length=500, blank=True, null=True)
    # market_available_cereals = models.BooleanField(default=False)
    # market_available_pulses = models.BooleanField(default=False)
    # market_available_vegetables = models.BooleanField(default=False)
    # market_available_fruits = models.BooleanField(default=False)
    # market_available_edible_oil = models.BooleanField(default=False)
    # market_available_milk_products = models.BooleanField(default=False)
    # market_available_egg_and_meat = models.BooleanField(default=False)
    # market_available_agriculture_tools= models.BooleanField(default=False)
    # market_available_other_non_edible_items = models.BooleanField(default=False)
    # market_available_construction_material = models.BooleanField(default=False)
    # market_available_clothing = models.BooleanField(default=False)
    # market_available_other = models.BooleanField(default=False)
    other_goods_available_in_nearest_market = models.CharField(max_length=1000, blank=True, null=True)
    distance_to_alternative_market = models.CharField(max_length=1000, blank=True, null=True)
    alternative_market_name = models.CharField(max_length=1000, blank=True, null=True)
    nearest_market_operation_during_disaster = models.CharField(max_length=1000, blank=True, null=True)
    easy_access_to_goods = models.CharField(max_length=1000, blank=True, null=True)
    how_goods_were_managed_if_not_available_in_market = models.CharField(max_length=1000, blank=True, null=True)
    warehouse_available_in_ward = models.CharField(max_length=1000, blank=True, null=True)
    coping_mechanism_during_disaster = models.CharField(max_length=1000, blank=True, null=True)
    # coping_mechanism_residing_elsewhere = models.BooleanField(default=False)
    # coping_mechanism_relatives_or_neighbour = models.BooleanField(default=False)
    # coping_mechanism_took_a_loan = models.BooleanField(default=False)
    # coping_mechanism_sold_jwelary_assests = models.BooleanField(default=False)
    # coping_mechanism_other_assest = models.BooleanField(default=False)
    # coping_mechanism_reduced_food_quantity = models.BooleanField(default=False)
    # coping_mechanism_sold_food_stocks = models.BooleanField(default=False)
    # coping_mechanism_cattle_livestock = models.BooleanField(default=False)
    # coping_mechanism_labour_enrollment_india = models.BooleanField(default=False)
    # coping_mechanism_other = models.BooleanField(default=False)
    other_coping_mechanism_during_disaster = models.CharField(max_length=1000, blank=True, null=True)
    emergency_kit_availability_in_house = models.CharField(max_length=1000, blank=True, null=True)
    emergency_kit_material_update_frequency = models.CharField(max_length=1000, blank=True, null=True)
    involved_disaster_training = models.CharField(max_length=1000, blank=True, null=True)
    involved_disaster_training_type = models.CharField(max_length=1000, blank=True, null=True)
    # disaster_risk_management_disaster_management = models.BooleanField(default=False)
    # disaster_risk_management_first_aid = models.BooleanField(default=False)
    # disaster_risk_management_search_and_rescue = models.BooleanField(default=False)
    # disaster_risk_management_psycho_social_support = models.BooleanField(default=False)
    # disaster_risk_management_wash = models.BooleanField(default=False)
    # disaster_risk_management_vca = models.BooleanField(default=False)
    # disaster_risk_management_none = models.BooleanField(default=False)
    # disaster_risk_management_other = models.BooleanField(default=False)
    involved_disaster_training_type_other =  models.CharField(max_length=1000, blank=True, null=True)
    involved_in_simulation_type = models.CharField(max_length=1000, blank=True, null=True)
    # simulation_involvement_earthquake = models.BooleanField(default=False)
    # simulation_involvement_flood = models.BooleanField(default=False)
    # simulation_involvement_fire = models.BooleanField(default=False)
    # simulation_involvement_landslide = models.BooleanField(default=False)
    # simulation_involvement_other = models.BooleanField(default=False)
    involved_in_simulation_type_other = models.CharField(max_length=1000, blank=True, null=True)
    knowledge_about_ldcrp = models.CharField(max_length=1000, blank=True, null=True)
    involvement_in_ldcrp_development_process = models.CharField(max_length=1000, blank=True, null=True)
    knowledge_about_dprp = models.CharField(max_length=1000, blank=True, null=True)
    involvement_in_dprp_development_process = models.CharField(max_length=1000, blank=True, null=True)
    prepared_contingency_plan = models.CharField(max_length=1000, blank=True, null=True)
    most_occuring_disasters_in_ward = models.CharField(max_length=1000, blank=True, null=True)
    # ward_falling_prone_area_flood = models.BooleanField(default=False)
    # ward_falling_prone_area_earthquake = models.BooleanField(default=False)
    # ward_falling_prone_area_landslide = models.BooleanField(default=False)
    # ward_falling_prone_area_fire = models.BooleanField(default=False)
    # ward_falling_prone_area_none = models.BooleanField(default=False)
    identified_safe_place_for_flood = models.CharField(max_length=1000, blank=True, null=True)
    distance_to_safe_place_for_flood = models.CharField(max_length=1000, blank=True, null=True)
    damages_occurred_during_flood = models.CharField(max_length=500, blank=True, null=True)
    # damages_occurred_during_flood_death_or_injured_family_member = models.BooleanField(default=False)
    # damages_occurred_during_flood_house = models.BooleanField(default=False)
    # damages_occurred_during_flood_land = models.BooleanField(default=False)
    # damages_occurred_during_flood_furniture = models.BooleanField(default=False)
    # damages_occurred_during_flood_livestock = models.BooleanField(default=False)
    # damages_occurred_during_flood_crops = models.BooleanField(default=False)
    # damages_occurred_during_flood_machinary = models.BooleanField(default=False)
    # damages_occurred_during_flood_personal_documents = models.BooleanField(default=False)
    # damages_occurred_during_flood_none = models.BooleanField(default=False)
    # damages_occurred_during_flood_other = models.BooleanField(default=False)
    other_damages_occurred_during_flood = models.CharField(max_length=500, blank=True, null=True)
    house_damage_type_during_flood = models.CharField(max_length=500, blank=True, null=True)
    # house_damage_type_damage_in_foundation = models.BooleanField(default=False)
    # house_damage_type_damage_in_roof = models.BooleanField(default=False)
    # house_damage_type_damage_in_walls = models.BooleanField(default=False)
    # house_damage_type_was_flooded = models.BooleanField(default=False)
    # house_damage_type_was_none = models.BooleanField(default=False)
    # house_damage_type_other = models.BooleanField(default=False)
    house_damage_type_during_flood_other = models.CharField(max_length=500, blank=True, null=True)
    migrated_place_during_flood = models.CharField(max_length=500, blank=True, null=True)
    migrated_place_during_flood_other = models.CharField(max_length=500, blank=True, null=True)
    damage_occurred_during_landslide = models.CharField(max_length=500, blank=True, null=True)
    # damages_landslide_death_or_injured_family_member = models.BooleanField(default=False)
    # damages_occurred_during_landslide_house = models.BooleanField(default=False)
    # damages_occurred_during_landslide_land = models.BooleanField(default=False)
    # damages_occurred_during_landslide_livestock = models.BooleanField(default=False)
    # damages_occurred_during_landslide_crops = models.BooleanField(default=False)
    # damages_occurred_during_landslide_none = models.BooleanField(default=False)
    # damages_occurred_during_landslide_other = models.BooleanField(default=False)
    other_damage_occurred_during_landslide = models.CharField(max_length=500, blank=True, null=True)
    house_damage_type_during_landslide = models.CharField(max_length=500, blank=True, null=True)
    # house_damage_type_landslide_completely = models.BooleanField(default=False)
    # house_damage_type_landslide_damage_in_foundation = models.BooleanField(default=False)
    # house_damage_type_landslide_damage_in_roof = models.BooleanField(default=False)
    # house_damage_type_landslide_damage_in_walls = models.BooleanField(default=False)
    # house_damage_type_landslide_was_none = models.BooleanField(default=False)
    # house_damage_type_landslide_other = models.BooleanField(default=False)
    house_damage_type_during_landslide_other = models.CharField(max_length=500, blank=True, null=True)
    migrated_place_during_landslide = models.CharField(max_length=500, blank=True, null=True)
    damages_occurred_during_earthquake = models.CharField(max_length=500, blank=True, null=True)
    # damages_earthquake_death_or_injured_family_member = models.BooleanField(default=False)
    # damages_occurred_during_earthquake_house = models.BooleanField(default=False)
    # damages_occurred_during_earthquake_land = models.BooleanField(default=False)
    # damages_occurred_during_earthquake_livestock = models.BooleanField(default=False)
    # damages_occurred_during_earthquake_crops = models.BooleanField(default=False)
    # damages_occurred_during_earthquake_none = models.BooleanField(default=False)
    # damages_occurred_during_earthquake_other = models.BooleanField(default=False)
    other_damages_occurred_during_earthquake = models.CharField(max_length=500, blank=True, null=True)
    house_damage_type_during_earthquake = models.CharField(max_length=500, blank=True, null=True)
    # house_damage_type_earthquake_completely = models.BooleanField(default=False)
    # house_damage_type_earthquake_damage_in_foundation = models.BooleanField(default=False)
    # house_damage_type_earthquake_damage_in_roof = models.BooleanField(default=False)
    # house_damage_type_earthquake_damage_in_walls = models.BooleanField(default=False)
    # house_damage_type_earthquake_was_none = models.BooleanField(default=False)
    # house_damage_type_earthquake_other = models.BooleanField(default=False)
    # house_damage_type_earthquake_other_mention_ne = models.CharField(max_length=500, blank=True, null=True)
    house_damage_type_during_earthquake_other = models.CharField(max_length=500, blank=True, null=True)
    migrated_place_during_earthquake = models.CharField(max_length=500, blank=True, null=True)
    # place_you_migrated_earthquake_ne = models.CharField(max_length=500, blank=True, null=True)
    # place_you_migrated_earthquake_en = models.CharField(max_length=500, blank=True, null=True)
    # place_you_migrated_earthquake_school = models.BooleanField(default=False)
    # place_you_migrated_earthquake_evacuation_shelter = models.BooleanField(default=False)
    # place_you_migrated_earthquake_relative_or_neighbour = models.BooleanField(default=False)
    # place_you_migrated_earthquake_open_space = models.BooleanField(default=False)
    # place_you_migrated_earthquake_other = models.BooleanField(default=False)
    damages_occurred_during_fire = models.CharField(max_length=500, blank=True, null=True)
    # damages_fire_death_or_injured_family_member = models.BooleanField(default=False)
    # damages_occurred_during_fire_house = models.BooleanField(default=False)
    # damages_occurred_during_fire_land = models.BooleanField(default=False)
    # damages_occurred_during_fire_livestock = models.BooleanField(default=False)
    # damages_occurred_during_fire_crops = models.BooleanField(default=False)
    # damages_occurred_during_fire_none = models.BooleanField(default=False)
    # damages_occurred_during_fire_other = models.BooleanField(default=False)
    other_damages_occured_during_fire = models.CharField(max_length=500, blank=True, null=True)
    house_damage_type_during_fire = models.CharField(max_length=500, blank=True, null=True)
    # house_damage_type_fire_completely = models.BooleanField(default=False)
    # house_damage_type_fire_damage_in_foundation = models.BooleanField(default=False)
    # house_damage_type_fire_damage_in_roof = models.BooleanField(default=False)
    # house_damage_type_fire_damage_in_walls = models.BooleanField(default=False)
    # house_damage_type_fire_was_none = models.BooleanField(default=False)
    # house_damage_type_fire_other = models.BooleanField(default=False)
    # house_damage_type_fire_other_mention_ne = models.CharField(max_length=500, blank=True, null=True)
    house_damage_type_during_fire_other = models.CharField(max_length=500, blank=True, null=True)
    fire_extinguisher_in_house = models.CharField(max_length=500, blank=True, null=True)
    migrated_place_during_fire = models.CharField(max_length=500, blank=True, null=True)
    # place_you_migrated_fire_school = models.BooleanField(default=False)
    # place_you_migrated_fire_evacuation_shelter = models.BooleanField(default=False)
    # place_you_migrated_fire_relative_or_neighbour = models.BooleanField(default=False)
    # place_you_migrated_fire_open_space = models.BooleanField(default=False)
    # place_you_migrated_fire_other = models.BooleanField(default=False)
    migrated_place_during_fire_other = models.CharField(max_length=500, blank=True, null=True)
    remarks = models.CharField(max_length=500, blank=True, null=True)




class OwnerFamilyData(models.Model):
    index = models.CharField(max_length=500, blank=True, null=True)
    parent_index = models.CharField(max_length=500, blank=True, null=True)
    name = models.CharField(max_length=500, blank=True, null=True)
    age_group = models.CharField(max_length=500, blank=True, null=True)
    gender = models.CharField(max_length=500, blank=True, null=True)
    citizenship_number = models.CharField(max_length=500, blank=True, null=True)
    education_level = models.CharField(max_length=500, blank=True, null=True)
    occupation = models.CharField(max_length=500, blank=True, null=True)
    occupation_other = models.CharField(max_length=500, blank=True, null=True)
    working_status = models.CharField(max_length=500, blank=True, null=True)
    monthly_income = models.CharField(max_length=500, blank=True, null=True)
    falling_under_social_security_criteria = models.CharField(max_length=500, blank=True, null=True)
    social_security_received = models.CharField(max_length=500, blank=True, null=True)
    reasons_for_not_received_social_security = models.CharField(max_length=500, blank=True, null=True)
    other_reasons_for_not_received_social_security = models.CharField(max_length=500, blank=True, null=True)
    status_of_family_member = models.CharField(max_length=500, blank=True, null=True)
    status_of_family_member_other =models.CharField(max_length=200, blank=True, null=True)
    disability_type = models.CharField(max_length=500, blank=True, null=True)
    disability_type_other = models.CharField(max_length=500, blank=True, null=True)
    chronic_illness =models.CharField(max_length=200, blank=True, null=True)
    chronic_illness_other =models.CharField(max_length=200, blank=True, null=True)
    survey = models.ForeignKey('HouseHoldData', on_delete=models.CASCADE, related_name= 'house_hold_data')

    def save(self, *args, **kwargs):
        self.survey__index = self.parent_index
        super().save(*args, **kwargs)


class AnimalDetailData(models.Model):
    index = models.CharField(max_length=500, blank=True, null=True)
    parent_index = models.CharField(max_length=500, blank=True, null=True)
    animal_type = models.CharField(max_length=500, blank=True, null=True)
    animal_number = models.CharField(max_length=500, blank=True, null=True)
    is_it_for_commercial_purpose = models.CharField(max_length=500, blank=True, null=True)
    survey = models.ForeignKey('HouseHoldData', on_delete=models.CASCADE, related_name= 'animal_detail_data')

    def save(self, *args, **kwargs):
        self.survey__index = self.parent_index
        super(AnimalDetailData, self).save(*args, **kwargs)




class OtherFamilyMember(models.Model):
    index = models.CharField(max_length=500, blank=True, null=True)
    parent_index = models.CharField(max_length=500, blank=True, null=True)
    other_family_numbers = models.CharField(max_length=500, blank=True, null=True)
    females_less_then_5_years = models.CharField(max_length=500, blank=True, null=True)
    males_less_then_5_years = models.CharField(max_length=500, blank=True, null=True)
    females_between_5_to_15_years = models.CharField(max_length=500, blank=True, null=True)
    males_between_5_to_15_years = models.CharField(max_length=500, blank=True, null=True)
    females_between_16_to_59_years = models.CharField(max_length=500, blank=True, null=True)
    males_between_16_to_59_years = models.CharField(max_length=500, blank=True, null=True)
    females_between_60_to_70_years = models.CharField(max_length=500, blank=True, null=True)
    males_between_60_to_70_years = models.CharField(max_length=500, blank=True, null=True)
    females_above_70_years = models.CharField(max_length=500, blank=True, null=True)
    males_above70_years = models.CharField(max_length=500, blank=True, null=True)
    total_persons = models.CharField(max_length=500, blank=True, null=True)
    pregnant_number = models.CharField(max_length=500, blank=True, null=True)
    disabled = models.CharField(max_length=500, blank=True, null=True)
    disablility_type = models.CharField(max_length=500, blank=True, null=True)
    disablility_type_other = models.CharField(max_length=500, blank=True, null=True)
    survey = models.ForeignKey('HouseHoldData', on_delete=models.CASCADE, related_name='other_family_member')

    def save(self, *args, **kwargs):
        self.survey__index = self.parent_index
        super(OtherFamilyMember, self).save(*args, **kwargs)






0
















































































































