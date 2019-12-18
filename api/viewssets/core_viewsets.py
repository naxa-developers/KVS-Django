from rest_framework import viewsets
from rest_framework.views import APIView
from core.models import Province, District, Municipality, Survey, AnimalDetail, FamilyMembers
from api.serializers.core_serializers import ProvinceSerializer, DistrictSerializer, MunicipalitySerializer, \
    SurveySerializer, AnimalDetailSerializer, FamilyMembersSerializer
from django.core.serializers import serialize
from rest_framework.response import Response
import json



class ProvinceGeojsonViewSet(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        province_id = self.request.query_params.get('id')
        if province_id:
            serializers = serialize('geojson',
                                    Province.objects.filter(id=province_id),
                                    geometry_field='boundary',
                                    fields=('pk', 'name', 'code'))
        else:
            serializers = serialize('geojson',
                                    Province.objects.all(),
                                    geometry_field='boundary',
                                    fields=('pk', 'name', 'code'))
        province_geo_json = json.loads(serializers)
        return Response(province_geo_json)


class DistrictGeojsonViewSet(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        district_id = self.request.query_params.get('id')
        if district_id:
            serializers = serialize('geojson',
                                    District.objects.filter(id=district_id),
                                    geometry_field='boundary',
                                    fields=('pk', 'name', 'province'))
        else:
            serializers = serialize('geojson',
                                    District.objects.all(),
                                    geometry_field='boundary',
                                    fields=('pk', 'name', 'province'))
        district_geo_json = json.loads(serializers)
        return Response(district_geo_json)


class MunicipalityGeojsonViewSet(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        municipality_id = self.request.query_params.get('id')
        if municipality_id:
            serializers = serialize('geojson', Municipality.objects.filter(
                id=municipality_id), geometry_field='boundary',
                                    fields=('pk', 'name', 'district'))
        else:
            serializers = serialize('geojson', Municipality.objects.all(),
                                    geometry_field='boundary',
                                    fields=('pk', 'name', 'district'))
        municipality_geo_json = json.loads(serializers)
        return Response(municipality_geo_json)


class SurveyViewSet(viewsets.ModelViewSet):
    serializer_class = SurveySerializer
    queryset = Survey.objects.all()
    permission_classes = []


class AnimalViewSet(viewsets.ModelViewSet):
    serializer_class = AnimalDetailSerializer
    queryset = AnimalDetail.objects.all()
    permission_classes = []


class FamilyMemberViewSet(viewsets.ModelViewSet):
    serializer_class = FamilyMembersSerializer
    queryset = FamilyMembers.objects.all()
    permission_classes = []
