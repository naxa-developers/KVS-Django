
from django.db import models
from django.contrib.gis.db.models import PointField, MultiPolygonField
from django.contrib.auth.models import Group, User
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image
import os.path


# Create your models here.


class Province(models.Model):
    name = models.CharField(max_length=50)
    code = models.IntegerField(null=True, blank=True)
    boundary = MultiPolygonField(null=True, blank=True)

    class Meta:
        ordering = ['name']

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

    class Meta:
        ordering = ['name']



class Municipality(models.Model):
    name = models.CharField(max_length=50)
    province = models.ForeignKey('Province', related_name='municipality',
                                 on_delete=models.CASCADE, blank=True, null=True)
    district = models.ForeignKey('District', related_name='municipality',
                                 on_delete=models.CASCADE)
    hlcit_code = models.CharField(max_length=1000, blank=True, null=True)
    boundary = MultiPolygonField(null=True, blank=True)


    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Ward(models.Model):
    name = models.CharField(max_length=50)
    province = models.ForeignKey('Province', related_name='ward',
                                 on_delete=models.CASCADE, blank=True, null=True)
    district = models.ForeignKey('District', related_name='ward',
                                 on_delete=models.CASCADE)
    municipality = models.ForeignKey('Municipality', related_name='ward',
                                 on_delete=models.CASCADE)


class UserRole(models.Model):
    user = models.ForeignKey(User, related_name='role', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='role',
                              on_delete=models.CASCADE)
    province = models.ForeignKey('Province', related_name='role',
                                 on_delete=models.CASCADE, null=True, blank=True)
    district = models.ForeignKey('District', related_name='role',
                                 on_delete=models.CASCADE, null=True, blank=True)
    municipality = models.ForeignKey('Municipality', related_name='role',
                                     on_delete=models.CASCADE, null=True, blank=True)
    ward = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Gallery(models.Model):
    image = models.ImageField(upload_to='house_gallery')
    survey = models.ForeignKey('HouseHoldData', on_delete=models.CASCADE, related_name='gallery')


class HouseHoldData(models.Model):
    index = models.CharField(max_length=1000, blank=True, null=True)
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
    date_of_birth = models.DateField(blank=True, null=True)
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
    other_occupation = models.CharField(max_length=1000, blank=True, null=True)
    business = models.CharField(max_length=1000, blank=True, null=True)
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
    other_insurance = models.CharField(max_length=1000, blank=True, null=True)
    vehicle = models.CharField(max_length=1000, blank=True, null=True)
    vehicles_other = models.CharField(max_length=1000, blank=True, null=True)
    facilities_type = models.CharField(max_length=1000, blank=True, null=True)
    other_facilities = models.CharField(max_length=1000, blank=True, null=True)
    fuel_type = models.CharField(max_length=1000, blank=True, null=True)
    other_fuel_type = models.CharField(max_length=1000, blank=True, null=True)
    land_ownership = models.CharField(max_length=1000, blank=True, null=True)
    house_type = models.CharField(max_length=1000, blank=True, null=True)
    house_type_other = models.CharField(max_length=1000, blank=True, null=True)
    house_built_year = models.CharField(max_length=1000, blank=True, null=True)
    house_stories = models.CharField(max_length=1000, blank=True, null=True)
    no_of_rooms = models.CharField(max_length=1000, blank=True, null=True)
    house_map_registered = models.CharField(max_length=1000, blank=True, null=True)
    building_standard_code = models.CharField(max_length=1000, blank=True, null=True)
    earthquake_resistance = models.CharField(max_length=1000, blank=True, null=True)
    flood_prone = models.CharField(max_length=1000, blank=True, null=True)
    flood_resilience_work = models.CharField(max_length=1000, blank=True, null=True)
    flood_resilience_activities = models.CharField(max_length=1000, blank=True, null=True)
    flood_activities_resilience_other = models.CharField(max_length=1000, blank=True, null=True)
    owned_land_area = models.CharField(max_length=1000, blank=True, null=True)
    owned_land_near_river = models.CharField(max_length=1000, blank=True, null=True)
    owned_land_area_near_river = models.CharField(max_length=1000, blank=True, null=True)
    owned_land_image_name = models.CharField(max_length=1000, blank=True, null=True)
    owned_land_image = models.ImageField(upload_to='house_hold', blank=True, null=True)
    technical_manpower_presence = models.CharField(max_length=1000, blank=True, null=True)
    manpower_type = models.CharField(max_length=1000, blank=True, null=True)
    doctor_sex = models.CharField(max_length=1000, blank=True, null=True)
    doctor_male_number = models.CharField(max_length=1000, blank=True, null=True)
    doctor_female_number = models.CharField(max_length=1000, blank=True, null=True)
    engineer_sex = models.CharField(max_length=1000, blank=True, null=True)
    engineer_male_number = models.CharField(max_length=1000, blank=True, null=True)
    engineer_female_number = models.CharField(max_length=1000, blank=True, null=True)
    subengineer_sex = models.CharField(max_length=1000, blank=True, null=True)
    subengineer_male = models.CharField(max_length=1000, blank=True, null=True)
    subengineer_female = models.CharField(max_length=1000, blank=True, null=True)
    nurse_sex = models.CharField(max_length=1000, blank=True, null=True)
    nurse_male_number = models.CharField(max_length=1000, blank=True, null=True)
    nurse_female_number = models.CharField(max_length=1000, blank=True, null=True)
    ha_lab_sex = models.CharField(max_length=1000, blank=True, null=True)
    ha_lab_male_number = models.CharField(max_length=1000, blank=True, null=True)
    ha_lab_female_number = models.CharField(max_length=1000, blank=True, null=True)
    veterinary_sex = models.CharField(max_length=1000, blank=True, null=True)
    veterinary_male_number = models.CharField(max_length=1000, blank=True, null=True)
    veterinary_female_number = models.CharField(max_length=1000, blank=True, null=True)
    dakarmi_sikarmi_sex = models.CharField(max_length=1000, blank=True, null=True)
    dakarmi_sikarmi_male_number = models.CharField(max_length=1000, blank=True, null=True)
    dakarmi_sikarmi_female_number = models.CharField(max_length=1000, blank=True, null=True)
    plumber_sex = models.CharField(max_length=1000, blank=True, null=True)
    plumber_male_number = models.CharField(max_length=1000, blank=True, null=True)
    plumber_female_number = models.CharField(max_length=1000, blank=True, null=True)
    electrician_sex = models.CharField(max_length=1000, blank=True, null=True)
    electrician_male_number = models.CharField(max_length=1000, blank=True, null=True)
    electrician_female_number = models.CharField(max_length=1000, blank=True, null=True)
    jt_sex = models.CharField(max_length=1000, blank=True, null=True)
    jt_male_number = models.CharField(max_length=1000, blank=True, null=True)
    jt_female_number = models.CharField(max_length=1000, blank=True, null=True)
    other_technical = models.CharField(max_length=1000, blank=True, null=True)
    other_technical_sex = models.CharField(max_length=1000, blank=True, null=True)
    other_technical_male_number = models.CharField(max_length=1000, blank=True, null=True)
    other_technical_female_number = models.CharField(max_length=1000, blank=True, null=True)
    distance_from_main_road = models.CharField(max_length=500, blank=True, null= True)
    road_type = models.CharField(max_length=500, blank=True, null= True)
    road_width = models.CharField(max_length=500, blank=True, null= True)
    road_capacity = models.CharField(max_length=500, blank=True, null= True)
    distance_from_nearest_school = models.CharField(max_length=500, blank=True, null= True)
    distance_from_nearest_health_institution = models.CharField(max_length=500, blank=True, null= True)
    distance_from_nearest_security_forces = models.CharField(max_length=500, blank=True, null= True)
    water_sources = models.CharField(max_length=500, blank=True, null= True)
    water_sources_other = models.CharField(max_length=500, blank=True, null= True)
    tubewell_type = models.CharField(max_length=1000, blank=True, null=True)
    tubewell_status = models.CharField(max_length=1000, blank=True, null=True)
    no_of_houses_using_tubewell = models.CharField(max_length=1000, blank=True, null=True)
    has_flood_effect_tubewell = models.CharField(max_length=1000, blank=True, null=True)
    public_tap_distance = models.CharField(max_length=1000, blank=True, null=True)
    toilet_facility = models.CharField(max_length=1000, blank=True, null=True)
    toilet_type = models.CharField(max_length=1000, blank=True, null=True)
    toilet_type_other = models.CharField(max_length=1000, blank=True, null=True)
    waterborne_disease = models.CharField(max_length=1000, blank=True, null=True)
    disaster_type = models.CharField(max_length=1000, blank=True, null=True)
    disaster_type_other = models.CharField(max_length=1000, blank=True, null=True)
    hazard_type = models.CharField(max_length=1000, blank=True, null=True)
    hazard_type_other = models.CharField(max_length=1000, blank=True, null=True)
    is_there_identified_risk_areas = models.CharField(max_length=1000, blank=True, null=True)
    disaster_information_medium = models.CharField(max_length=1000, blank=True, null=True)
    disaster_information_medium_other = models.CharField(max_length=1000, blank=True, null=True)
    knowledge_on_early_warning_system = models.CharField(max_length=1000, blank=True, null=True)
    early_warning_system_installed_nearby = models.CharField(max_length=1000, blank=True, null=True)
    got_early_warning_during_disaster = models.CharField(max_length=1000, blank=True, null=True)
    got_early_warning_during_through = models.CharField(max_length=1000, blank=True, null=True)
    medium_suitable_for_early_warning = models.CharField(max_length=1000, blank=True, null=True)
    other_medium_suitable_for_early_warning = models.CharField(max_length=1000, blank=True, null=True)
    evacuation_shelter_availability = models.CharField(max_length=1000, blank=True, null=True)
    distance_to_evacuation_shelter = models.CharField(max_length=1000, blank=True, null=True)
    capacity_of_evacuation_shelter = models.CharField(max_length=1000, blank=True, null=True)
    distance_to_nearest_open_space = models.CharField(max_length=1000, blank=True, null=True)
    distance_to_nearest_market = models.CharField(max_length=1000, blank=True, null=True)
    goods_available_in_nearest_market = models.CharField(max_length=500, blank=True, null=True)
    other_goods_available_in_nearest_market = models.CharField(max_length=1000, blank=True, null=True)
    distance_to_alternative_market = models.CharField(max_length=1000, blank=True, null=True)
    alternative_market_name = models.CharField(max_length=1000, blank=True, null=True)
    nearest_market_operation_during_disaster = models.CharField(max_length=1000, blank=True, null=True)
    easy_access_to_goods = models.CharField(max_length=1000, blank=True, null=True)
    how_goods_were_managed_if_not_available_in_market = models.CharField(max_length=1000, blank=True, null=True)
    warehouse_available_in_ward = models.CharField(max_length=1000, blank=True, null=True)
    coping_mechanism_during_disaster = models.CharField(max_length=1000, blank=True, null=True)
    other_coping_mechanism_during_disaster = models.CharField(max_length=1000, blank=True, null=True)
    emergency_kit_availability_in_house = models.CharField(max_length=1000, blank=True, null=True)
    emergency_kit_material_update_frequency = models.CharField(max_length=1000, blank=True, null=True)
    involved_disaster_training = models.CharField(max_length=1000, blank=True, null=True)
    involved_disaster_training_type = models.CharField(max_length=1000, blank=True, null=True)
    involved_disaster_training_type_other =  models.CharField(max_length=1000, blank=True, null=True)
    involved_in_simulation_type = models.CharField(max_length=1000, blank=True, null=True)
    involved_in_simulation_type_other = models.CharField(max_length=1000, blank=True, null=True)
    knowledge_about_ldcrp = models.CharField(max_length=1000, blank=True, null=True)
    involvement_in_ldcrp_development_process = models.CharField(max_length=1000, blank=True, null=True)
    knowledge_about_dprp = models.CharField(max_length=1000, blank=True, null=True)
    involvement_in_dprp_development_process = models.CharField(max_length=1000, blank=True, null=True)
    prepared_contingency_plan = models.CharField(max_length=1000, blank=True, null=True)
    most_occuring_disasters_in_ward = models.CharField(max_length=1000, blank=True, null=True)
    identified_safe_place_for_flood = models.CharField(max_length=1000, blank=True, null=True)
    distance_to_safe_place_for_flood = models.CharField(max_length=1000, blank=True, null=True)
    damages_occurred_during_flood = models.CharField(max_length=500, blank=True, null=True)
    other_damages_occurred_during_flood = models.CharField(max_length=500, blank=True, null=True)
    house_damage_type_during_flood = models.CharField(max_length=500, blank=True, null=True)
    house_damage_type_during_flood_other = models.CharField(max_length=500, blank=True, null=True)
    migrated_place_during_flood = models.CharField(max_length=500, blank=True, null=True)
    migrated_place_during_flood_other = models.CharField(max_length=500, blank=True, null=True)
    damage_occurred_during_landslide = models.CharField(max_length=500, blank=True, null=True)
    other_damage_occurred_during_landslide = models.CharField(max_length=500, blank=True, null=True)
    house_damage_type_during_landslide = models.CharField(max_length=500, blank=True, null=True)
    house_damage_type_during_landslide_other = models.CharField(max_length=500, blank=True, null=True)
    migrated_place_during_landslide = models.CharField(max_length=500, blank=True, null=True)
    damages_occurred_during_earthquake = models.CharField(max_length=500, blank=True, null=True)
    other_damages_occurred_during_earthquake = models.CharField(max_length=500, blank=True, null=True)
    house_damage_type_during_earthquake = models.CharField(max_length=500, blank=True, null=True)
    house_damage_type_during_earthquake_other = models.CharField(max_length=500, blank=True, null=True)
    migrated_place_during_earthquake = models.CharField(max_length=500, blank=True, null=True)
    damages_occurred_during_fire = models.CharField(max_length=500, blank=True, null=True)
    other_damages_occured_during_fire = models.CharField(max_length=500, blank=True, null=True)
    house_damage_type_during_fire = models.CharField(max_length=500, blank=True, null=True)
    house_damage_type_during_fire_other = models.CharField(max_length=500, blank=True, null=True)
    fire_extinguisher_in_house = models.CharField(max_length=500, blank=True, null=True)
    migrated_place_during_fire = models.CharField(max_length=500, blank=True, null=True)
    migrated_place_during_fire_other = models.CharField(max_length=500, blank=True, null=True)
    remarks = models.CharField(max_length=500, blank=True, null=True)
    owned_land_image_thumbnail = models.ImageField(upload_to='thumbs', editable=False, null=True, blank=True)

    def make_thumbnail(self):

        image = Image.open(self.owned_land_image)
        image.thumbnail((600, 400), Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.owned_land_image.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False  # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.owned_land_image_thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True

    def save(self, *args, **kwargs):
        if self.owned_land_image:
            if not self.make_thumbnail():
                # set to a default thumbnail
                raise Exception('Could not create thumbnail - is the file type valid?')

        else:
            pass
        super(HouseHoldData, self).save(*args, **kwargs)

    def __str__(self):
        return self.owner_name




class OwnerFamilyData(models.Model):
    index = models.CharField(max_length=500, blank=True, null=True)
    parent_index = models.CharField(max_length=500, blank=True, null=True)
    name = models.CharField(max_length=500, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
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


class AnimalDetailData(models.Model):
    index = models.CharField(max_length=500, blank=True, null=True)
    parent_index = models.CharField(max_length=500, blank=True, null=True)
    animal_type = models.CharField(max_length=500, blank=True, null=True)
    animal_type_other = models.CharField(max_length=500, blank=True, null=True)
    animal_number = models.CharField(max_length=500, blank=True, null=True)
    is_it_for_commercial_purpose = models.CharField(max_length=500, blank=True, null=True)
    survey = models.ForeignKey('HouseHoldData', on_delete=models.CASCADE, related_name= 'animal_detail_data')



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



















































































































