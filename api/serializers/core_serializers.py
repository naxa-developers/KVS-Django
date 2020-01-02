from core.models import Province, District, Municipality, HouseHoldData, AnimalDetailData, OwnerFamilyData
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

class HouseHoldDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseHoldData
        fields = '__all__'

class AnimalDetailDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalDetailData
        fields = '__all__'

class OwnerFamilyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnerFamilyData
        fields = '__all__'

