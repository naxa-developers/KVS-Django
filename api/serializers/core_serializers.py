from core.models import Province, District, Municipality, HouseHoldData, AnimalDetailData, OwnerFamilyData, Gallery
from rest_framework import serializers


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'


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

class HouseHoldDataSerializer(serializers.ModelSerializer):
    family_size = serializers.SerializerMethodField()
    social_security_received = serializers.SerializerMethodField()

    class Meta:
        model = HouseHoldData
        fields = ('id', 'index', 'deviceid', 'date', 'surveyor_name', 'place_name', 'province', 'district', 'municipality',
                  'ward', 'house_number', 'latitude', 'longitude', 'altitude', 'gps_precision', 'household_number',
                  'owner_name', 'date_of_birth', 'owner_age', 'owner_sex', 'owner_status', 'owner_status_other', 'owner_caste',
                  'owner_caste_other', 'religion', 'religion_other', 'mother_tongue', 'mother_tongue_other',
                  'contact_no', 'owner_education', 'owner_citizenship_no', 'responder_name', 'responder_sex',
                  'responder_age', 'responder_contact', 'other_family_living', 'main_occupation', 'other_occupation',
                  'business', 'other_business', 'other_small_business', 'crop_sufficiency', 'food_type', 'main_staple',
                  'pulses', 'vegetables', 'fruits', 'meat_and_fish', 'milk_and_products', 'sugar_products',
                  'oil_products', 'condiments', 'monthly_expenses', 'monthly_income', 'loan', 'loan_amount',
                  'loan_duration', 'animal_presence', 'insurance', 'other_insurance', 'vehicle', 'vehicles_other',
                  'facilities_type', 'other_facilities', 'fuel_type', 'other_fuel_type', 'land_ownership', 'house_type',
                  'house_type_other', 'house_built_year', 'house_stories', 'no_of_rooms', 'house_map_registered',
                  'building_standard_code', 'earthquake_resistance', 'flood_prone', 'flood_resilience_activities',
                  'flood_activities_resilience_other', 'owned_land_area', 'owned_land_near_river',
                  'owned_land_area_near_river', 'owned_land_image', 'technical_manpower_presence', 'manpower_type',
                  'doctor_sex', 'doctor_male_number', 'doctor_female_number', 'engineer_sex', 'engineer_male_number',
                  'engineer_female_number', 'subengineer_sex', 'subengineer_male', 'subengineer_female', 'nurse_sex',
                  'nurse_male_number', 'nurse_female_number', 'ha_lab_sex', 'ha_lab_male_number',
                  'ha_lab_female_number', 'veterinary_sex', 'veterinary_male_number', 'veterinary_female_number',
                  'dakarmi_sikarmi_sex', 'dakarmi_sikarmi_male_number', 'dakarmi_sikarmi_female_number',
                  'plumber_sex', 'plumber_male_number', 'plumber_female_number', 'electrician_sex',
                  'electrician_male_number', 'electrician_female_number', 'jt_sex', 'jt_male_number',
                  'jt_female_number', 'other_technical', 'other_technical_sex', 'other_technical_male_number',
                  'other_technical_female_number', 'distance_from_main_road', 'road_type', 'road_width',
                  'road_capacity', 'distance_from_nearest_school', 'distance_from_nearest_health_institution',
                  'distance_from_nearest_security_forces', 'water_sources', 'water_sources_other', 'tubewell_type',
                  'tubewell_status', 'no_of_houses_using_tubewell', 'has_flood_effect_tubewell', 'public_tap_distance',
                  'toilet_facility', 'toilet_type', 'toilet_type_other', 'waterborne_disease', 'disaster_type',
                  'disaster_type_other', 'hazard_type', 'hazard_type_other', 'is_there_identified_risk_areas',
                  'disaster_information_medium', 'disaster_information_medium_other',
                  'knowledge_on_early_warning_system', 'early_warning_system_installed_nearby',
                  'got_early_warning_during_disaster', 'got_early_warning_during_through',
                  'medium_suitable_for_early_warning', 'other_medium_suitable_for_early_warning',
                  'evacuation_shelter_availability', 'distance_to_evacuation_shelter', 'capacity_of_evacuation_shelter',
                  'distance_to_nearest_open_space', 'distance_to_nearest_market', 'goods_available_in_nearest_market',
                  'other_goods_available_in_nearest_market', 'distance_to_alternative_market', 'alternative_market_name',
                  'nearest_market_operation_during_disaster', 'easy_access_to_goods',
                  'how_goods_were_managed_if_not_available_in_market', 'warehouse_available_in_ward',
                  'coping_mechanism_during_disaster', 'other_coping_mechanism_during_disaster',
                  'emergency_kit_availability_in_house', 'emergency_kit_material_update_frequency',
                  'involved_disaster_training', 'involved_disaster_training_type', 'involved_disaster_training_type_other',
                  'involved_in_simulation_type', 'involved_in_simulation_type_other', 'knowledge_about_ldcrp',
                  'involvement_in_ldcrp_development_process', 'knowledge_about_dprp',
                  'involvement_in_dprp_development_process', 'prepared_contingency_plan', 'most_occuring_disasters_in_ward',
                  'identified_safe_place_for_flood', 'distance_to_safe_place_for_flood', 'damages_occurred_during_flood',
                  'other_damages_occurred_during_flood', 'house_damage_type_during_flood', 'house_damage_type_during_flood_other',
                  'migrated_place_during_flood', 'migrated_place_during_flood_other', 'damage_occurred_during_landslide',
                  'other_damage_occurred_during_landslide', 'house_damage_type_during_landslide', 'house_damage_type_during_landslide_other',
                  'migrated_place_during_landslide', 'damages_occurred_during_earthquake', 'other_damages_occurred_during_earthquake',
                  'house_damage_type_during_earthquake', 'house_damage_type_during_earthquake_other', 'migrated_place_during_earthquake',
                  'damages_occurred_during_fire', 'other_damages_occured_during_fire', 'house_damage_type_during_fire',
                  'house_damage_type_during_fire_other', 'fire_extinguisher_in_house', 'migrated_place_during_fire',
                  'migrated_place_during_fire_other', 'remarks', 'family_size' , 'social_security_received', 'owned_land_image_thumbnail'
                  )

    def get_family_size(self,obj):
        size = obj.house_hold_data.all().count()
        return size


    def get_social_security_received(self, obj):
        query = obj.house_hold_data.filter(social_security_received__icontains='Yes')
        if not query:
            return False
        else:
            return True


class HouseHoldAlternativeSerializer(serializers.ModelSerializer):
    family_size = serializers.SerializerMethodField()
    social_security_received = serializers.SerializerMethodField()
    male_number = serializers.SerializerMethodField()
    female_number = serializers.SerializerMethodField()
    member_received_social_security_number = serializers.SerializerMethodField()
    member_not_received_social_security_number = serializers.SerializerMethodField()
    total_security_received_members = serializers.SerializerMethodField()

    class Meta:
        model = HouseHoldData
        fields = ('id', 'index', 'province', 'district', 'municipality', 'owner_name','date_of_birth', 'owner_age', 'owner_sex',
                  'owner_citizenship_no', 'contact_no', 'ward', 'family_size', 'social_security_received',
                  'latitude', 'longitude', 'main_occupation', 'owner_education', 'mother_tongue', 'male_number',
                  'female_number', 'member_received_social_security_number',
                  'member_not_received_social_security_number', 'total_security_received_members')

    def get_family_size(self,obj):
        size = obj.house_hold_data.all().count()
        return size

    def get_social_security_received(self, obj):
        query = obj.house_hold_data.filter(social_security_received__icontains='Yes')
        if not query:
            return False
        else:
            return True

    def get_male_number(self,obj):
        total_count = obj.house_hold_data.all().count()
        female_count = obj.house_hold_data.filter(gender__icontains='female').count()
        male_count = total_count-female_count

        return male_count

    def get_female_number(self,obj):
        female_count = obj.house_hold_data.filter(gender__icontains='female').count()
        return female_count

    def get_member_received_social_security_number(self, obj):
        received = obj.house_hold_data.filter(social_security_received__icontains='Yes').count()
        return received

    def get_member_not_received_social_security_number(self,obj):
        received = obj.house_hold_data.filter(social_security_received__icontains='Yes').count()
        all_member = obj.house_hold_data.all().count()
        not_received = all_member-received
        return not_received

    def get_total_security_received_members(self,obj):
        member = OwnerFamilyData.objects.filter(social_security_received__icontains='Yes').count()
        return member




class AnimalDetailDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalDetailData
        fields = '__all__'


class OwnerFamilyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnerFamilyData
        fields = '__all__'

