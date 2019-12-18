from core.models import Province, District, Municipality, Survey, FamilyMembers, AnimalDetail
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


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'


class FamilyMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyMembers
        fields = '__all__'


class AnimalDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalDetail
        fields = '__all__'

