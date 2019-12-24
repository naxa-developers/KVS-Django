from django.contrib import admin
from core.models import Province, District, Municipality, DamageList, HouseDamageList, DisasterList, \
    MigrationList, OccupationList, BusinessList, FoodChoice, InsuranceList, VehicleList, FacilityList, \
    FuelTypeList, WorkDoneOnFloodList, DrinkingWaterList, TechnicalFieldList, InformationMediumList, \
    WarningMediumList, MaterialsInNearestMarketList, CopingMechanismList, DisasterPreparednessMechanismList, \
    GenderList, WhoseOwnershipList, HouseTypeList, OwnershipList, EthnicityList, ReligionList, MotherTongueList, \
    EducationList, PermitList, RoadType, RoadCapacity, LatrineList, InvolvementList, FamilyMemberCriterialist, \
    AgeGroupList, PopulationChoicesList, ChronicIllnessList, DisabilityList

from import_export.admin import ImportExportModelAdmin


admin.site.register(Province)
admin.site.register(District)
admin.site.register(Municipality)

# choices field registered

admin.site.register(DamageList)
admin.site.register(HouseDamageList)
admin.site.register(DisasterList)
admin.site.register(MigrationList)
admin.site.register(OccupationList)
admin.site.register(BusinessList)
admin.site.register(FoodChoice)
admin.site.register(InsuranceList)
admin.site.register(VehicleList)
admin.site.register(FacilityList)
admin.site.register(FuelTypeList)
admin.site.register(WorkDoneOnFloodList)
admin.site.register(DrinkingWaterList)
admin.site.register(TechnicalFieldList)
admin.site.register(InformationMediumList)
admin.site.register(WarningMediumList)
admin.site.register(MaterialsInNearestMarketList)
admin.site.register(CopingMechanismList)
admin.site.register(DisasterPreparednessMechanismList)

admin.site.register(GenderList)
admin.site.register(WhoseOwnershipList)
admin.site.register(HouseTypeList)
admin.site.register(OwnershipList)
admin.site.register(EthnicityList)
admin.site.register(ReligionList)
admin.site.register(MotherTongueList)
admin.site.register(EducationList)
admin.site.register(PermitList)
admin.site.register(RoadType)
admin.site.register(RoadCapacity)
admin.site.register(LatrineList)


admin.site.register(InvolvementList)
admin.site.register(FamilyMemberCriterialist)
admin.site.register(AgeGroupList)
admin.site.register(PopulationChoicesList)
admin.site.register(ChronicIllnessList)
admin.site.register(DisabilityList)


# class SurveyAdmin(ImportExportModelAdmin):
#     resource_class = SurveyResource
#
#
# admin.site.register(Survey, SurveyAdmin)