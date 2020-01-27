from rest_framework import serializers
from front.models import Header, AboutProject, Contact, OurMission, OverallSystemFeatures


class HeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Header
        fields = '__all__'


class AboutProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutProject
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class OurMissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OurMission
        fields = '__all__'


class OverallSystemFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverallSystemFeatures
        fields = '__all__'