from rest_framework import viewsets
from rest_framework.views import APIView
from core.models import Province, District, Municipality, HouseHoldData, AnimalDetailData, OwnerFamilyData
from api.serializers.core_serializers import HouseHoldDataSerializer, OwnerFamilyDataSerializer, \
    AnimalDetailDataSerializer
from django.core.serializers import serialize
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
import json
from django.db.models import Count, Q
from rest_framework.renderers import JSONRenderer
import ast

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
    filterset_fields = ['index', 'id','owner_age', 'ward', 'owner_age']

    # def filter_queryset(self, queryset):



class AnimalDetailViewSet(viewsets.ModelViewSet):
    serializer_class = AnimalDetailDataSerializer
    queryset = AnimalDetailData.objects.all()
    permission_classes = []


class FamilyDetailViewSet(viewsets.ModelViewSet):
    serializer_class = OwnerFamilyDataSerializer
    queryset = OwnerFamilyData.objects.all()
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'social_security_received']


class OverviewViewSet(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        data = []
        owner_detail = OwnerFamilyData.objects.all()
        house_hold = HouseHoldData.objects.all()
        total_house = HouseHoldData.objects.all().count()
        house_ownership_male = house_hold.filter(owner_sex='Male').count()
        house_ownership_female = house_hold.filter(owner_sex='Female').count()
        total_population = OwnerFamilyData.objects.all().count()
        male_population = owner_detail.filter(gender='Male').count()
        female_population = owner_detail.filter(gender='Female').count()
        house_received_social_security = owner_detail.filter(social_security_received='Yes').distinct('parent_index').count()
        house_not_received_social_security = total_house - house_received_social_security

        data.append({
            "total_house": total_house,
            "social_security_received": house_received_social_security,
            "social_security_not_received": house_not_received_social_security,
            "total_population": total_population,
            "male_population": male_population,
            "female_population": female_population,
            "house_ownership_male": house_ownership_male,
            "house_ownership_female": house_ownership_female,

        })

        return Response({'data':data})


class UniqueValuesViewSet(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        data = []

        ward_list = []
        edu_list = []
        age_group = ['0-20','20-40','40-60','60-80','80-100']
        house_hold = HouseHoldData.objects.all()
        owner_family = OwnerFamilyData.objects.all()
        wards_list = house_hold.values('ward').distinct('ward')
        education_list = owner_family.values('education_level').distinct('education_level')
        age_group_list = owner_family.values('age_group').distinct('age_group')
        parent_indexes = owner_family.values('parent_index').distinct('parent_index')
        # family_mem = HouseHoldData.objects.annotate(count=Count('house_hold_data')).distinct('count')
        print(parent_indexes)

        for house in house_hold:
            ward = house.ward
            if ward not in ward_list:
                ward_list.append(ward)
        print(ward_list)


        for house in owner_family:
            edu = house.education_level
            if edu not in edu_list:
                edu_list.append(edu)
        print(edu_list)


        # for house in owner_family:
        #     edu = house.age_group
        #     if edu not in age_group:
        #         age_group.append(edu)
        # print(age_group)

        print(age_group)


        num_of_family = []

        for parent in parent_indexes:
            num = OwnerFamilyData.objects.filter(parent_index=parent['parent_index']).count()
            if num in num_of_family:
                pass
            else:
                num_of_family.append(num)

        data.append({
            "ward": ward_list,
            "education": edu_list,
            "age group": age_group,
            "number of family": num_of_family
        })

        return Response({'data':data})



class FrontViewSet(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        wards = self.request.data.get('wards', None)
        education_lists = self.request.data.get('education_lists', None)
        age_group_list = self.request.data.get('age_group_list', None)
        family_members_list = self.request.data.get('family_members_list', None)

        if wards:
            wards_list = ast.literal_eval(wards)
            queryset = HouseHoldData.objects.filter(ward__in=wards_list)
            app_data = HouseHoldDataSerializer(queryset, many=True).data

        if education_lists:
            edu_list = ast.literal_eval(education_lists)
            queryset = HouseHoldData.objects.filter(owner_education__in=edu_list)
            app_data = HouseHoldDataSerializer(queryset, many=True).data

        if family_members_list:
            f_list = ast.literal_eval(family_members_list)
            queryset = HouseHoldData.objects.annotate(count=Count('house_hold_data')).filter(count__in=f_list)
            app_data = HouseHoldDataSerializer(queryset, many=True).data

        if age_group_list:
            age_list = ast.literal_eval(age_group_list)
            # print(age_list)
            age_m = []
            for i in age_list:
                age = i.split('-')
                age_m.append(age)

            # print(age_m[0][0])
            app_data = {}
            for age_value in age_m:
                # print (age_value[0])
                queryset = HouseHoldData.objects.filter(Q(owner_age__range=[age_value[0], age_value[1]]))
                data = HouseHoldDataSerializer(queryset, many=True).data
                app_data.update({'range_'+age_value[0]+'_'+age_value[1]:data})
                # queryset.append(query)


                # print(app_data)
            #     query = HouseHoldData.objects.filter(owner_age__range=[age[0],age[1]])
            #     queryset.append(query)


        if wards and education_lists:
            wards_list = ast.literal_eval(wards)
            edu_list = ast.literal_eval(education_lists)
            queryset = HouseHoldData.objects.filter(ward__in=wards_list, owner_education__in=edu_list)
            app_data = HouseHoldDataSerializer(queryset, many=True).data


        if wards and family_members_list:
            wards_list = ast.literal_eval(wards)
            f_list = ast.literal_eval(family_members_list)
            queryset = HouseHoldData.objects.filter(ward__in=wards_list).annotate(count=Count('house_hold_data')).filter(count__in=f_list)
            app_data = HouseHoldDataSerializer(queryset, many=True).data


        if wards and age_group_list:
            wards_list = ast.literal_eval(wards)
            age_list = ast.literal_eval(age_group_list)
            query = HouseHoldData.objects.filter(ward__in=wards_list)
            age_m = []
            for i in age_list:
                age = i.split('-')
                age_m.append(age)

            # print(age_m[0][0])
            app_data = {}
            for age_value in age_m:
                # print (age_value[0])
                queryset = query.filter(Q(owner_age__range=[age_value[0], age_value[1]]))
                data = HouseHoldDataSerializer(queryset, many=True).data
                app_data.update({'range_' + age_value[0] + '_' + age_value[1]: data})


        if education_lists and family_members_list:
            edu_list = ast.literal_eval(education_lists)
            f_list = ast.literal_eval(family_members_list)
            queryset = HouseHoldData.objects.filter(owner_education__in=edu_list).annotate(count=Count('house_hold_data')).filter(count__in=f_list)
            app_data = HouseHoldDataSerializer(queryset, many=True).data


        if education_lists and age_group_list:
            edu_list = ast.literal_eval(education_lists)
            age_list = ast.literal_eval(age_group_list)
            query = HouseHoldData.objects.filter(owner_education__in=edu_list)
            age_m = []
            for i in age_list:
                age = i.split('-')
                age_m.append(age)

            # print(age_m[0][0])
            app_data = {}
            for age_value in age_m:
                # print (age_value[0])
                queryset = query.filter(Q(owner_age__range=[age_value[0], age_value[1]]))
                data = HouseHoldDataSerializer(queryset, many=True).data
                app_data.update({'range_' + age_value[0] + '_' + age_value[1]: data})


        if family_members_list and age_group_list:
            f_list = ast.literal_eval(family_members_list)
            age_list = ast.literal_eval(age_group_list)
            query = HouseHoldData.objects.annotate(count=Count('house_hold_data')).filter(count__in=f_list)
            age_m = []
            for i in age_list:
                age = i.split('-')
                age_m.append(age)

            # print(age_m[0][0])
            app_data = {}
            for age_value in age_m:
                # print (age_value[0])
                queryset = query.filter(Q(owner_age__range=[age_value[0], age_value[1]]))
                data = HouseHoldDataSerializer(queryset, many=True).data
                app_data.update({'range_' + age_value[0] + '_' + age_value[1]: data})


        if wards and education_lists and family_members_list:
            wards_list = ast.literal_eval(wards)
            edu_list = ast.literal_eval(education_lists)
            f_list = ast.literal_eval(family_members_list)
            queryset = HouseHoldData.objects.filter(ward__in=wards_list, owner_education__in=edu_list).annotate(count=Count('house_hold_data')).filter(count__in=f_list)
            app_data = HouseHoldDataSerializer(queryset, many=True).data



        if education_lists and family_members_list and age_group_list:
            age_list = ast.literal_eval(age_group_list)
            edu_list = ast.literal_eval(education_lists)
            f_list = ast.literal_eval(family_members_list)
            query = HouseHoldData.objects.filter(owner_education__in=edu_list).annotate(count=Count('house_hold_data')).filter(count__in=f_list)
            age_m = []
            for i in age_list:
                age = i.split('-')
                age_m.append(age)

            # print(age_m[0][0])
            app_data = {}
            for age_value in age_m:
                # print (age_value[0])
                queryset = query.filter(Q(owner_age__range=[age_value[0], age_value[1]]))
                data = HouseHoldDataSerializer(queryset, many=True).data
                app_data.update({'range_' + age_value[0] + '_' + age_value[1]: data})


        if wards and family_members_list and age_group_list:
            age_list = ast.literal_eval(age_group_list)
            wards_list = ast.literal_eval(wards)
            f_list = ast.literal_eval(family_members_list)
            query = HouseHoldData.objects.filter(ward__in=wards_list).annotate(count=Count('house_hold_data')).filter(count__in=f_list)
            age_m = []
            for i in age_list:
                age = i.split('-')
                age_m.append(age)

            # print(age_m[0][0])
            app_data = {}
            for age_value in age_m:
                # print (age_value[0])
                queryset = query.filter(Q(owner_age__range=[age_value[0], age_value[1]]))
                data = HouseHoldDataSerializer(queryset, many=True).data
                app_data.update({'range_' + age_value[0] + '_' + age_value[1]: data})


        if wards and education_lists and age_group_list:
            age_list = ast.literal_eval(age_group_list)
            wards_list = ast.literal_eval(wards)
            edu_list = ast.literal_eval(education_lists)
            query = HouseHoldData.objects.filter(ward__in=wards_list, owner_education__in=edu_list)
            age_m = []
            for i in age_list:
                age = i.split('-')
                age_m.append(age)

            # print(age_m[0][0])
            app_data = {}
            for age_value in age_m:
                # print (age_value[0])
                queryset = query.filter(Q(owner_age__range=[age_value[0], age_value[1]]))
                data = HouseHoldDataSerializer(queryset, many=True).data
                app_data.update({'range_' + age_value[0] + '_' + age_value[1]: data})


        if wards and education_lists and family_members_list and age_group_list:
            f_list = ast.literal_eval(family_members_list)
            age_list = ast.literal_eval(age_group_list)
            wards_list = ast.literal_eval(wards)
            edu_list = ast.literal_eval(education_lists)
            query = HouseHoldData.objects.filter(ward__in=wards_list, owner_education__in=edu_list).annotate(count=Count('house_hold_data')).filter(count__in=f_list)
            age_m = []
            for i in age_list:
                age = i.split('-')
                age_m.append(age)

            # print(age_m[0][0])
            app_data = {}
            for age_value in age_m:
                # print (age_value[0])
                queryset = query.filter(Q(owner_age__range=[age_value[0], age_value[1]]))
                data = HouseHoldDataSerializer(queryset, many=True).data
                app_data.update({'range_' + age_value[0] + '_' + age_value[1]: data})






        # data = HouseHoldDataSerializer(queryset, many=True).data

        # json = JSONRenderer().render(data)


        return Response({'data':app_data})








