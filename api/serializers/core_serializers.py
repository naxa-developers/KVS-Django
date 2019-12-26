from core.models import Province, District, Municipality, HouseHold, AnimalDetails, OwnerFamily, Occupation, \
    DisasterProne, FoodEaten, Insurance, Vehicle, Facilities, Fuel, WorkDoneOnFlood, DrinkingWater, \
    TechnicalField, InformationMedium, WarningMediumSuitableForDisaster, MaterialsInNearestMarket, \
    CopingMechanism, DisasterPreparednessMechanism, InvolvedInSimulation, GuideLine, WardFallingProneArea, \
    WhoseOwnershipData, HouseType, RoadCapacity, Latrine, FamilyMemberCriteriaData, PopulationChoiceData, \
    ChronicIllnessData, DisabilityData
from rest_framework import serializers


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'


class MunicipalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality
        fields = '__all__'


class OccupationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occupation
        fields = '__all__'


class DisasterProneSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisasterProne
        fields = '__all__'


class FoodEatenSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodEaten
        fields = '__all__'


class InsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facilities
        fields = '__all__'


class FuelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fuel
        fields = '__all__'


class WorkDoneOnFloodSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkDoneOnFlood
        fields = '__all__'


class DrinkingWaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrinkingWater
        fields = '__all__'


class TechnicalFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalField
        fields = '__all__'


class InformationMediumSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformationMedium
        fields = '__all__'


class WarningMediumSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarningMediumSuitableForDisaster
        fields = '__all__'


class MaterialsInNearestMarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialsInNearestMarket
        fields = '__all__'


class CopingMechanismSerializer(serializers.ModelSerializer):
    class Meta:
        model = CopingMechanism
        fields = '__all__'


class DisasterPreparednessMechanismSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisasterPreparednessMechanism
        fields = '__all__'


class InvolvedInSimulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvolvedInSimulation
        fields = '__all__'


class GuideLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuideLine
        fields = '__all__'


class WardFallingProneAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = WardFallingProneArea
        fields = '__all__'


class WhoseOwnershipDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhoseOwnershipData
        fields = '__all__'


class HouseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseType
        fields = '__all__'


class RoadCapacitySerializer(serializers.ModelSerializer):
    class Meta:
        model = RoadCapacity
        fields = '__all__'


class LatrineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Latrine
        fields = '__all__'


class HouseHoldSerializer(serializers.ModelSerializer):
    occupation = OccupationSerializer(many=True)
    disaster_prone = DisasterProneSerializer(many=True)
    food_eaten = FoodEatenSerializer(many=True)
    insurance = InsuranceSerializer(many=True)
    vehicle = VehicleSerializer(many=True)
    facility = FacilitySerializer(many=True)
    fuel = FuelSerializer(many=True)
    work_done = WorkDoneOnFloodSerializer(many=True)
    drinking_water = DrinkingWaterSerializer(many=True)
    technical_man = TechnicalFieldSerializer(many=True)
    info_medium = InformationMediumSerializer(many=True)
    warn_medium = WarningMediumSerializer(many=True)
    market_material = MaterialsInNearestMarketSerializer(many=True)
    coping_mechanism = CopingMechanismSerializer(many=True)
    disaster_prepare = DisasterPreparednessMechanismSerializer(many=True)
    simulation = InvolvedInSimulationSerializer(many=True)
    guide_line = GuideLineSerializer(many=True)
    ward_prone = WardFallingProneAreaSerializer(many=True)
    whose_ownership = WhoseOwnershipDataSerializer(many=True)
    house_type = HouseTypeSerializer(many=True)
    household_road = RoadCapacitySerializer(many=True)
    latrine = LatrineSerializer(many=True)

    class Meta:
        model = HouseHold
        fields = ['index', 'start_date', 'end_date', 'surveyor_name', 'name_of_place',
                  'ward_no', 'location', 'altitude', 'precision', 'household_no', 'house_holder_name',
                  'age_of_owner', 'gender_of_house_owner', 'status_of_owner', 'if_other_owner_status',
                  'ethnicity', 'other_ethnicity', 'religion', 'religion_other', 'mother_tongue', 'other_mother_tongue',
                  'contact_num', 'education_level', 'owner_citizenship_number', 'responder_name', 'responder_gender',
                  'responder_age', 'responder_contact', 'other_family_member', 'foods_eaten_in_last7_day',
                  'monthly_expanses', 'monthly_income', 'if_loan_amount', 'loan_time', 'have_livestock',
                  'date_of_establishment', 'number_of_storey', 'number_of_rooms', 'received_building_permit',
                  'building_completion_certificate', 'is_house_earthquake_resilience', 'is_house_landslide_resilience',
                  'how_much_land_ownership', 'does_land_lies_near_river_flood_plain', 'land_near_river_flood_plain',
                  'image_with_landscape', 'time_for_nearest_road', 'road_type', 'road_width', 'time_to_nearest_school',
                  'time_to_nearest_health_institution', 'time_to_nearest_security_force',
                  'does_ward_have_identified_risk_area', 'do_you_know_about_warning_system', 'is_there_waning_system',
                  'did_you_got_early_information_in_disaster', 'if_yes_which_medium_was_used',
                  'does_ward_have_evacuation_shelter', 'distance_to_evacuation_shelter',
                  'capacity_of_evacuation_shelter', 'distance_to_nearest_openspace', 'how_far_nearest_market',
                  'was_nearest_market_operating_in_disaster', 'was_material_easily_available',
                  'if_not_material_how_you_managed', 'how_far_is_alternative_market', 'name_of_alternative_market',
                  'is_there_warehouse_in_your_ward', 'how_often_replace_material_in_emergency_kit',
                  'contingency_plan_involvement', 'occupation', 'disaster_prone', 'insurance', 'food_eaten', 'vehicle', 'facility',
                  'fuel', 'work_done', 'drinking_water', 'technical_man', 'info_medium', 'warn_medium', 'guide_line',
                  'market_material', 'coping_mechanism', 'disaster_prepare', 'ward_prone', 'whose_ownership',
                  'house_type', 'household_road', 'latrine', 'whose_ownership', 'simulation'
                  ]


class FamilyMemberCriteriaDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyMemberCriteriaData
        fields = '__all__'


class PopulationChoiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopulationChoiceData
        fields = '__all__'


class ChronicIllnessDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChronicIllnessData
        fields = '__all__'


class DisabilityDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisabilityData
        fields = '__all__'


class OwnerFamilySerializer(serializers.ModelSerializer):
    family_member_criteria = FamilyMemberCriteriaDataSerializer(many=True)
    population_choice = PopulationChoiceDataSerializer(many=True)
    chronic_illness = ChronicIllnessDataSerializer(many=True)
    disability = DisabilityDataSerializer(many=True)

    class Meta:
        model = OwnerFamily
        fields = [
            'name', 'age_group', 'education_level', 'gender', 'citizenship_num', 'occupation_of_family',
            'involvement_in_occupation', 'if_other_occupation', 'monthly_income', 'household',
            'received_social_security', 'reason_not_received_social_security', 'other_population_choices',
            'family_member_criteria', 'population_choice', 'chronic_illness', 'disability'
        ]


class AnimalDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalDetails
        fields = '__all__'
