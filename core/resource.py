from import_export import resources
from .models import HouseHoldData, OwnerFamilyData, AnimalDetailData, OtherFamilyMember


class HouseholdResource(resources.ModelResource):
    class Meta:
        model = HouseHoldData


class OwnerFamilyResource(resources.ModelResource):
    class Meta:
        model = OwnerFamilyData


class AnimalDetailResource(resources.ModelResource):
    class Meta:
        model = AnimalDetailData

class OtherFamilyResource(resources.ModelResource):
    class Meta:
        model = OtherFamilyMember
