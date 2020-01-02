from rest_framework import viewsets
from rest_framework.views import APIView
from core.models import Province, District, Municipality, HouseHoldData, AnimalDetailData, OwnerFamilyData
from api.serializers.core_serializers import HouseHoldDataSerializer, OwnerFamilyDataSerializer, \
    AnimalDetailDataSerializer
from django.core.serializers import serialize
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
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


class HouseHoldViewSet(viewsets.ModelViewSet):
    serializer_class = HouseHoldDataSerializer
    queryset = HouseHoldData.objects.all()
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['index', 'id','owner_age',]


class AnimalDetailViewSet(viewsets.ModelViewSet):
    serializer_class = AnimalDetailDataSerializer
    queryset = AnimalDetailData.objects.all()
    permission_classes = []


class FamilyDetailViewSet(viewsets.ModelViewSet):
    serializer_class = OwnerFamilyDataSerializer
    queryset = OwnerFamilyData.objects.all()
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'received_social_security']


