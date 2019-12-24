
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
    hlcit_code = models.CharField(max_length=100, blank=True, null=True)
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


class DamageList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class HouseDamageList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class DamageType(models.Model):
    damages = models.BooleanField(default=False)
    damage_type = models.ForeignKey('DamageList', on_delete=models.CASCADE, related_name='damage_type')
    if_house_damage_type = models.ForeignKey('HouseDamageList', on_delete=models.CASCADE,
                                             related_name='damage_type', blank=True, null=True)
    if_house_other_damage = models.CharField(max_length=500, blank=True, null=True)
    damage_other = models.CharField(max_length=500, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.damage_type.name != 'house':
            if_house_damage_type = None
        super(DamageType, self).save(*args, **kwargs)


class DisasterList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MigrationList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class DisasterProne(models.Model):
    MIGRATED_CHOICES = (
        (1, 'School'),
        (1, 'Evacuation shelter'),
        (1, 'In relative/neighbor\'s house'),
        (1, 'Open space'),
        (1, 'Other'),
    )
    name = models.ForeignKey('DisasterList', on_delete=models.CASCADE, related_name='disaster_prone')
    disaster_other = models.CharField(max_length=500, blank=True, null=True)
    damage_type = models.ForeignKey('DamageType', on_delete=models.CASCADE, blank=True, null=True)
    migration = models.BooleanField(default=False)
    place = models.CharField(max_length=500, blank=True, null=True)
    how_long_you_migrated = models.CharField(max_length=300, blank=True, null=True)
    capacity_of_migration_sheltered = models.IntegerField(blank=True, null=True)
    migration_choice = models.IntegerField(blank=True, null=True, choices=MIGRATED_CHOICES)
    if_other_migration_choice = models.CharField(max_length=500, blank=True, null=True)
    house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='disaster_prone')
    have_fire_extinguisher = models.NullBooleanField(default=False)

    def __str__(self):
        return self.name


class VulnerablePopulation(models.Model):
    POPULATION_CHOICES = (
        (1, 'Pregnant'),
        (2, 'Breast feeding woman'),
        (3, 'Single Woman/widow'),
        (4, 'Senior Citizen'),
        (5, 'People with disability'),
        (6, 'Chronic illness'),
        (7, 'Nutrition support'),
    )
    name = models.IntegerField(choices=POPULATION_CHOICES, default=1)


class OccupationList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BusinessList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Occupation(models.Model):
    occupation = models.ForeignKey('OccupationList', on_delete=models.CASCADE, related_name='occupation')
    if_occupation = models.BooleanField(default=False)
    if_business = models.BooleanField(default=False)
    if_business_its_type = models.ForeignKey('BusinessList', on_delete=models.CASCADE, related_name='occupation')
    if_other_occupation = models.CharField(max_length=300, blank=True, null=True)
    if_other_business_occupation = models.CharField(max_length=300, blank=True, null=True)
    if_other_agriculture_business = models.CharField(max_length=300, blank=True, null=True)
    if_other_small_business = models.CharField(max_length=300, blank=True, null=True)
    if_agriculture_business_harvest_sufficient = models.CharField(max_length=200, blank=True, null=True)
    house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE,
                                   related_name='occupation', blank=True, null=True)

    def __str__(self):
        return self.occupation

    def save(self, *args, **kwargs):
        if self.occupation.name == 'Business':
            self.if_business = True
        elif self.occupation.name != 'Business':
            self.if_business_its_type = None
            self.if_other_business_occupation = None
            self.if_other_agriculture_business = None
            self.if_other_small_business = None
            self.if_agriculture_business_harvest_sufficient = None
        else:
            pass
        super(Occupation, self).save(*args, **kwargs)


class FoodChoice(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class FoodEaten(models.Model):
    food = models.ForeignKey('FoodChoice', on_delete=models.CASCADE,
                             related_name='food_eaten', null=True, blank=True)
    no_of_days_food_eaten = models.IntegerField(blank=True, null=True)
    house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='food_eaten')

    def __str__(self):
        return self.food.name


class InsuranceList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Insurance(models.Model):
    have_insurance = models.BooleanField(default=False)
    insurance = models.ForeignKey('InsuranceList', on_delete=models.CASCADE,
                                  related_name='insurance', null=True, blank=True)
    if_other_insurance_choice = models.CharField(max_length=500, blank=True, null=True)
    house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='insurance')


class VehicleList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    vehicle = models.ForeignKey('VehicleList', on_delete=models.CASCADE,
                                related_name='vehicle', null=True, blank=True)
    have_vehicle = models.BooleanField(default=False)
    if_other_heavy_equipment = models.CharField(max_length=1000, blank=True, null=True)
    house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='vehicle')


class FacilityList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Facilities(models.Model):
    facility = models.ForeignKey('FacilityList', on_delete=models.CASCADE,
                                 related_name='facility', null=True, blank=True)
    have_facility = models.BooleanField(default=False)
    if_other_facility = models.CharField(max_length=1000, blank=True, null=True)
    house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='facility')


class FuelTypeList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Fuel(models.Model):
    fuel = models.ForeignKey('FuelTypeList', on_delete=models.CASCADE,
                             related_name='fuel', null=True, blank=True)
    have_fuel = models.BooleanField(default=False)
    if_other_fuel = models.CharField(max_length=1000, blank=True, null=True)
    house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='fuel')


class WorkDoneOnFloodList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class WorkDoneOnFlood(models.Model):
    work_done = models.ForeignKey('WorkDoneOnFloodList', on_delete=models.CASCADE,
                                  related_name='work_done', null=True, blank=True)
    if_other_work = models.CharField(max_length=1000, blank=True, null=True)
    house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='work_done')


class DrinkingWaterList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class DrinkingWater(models.Model):
    STATUS_CHOICE = (
        (1, 'Public'),
        (1, 'Private')
    )

    drinking_water = models.ForeignKey('DrinkingWaterList', on_delete=models.CASCADE,
                                       related_name='drinking_water',null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICE, blank=True, null=True)
    if_other_drinking_water = models.CharField(max_length=1000, blank=True, null=True)
    number_of_house_using_source = models.IntegerField(blank=True, null=True)
    distance_to_source = models.CharField(max_length=100, blank=True, null=True)
    house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='drinking_water')


class TechnicalFieldList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TechnicalField(models.Model):
    GENDER_CHOICES = (
        (1, 'Male'),
        (2, 'Female')
    )

    technical = models.ForeignKey('TechnicalField', on_delete=models.CASCADE,
                                  related_name='technical_man', null=True, blank=True)
    number_of_technical = models.IntegerField(blank=True, null=True)
    gender = models.OneToOneField('GenderList', on_delete=models.CASCADE,
                                  related_name='technical_gender', blank=True, null=True)
    if_other_technical = models.CharField(max_length=1000, blank=True, null=True)
    house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='technical_man')


class InformationMediumList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class InformationMedium(models.Model):
    info_medium = models.ForeignKey('InformationMediumList', on_delete=models.CASCADE,
                                    related_name='info_medium', null=True, blank=True)
    have_information = models.BooleanField(default=False)
    if_other_medium = models.CharField(max_length=200, blank=True, null=True)
    house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='info_medium')


class WarningMediumList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class WarningMediumSuitableForDisaster(models.Model):
    warning_medium = models.ForeignKey('WarningMediumList', on_delete=models.CASCADE,
                                       related_name='warn_medium', null=True, blank=True)
    if_warning_medium = models.BooleanField(default=False)
    if_other_medium = models.CharField(max_length=200, blank=True, null=True)
    house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='warn_medium')


class MaterialsInNearestMarketList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MaterialsInNearestMarket(models.Model):
    material_in_market = models.ForeignKey('MaterialsInNearestMarketList', on_delete=models.CASCADE,
                                           related_name='market_material', null=True, blank=True)
    is_material_available = models.NullBooleanField(default=False)
    if_other_material = models.CharField(max_length=200, blank=True, null=True)
    house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='market_material')


class CopingMechanismList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CopingMechanism(models.Model):
    coping_medium = models.ForeignKey('CopingMechanismList', on_delete=models.CASCADE,
                                      related_name='coping_mechanism', null=True, blank=True)
    is_coping_medium = models.NullBooleanField(default=False)
    if_other_medium = models.CharField(max_length=200, blank=True, null=True)
    house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='coping_mechanism')


class DisasterPreparednessMechanismList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class DisasterPreparednessMechanism(models.Model):
    preparedness = models.ForeignKey('DisasterPreparednessMechanismList', on_delete=models.CASCADE,
                                     related_name='disaster_prepare', null=True, blank=True)
    involved_in_disaster_preparedness = models.NullBooleanField(default=False)
    if_other_preparedness = models.CharField(max_length=200, blank=True, null=True)
    house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='disaster_prepare')


class InvolvedInSimulation(models.Model):
    simulation = models.ForeignKey('DisasterList', on_delete=models.CASCADE,
                                   related_name='simulation', null=True, blank=True)
    involved_in_hazard_simulation = models.NullBooleanField(default=False)
    if_other_simulation = models.CharField(max_length=200, blank=True, null=True)
    house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='simulation')


class GuideLineList(models.Model):
    name = models.CharField(max_length=200)


class GuideLine(models.Model):
    GUIDELINE_CHOICES = (
        (1, 'LDCRP guideline'),
        (1, 'DPRP guideline'),
    )
    guideline = models.ForeignKey('GuideLineList', on_delete=models.CASCADE,
                                  related_name='guideLine', null=True, blank=True)
    know_about_guideline = models.BooleanField(default=False)
    involved_in_development_process = models.BooleanField(default=False)
    house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE,
                                   related_name='guideLine', blank=True, null=True)


class WardFallingProneArea(models.Model):
    prone_area = models.ForeignKey('DisasterList', on_delete=models.CASCADE,
                                   related_name='ward_prone', null=True, blank=True)
    is_prone_area = models.BooleanField(default=False)
    ward_identified_safe_place_during = models.BooleanField(default=False)
    time_to_safe_place = models.CharField(blank=True, null=True, max_length=200)
    disaster_prone = models.ForeignKey('DisasterProne', on_delete=models.CASCADE, related_name='ward_prone')


class GenderList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class WhoseOwnershipList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class WhoseOwnershipData(models.Model):
    ownership = models.ForeignKey('WhoseOwnershipList', on_delete=models.CASCADE, related_name='WhoseOwnershipData')
    have_ownership = models.BooleanField(default=False)
    house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='WhoseOwnershipData')


class HouseTypeList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class HouseType(models.Model):
    ownership = models.ForeignKey('HouseTypeList', on_delete=models.CASCADE)
    have_house = models.BooleanField(default=False)
    house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='house_type')


class OwnershipList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class EthnicityList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ReligionList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MotherTongueList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class EducationList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PermitList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class RoadType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class RoadCapacity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class RoadCapacityType(models.Model):
    road = models.ForeignKey('RoadCapacity', on_delete=models.CASCADE,
                             related_name='household_road', blank=True, null=True)
    have_road = models.BooleanField(default=False)
    house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='household_road')


class LatrineList(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Latrine(models.Model):
    latrine = models.ForeignKey('LatrineList', on_delete=models.CASCADE,
                                related_name='latrine', blank=True, null=True)
    have_latrine = models.BooleanField(default=False)
    if_other_latrine = models.CharField(max_length=200, blank=True, null=True)
    house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='latrine')


class HouseHold(models.Model):
    index = models.IntegerField(blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    surveyor_name = models.CharField(max_length=500)
    name_of_place = models.CharField(max_length=500)
    ward_no = models.IntegerField(blank=True, null=True)
    location = PointField(geography=True, srid=4326, blank=True, null=True)
    altitude = models.CharField(max_length=100, blank=True, null=True)
    precision = models.CharField(max_length=100, blank=True, null=True)
    household_no = models.IntegerField(blank=True, null=True)
    house_holder_name = models.CharField(max_length=500, blank=True, null=True)
    age_of_owner = models.IntegerField()
    gender_of_house_owner = models.OneToOneField('GenderList', on_delete=models.CASCADE,
                                                 related_name='gender', blank=True, null=True)
    status_of_owner = models.OneToOneField('OwnershipList', on_delete=models.CASCADE,
                                           related_name='status', blank=True, null=True)
    if_other_owner_status = models.CharField(max_length=500, blank=True, null=True)
    ethnicity = models.OneToOneField('OwnershipList', on_delete=models.CASCADE,
                                     related_name='ethnicity', blank=True, null=True)
    other_ethnicity = models.CharField(max_length=200, blank=True, null=True)
    religion = models.OneToOneField('ReligionList', on_delete=models.CASCADE,
                                    related_name='religion', blank=True, null=True)
    religion_other = models.CharField(max_length=200, blank=True, null=True)
    mother_tongue = models.OneToOneField('MotherTongueList', on_delete=models.CASCADE,
                                         related_name='mother_tongue', blank=True, null=True)
    other_mother_tongue = models.CharField(max_length=200, blank=True, null=True)
    contact_num = models.CharField(max_length=50, blank=True, null=True)
    education_level = models.OneToOneField('EducationList', on_delete=models.CASCADE,
                                           related_name='education_level', blank=True, null=True)
    owner_citizenship_number = models.CharField(max_length=100, blank=True, null=True)
    responder_name = models.CharField(max_length=200, blank=True, null=True)
    responder_gender = models.OneToOneField('GenderList', on_delete=models.CASCADE,
                                            related_name='responder_gender', blank=True, null=True)
    responder_age = models.CharField(max_length=5, blank=True, null=True)
    responder_contact = models.CharField(max_length=20, blank=True, null=True)
    other_family_member = models.BooleanField(default=False)
    foods_eaten_in_last7_day = models.CharField(max_length=1000, blank=True, null=True)
    monthly_expanses = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    monthly_income = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    if_loan_amount = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
    loan_time = models.CharField(blank=True, null=True, max_length=300)
    have_livestock = models.BooleanField(default=False)
    date_of_establishment = models.CharField(max_length=100, blank=True, null=True)
    number_of_storey = models.CharField(max_length=10, blank=True, null=True)
    number_of_rooms = models.CharField(max_length=10, blank=True, null=True)
    received_building_permit = models.OneToOneField('PermitList', on_delete=models.CASCADE,
                                                    related_name='received_building_permit', blank=True, null=True)
    building_completion_certificate = models.OneToOneField('PermitList', on_delete=models.CASCADE,
                                                           related_name='building_completion_certificate', blank=True, null=True)
    is_house_earthquake_resilience = models.BooleanField(default=False)
    is_house_landslide_resilience = models.BooleanField(default=False)
    how_much_land_ownership = models.CharField(max_length=1000, blank=True, null=True)
    does_land_lies_near_river_flood_plain = models.BooleanField(default=False)
    land_near_river_flood_plain = models.CharField(max_length=1000, blank=True, null=True)
    image_with_landscape = models.ImageField(upload_to='house_hold', blank=True, null=True)
    time_for_nearest_road = models.CharField(max_length=200, blank=True, null=True)
    road_type = models.OneToOneField('RoadType', on_delete=models.CASCADE,
                                     related_name='road_type', blank=True, null=True)
    road_width = models.CharField(max_length=100, blank=True, null=True)
    time_to_nearest_school = models.CharField(max_length=200, blank=True, null=True)
    time_to_nearest_health_institution = models.CharField(max_length=200, blank=True, null=True)
    time_to_nearest_security_force = models.CharField(max_length=200, blank=True, null=True)
    does_ward_have_identified_risk_area = models.BooleanField(default=False)
    do_you_know_about_warning_system = models.BooleanField(default=False)
    is_there_waning_system = models.BooleanField(default=False)
    did_you_got_early_information_in_disaster = models.BooleanField(default=False)
    if_yes_which_medium_was_used = models.CharField(max_length=200, blank=True, null=True)
    does_ward_have_evacuation_shelter = models.BooleanField(default=False)
    distance_to_evacuation_shelter = models.CharField(max_length=100, blank=True, null=True)
    capacity_of_evacuation_shelter = models.BigIntegerField(blank=True, null=True)
    distance_to_nearest_openspace = models.CharField(max_length=100, blank=True, null=True)
    how_far_nearest_market = models.CharField(max_length=100, blank=True, null=True)
    was_nearest_market_operating_in_disaster = models.BooleanField(default=True)
    was_material_easily_available = models.CharField(max_length=100, blank=True, null=True)
    if_not_material_how_you_managed = models.CharField(max_length=100, blank=True, null=True)
    how_far_is_alternative_market = models.CharField(max_length=100, blank=True, null=True)
    name_of_alternative_market = models.CharField(max_length=100, blank=True, null=True)
    is_there_warehouse_in_your_ward = models.BooleanField(default=True)
    how_often_replace_material_in_emergency_kit = models.CharField(max_length=100)
    contingency_plan_involvement = models.BooleanField(default=False)

    @property
    def latitude(self):
        return self.location.y

    @property
    def longitude(self):
        return self.location.x

    def __str__(self):
        return self.house_holder_name + ',' + self.name_of_place


class InvolvementList(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class FamilyMemberCriterialist(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name


class FamilyMemberCriteriaData(models.Model):
    member_type = models.ForeignKey('FamilyMemberCriterialist', on_delete=models.CASCADE, related_name='family_member_criteria')
    if_member_type = models.BooleanField(default=False)
    owner_family = models.ForeignKey('OwnerFamily', on_delete=models.CASCADE, related_name='family_member_criteria')


class AgeGroupList(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class PopulationChoicesList(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class PopulationChoiceData(models.Model):
    population_choice = models.ForeignKey('PopulationChoicesList', on_delete=models.CASCADE,
                                          related_name='population_choice')
    if_member_type = models.BooleanField(default=False)
    owner_family = models.ForeignKey('OwnerFamily', on_delete=models.CASCADE, related_name='population_choice')


class ChronicIllnessList(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class ChronicIllnessData(models.Model):
    chronic_illness = models.ForeignKey('ChronicIllnessList', on_delete=models.CASCADE,
                                        related_name='chronic_illness')
    if_chronic_illness = models.BooleanField(default=False)
    if_other_chronic_illness = models.CharField(max_length=200, blank=True, null=True)
    owner_family = models.ForeignKey('OwnerFamily', on_delete=models.CASCADE, related_name='chronic_illness')


class DisabilityList(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class DisabilityData(models.Model):
    population_choice = models.ForeignKey('DisabilityList', on_delete=models.CASCADE,
                                          related_name='disability')
    if_disability = models.BooleanField(default=False)
    if_other_disability = models.CharField(max_length=200, blank=True, null=True)
    owner_family = models.ForeignKey('OwnerFamily', on_delete=models.CASCADE, related_name='disability')


class OwnerFamily(models.Model):
    name = models.CharField(max_length=200)
    age_group = models.OneToOneField('AgeGroupList', on_delete=models.CASCADE,
                                     related_name='age_group', blank=True, null=True)
    education_level = models.OneToOneField('EducationList', on_delete=models.CASCADE,
                                           related_name='family_education_level', blank=True, null=True)
    gender = models.OneToOneField('GenderList', on_delete=models.CASCADE,
                                  related_name='family_gender', blank=True, null=True)
    citizenship_num = models.CharField(max_length=30, blank=True, null=True)
    occupation_of_family = models.OneToOneField('Occupation', on_delete=models.CASCADE,
                                                related_name='family_occupation', blank=True, null=True)
    involvement_in_occupation = models.OneToOneField('InvolvementList', on_delete=models.CASCADE,
                                                     related_name='involvement', blank=True, null=True)
    if_other_occupation = models.CharField(max_length=300, blank=True, null=True)
    monthly_income = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    household = models.ForeignKey('OwnerFamily', on_delete=models.CASCADE, related_name='owner_family')
    received_social_security = models.BooleanField(default=False)
    reason_not_received_social_security = models.CharField(blank=True, null=True, max_length=200)
    other_population_choices = models.CharField(max_length=100, blank=True, null=True)

    # does_family_member meet_any_of_the_criteria = models.IntegerField()

    def __str__(self):
        return self.name


class AnimalDetails(models.Model):
    type_of_livestock = models.CharField(max_length=100)
    number_of_livestock = models.IntegerField()
    commercial_purpose = models.BooleanField(default=False)
    household = models.ForeignKey('OwnerFamily', on_delete=models.CASCADE, related_name='animal_detail')

    def __str__(self):
        return self.type_of_livestock






















































































































