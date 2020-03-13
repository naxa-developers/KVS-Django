from rest_framework import viewsets
from front.models import Header, OverallSystemFeatures, OurMission, Contact, AboutProject
from api.serializers.front_serializers import HeaderSerializer, OverallSystemFeaturesSerializer, ContactSerializer, \
    OurMissionSerializer, AboutProjectSerializer


class HeaderViewSet(viewsets.ModelViewSet):
    serializer_class = HeaderSerializer
    queryset = Header.objects.all()
    permission_classes = []


class OverallSystemFeaturesViewSet(viewsets.ModelViewSet):
    serializer_class = OverallSystemFeaturesSerializer
    queryset = OverallSystemFeatures.objects.all()
    permission_classes = []


class OurMissionViewSet(viewsets.ModelViewSet):
    serializer_class = OurMissionSerializer
    queryset = OurMission.objects.all()
    permission_classes = []


class AboutProjectViewSet(viewsets.ModelViewSet):
    serializer_class = AboutProjectSerializer
    queryset = AboutProject.objects.all()
    permission_classes = []


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()
    permission_classes = []



