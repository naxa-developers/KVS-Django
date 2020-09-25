from django.contrib import admin
from core.models import Province, District, Municipality, HouseHoldData, AnimalDetailData, OwnerFamilyData, \
    OtherFamilyMember, UserRole, Ward

from core.resource import OwnerFamilyResource, AnimalDetailResource, HouseholdResource, OtherFamilyResource

from import_export.admin import ImportExportModelAdmin
from core.generals import export_municipality_csv, export_district_csv



admin.site.register(Province)
# admin.site.register(District)
# admin.site.register(Municipality)
admin.site.register(Ward)
admin.site.register(UserRole)


class HouseHoldAdmin(ImportExportModelAdmin):
    resource_class = HouseholdResource
    list_display = ('index', 'owner_name', 'surveyor_name')
    search_fields = ('index', 'owner_name')

admin.site.register(HouseHoldData, HouseHoldAdmin)



class OwnerFamilyAdmin(ImportExportModelAdmin):
    resource_class = OwnerFamilyResource
    list_display = ('index', 'parent_index', 'name', 'survey')
    search_fields = ('index', 'parent_index', 'name')


admin.site.register(OwnerFamilyData, OwnerFamilyAdmin)


class AnimalDetailAdmin(ImportExportModelAdmin):
    resource_class = AnimalDetailResource

admin.site.register(AnimalDetailData, AnimalDetailAdmin)


class OtherFamilyAdmin(ImportExportModelAdmin):
    resource_class = OtherFamilyResource
    list_display = ('index', 'parent_index', 'total_persons', 'survey')
    search_fields = ('index', 'parent_index', 'survey')

admin.site.register(OtherFamilyMember, OtherFamilyAdmin)



#adding export of municipality as csv on admin site

# admin.site.add_action(export_municipality_csv)


class MyAdmin(admin.ModelAdmin):
    actions = [export_municipality_csv]


admin.site.register(Municipality, MyAdmin)

class DistrictAdmin(admin.ModelAdmin):
    actions = [export_district_csv]

admin.site.register(District, DistrictAdmin)
