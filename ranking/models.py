from django.db import models


class Theme(models.Model):
    name = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=6, decimal_places=3)
    calculated_value = models.DecimalField(
        max_digits=6, decimal_places=3, null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent_theme = models.ForeignKey("ranking.Theme", on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=6, decimal_places=3)
    calculated_value = models.DecimalField(
        max_digits=6, decimal_places=3, null=True, blank=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    SCORING_METHOD_CHOICES = (
        ('substrings',	'scoring based on a fixed number of substrings'),
        ('yes/no',	'scoring based on simple yes or no'),
        ('keywords', 'scoring based on a fixed number of keywords'),
        ('composite_count',	'options varries from No to More than 1'),
        ('multifield_substring',
         'one that combines data from 2 or more fields based on substrings'),
        ('range_based', 'options have some kind of range of values, e.g. distance 50-100 metre, 100-200 metre')
    )

    MAP_TO_FIELD_CHOICES = (('alternative_market_name', 'alternative_market_name'), ('altitude', 'altitude'), ('animal_presence', 'animal_presence'), ('building_standard_code', 'building_standard_code'), ('business', 'business'), ('capacity_of_evacuation_shelter', 'capacity_of_evacuation_shelter'), ('condiments', 'condiments'), ('contact_no', 'contact_no'), ('coping_mechanism_during_disaster', 'coping_mechanism_during_disaster'), ('crop_sufficiency', 'crop_sufficiency'), ('dakarmi_sikarmi_female_number', 'dakarmi_sikarmi_female_number'), ('dakarmi_sikarmi_male_number', 'dakarmi_sikarmi_male_number'), ('dakarmi_sikarmi_sex', 'dakarmi_sikarmi_sex'), ('damage_occurred_during_landslide', 'damage_occurred_during_landslide'), ('damages_occurred_during_earthquake', 'damages_occurred_during_earthquake'), ('damages_occurred_during_fire', 'damages_occurred_during_fire'), ('damages_occurred_during_flood', 'damages_occurred_during_flood'), ('date_of_birth', 'date_of_birth'), ('deviceid', 'deviceid'), ('disaster_information_medium', 'disaster_information_medium'), ('disaster_information_medium_other', 'disaster_information_medium_other'), ('disaster_type', 'disaster_type'), ('disaster_type_other', 'disaster_type_other'), ('distance_from_main_road', 'distance_from_main_road'), ('distance_from_nearest_health_institution', 'distance_from_nearest_health_institution'), ('distance_from_nearest_school', 'distance_from_nearest_school'), ('distance_from_nearest_security_forces', 'distance_from_nearest_security_forces'), ('distance_to_alternative_market', 'distance_to_alternative_market'), ('distance_to_evacuation_shelter', 'distance_to_evacuation_shelter'), ('distance_to_nearest_market', 'distance_to_nearest_market'), ('distance_to_nearest_open_space', 'distance_to_nearest_open_space'), ('distance_to_safe_place_for_flood', 'distance_to_safe_place_for_flood'), ('district', 'district'), ('doctor_female_number', 'doctor_female_number'), ('doctor_male_number', 'doctor_male_number'), ('doctor_sex', 'doctor_sex'), ('early_warning_system_installed_nearby', 'early_warning_system_installed_nearby'), ('earthquake_resistance', 'earthquake_resistance'), ('easy_access_to_goods', 'easy_access_to_goods'), ('electrician_female_number', 'electrician_female_number'), ('electrician_male_number', 'electrician_male_number'), ('electrician_sex', 'electrician_sex'), ('emergency_kit_availability_in_house', 'emergency_kit_availability_in_house'), ('emergency_kit_material_update_frequency', 'emergency_kit_material_update_frequency'), ('engineer_female_number', 'engineer_female_number'), ('engineer_male_number', 'engineer_male_number'), ('engineer_sex', 'engineer_sex'), ('evacuation_shelter_availability', 'evacuation_shelter_availability'), ('facilities_type', 'facilities_type'), ('fire_extinguisher_in_house', 'fire_extinguisher_in_house'), ('flood_activities_resilience_other', 'flood_activities_resilience_other'), ('flood_prone', 'flood_prone'), ('flood_resilience_activities', 'flood_resilience_activities'), ('flood_resilience_work', 'flood_resilience_work'), ('food_type', 'food_type'), ('fruits', 'fruits'), ('fuel_type', 'fuel_type'), ('goods_available_in_nearest_market', 'goods_available_in_nearest_market'), ('got_early_warning_during_disaster', 'got_early_warning_during_disaster'), ('got_early_warning_during_through', 'got_early_warning_during_through'), ('gps_precision', 'gps_precision'), ('ha_lab_female_number', 'ha_lab_female_number'), ('ha_lab_male_number', 'ha_lab_male_number'), ('ha_lab_sex', 'ha_lab_sex'), ('has_flood_effect_tubewell', 'has_flood_effect_tubewell'), ('hazard_type', 'hazard_type'), ('hazard_type_other', 'hazard_type_other'), ('house_built_year', 'house_built_year'), ('house_damage_type_during_earthquake', 'house_damage_type_during_earthquake'), ('house_damage_type_during_earthquake_other', 'house_damage_type_during_earthquake_other'), ('house_damage_type_during_fire', 'house_damage_type_during_fire'), ('house_damage_type_during_fire_other', 'house_damage_type_during_fire_other'), ('house_damage_type_during_flood', 'house_damage_type_during_flood'), ('house_damage_type_during_flood_other', 'house_damage_type_during_flood_other'), ('house_damage_type_during_landslide', 'house_damage_type_during_landslide'), ('house_damage_type_during_landslide_other', 'house_damage_type_during_landslide_other'), ('house_map_registered', 'house_map_registered'), ('house_number', 'house_number'), ('house_stories', 'house_stories'), ('house_type', 'house_type'), ('house_type_other', 'house_type_other'), ('household_number', 'household_number'), ('how_goods_were_managed_if_not_available_in_market', 'how_goods_were_managed_if_not_available_in_market'), ('identified_safe_place_for_flood', 'identified_safe_place_for_flood'), ('insurance', 'insurance'), ('involved_disaster_training', 'involved_disaster_training'), ('involved_disaster_training_type', 'involved_disaster_training_type'), ('involved_disaster_training_type_other', 'involved_disaster_training_type_other'), ('involved_in_simulation_type', 'involved_in_simulation_type'), ('involved_in_simulation_type_other', 'involved_in_simulation_type_other'), ('involvement_in_dprp_development_process', 'involvement_in_dprp_development_process'), (
        'involvement_in_ldcrp_development_process', 'involvement_in_ldcrp_development_process'), ('is_there_identified_risk_areas', 'is_there_identified_risk_areas'), ('jt_female_number', 'jt_female_number'), ('jt_male_number', 'jt_male_number'), ('jt_sex', 'jt_sex'), ('knowledge_about_dprp', 'knowledge_about_dprp'), ('knowledge_about_ldcrp', 'knowledge_about_ldcrp'), ('knowledge_on_early_warning_system', 'knowledge_on_early_warning_system'), ('land_ownership', 'land_ownership'), ('latitude', 'latitude'), ('loan', 'loan'), ('loan_amount', 'loan_amount'), ('loan_duration', 'loan_duration'), ('longitude', 'longitude'), ('main_occupation', 'main_occupation'), ('main_staple', 'main_staple'), ('manpower_type', 'manpower_type'), ('meat_and_fish', 'meat_and_fish'), ('medium_suitable_for_early_warning', 'medium_suitable_for_early_warning'), ('migrated_place_during_earthquake', 'migrated_place_during_earthquake'), ('migrated_place_during_fire', 'migrated_place_during_fire'), ('migrated_place_during_fire_other', 'migrated_place_during_fire_other'), ('migrated_place_during_flood', 'migrated_place_during_flood'), ('migrated_place_during_flood_other', 'migrated_place_during_flood_other'), ('migrated_place_during_landslide', 'migrated_place_during_landslide'), ('milk_and_products', 'milk_and_products'), ('monthly_expenses', 'monthly_expenses'), ('monthly_income', 'monthly_income'), ('most_occuring_disasters_in_ward', 'most_occuring_disasters_in_ward'), ('mother_tongue', 'mother_tongue'), ('mother_tongue_other', 'mother_tongue_other'), ('municipality', 'municipality'), ('nearest_market_operation_during_disaster', 'nearest_market_operation_during_disaster'), ('no_of_houses_using_tubewell', 'no_of_houses_using_tubewell'), ('no_of_rooms', 'no_of_rooms'), ('nurse_female_number', 'nurse_female_number'), ('nurse_male_number', 'nurse_male_number'), ('nurse_sex', 'nurse_sex'), ('oil_products', 'oil_products'), ('other_business', 'other_business'), ('other_coping_mechanism_during_disaster', 'other_coping_mechanism_during_disaster'), ('other_damage_occurred_during_landslide', 'other_damage_occurred_during_landslide'), ('other_damages_occured_during_fire', 'other_damages_occured_during_fire'), ('other_damages_occurred_during_earthquake', 'other_damages_occurred_during_earthquake'), ('other_damages_occurred_during_flood', 'other_damages_occurred_during_flood'), ('other_facilities', 'other_facilities'), ('other_family_living', 'other_family_living'), ('other_fuel_type', 'other_fuel_type'), ('other_goods_available_in_nearest_market', 'other_goods_available_in_nearest_market'), ('other_insurance', 'other_insurance'), ('other_medium_suitable_for_early_warning', 'other_medium_suitable_for_early_warning'), ('other_occupation', 'other_occupation'), ('other_small_business', 'other_small_business'), ('other_technical', 'other_technical'), ('other_technical_female_number', 'other_technical_female_number'), ('other_technical_male_number', 'other_technical_male_number'), ('other_technical_sex', 'other_technical_sex'), ('owned_land_area', 'owned_land_area'), ('owned_land_area_near_river', 'owned_land_area_near_river'), ('owned_land_image', 'owned_land_image'), ('owned_land_image_name', 'owned_land_image_name'), ('owned_land_image_thumbnail', 'owned_land_image_thumbnail'), ('owned_land_near_river', 'owned_land_near_river'), ('owner_age', 'owner_age'), ('owner_caste', 'owner_caste'), ('owner_caste_other', 'owner_caste_other'), ('owner_citizenship_no', 'owner_citizenship_no'), ('owner_education', 'owner_education'), ('owner_name', 'owner_name'), ('owner_sex', 'owner_sex'), ('owner_status', 'owner_status'), ('owner_status_other', 'owner_status_other'), ('place_name', 'place_name'), ('plumber_female_number', 'plumber_female_number'), ('plumber_male_number', 'plumber_male_number'), ('plumber_sex', 'plumber_sex'), ('prepared_contingency_plan', 'prepared_contingency_plan'), ('province', 'province'), ('public_tap_distance', 'public_tap_distance'), ('pulses', 'pulses'), ('religion', 'religion'), ('religion_other', 'religion_other'), ('remarks', 'remarks'), ('responder_age', 'responder_age'), ('responder_contact', 'responder_contact'), ('responder_name', 'responder_name'), ('responder_sex', 'responder_sex'), ('risk_score', 'risk_score'), ('road_capacity', 'road_capacity'), ('road_type', 'road_type'), ('road_width', 'road_width'), ('subengineer_female', 'subengineer_female'), ('subengineer_male', 'subengineer_male'), ('subengineer_sex', 'subengineer_sex'), ('sugar_products', 'sugar_products'), ('surveyor_name', 'surveyor_name'), ('technical_manpower_presence', 'technical_manpower_presence'), ('toilet_facility', 'toilet_facility'), ('toilet_type', 'toilet_type'), ('toilet_type_other', 'toilet_type_other'), ('tubewell_status', 'tubewell_status'), ('tubewell_type', 'tubewell_type'), ('vegetables', 'vegetables'), ('vehicle', 'vehicle'), ('vehicles_other', 'vehicles_other'), ('veterinary_female_number', 'veterinary_female_number'), ('veterinary_male_number', 'veterinary_male_number'), ('veterinary_sex', 'veterinary_sex'), ('ward', 'ward'), ('warehouse_available_in_ward', 'warehouse_available_in_ward'), ('water_sources', 'water_sources'), ('water_sources_other', 'water_sources_other'), ('waterborne_disease', 'waterborne_disease'))

    question = models.CharField(max_length=200)
    parent_category = models.ForeignKey(
        "ranking.Category", on_delete=models.CASCADE)
    directly_mappable = models.BooleanField(default=True)
    scoring_method = models.CharField(
        choices=SCORING_METHOD_CHOICES, max_length=200, default='substrings')
    map_to_field_1 = models.CharField(
        choices=MAP_TO_FIELD_CHOICES, max_length=200, default=None)
    map_to_field_2 = models.CharField(
        choices=MAP_TO_FIELD_CHOICES, max_length=200, null=True, blank=True)
    map_to_model = models.CharField(max_length=500)
    weight = models.DecimalField(max_digits=6, decimal_places=3)
    calculated_value = models.DecimalField(
        max_digits=6, decimal_places=3, null=True, blank=True)

    def __str__(self):
        return self.question


class Answer(models.Model):
    ANSWER_TYPES_CHOICES = (
        ('substring', 'answer should be derived from substring of the field data'),
        ('code_mapping', 'certain coding mechanism in the data, e.g. number codes mentioned in data for different answer options'),
        ('time_range_from_substring',
         'time range need to be derived from substring of the field'),
        ('count_from_substring', 'count need to be derived from substring of the field'),
        ('complex_calculation',	'involves a number of factors ans fields to find the score')
    )
    answer_choice = models.CharField(max_length=100)
    parent_question = models.ForeignKey(
        "ranking.Question", on_delete=models.CASCADE)
    answer_types = models.CharField(
        choices=ANSWER_TYPES_CHOICES, max_length=200, default='substrings')
    weight = models.DecimalField(max_digits=6, decimal_places=3)
    calculated_value = models.DecimalField(
        max_digits=6, decimal_places=3, null=True, blank=True)

    def __str__(self):
        return self.answer_choice
