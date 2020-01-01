
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


# class DamageList(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class HouseDamageList(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class DamageType(models.Model):
#     damages = models.BooleanField(default=False)
#     damage_type = models.ForeignKey('DamageList', on_delete=models.CASCADE, related_name='damage_type')
#     if_house_damage_type = models.ForeignKey('HouseDamageList', on_delete=models.CASCADE,
#                                              related_name='damage_type', blank=True, null=True)
#     if_house_other_damage = models.CharField(max_length=500, blank=True, null=True)
#     damage_other = models.CharField(max_length=500, blank=True, null=True)
#
#
#
# class DisasterList(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class MigrationList(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class DisasterProne(models.Model):
#     MIGRATED_CHOICES = (
#         (1, 'School'),
#         (1, 'Evacuation shelter'),
#         (1, 'In relative/neighbor\'s house'),
#         (1, 'Open space'),
#         (1, 'Other'),
#     )
#     name = models.ForeignKey('DisasterList', on_delete=models.CASCADE, related_name='disaster_prone')
#     is_disaster_prone = models.BooleanField(default=False)
#     disaster_other = models.CharField(max_length=500, blank=True, null=True)
#     damage_type = models.ForeignKey('DamageType', on_delete=models.CASCADE, blank=True, null=True)
#     migration = models.BooleanField(default=False)
#     place = models.CharField(max_length=500, blank=True, null=True)
#     how_long_you_migrated = models.CharField(max_length=300, blank=True, null=True)
#     capacity_of_migration_sheltered = models.IntegerField(blank=True, null=True)
#     migration_choice = models.IntegerField(blank=True, null=True, choices=MIGRATED_CHOICES)
#     if_other_migration_choice = models.CharField(max_length=500, blank=True, null=True)
#     house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='disaster_prone')
#     have_fire_extinguisher = models.NullBooleanField(default=False)
#
#     def __str__(self):
#         return self.name
#
#
# class VulnerablePopulation(models.Model):
#     POPULATION_CHOICES = (
#         (1, 'Pregnant'),
#         (2, 'Breast feeding woman'),
#         (3, 'Single Woman/widow'),
#         (4, 'Senior Citizen'),
#         (5, 'People with disability'),
#         (6, 'Chronic illness'),
#         (7, 'Nutrition support'),
#     )
#     name = models.IntegerField(choices=POPULATION_CHOICES, default=1)
#
#
# class OccupationList(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class BusinessList(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class Occupation(models.Model):
#     occupation = models.ForeignKey('OccupationList', on_delete=models.CASCADE, related_name='occupation')
#     if_occupation = models.BooleanField(default=False)
#     if_business = models.BooleanField(default=False)
#     if_business_its_type = models.ForeignKey('BusinessList', on_delete=models.CASCADE, related_name='occupation')
#     if_other_occupation = models.CharField(max_length=300, blank=True, null=True)
#     if_other_business_occupation = models.CharField(max_length=300, blank=True, null=True)
#     if_other_agriculture_business = models.CharField(max_length=300, blank=True, null=True)
#     if_other_small_business = models.CharField(max_length=300, blank=True, null=True)
#     if_agriculture_business_harvest_sufficient = models.CharField(max_length=200, blank=True, null=True)
#     house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE,
#                                    related_name='occupation', blank=True, null=True)
#
#     def __str__(self):
#         return self.occupation
#
#     def save(self, *args, **kwargs):
#         if self.occupation.name == 'Business':
#             self.if_business = True
#         elif self.occupation.name != 'Business':
#             self.if_business_its_type = None
#             self.if_other_business_occupation = None
#             self.if_other_agriculture_business = None
#             self.if_other_small_business = None
#             self.if_agriculture_business_harvest_sufficient = None
#         else:
#             pass
#         super(Occupation, self).save(*args, **kwargs)
#
#
# class FoodChoice(models.Model):
#     name = models.CharField(max_length=500)
#
#     def __str__(self):
#         return self.name
#
#
# class FoodEaten(models.Model):
#     food = models.ForeignKey('FoodChoice', on_delete=models.CASCADE,
#                              related_name='food_eaten', null=True, blank=True)
#     no_of_days_food_eaten = models.IntegerField(blank=True, null=True)
#     house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='food_eaten')
#
#     def __str__(self):
#         return self.food.name
#
#
# class InsuranceList(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class Insurance(models.Model):
#     have_insurance = models.BooleanField(default=False)
#     insurance = models.ForeignKey('InsuranceList', on_delete=models.CASCADE,
#                                   related_name='insurance', null=True, blank=True)
#     if_other_insurance_choice = models.CharField(max_length=500, blank=True, null=True)
#     house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='insurance')
#
#
# class VehicleList(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class Vehicle(models.Model):
#     vehicle = models.ForeignKey('VehicleList', on_delete=models.CASCADE,
#                                 related_name='vehicle', null=True, blank=True)
#     have_vehicle = models.BooleanField(default=False)
#     if_other_heavy_equipment = models.CharField(max_length=1000, blank=True, null=True)
#     house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='vehicle')
#
#
# class FacilityList(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class Facilities(models.Model):
#     facility = models.ForeignKey('FacilityList', on_delete=models.CASCADE,
#                                  related_name='facility', null=True, blank=True)
#     have_facility = models.BooleanField(default=False)
#     if_other_facility = models.CharField(max_length=1000, blank=True, null=True)
#     house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='facility')
#
#
# class FuelTypeList(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class Fuel(models.Model):
#     fuel = models.ForeignKey('FuelTypeList', on_delete=models.CASCADE,
#                              related_name='fuel', null=True, blank=True)
#     have_fuel = models.BooleanField(default=False)
#     if_other_fuel = models.CharField(max_length=1000, blank=True, null=True)
#     house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='fuel')
#
#
# class WorkDoneOnFloodList(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class WorkDoneOnFlood(models.Model):
#     work_done = models.ForeignKey('WorkDoneOnFloodList', on_delete=models.CASCADE,
#                                   related_name='work_done', null=True, blank=True)
#     if_work_done = models.BooleanField(default=False)
#     if_other_work = models.CharField(max_length=1000, blank=True, null=True)
#     house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='work_done')
#
#
# class DrinkingWaterList(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class DrinkingWater(models.Model):
#     STATUS_CHOICE = (
#         (1, 'Public'),
#         (1, 'Private')
#     )
#
#     drinking_water = models.ForeignKey('DrinkingWaterList', on_delete=models.CASCADE,
#                                        related_name='drinking_water',null=True, blank=True)
#     if_drinking_water = models.BooleanField(default=False)
#     status = models.CharField(max_length=1000, blank=True, null=True)
#     if_other_drinking_water = models.CharField(max_length=1000, blank=True, null=True)
#     number_of_house_using_source = models.IntegerField(blank=True, null=True)
#     distance_to_source = models.CharField(max_length=100, blank=True, null=True)
#     house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='drinking_water')
#
#
# class TechnicalFieldList(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class TechnicalField(models.Model):
#     GENDER_CHOICES = (
#         (1, 'Male'),
#         (2, 'Female')
#     )
#
#     technical = models.ForeignKey('TechnicalField', on_delete=models.CASCADE,
#                                   related_name='technical_man', null=True, blank=True)
#     if_technical = models.BooleanField(default=False)
#     if_sex_female = models.BooleanField(default=False)
#     female_num = models.CharField(max_length=10,blank=True, null=True)
#     male_num = models.CharField(max_length=10,blank=True, null=True)
#     if_sex_male = models.BooleanField(default=False)
#     if_other_technical = models.CharField(max_length=1000, blank=True, null=True)
#     house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='technical_man')
#
#
# class InformationMediumList(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class InformationMedium(models.Model):
#     info_medium = models.ForeignKey('InformationMediumList', on_delete=models.CASCADE,
#                                     related_name='info_medium', null=True, blank=True)
#     have_information = models.BooleanField(default=False)
#     if_other_medium = models.CharField(max_length=200, blank=True, null=True)
#     house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='info_medium')
#
#
# class WarningMediumList(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class WarningMediumSuitableForDisaster(models.Model):
#     warning_medium = models.ForeignKey('WarningMediumList', on_delete=models.CASCADE,
#                                        related_name='warn_medium', null=True, blank=True)
#     if_warning_medium = models.BooleanField(default=False)
#     if_other_medium = models.CharField(max_length=200, blank=True, null=True)
#     house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='warn_medium')
#
#
# class MaterialsInNearestMarketList(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class MaterialsInNearestMarket(models.Model):
#     material_in_market = models.ForeignKey('MaterialsInNearestMarketList', on_delete=models.CASCADE,
#                                            related_name='market_material', null=True, blank=True)
#     is_material_available = models.NullBooleanField(default=False)
#     if_other_material = models.CharField(max_length=200, blank=True, null=True)
#     house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='market_material')
#
#
# class CopingMechanismList(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class CopingMechanism(models.Model):
#     coping_medium = models.ForeignKey('CopingMechanismList', on_delete=models.CASCADE,
#                                       related_name='coping_mechanism', null=True, blank=True)
#     is_coping_medium = models.NullBooleanField(default=False)
#     if_other_medium = models.CharField(max_length=200, blank=True, null=True)
#     house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='coping_mechanism')
#
#
# class DisasterPreparednessMechanismList(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class DisasterPreparednessMechanism(models.Model):
#     preparedness = models.ForeignKey('DisasterPreparednessMechanismList', on_delete=models.CASCADE,
#                                      related_name='disaster_prepare', null=True, blank=True)
#     involved_in_disaster_preparedness = models.NullBooleanField(default=False)
#     if_other_preparedness = models.CharField(max_length=200, blank=True, null=True)
#     house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='disaster_prepare')
#
#
# class InvolvedInSimulation(models.Model):
#     simulation = models.ForeignKey('DisasterList', on_delete=models.CASCADE,
#                                    related_name='simulation', null=True, blank=True)
#     involved_in_f_simulation = models.NullBooleanField(default=False)
#     if_other_simulation = models.CharField(max_length=200, blank=True, null=True)
#     house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='simulation')
#
#
# class GuideLineList(models.Model):
#     name = models.CharField(max_length=200)
#
#
# class GuideLine(models.Model):
#     GUIDELINE_CHOICES = (
#         (1, 'LDCRP guideline'),
#         (1, 'DPRP guideline'),
#     )
#     guideline = models.ForeignKey('GuideLineList', on_delete=models.CASCADE,
#                                   related_name='guideLine', null=True, blank=True)
#     know_about_guideline = models.BooleanField(default=False)
#     involved_in_development_process = models.BooleanField(default=False)
#     house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE,
#                                    related_name='guide_line', blank=True, null=True)
#
#
# class WardFallingProneArea(models.Model):
#     prone_area = models.ForeignKey('DisasterList', on_delete=models.CASCADE,
#                                    related_name='ward_prone', null=True, blank=True)
#     is_prone_area = models.BooleanField(default=False)
#     ward_identified_safe_place_during = models.BooleanField(default=False)
#     time_to_safe_place = models.CharField(blank=True, null=True, max_length=200)
#     disaster_prone = models.ForeignKey('DisasterProne', on_delete=models.CASCADE, related_name='ward_prone')
#
#
# class GenderList(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class WhoseOwnershipList(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class WhoseOwnershipData(models.Model):
#     ownership = models.ForeignKey('WhoseOwnershipList', on_delete=models.CASCADE, related_name='whose_ownership')
#     have_ownership = models.BooleanField(default=False)
#     house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='whose_ownership')
#
#
# class HouseTypeList(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class HouseType(models.Model):
#     ownership = models.ForeignKey('HouseTypeList', on_delete=models.CASCADE)
#     have_house = models.BooleanField(default=False)
#     if_other = models.CharField(max_length=300, blank=True, null=True)
#     house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='house_type')
#
#
# class OwnershipList(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class EthnicityList(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class ReligionList(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class MotherTongueList(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class EducationList(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class PermitList(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class RoadType(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class RoadCapacity(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class RoadCapacityType(models.Model):
#     road = models.ForeignKey('RoadCapacity', on_delete=models.CASCADE,
#                              related_name='household_road', blank=True, null=True)
#     have_road = models.BooleanField(default=False)
#     house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='household_road')
#
#
# class LatrineList(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
#
# class Latrine(models.Model):
#     latrine = models.ForeignKey('LatrineList', on_delete=models.CASCADE,
#                                 related_name='latrine', blank=True, null=True)
#     have_latrine = models.BooleanField(default=False)
#     if_other_latrine = models.CharField(max_length=200, blank=True, null=True)
#     house_hold = models.ForeignKey('HouseHold', on_delete=models.CASCADE, related_name='latrine')
#
#
# class HouseHold(models.Model):
#     index = models.IntegerField(blank=True, null=True)
#     start_date = models.DateTimeField(blank=True, null=True)
#     end_date = models.DateTimeField(blank=True, null=True)
#     surveyor_name = models.CharField(max_length=500)
#     name_of_place = models.CharField(max_length=500)
#     ward_no = models.IntegerField(blank=True, null=True)
#     location = PointField(geography=True, srid=4326, blank=True, null=True)
#     altitude = models.CharField(max_length=100, blank=True, null=True)
#     precision = models.CharField(max_length=100, blank=True, null=True)
#     household_no = models.IntegerField(blank=True, null=True)
#     house_holder_name = models.CharField(max_length=500, blank=True, null=True)
#     age_of_owner = models.IntegerField()
#     gender_of_house_owner = models.OneToOneField('GenderList', on_delete=models.CASCADE,
#                                                  related_name='gender', blank=True, null=True)
#     status_of_owner = models.OneToOneField('OwnershipList', on_delete=models.CASCADE,
#                                            related_name='status', blank=True, null=True)
#     if_other_owner_status = models.CharField(max_length=500, blank=True, null=True)
#     ethnicity = models.OneToOneField('OwnershipList', on_delete=models.CASCADE,
#                                      related_name='ethnicity', blank=True, null=True)
#     other_ethnicity = models.CharField(max_length=200, blank=True, null=True)
#     religion = models.OneToOneField('ReligionList', on_delete=models.CASCADE,
#                                     related_name='religion', blank=True, null=True)
#     religion_other = models.CharField(max_length=200, blank=True, null=True)
#     mother_tongue = models.OneToOneField('MotherTongueList', on_delete=models.CASCADE,
#                                          related_name='mother_tongue', blank=True, null=True)
#     other_mother_tongue = models.CharField(max_length=200, blank=True, null=True)
#     contact_num = models.CharField(max_length=50, blank=True, null=True)
#     education_level = models.OneToOneField('EducationList', on_delete=models.CASCADE,
#                                            related_name='education_level', blank=True, null=True)
#     owner_citizenship_number = models.CharField(max_length=100, blank=True, null=True)
#     responder_name = models.CharField(max_length=200, blank=True, null=True)
#     responder_gender = models.OneToOneField('GenderList', on_delete=models.CASCADE,
#                                             related_name='responder_gender', blank=True, null=True)
#     responder_age = models.CharField(max_length=5, blank=True, null=True)
#     responder_contact = models.CharField(max_length=20, blank=True, null=True)
#     other_family_member = models.BooleanField(default=False)
#     foods_eaten_in_last7_day = models.CharField(max_length=1000, blank=True, null=True)
#     monthly_expanses = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
#     monthly_income = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
#     if_loan_amount = models.DecimalField(max_digits=15, decimal_places=3, blank=True, null=True)
#     loan_time = models.CharField(blank=True, null=True, max_length=300)
#     have_livestock = models.BooleanField(default=False)
#     date_of_establishment = models.CharField(max_length=100, blank=True, null=True)
#     number_of_storey = models.CharField(max_length=10, blank=True, null=True)
#     number_of_rooms = models.CharField(max_length=10, blank=True, null=True)
#     received_building_permit = models.OneToOneField('PermitList', on_delete=models.CASCADE,
#                                                     related_name='received_building_permit', blank=True, null=True)
#     building_completion_certificate = models.OneToOneField('PermitList', on_delete=models.CASCADE,
#                                                            related_name='building_completion_certificate', blank=True, null=True)
#     is_house_earthquake_resilience = models.BooleanField(default=False)
#     is_house_landslide_resilience = models.BooleanField(default=False)
#     how_much_land_ownership = models.CharField(max_length=1000, blank=True, null=True)
#     does_land_lies_near_river_flood_plain = models.BooleanField(default=False)
#     land_near_river_flood_plain = models.CharField(max_length=1000, blank=True, null=True)
#     image_with_landscape = models.ImageField(upload_to='house_hold', blank=True, null=True)
#     time_for_nearest_road = models.CharField(max_length=200, blank=True, null=True)
#     road_type = models.OneToOneField('RoadType', on_delete=models.CASCADE,
#                                      related_name='road_type', blank=True, null=True)
#     road_width = models.CharField(max_length=100, blank=True, null=True)
#     time_to_nearest_school = models.CharField(max_length=200, blank=True, null=True)
#     time_to_nearest_health_institution = models.CharField(max_length=200, blank=True, null=True)
#     time_to_nearest_security_force = models.CharField(max_length=200, blank=True, null=True)
#     does_ward_have_identified_risk_area = models.BooleanField(default=False)
#     do_you_know_about_warning_system = models.BooleanField(default=False)
#     is_there_waning_system = models.BooleanField(default=False)
#     did_you_got_early_information_in_disaster = models.BooleanField(default=False)
#     if_yes_which_medium_was_used = models.CharField(max_length=200, blank=True, null=True)
#     does_ward_have_evacuation_shelter = models.BooleanField(default=False)
#     distance_to_evacuation_shelter = models.CharField(max_length=100, blank=True, null=True)
#     capacity_of_evacuation_shelter = models.BigIntegerField(blank=True, null=True)
#     distance_to_nearest_openspace = models.CharField(max_length=100, blank=True, null=True)
#     how_far_nearest_market = models.CharField(max_length=100, blank=True, null=True)
#     was_nearest_market_operating_in_disaster = models.BooleanField(default=True)
#     was_material_easily_available = models.CharField(max_length=100, blank=True, null=True)
#     if_not_material_how_you_managed = models.CharField(max_length=100, blank=True, null=True)
#     how_far_is_alternative_market = models.CharField(max_length=100, blank=True, null=True)
#     name_of_alternative_market = models.CharField(max_length=100, blank=True, null=True)
#     is_there_warehouse_in_your_ward = models.BooleanField(default=True)
#     how_often_replace_material_in_emergency_kit = models.CharField(max_length=100)
#     contingency_plan_involvement = models.BooleanField(default=False)
#     ward_has_safe_place = models.CharField(max_length=100, blank=True, null=True)
#     distance_to_safe_place = models.CharField(max_length=200, blank=True, null=True)
#
#
#
#     @property
#     def latitude(self):
#         return self.location.y
#
#     @property
#     def longitude(self):
#         return self.location.x
#
#     def __str__(self):
#         return self.house_holder_name + ',' + self.name_of_place
#
#
# class InvolvementList(models.Model):
#     name = models.CharField(max_length=100, blank=True, null=True)
#
#     def __str__(self):
#         return self.name
#
#
# class FamilyMemberCriterialist(models.Model):
#     name = models.CharField(max_length=500, blank=True, null=True)
#
#     def __str__(self):
#         return self.name
#
#
# class FamilyMemberCriteriaData(models.Model):
#     member_type = models.ForeignKey('FamilyMemberCriterialist', on_delete=models.CASCADE, related_name='family_member_criteria')
#     if_member_type = models.BooleanField(default=False)
#     owner_family = models.ForeignKey('OwnerFamily', on_delete=models.CASCADE, related_name='family_member_criteria')
#
#
# class AgeGroupList(models.Model):
#     name = models.CharField(max_length=100, blank=True, null=True)
#
#     def __str__(self):
#         return self.name
#
#
# class PopulationChoicesList(models.Model):
#     name = models.CharField(max_length=100, blank=True, null=True)
#
#     def __str__(self):
#         return self.name
#
#
# class PopulationChoiceData(models.Model):
#     population_choice = models.ForeignKey('PopulationChoicesList', on_delete=models.CASCADE,
#                                           related_name='population_choice')
#     if_member_type = models.BooleanField(default=False)
#     owner_family = models.ForeignKey('OwnerFamily', on_delete=models.CASCADE, related_name='population_choice')
#
#
# class ChronicIllnessList(models.Model):
#     name = models.CharField(max_length=100, blank=True, null=True)
#
#     def __str__(self):
#         return self.name
#
#
# class ChronicIllnessData(models.Model):
#     chronic_illness = models.ForeignKey('ChronicIllnessList', on_delete=models.CASCADE,
#                                         related_name='chronic_illness')
#     if_chronic_illness = models.BooleanField(default=False)
#     if_other_chronic_illness = models.CharField(max_length=200, blank=True, null=True)
#     owner_family = models.ForeignKey('OwnerFamily', on_delete=models.CASCADE, related_name='chronic_illness')
#
#
# class DisabilityList(models.Model):
#     name = models.CharField(max_length=100, blank=True, null=True)
#
#     def __str__(self):
#         return self.name
#
#
# class DisabilityData(models.Model):
#     population_choice = models.ForeignKey('DisabilityList', on_delete=models.CASCADE,
#                                           related_name='disability')
#     if_disability = models.BooleanField(default=False)
#     if_other_disability = models.CharField(max_length=200, blank=True, null=True)
#     owner_family = models.ForeignKey('OwnerFamily', on_delete=models.CASCADE, related_name='disability')
#
#
# class OwnerFamily(models.Model):
#     name = models.CharField(max_length=200)
#     age_group = models.OneToOneField('AgeGroupList', on_delete=models.CASCADE,
#                                      related_name='age_group', blank=True, null=True)
#     education_level = models.OneToOneField('EducationList', on_delete=models.CASCADE,
#                                            related_name='family_education_level', blank=True, null=True)
#     gender = models.OneToOneField('GenderList', on_delete=models.CASCADE,
#                                   related_name='family_gender', blank=True, null=True)
#     citizenship_num = models.CharField(max_length=30, blank=True, null=True)
#     occupation_of_family = models.OneToOneField('Occupation', on_delete=models.CASCADE,
#                                                 related_name='family_occupation', blank=True, null=True)
#     involvement_in_occupation = models.OneToOneField('InvolvementList', on_delete=models.CASCADE,
#                                                      related_name='involvement', blank=True, null=True)
#     if_other_occupation = models.CharField(max_length=300, blank=True, null=True)
#     monthly_income = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
#     household = models.ForeignKey('OwnerFamily', on_delete=models.CASCADE, related_name='owner_family')
#     received_social_security = models.BooleanField(default=False)
#     reason_not_received_social_security = models.CharField(blank=True, null=True, max_length=200)
#     other_population_choices = models.CharField(max_length=100, blank=True, null=True)
#
#     # does_family_member meet_any_of_the_criteria = models.IntegerField()
#
#     def __str__(self):
#         return self.name
#
#
# class AnimalDetails(models.Model):
#     type_of_livestock = models.CharField(max_length=100)
#     number_of_livestock = models.IntegerField()
#     commercial_purpose = models.BooleanField(default=False)
#     household = models.ForeignKey('OwnerFamily', on_delete=models.CASCADE, related_name='animal_detail')
#
#     def __str__(self):
#         return self.type_of_livestock


class HouseHoldData(models.Model):
    index = models.CharField(max_length=1000, blank=True, null=True)
    start_date = models.CharField(max_length=1000, blank=True, null=True)
    end_date = models.CharField(max_length=1000, blank=True, null=True)
    survayor_name = models.CharField(max_length=1000, blank=True, null=True)
    place_name = models.CharField(max_length=1000, blank=True, null=True)
    house_num = models.CharField(max_length=1000, blank=True, null=True)
    latitude = models.CharField(max_length=1000, blank=True, null=True)
    longitude = models.CharField(max_length=1000, blank=True, null=True)
    altitude = models.CharField(max_length=1000, blank=True, null=True)
    precision = models.CharField(max_length=1000, blank=True, null=True)
    household_number = models.CharField(max_length=1000, blank=True, null=True)
    owner_name = models.CharField(max_length=1000, blank=True, null=True)
    owner_age = models.CharField(max_length=100, blank=True, null=True)
    owner_sex_ne = models.CharField(max_length=100, blank=True, null=True)
    owner_sex_en = models.CharField(max_length=100, blank=True, null=True)
    status_owner_ne = models.CharField(max_length=100, blank=True, null=True)
    status_owner = models.CharField(max_length=100, blank=True, null=True)
    caste_owner_ne = models.CharField(max_length=100, blank=True, null=True)
    caste_owner_en = models.CharField(max_length=100, blank=True, null=True)
    religion_ne = models.CharField(max_length=100, blank=True, null=True)
    religion_en = models.CharField(max_length=100, blank=True, null=True)
    mother_tounge_ne = models.CharField(max_length=100, blank=True, null=True)
    mother_tounge_en = models.CharField(max_length=100, blank=True, null=True)
    mother_tounge_other = models.CharField(max_length=100, blank=True, null=True)
    owner_contact = models.CharField(max_length=100, blank=True, null=True)
    education_owner_ne = models.CharField(max_length=100, blank=True, null=True)
    education_owner_en = models.CharField(max_length=100, blank=True, null=True)
    citizenship_num = models.CharField(max_length=100, blank=True, null=True)
    responder_name = models.CharField(max_length=100, blank=True, null=True)
    responder_sex_ne = models.CharField(max_length=100, blank=True, null=True)
    responder_sex_en = models.CharField(max_length=100, blank=True, null=True)
    responder_age = models.CharField(max_length=100, blank=True, null=True)
    responder_contact = models.CharField(max_length=100, blank=True, null=True)
    other_family_member_ne = models.CharField(max_length=100, blank=True, null=True)
    other_family_member_en = models.CharField(max_length=100, blank=True, null=True)
    main_occupation_ne = models.CharField(max_length=100, blank=True, null=True)
    main_occupation_en = models.CharField(max_length=100, blank=True, null=True)
    main_occupation_agriculture =  models.BooleanField(default=False)
    main_occupation_agriculture_wages =  models.BooleanField(default=False)
    main_occupation_daily_wages =  models.BooleanField(default=False)
    main_occupation_government_job =  models.BooleanField(default=False)
    main_occupation_non_government_job =  models.BooleanField(default=False)
    main_occupation_foreign_employment =  models.BooleanField(default=False)
    main_occupation_self =  models.BooleanField(default=False)
    main_occupation_business =  models.BooleanField(default=False)
    main_occupation_labour_nepal =  models.BooleanField(default=False)
    main_occupation_labour_india =  models.BooleanField(default=False)
    main_occupation_other =  models.BooleanField(default=False)
    if_other_occupation = models.CharField(max_length=100, blank=True, null=True)
    if_business = models.BooleanField(default=False)
    if_business_grocery_store = models.BooleanField(default=False)
    if_business_pharmacy = models.BooleanField(default=False)
    if_business_stationary = models.BooleanField(default=False)
    if_business_hardware = models.BooleanField(default=False)
    if_business_hotel = models.BooleanField(default=False)
    if_business_poultry = models.BooleanField(default=False)
    if_business_livestock = models.BooleanField(default=False)
    if_business_cattle = models.BooleanField(default=False)
    if_business_other_agriculture_business = models.BooleanField(default=False)
    if_business_other_small_business = models.BooleanField(default=False)
    if_business_other = models.BooleanField(default=False)
    if_other_business_mention = models.CharField(max_length=100, blank=True, null=True)
    if_other_small_business_mention = models.CharField(max_length=100, blank=True, null=True)
    crop_sufficiency_ne = models.CharField(max_length=100, blank=True, null=True)
    crop_sufficiency_en = models.CharField(max_length=100, blank=True, null=True)
    food_type_en = models.CharField(max_length=100, blank=True, null=True)
    food_type_ne = models.CharField(max_length=100, blank=True, null=True)
    num_of_days_food_eaten_staples =models.IntegerField(blank=True, null=True)
    num_of_days_food_eaten_pulses =models.IntegerField(blank=True, null=True)
    num_of_days_food_eaten_vegetables =models.IntegerField(blank=True, null=True)
    num_of_days_food_eaten_fruits =models.IntegerField(blank=True, null=True)
    num_of_days_food_eaten_mean_and_fish =models.IntegerField(blank=True, null=True)
    num_of_days_food_eaten_milk_products =models.IntegerField(blank=True, null=True)
    num_of_days_food_eaten_sugar_products =models.IntegerField(blank=True, null=True)
    num_of_days_food_eaten_oil_products =models.IntegerField(blank=True, null=True)
    num_of_days_food_eaten_condiments =models.IntegerField(blank=True, null=True)
    monthly_expanses = models.CharField(max_length=100, blank=True, null=True)
    monthly_income = models.CharField(max_length=100, blank=True, null=True)
    loan_from_financial_institution_ne = models.CharField(max_length=100, blank=True, null=True)
    loan_from_financial_institution_en = models.CharField(max_length=100, blank=True, null=True)
    loan_amount = models.CharField(max_length=100, blank=True, null=True)
    duration_of_loan = models.CharField(max_length=100, blank=True, null=True)
    animal_detail_presence_ne = models.CharField(max_length=100, blank=True, null=True)
    animal_detail_presence_en = models.CharField(max_length=100, blank=True, null=True)
    insurance_ne = models.CharField(max_length=100, blank=True, null=True)
    insurance_en = models.CharField(max_length=100, blank=True, null=True)
    insurance_life_insurance = models.BooleanField(default=False)
    insurance_livestock_insurance = models.BooleanField(default=False)
    insurance_crops_insurance = models.BooleanField(default=False)
    insurance_house_or_assest_insurance = models.BooleanField(default=False)
    insurance_other_insurance = models.BooleanField(default=False)
    vehicle_ne = models.CharField(max_length=100, blank=True, null=True)
    vehicle_en = models.CharField(max_length=100, blank=True, null=True)
    vehicle_motorcycle = models.BooleanField(default=False)
    vehicle_car_jeep_van_personal = models.BooleanField(default=False)
    vehicle_car_jeep_van_commercial = models.BooleanField(default=False)
    vehicle_minibus_minitruck = models.BooleanField(default=False)
    vehicle_minibus_cycle = models.BooleanField(default=False)
    vehicle_bus_tipper_big_vehicle = models.BooleanField(default=False)
    vehicle_bus_tipper_big_vehicle = models.BooleanField(default=False)
    vehicle_tractor_power_trailer = models.BooleanField(default=False)
    vehicle_other_heavy_equipment = models.BooleanField(default=False)
    vehicle_no_any_vehicle = models.BooleanField(default=False)
    vehicle_if_other_mention = models.CharField(max_length=100, blank=True, null=True)
    facility_ne = models.CharField(max_length=100, blank=True, null=True)
    facility_en = models.CharField(max_length=100, blank=True, null=True)
    facility_radio = models.BooleanField(default=False)
    facility_tv = models.BooleanField(default=False)
    facility_fridge = models.BooleanField(default=False)
    facility_oven = models.BooleanField(default=False)
    facility_telephone_mobile = models.BooleanField(default=False)
    facility_washing_machine = models.BooleanField(default=False)
    facility_internet = models.BooleanField(default=False)
    facility_other = models.BooleanField(default=False)
    facility_if_other_mention = models.CharField(max_length=100, blank=True, null=True)
    fuel_ne = models.CharField(max_length=100, blank=True, null=True)
    fuel_en = models.CharField(max_length=100, blank=True, null=True)
    fuel_type_kerosene = models.BooleanField(default=False)
    fuel_type_lpg = models.BooleanField(default=False)
    fuel_type_guitha = models.BooleanField(default=False)
    fuel_type_bio_gas = models.BooleanField(default=False)
    fuel_type_electrical = models.BooleanField(default=False)
    fuel_type_firewood_coal = models.BooleanField(default=False)
    fuel_type_other = models.BooleanField(default=False)
    fuel_if_other_mention = models.CharField(max_length=100, blank=True, null=True)
    ownership_detail_ne = models.CharField(max_length=100, blank=True, null=True)
    ownership_detail_en = models.CharField(max_length=100, blank=True, null=True)
    ownership_detail_male = models.BooleanField(default=False)
    ownership_detail_female = models.BooleanField(default=False)
    ownership_detail_other = models.BooleanField(default=False)
    house_type_ne = models.CharField(max_length=100, blank=True, null=True)
    house_type_en = models.CharField(max_length=100, blank=True, null=True)
    house_type_rcc_framework = models.BooleanField(default=False)
    house_type_cgi_celling = models.BooleanField(default=False)
    house_type_pallet_ash_soil = models.BooleanField(default=False)
    house_type_semi_permanent_house = models.BooleanField(default=False)
    house_type_temporary_cgi_roof = models.BooleanField(default=False)
    house_type_temporary_thatched_mud_roof = models.BooleanField(default=False)
    house_type_other = models.BooleanField(default=False)
    house_if_other_mention = models.CharField(max_length=100, blank=True, null=True)
    established_year = models.CharField(max_length=100, blank=True, null=True)
    house_storey = models.CharField(max_length=10, blank=True, null=True)
    house_room = models.CharField(max_length=10, blank=True, null=True)
    house_map_ne = models.CharField(max_length=100, blank=True, null=True)
    house_map_en = models.CharField(max_length=100, blank=True, null=True)
    building_standard_code_ne = models.CharField(max_length=100, blank=True, null=True)
    building_standard_code_en = models.CharField(max_length=100, blank=True, null=True)
    earthquake_resistance_ne = models.CharField(max_length=100, blank=True, null=True)
    earthquake_resistance_en = models.CharField(max_length=100, blank=True, null=True)
    flood_prone_ne = models.CharField(max_length=100, blank=True, null=True)
    flood_prone_en = models.CharField(max_length=100, blank=True, null=True)
    flood_prone_activities_ne = models.CharField(max_length=100, blank=True, null=True)
    flood_prone_activities_en = models.CharField(max_length=100, blank=True, null=True)
    flood_activities_raised_plinth = models.BooleanField(default=False)
    flood_activities_strong_wall = models.BooleanField(default=False)
    flood_activities_proper_drainage = models.BooleanField(default=False)
    flood_activities_other = models.BooleanField(default=False)
    flood_activities_if_other_mention = models.CharField(max_length=100, blank=True, null=True)
    land_ownership_ne = models.CharField(max_length=100, blank=True, null=True)
    land_ownership_en = models.CharField(max_length=100, blank=True, null=True)
    does_land_near_river_ne = models.CharField(max_length=100, blank=True, null=True)
    does_land_near_river_en = models.CharField(max_length=100, blank=True, null=True)
    if_land_near_image = models.ImageField(upload_to='house_hold', blank=True, null=True)
    if_image_ne = models.CharField(max_length=100, blank=True, null=True)
    if_image_en = models.CharField(max_length=100, blank=True, null=True)
    manpower_type_ne = models.CharField(max_length=100, blank=True, null=True)
    manpower_type_en = models.CharField(max_length=100, blank=True, null=True)
    manpower_doctor = models.BooleanField(default=False)
    manpower_engineer = models.BooleanField(default=False)
    manpower_sub_engineer = models.BooleanField(default=False)
    manpower_nurse = models.BooleanField(default=False)
    manpower_ha_lab_assitant_pharmacist = models.BooleanField(default=False)
    manpower_veterinary = models.BooleanField(default=False)
    manpower_carpenter = models.BooleanField(default=False)
    manpower_plumber = models.BooleanField(default=False)
    manpower_electrician = models.BooleanField(default=False)
    manpower_jt_or_jta = models.BooleanField(default=False)
    manpower_other = models.BooleanField(default=False)
    doctor_sex_ne = models.CharField(max_length=100, blank=True, null=True)
    doctor_sex_en = models.CharField(max_length=100, blank=True, null=True)
    doctor_sex_male = models.BooleanField(default=False)
    doctor_sex_female = models.BooleanField(default=False)
    doctor_sex_male_number = models.CharField(max_length=100, blank=True, null=True)
    doctor_sex_female_number = models.CharField(max_length=100, blank=True, null=True)
    engineer_sex_ne = models.CharField(max_length=100, blank=True, null=True)
    engineer_sex_en = models.CharField(max_length=100, blank=True, null=True)
    engineer_sex_male = models.BooleanField(default=False)
    engineer_sex_female = models.BooleanField(default=False)
    engineer_sex_male_number = models.CharField(max_length=100, blank=True, null=True)
    engineer_sex_female_number = models.CharField(max_length=100, blank=True, null=True)
    nurse_sex_ne = models.CharField(max_length=100, blank=True, null=True)
    nurse_sex_en = models.CharField(max_length=100, blank=True, null=True)
    nurse_sex_male = models.BooleanField(default=False)
    nurse_sex_female = models.BooleanField(default=False)
    nurse_sex_male_number = models.CharField(max_length=100, blank=True, null=True)
    nurse_sex_female_number = models.CharField(max_length=100, blank=True, null=True)
    ha_lab_sex_ne = models.CharField(max_length=100, blank=True, null=True)
    ha_lab_sex_en = models.CharField(max_length=100, blank=True, null=True)
    ha_lab_sex_male = models.BooleanField(default=False)
    ha_lab_sex_female = models.BooleanField(default=False)
    ha_lab_sex_male_number = models.CharField(max_length=100, blank=True, null=True)
    ha_lab_sex_female_number = models.CharField(max_length=100, blank=True, null=True)
    veterinary_sex_ne = models.CharField(max_length=100, blank=True, null=True)
    veterinary_sex_en = models.CharField(max_length=100, blank=True, null=True)
    veterinary_sex_male = models.BooleanField(default=False)
    veterinary_sex_female = models.BooleanField(default=False)
    veterinary_sex_male_number = models.CharField(max_length=100, blank=True, null=True)
    veterinary_sex_female_number = models.CharField(max_length=100, blank=True, null=True)
    carpenter_sex_ne = models.CharField(max_length=100, blank=True, null=True)
    carpenter_sex_en = models.CharField(max_length=100, blank=True, null=True)
    carpenter_sex_male = models.BooleanField(default=False)
    carpenter_sex_female = models.BooleanField(default=False)
    carpenter_sex_male_number = models.CharField(max_length=100, blank=True, null=True)
    carpenter_sex_female_number = models.CharField(max_length=100, blank=True, null=True)
    plumber_sex_ne = models.CharField(max_length=100, blank=True, null=True)
    plumber_sex_en = models.CharField(max_length=100, blank=True, null=True)
    plumber_sex_male = models.BooleanField(default=False)
    plumber_sex_female = models.BooleanField(default=False)
    plumber_sex_male_number = models.CharField(max_length=100, blank=True, null=True)
    plumber_sex_female_number = models.CharField(max_length=100, blank=True, null=True)
    electrician_sex_en = models.CharField(max_length=100, blank=True, null=True)
    electrician_sex_ne = models.CharField(max_length=100, blank=True, null=True)
    electrician_sex_male = models.BooleanField(default=False)
    electrician_sex_female = models.BooleanField(default=False)
    electrician_sex_male_number = models.CharField(max_length=100, blank=True, null=True)
    electrician_sex_female_number = models.CharField(max_length=100, blank=True, null=True)
    jt_or_jta_sex_en = models.CharField(max_length=100, blank=True, null=True)
    jt_or_jta_sex_ne = models.CharField(max_length=100, blank=True, null=True)
    jt_or_jta_sex_male = models.BooleanField(default=False)
    jt_or_jta_sex_female = models.BooleanField(default=False)
    jt_or_jta_sex_male_number = models.CharField(max_length=100, blank=True, null=True)
    jt_or_jta_sex_female_number = models.CharField(max_length=100, blank=True, null=True)
    other_sex_en = models.CharField(max_length=100, blank=True, null=True)
    other_sex_ne = models.CharField(max_length=100, blank=True, null=True)
    other_sex_male = models.BooleanField(default=False)
    other_sex_female = models.BooleanField(default=False)
    other_sex_male_number = models.CharField(max_length=100, blank=True, null=True)
    other_sex_female_number = models.CharField(max_length=100, blank=True, null=True)
    main_road_distance_ne = models.CharField(max_length=500, blank=True, null= True)
    main_road_distance_en = models.CharField(max_length=500, blank=True, null= True)
    road_type_ne = models.CharField(max_length=500, blank=True, null= True)
    road_type_en = models.CharField(max_length=500, blank=True, null= True)
    road_width = models.CharField(max_length=500, blank=True, null= True)
    road_capacity_ne = models.CharField(max_length=500, blank=True, null= True)
    road_capacity_en = models.CharField(max_length=500, blank=True, null= True)
    road_type_crane_dozer = models.BooleanField(default=False)
    road_type_minibus_minitruck = models.BooleanField(default=False)
    road_type_tractor_power_tailor = models.BooleanField(default=False)
    road_type_tractor_fire_brigade = models.BooleanField(default=False)
    road_type_tractor_bus_pickup_car = models.BooleanField(default=False)
    road_type_tractor_motorcycle = models.BooleanField(default=False)
    nearest_school_distance_ne = models.CharField(max_length=500, blank=True, null= True)
    nearest_school_distance_en = models.CharField(max_length=500, blank=True, null= True)
    nearest_health_distance_ne = models.CharField(max_length=500, blank=True, null= True)
    nearest_health_distance_en = models.CharField(max_length=500, blank=True, null= True)
    nearest_security_distance_ne = models.CharField(max_length=500, blank=True, null= True)
    nearest_security_distance_en = models.CharField(max_length=500, blank=True, null= True)
    water_sources_ne = models.CharField(max_length=500, blank=True, null= True)
    water_sources_en = models.CharField(max_length=500, blank=True, null= True)
    water_sources_public_tap_stand = models.BooleanField(default=False)
    water_sources_private_tap_stand = models.BooleanField(default=False)
    water_sources_spring = models.BooleanField(default=False)
    water_sources_river = models.BooleanField(default=False)
    water_sources_tube_well = models.BooleanField(default=False)
    water_sources_other = models.BooleanField(default=False)
    if_tube_well_private_or_public_ne = models.CharField(max_length=100, blank=True, null=True)
    if_tube_well_private_or_public_en = models.CharField(max_length=100, blank=True, null=True)
    if_tube_well_status_of_well_ne = models.CharField(max_length=100, blank=True, null=True)
    if_tube_well_status_of_well_en = models.CharField(max_length=100, blank=True, null=True)
    num_of_house_using_tube_well = models.CharField(max_length=100, blank=True, null=True)
    has_flood_effect_tube_well = models.CharField(max_length=100, blank=True, null=True)
    public_tap_distance_ne = models.CharField(max_length=100, blank=True, null=True)
    public_tap_distance_en = models.CharField(max_length=100, blank=True, null=True)
    have_toilet_ne = models.CharField(max_length=100, blank=True, null=True)
    have_toilet_en = models.CharField(max_length=100, blank=True, null=True)
    toilet_type_ne = models.CharField(max_length=100, blank=True, null=True)
    toilet_type_en = models.CharField(max_length=100, blank=True, null=True)
    toilet_type_Drainage = models.BooleanField(default=False)
    toilet_type_pit_hole = models.BooleanField(default=False)
    toilet_type_bio_gas_attached = models.BooleanField(default=False)
    toilet_type_septic_tank = models.BooleanField(default=False)
    toilet_type_ring_type = models.BooleanField(default=False)
    toilet_type_other = models.BooleanField(default=False)
    toilet_type_other_mention = models.CharField(max_length=100, blank=True, null=True)
    waterborne_disease_ne = models.CharField(max_length=100, blank=True, null=True)
    waterborne_disease_en = models.CharField(max_length=100, blank=True, null=True)
    disaster_detail_en = models.CharField(max_length=100, blank=True, null=True)
    disaster_detail_ne = models.CharField(max_length=100, blank=True, null=True)
    disaster_type_flood = models.BooleanField(default=False)
    disaster_type_landslide = models.BooleanField(default=False)
    disaster_type_fire = models.BooleanField(default=False)
    disaster_type_black_spot = models.BooleanField(default=False)
    disaster_type_snake_bite = models.BooleanField(default=False)
    disaster_type_animal_attack = models.BooleanField(default=False)
    disaster_type_lightening = models.BooleanField(default=False)
    disaster_type_road_accident = models.BooleanField(default=False)
    disaster_type_cold_wind = models.BooleanField(default=False)
    disaster_type_other = models.BooleanField(default=False)
    disaster_type_other_mention = models.CharField(max_length=100, blank=True, null=True)
    hazard_detail_en = models.CharField(max_length=100, blank=True, null=True)
    hazard_detail_ne = models.CharField(max_length=100, blank=True, null=True)
    hazard_type_flood = models.BooleanField(default=False)
    hazard_type_landslide = models.BooleanField(default=False)
    hazard_type_fire = models.BooleanField(default=False)
    hazard_type_black_spot = models.BooleanField(default=False)
    hazard_type_snake_bite = models.BooleanField(default=False)
    hazard_type_animal_attack = models.BooleanField(default=False)
    hazard_type_lightening = models.BooleanField(default=False)
    hazard_type_road_accident = models.BooleanField(default=False)
    hazard_type_cold_wind = models.BooleanField(default=False)
    hazard_type_other = models.BooleanField(default=False)
    hazard_type_other_mention = models.CharField(max_length=100, blank=True, null=True)
    risk_area_ne = models.CharField(max_length=100, blank=True, null=True)
    risk_area_en = models.CharField(max_length=100, blank=True, null=True)
    information_medium_ne = models.CharField(max_length=100, blank=True, null=True)
    information_medium_en = models.CharField(max_length=100, blank=True, null=True)
    information_medium_radio_or_tv = models.BooleanField(default=False)
    information_medium_local_resident = models.BooleanField(default=False)
    information_medium_local_newspaper = models.BooleanField(default=False)
    information_medium_related_people = models.BooleanField(default=False)
    information_medium_other = models.BooleanField(default=False)
    information_medium_other_mention = models.CharField(max_length=100, blank=True, null=True)
    know_about_early_warning_system_ne = models.CharField(max_length=100, blank=True, null=True)
    know_about_early_warning_system_en = models.CharField(max_length=100, blank=True, null=True)
    is_there_early_warning_in_ward_ne = models.CharField(max_length=100, blank=True, null=True)
    is_there_early_warning_in_war_en = models.CharField(max_length=100, blank=True, null=True)
    got_early_information_in_disaster_en = models.CharField(max_length=100, blank=True, null=True)
    got_early_information_in_disaster_ne = models.CharField(max_length=100, blank=True, null=True)
    which_medium_suitable_for_ews_en = models.CharField(max_length=100, blank=True, null=True)
    which_medium_suitable_for_ews_ne = models.CharField(max_length=100, blank=True, null=True)
    which_medium_suitable_for_ews_radio = models.BooleanField(default=False)
    which_medium_suitable_for_ews_tv = models.BooleanField(default=False)
    which_medium_suitable_for_ews_miking = models.BooleanField(default=False)
    which_medium_suitable_for_ews_siren = models.BooleanField(default=False)
    which_medium_suitable_for_ews_sms = models.BooleanField(default=False)
    which_medium_suitable_for_ews_other = models.BooleanField(default=False)
    medium_suitable_for_ews = models.CharField(max_length=100, blank=True, null=True)
    does_ward_has_evacuation_center = models.CharField(max_length=100, blank=True, null=True)
    distance_to_evacuation_center = models.CharField(max_length=100, blank=True, null=True)
    capacity_of_evacuation_center = models.CharField(max_length=100, blank=True, null=True)
    distance_to_nearest_open_space = models.CharField(max_length=100, blank=True, null=True)
    market_distance = models.CharField(max_length=100, blank=True, null=True)
    available_in_market_en = models.CharField(max_length=500, blank=True, null=True)
    available_in_market_np = models.CharField(max_length=500, blank=True, null=True)
    market_available_cereals = models.BooleanField(default=False)
    market_available_pulses = models.BooleanField(default=False)
    market_available_vegetables = models.BooleanField(default=False)
    market_available_fruits = models.BooleanField(default=False)
    market_available_edible_oil = models.BooleanField(default=False)
    market_available_milk_products = models.BooleanField(default=False)
    market_available_egg_and_meat = models.BooleanField(default=False)
    market_available_agriculture_tools= models.BooleanField(default=False)
    market_available_other_non_edible_items = models.BooleanField(default=False)
    market_available_construction_material = models.BooleanField(default=False)
    market_available_clothing = models.BooleanField(default=False)
    market_available_other = models.BooleanField(default=False)
    market_available_other_mention = models.CharField(max_length=100, blank=True, null=True)
    distance_alternative_market = models.CharField(max_length=100, blank=True, null=True)
    name_alternative_market = models.CharField(max_length=100, blank=True, null=True)
    market_operating_en = models.CharField(max_length=100, blank=True, null=True)
    market_operating_ne = models.CharField(max_length=100, blank=True, null=True)
    easily_materials_available = models.CharField(max_length=100, blank=True, null=True)
    if_no_material_management = models.CharField(max_length=100, blank=True, null=True)
    warehouse_in_ward = models.CharField(max_length=100, blank=True, null=True)
    coping_mechanism = models.CharField(max_length=100, blank=True, null=True)
    coping_mechanism_residing_elsewhere = models.BooleanField(default=False)
    coping_mechanism_relatives_or_neighbour = models.BooleanField(default=False)
    coping_mechanism_took_a_loan = models.BooleanField(default=False)
    coping_mechanism_sold_jwelary_assests = models.BooleanField(default=False)
    coping_mechanism_other_assest = models.BooleanField(default=False)
    coping_mechanism_reduced_food_quantity = models.BooleanField(default=False)
    coping_mechanism_sold_food_stocks = models.BooleanField(default=False)
    coping_mechanism_cattle_livestock = models.BooleanField(default=False)
    coping_mechanism_labour_enrollment_india = models.BooleanField(default=False)
    coping_mechanism_other = models.BooleanField(default=False)
    coping_mechanism_other_mention = models.CharField(max_length=100, blank=True, null=True)
    house_has_emergency_kit = models.CharField(max_length=100, blank=True, null=True)
    disaster_risk_management_involvement_en = models.CharField(max_length=100, blank=True, null=True)
    disaster_risk_management_involvement_np = models.CharField(max_length=100, blank=True, null=True)
    disaster_risk_management_disaster_management = models.BooleanField(default=False)
    disaster_risk_management_first_aid = models.BooleanField(default=False)
    disaster_risk_management_search_and_rescue = models.BooleanField(default=False)
    disaster_risk_management_psycho_social_support = models.BooleanField(default=False)
    disaster_risk_management_wash = models.BooleanField(default=False)
    disaster_risk_management_vca = models.BooleanField(default=False)
    disaster_risk_management_none = models.BooleanField(default=False)
    disaster_risk_management_other = models.BooleanField(default=False)
    disaster_risk_management_other_mention =  models.CharField(max_length=100, blank=True, null=True)
    involvement_in_simulation_en = models.CharField(max_length=100, blank=True, null=True)
    involvement_in_simulation_ne = models.CharField(max_length=100, blank=True, null=True)
    simulation_involvement_earthquake = models.BooleanField(default=False)
    simulation_involvement_flood = models.BooleanField(default=False)
    simulation_involvement_fire = models.BooleanField(default=False)
    simulation_involvement_landslide = models.BooleanField(default=False)
    simulation_involvement_other = models.BooleanField(default=False)
    simulation_involvement_other_mention = models.CharField(max_length=100, blank=True, null=True)
    know_about_ldcrp_guideline = models.CharField(max_length=100, blank=True, null=True)
    involved_in_ldcrp_guideline = models.CharField(max_length=100, blank=True, null=True)
    know_about_drpc_guideline = models.CharField(max_length=100, blank=True, null=True)
    involved_in_dprc_guideline = models.CharField(max_length=100, blank=True, null=True)
    contingency_plan = models.CharField(max_length=100, blank=True, null=True)
    ward_falling_prone_area = models.CharField(max_length=100, blank=True, null=True)
    ward_falling_prone_area_flood = models.BooleanField(default=False)
    ward_falling_prone_area_earthquake = models.BooleanField(default=False)
    ward_falling_prone_area_landslide = models.BooleanField(default=False)
    ward_falling_prone_area_fire = models.BooleanField(default=False)
    ward_falling_prone_area_none = models.BooleanField(default=False)
    identified_safe_place_in_flood = models.CharField(max_length=100, blank=True, null=True)
    distance_to_safe_place = models.CharField(max_length=100, blank=True, null=True)
    damages_occurred_during_flood = models.CharField(max_length=500, blank=True, null=True)
    damages_occurred_during_flood_death_or_injured_family_member = models.BooleanField(default=False)
    damages_occurred_during_flood_house = models.BooleanField(default=False)
    damages_occurred_during_flood_land = models.BooleanField(default=False)
    damages_occurred_during_flood_furniture = models.BooleanField(default=False)
    damages_occurred_during_flood_livestock = models.BooleanField(default=False)
    damages_occurred_during_flood_crops = models.BooleanField(default=False)
    damages_occurred_during_flood_machinary = models.BooleanField(default=False)
    damages_occurred_during_flood_personal_documents = models.BooleanField(default=False)
    damages_occurred_during_flood_none = models.BooleanField(default=False)
    damages_occurred_during_flood_other = models.BooleanField(default=False)
    damages_occurred_during_flood_other_mention = models.CharField(max_length=500, blank=True, null=True)
    house_damage_type = models.CharField(max_length=500, blank=True, null=True)
    house_damage_type_damage_in_foundation = models.BooleanField(default=False)
    house_damage_type_damage_in_roof = models.BooleanField(default=False)
    house_damage_type_damage_in_walls = models.BooleanField(default=False)
    house_damage_type_was_flooded = models.BooleanField(default=False)
    house_damage_type_was_none = models.BooleanField(default=False)
    house_damage_type_other = models.BooleanField(default=False)
    house_damage_type_other_mention = models.CharField(max_length=500, blank=True, null=True)
    migrated_in_the_time_of_flood = models.CharField(max_length=500, blank=True, null=True)
    damages_occurred_during_landslide = models.CharField(max_length=500, blank=True, null=True)
    damages_landslide_death_or_injured_family_member = models.BooleanField(default=False)
    damages_occurred_during_landslide_house = models.BooleanField(default=False)
    damages_occurred_during_landslide_land = models.BooleanField(default=False)
    damages_occurred_during_landslide_livestock = models.BooleanField(default=False)
    damages_occurred_during_landslide_crops = models.BooleanField(default=False)
    damages_occurred_during_landslide_none = models.BooleanField(default=False)
    damages_occurred_during_landslide_other = models.BooleanField(default=False)
    damages_occurred_during_landslide_other_mention = models.CharField(max_length=500, blank=True, null=True)
    house_damage_type_landslide = models.CharField(max_length=500, blank=True, null=True)
    house_damage_type_landslide_completely = models.BooleanField(default=False)
    house_damage_type_landslide_damage_in_foundation = models.BooleanField(default=False)
    house_damage_type_landslide_damage_in_roof = models.BooleanField(default=False)
    house_damage_type_landslide_damage_in_walls = models.BooleanField(default=False)
    house_damage_type_landslide_was_none = models.BooleanField(default=False)
    house_damage_type_landslide_other = models.BooleanField(default=False)
    house_damage_type_landslide_other_mention = models.CharField(max_length=500, blank=True, null=True)
    migrated_in_the_time_of_landslide = models.CharField(max_length=500, blank=True, null=True)
    damages_occurred_during_earthquake = models.CharField(max_length=500, blank=True, null=True)
    damages_earthquake_death_or_injured_family_member = models.BooleanField(default=False)
    damages_occurred_during_earthquake_house = models.BooleanField(default=False)
    damages_occurred_during_earthquake_land = models.BooleanField(default=False)
    damages_occurred_during_earthquake_livestock = models.BooleanField(default=False)
    damages_occurred_during_earthquake_crops = models.BooleanField(default=False)
    damages_occurred_during_earthquake_none = models.BooleanField(default=False)
    damages_occurred_during_earthquake_other = models.BooleanField(default=False)
    damages_occurred_during_earthquake_other_mention = models.CharField(max_length=500, blank=True, null=True)
    house_damage_type_earthquake = models.CharField(max_length=500, blank=True, null=True)
    house_damage_type_earthquake_completely = models.BooleanField(default=False)
    house_damage_type_earthquake_damage_in_foundation = models.BooleanField(default=False)
    house_damage_type_earthquake_damage_in_roof = models.BooleanField(default=False)
    house_damage_type_earthquake_damage_in_walls = models.BooleanField(default=False)
    house_damage_type_earthquake_was_none = models.BooleanField(default=False)
    house_damage_type_earthquake_other = models.BooleanField(default=False)
    house_damage_type_earthquake_other_mention = models.CharField(max_length=500, blank=True, null=True)
    migrated_in_the_time_of_earthquake = models.CharField(max_length=500, blank=True, null=True)
    place_you_migrated_earthquake = models.CharField(max_length=500, blank=True, null=True)
    place_you_migrated_earthquake_school = models.BooleanField(default=False)
    place_you_migrated_earthquake_evacuation_shelter = models.BooleanField(default=False)
    place_you_migrated_earthquake_relative_or_neighbour = models.BooleanField(default=False)
    place_you_migrated_earthquake_open_space = models.BooleanField(default=False)
    place_you_migrated_earthquake_other = models.BooleanField(default=False)
    place_you_migrated_earthquake_other_mention = models.CharField(max_length=500, blank=True, null=True)
    damages_occurred_during_fire = models.CharField(max_length=500, blank=True, null=True)
    damages_fire_death_or_injured_family_member = models.BooleanField(default=False)
    damages_occurred_during_fire_house = models.BooleanField(default=False)
    damages_occurred_during_fire_land = models.BooleanField(default=False)
    damages_occurred_during_fire_livestock = models.BooleanField(default=False)
    damages_occurred_during_fire_crops = models.BooleanField(default=False)
    damages_occurred_during_fire_none = models.BooleanField(default=False)
    damages_occurred_during_fire_other = models.BooleanField(default=False)
    damages_occurred_during_fire_other_mention = models.CharField(max_length=500, blank=True, null=True)
    house_damage_type_fire = models.CharField(max_length=500, blank=True, null=True)
    house_damage_type_fire_completely = models.BooleanField(default=False)
    house_damage_type_fire_damage_in_foundation = models.BooleanField(default=False)
    house_damage_type_fire_damage_in_roof = models.BooleanField(default=False)
    house_damage_type_fire_damage_in_walls = models.BooleanField(default=False)
    house_damage_type_fire_was_none = models.BooleanField(default=False)
    house_damage_type_fire_other = models.BooleanField(default=False)
    house_damage_type_fire_other_mention = models.CharField(max_length=500, blank=True, null=True)
    migrated_in_the_time_of_fire = models.CharField(max_length=500, blank=True, null=True)
    place_you_migrated_fire = models.CharField(max_length=500, blank=True, null=True)
    place_you_migrated_fire_school = models.BooleanField(default=False)
    place_you_migrated_fire_evacuation_shelter = models.BooleanField(default=False)
    place_you_migrated_fire_relative_or_neighbour = models.BooleanField(default=False)
    place_you_migrated_fire_open_space = models.BooleanField(default=False)
    place_you_migrated_fire_other = models.BooleanField(default=False)
    place_you_migrated_fire_other_mention = models.CharField(max_length=500, blank=True, null=True)



class OwnerFamilyData(models.Model):
    name = models.CharField(max_length=500, blank=True, null=True)
    age_group = models.CharField(max_length=500, blank=True, null=True)
    gender = models.CharField(max_length=500, blank=True, null=True)
    citizenship_number = models.CharField(max_length=500, blank=True, null=True)
    education_level = models.CharField(max_length=500, blank=True, null=True)
    main_occupation_of_family = models.CharField(max_length=500, blank=True, null=True)
    if_other_occupation = models.CharField(max_length=500, blank=True, null=True)
    involvement_in_occupation = models.CharField(max_length=500, blank=True, null=True)
    monthly_income = models.CharField(max_length=500, blank=True, null=True)
    family_member_meet_criteria = models.CharField(max_length=500, blank=True, null=True)
    family_member_meet_criteria_senior_citizen_of_70 = models.BooleanField(default=False)
    family_member_meet_criteria_senior_citizen_of_60 = models.BooleanField(default=False)
    family_member_meet_criteria_unmarried_60_old_women = models.BooleanField(default=False)
    family_member_meet_criteria_single_60_old_women = models.BooleanField(default=False)
    family_member_meet_criteria_widow_of_any_age = models.BooleanField(default=False)
    family_member_meet_criteria_received_red_color_blindness = models.BooleanField(default=False)
    family_member_meet_criteria_received_blue_color_blindness = models.BooleanField(default=False)
    family_member_meet_criteria_endangered_trives_of_any_age = models.BooleanField(default=False)
    family_member_meet_criteria_children_under_5_dalit_and_children = models.BooleanField(default=False)
    family_member_meet_criteria_none_of_above = models.BooleanField(default=False)
    received_social_security = models.CharField(max_length=500, blank=True, null=True)
    reasons_for_not_received_social_security = models.CharField(max_length=500, blank=True, null=True)
    family_criteria_belonging_to = models.CharField(max_length=500, blank=True, null=True)
    family_criteria_belonging_to_pregnant = models.BooleanField(default=False)
    family_criteria_belonging_to_lactating_mother = models.BooleanField(default=False)
    family_criteria_belonging_to_single_woman = models.BooleanField(default=False)
    family_criteria_belonging_to_senior_citizen = models.BooleanField(default=False)
    family_criteria_belonging_to_breast_feeding_baby = models.BooleanField(default=False)
    family_criteria_belonging_to_people_with_disability = models.BooleanField(default=False)
    family_criteria_belonging_to_people_with_chronic_illness = models.BooleanField(default=False)
    family_criteria_belonging_to_none_of_above = models.BooleanField(default=False)
    family_criteria_belonging_other = models.BooleanField(default=False)
    family_criteria_belonging_other_mention = models.BooleanField(default=False)
    reasons_for_not_received_social_security = models.CharField(max_length=500, blank=True, null=True)
    people_with_disability = models.CharField(max_length=500, blank=True, null=True)
    people_with_disability_mental_or_psychological_disability = models.BooleanField(default=False)
    people_with_disability_intellectual_disability = models.BooleanField(default=False)
    people_with_disability_multiple_disability = models.BooleanField(default=False)
    people_with_disability_difficulties_with_communicating = models.BooleanField(default=False)
    people_with_disability_difficulties_with_seeing = models.BooleanField(default=False)
    people_with_disability_difficulties_with_hearing = models.BooleanField(default=False)
    people_with_disability_both_seeing_and_hearing = models.BooleanField(default=False)
    people_with_disability_difficulties_with_self_care = models.BooleanField(default=False)
    people_with_disability_difficulties_with_remembering = models.BooleanField(default=False)
    people_with_disability_difficulties_with_climbing_steps = models.BooleanField(default=False)
    people_with_disability_other = models.BooleanField(default=False)
    people_with_disability_other_mention = models.BooleanField(default=False)
    chronic_illness_type = models.CharField(max_length=200, blank=True, null=True)
    chronic_illness_type_diabetes = models.CharField(max_length=200, blank=True, null=True)
    chronic_illness_type_asthama = models.CharField(max_length=200, blank=True, null=True)
    chronic_illness_type_heart_diseases = models.CharField(max_length=200, blank=True, null=True)
    chronic_illness_type_kidney_diseases = models.CharField(max_length=200, blank=True, null=True)
    chronic_illness_type_cancer = models.CharField(max_length=200, blank=True, null=True)
    chronic_illness_type_aids = models.CharField(max_length=200, blank=True, null=True)
    chronic_illness_type_alzheimer = models.CharField(max_length=200, blank=True, null=True)
    chronic_illness_type_other = models.CharField(max_length=200, blank=True, null=True)
    chronic_illness_type_other_mention = models.CharField(max_length=500, blank=True, null=True)
    survey = models.ForeignKey('HouseHoldData', on_delete=models.CASCADE, related_name= 'house_hold_data')


class AnimalDetailData(models.Model):
    type = models.CharField(max_length=500, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    is_it_for_commercial_purpose = models.CharField(max_length=500, blank=True, null=True)
    survey = models.ForeignKey('HouseHoldData', on_delete=models.CASCADE, related_name= 'animal_detail_data')








0
















































































































