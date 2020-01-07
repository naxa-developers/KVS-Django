from django.contrib import admin
from core.models import Province, District, Municipality, HouseHoldData, AnimalDetailData, OwnerFamilyData, \
    OtherFamilyMember

from core.resource import OwnerFamilyResource, AnimalDetailResource, HouseholdResource, OtherFamilyResource

from import_export.admin import ImportExportModelAdmin


admin.site.register(Province)
admin.site.register(District)
admin.site.register(Municipality)


class HouseHoldAdmin(ImportExportModelAdmin):
    resource_class = HouseholdResource


admin.site.register(HouseHoldData, HouseHoldAdmin)



class OwnerFamilyAdmin(ImportExportModelAdmin):
    resource_class = OwnerFamilyResource


admin.site.register(OwnerFamilyData, OwnerFamilyAdmin)


class AnimalDetailAdmin(ImportExportModelAdmin):
    resource_class = AnimalDetailResource


admin.site.register(AnimalDetailData, AnimalDetailAdmin)


class OtherFamilyAdmin(ImportExportModelAdmin):
    resource_class = OtherFamilyResource


admin.site.register(OtherFamilyMember, OtherFamilyAdmin)
