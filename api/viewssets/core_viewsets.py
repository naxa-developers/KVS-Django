from rest_framework import viewsets
from rest_framework.views import APIView
from core.models import Province, District, Municipality, HouseHoldData, AnimalDetailData, OwnerFamilyData
from api.serializers.core_serializers import HouseHoldDataSerializer, OwnerFamilyDataSerializer, \
    AnimalDetailDataSerializer, HouseHoldAlternativeSerializer
from django.core.serializers import serialize
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
import json
from django.db.models import Count, Q, Sum
from rest_framework.renderers import JSONRenderer
import ast
from core.generals import edu_matching, member_edu_matching
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# from django.db.models import Q
from rest_framework.parsers import FileUploadParser
from core.management.commands.house_upload_front import house_upload
# from core.generals import member_edu_matching
# import pandas as pd


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
    filterset_fields = ['id','index','owner_age', 'ward', 'owner_age']


    # def get_queryset(self, request):
    #     user = self.request.user
    #     return super(self).get_queryset()

    # def filter_queryset(self, queryset):



class AnimalDetailViewSet(viewsets.ModelViewSet):
    serializer_class = AnimalDetailDataSerializer
    queryset = AnimalDetailData.objects.all()
    permission_classes = []


    def get_queryset(self):
        house_index = self.request.query_params.get('house_index')
        queryset = AnimalDetailData.objects.filter(parent_index=house_index)

        return queryset


class FamilyDetailViewSet(viewsets.ModelViewSet):
    serializer_class = OwnerFamilyDataSerializer
    queryset = OwnerFamilyData.objects.all()
    permission_classes = []
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['id', 'social_security_received']


    def get_queryset(self):
        house_index = self.request.query_params.get('house_index')
        queryset = OwnerFamilyData.objects.filter(parent_index=house_index)

        return queryset


class OverviewViewSet(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        user = self.request.user
        roles = user.role.all()
        user_ward = []
        user_municipality = []
        user_district = []
        user_province = []
        for i in roles:
            if i.ward:
                user_ward.append(i.ward)
            if i.province:
                user_province.append(i.province.id)
            if i.municipality:
                user_municipality.append(i.municipality.id)
            if i.district:
                user_district.append(i.district.id)

        # creating dynamic q objects to query based on user ward, district and municipality and province
        q = Q()
        if user_ward:
            q &= Q(ward__in=user_ward)

        if user_municipality:
            q &= Q(municipality__in=user_municipality)

        if user_district:
            q &= Q(district__in=user_district)

        if user_province:
            q &= Q(province__in=user_province)

        data = []
        # owner_detail = OwnerFamilyData.objects.all()
        house_hold = HouseHoldData.objects.filter(q)
        # print(house_hold.count())
        total_house = house_hold.count()
        house_ownership_male = house_hold.filter(owner_sex='Male').count()
        house_ownership_female = house_hold.filter(owner_sex='Female').count()

        # total_population = OwnerFamilyData.objects.all().count()

        # owner_detail = []
        # for i in house_hold:
        #     house_id = i.id
        #     owner_fam = OwnerFamilyData.objects.filter(survey__id=house_id)
        #     for each in owner_fam:
        #         owner_detail.append(each)
        #
        # print(owner_detail.count())
        #
        # male_population = owner_detail.filter(gender='Male').count()
        # female_population = owner_detail.filter(gender='Female').count()
        # house_received_social_security = owner_detail.filter(social_security_received='Yes').distinct('parent_index').count()

        male = house_hold.annotate(male_count=Count('house_hold_data',filter=Q(house_hold_data__gender__icontains='male')),
                                           female_count=Count('house_hold_data',filter=Q(house_hold_data__gender__icontains='Female')),
                                           socail_count=Count('house_hold_data', filter=Q(house_hold_data__social_security_received='Yes')),
                                           ).aggregate(total_male=Sum('male_count'),total_feamle=Sum('female_count'),total_social=Sum('socail_count'))


        #
        # female = house_hold.annotate(count=Count('house_hold_data',filter=Q(house_hold_data__gender__icontains='Female'))).aggregate(Sum('count'))
        # house_received_social_security = house_hold.annotate(count=Count('house_hold_data',filter=Q(social_security_received='Yes'))).aggregate(Sum('count'))
        # # house_received_social_security = owner_detail.filter(social_security_received='Yes').distinct('parent_index').count()
        #
        male_population = male.get('total_male')
        female_population = male.get('total_feamle')
        total_population = male_population + female_population
        house_received_social_security = male.get('total_social')
        house_not_received_social_security = total_house - house_received_social_security

        edu_level_illiterate = house_hold.filter(owner_education__icontains='Illiterate').count()
        edu_level_literate = house_hold.filter(owner_education__icontains='Literate / ordinary').count()
        edu_level_seconday = house_hold.filter(owner_education__icontains='Secondary level').count()
        edu_level_basic_level_1 = house_hold.filter(owner_education__icontains='Basic Level 1').count()
        edu_level_graduate = house_hold.filter(owner_education__icontains='Graduate').count()

        #mother tongue
        mother_tongue_tharu = house_hold.filter(mother_tongue__icontains='Tharu').count()
        mother_tongue_tamang = house_hold.filter(mother_tongue__icontains='Tamang').count()
        mother_tongue_other = house_hold.filter(mother_tongue__icontains='Other').count()
        mother_tongue_newari = house_hold.filter(mother_tongue__icontains='Newari').count()
        mother_tongue_limbu = house_hold.filter(mother_tongue__icontains='Limbu').count()
        mother_tongue_rajbanshi = house_hold.filter(mother_tongue__icontains='Rajbanshi').count()
        mother_tongue_maithi = house_hold.filter(mother_tongue__icontains='Maithi').count()


        #main occupation
        occupation_agriculture = house_hold.filter(main_occupation__icontains='Agriculture').count()
        occupation_agriculture_wages = house_hold.filter(main_occupation__icontains='(Agricultural wages').count()
        occupation_daily_wages = house_hold.filter(main_occupation__icontains='Daily wages').count()
        occupation_government_service = house_hold.filter(main_occupation__icontains='Government service').count()
        occupation_non_government_service = house_hold.filter(main_occupation__icontains='Non-government service').count()
        occupation_foreign_employment = house_hold.filter(main_occupation__icontains='Foreign employment').count()
        occupation_entrepreneur = house_hold.filter(main_occupation__icontains='Entrepreneur').count()
        occupation_business = house_hold.filter(main_occupation__icontains='Business').count()
        occupation_labour_india = house_hold.filter(main_occupation__icontains='Seasonal labor, India').count()
        occupation_labour_nepal = house_hold.filter(main_occupation__icontains='Seasonal labor, Nepal').count()
        occupation_student = house_hold.filter(main_occupation__icontains='Student').count()
        occupation_other = house_hold.filter(main_occupation__icontains='Other').count()

        #num of family_member
        member_2_to_4 = house_hold.annotate(count=Count('house_hold_data')).filter(count__gte=2, count__lte=3).count()
        member_4_to_6 = house_hold.annotate(count=Count('house_hold_data')).filter(count__gte=4, count__lte=5).count()
        member_6_to_8 = house_hold.annotate(count=Count('house_hold_data')).filter(count__gte=6, count__lte=7).count()
        member_8_to_10 = house_hold.annotate(count=Count('house_hold_data')).filter(count__gte=8, count__lte=10).count()
        member_above_10 = house_hold.annotate(count=Count('house_hold_data')).filter(count__gte=11).count()


        data.append({
            "total_house": total_house,
            "social_security_received": house_received_social_security,
            "social_security_not_received": house_not_received_social_security,
            "total_population": total_population,
            "male_population": male_population,
            "female_population": female_population,
            "house_ownership_male": house_ownership_male,
            "house_ownership_female": house_ownership_female,
            "mother_tongue_tharu": mother_tongue_tharu,
            "mother_tongue_tamang":mother_tongue_tamang,
            "mother_tongue_other": mother_tongue_other,
            "mother_tongue_newari": mother_tongue_newari,
            "mother_tongue_limbu": mother_tongue_limbu,
            "mother_tongue_rajbanshi": mother_tongue_rajbanshi,
            "mother_tongue_maithi": mother_tongue_maithi,
            "occupation_agriculture": occupation_agriculture,
            "occupation_agriculture_wages": occupation_agriculture_wages,
            "occupation_daily_wages": occupation_daily_wages,
            "occupation_government_service": occupation_government_service,
            "occupation_non_government_service": occupation_non_government_service,
            "occupation_foreign_employment": occupation_foreign_employment,
            "occupation_entrepreneur": occupation_entrepreneur,
            "occupation_business": occupation_business,
            "occupation_labour_india": occupation_labour_india,
            "occupation_foreign_labour_nepal": occupation_labour_nepal,
            "occupation_student": occupation_student,
            "occupation_other": occupation_other,
            "member_2_to_4": member_2_to_4,
            "member_4_to_6": member_4_to_6,
            "member_6_to_8": member_6_to_8,
            "member_8_to_10": member_8_to_10,
            "member_above_10": member_above_10,
            "edu_level_illiterate": edu_level_illiterate,
            "edu_level_literate": edu_level_literate,
            "edu_level_seconday": edu_level_seconday,
            "edu_level_basic_level_1": edu_level_basic_level_1,
            "edu_level_graduate": edu_level_graduate,

        })

        return Response({'data':data})

#front filter api


class FddViewSet(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        ward = self.request.data.get('ward')
        social_security_received = self.request.data.get('social_security_received')
        citizen = self.request.data.get('senior_citizen')
        education_list = self.request.data.get('education')
        flood = self.request.data.get('flood')
        user = self.request.user
        roles = user.role.all()
        user_ward = []
        user_municipality = []
        user_district = []
        user_province = []
        print(user_ward)
        for i in roles:
            if i.ward:
                user_ward.append(i.ward)
            if i.province:
                user_province.append(i.province.id)
            if i.municipality:
                user_municipality.append(i.municipality.id)
            if i.district:
                user_district.append(i.district.id)


        #creating dynamic q objects to query based on user ward, district and municipality and province
        q = Q()
        if user_ward:
            q &= Q(ward__in=user_ward)

        if user_municipality:
            q &= Q(municipality__in=user_municipality)


        if user_district:
            q &= Q(district__in=user_district)


        if user_province:
            q &= Q(province__in=user_province)



        query = HouseHoldData.objects.filter(q)
        # print('abc')
        # print(query.count())
        # print('abc')

        if ward and flood and social_security_received and citizen and education_list:
            print('vvv')
            edu_list = ast.literal_eval(education_list)
            query = edu_matching(edu_list, query)
            index = []
            wards_list = ast.literal_eval(ward)
            family = OwnerFamilyData.objects.filter(falling_under_social_security_criteria__icontains=citizen,
                                                    social_security_received__icontains=social_security_received)
            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)
            queryset = query.filter(flood_prone__icontains=flood, ward__in=wards_list, index__in=index)

        elif ward and flood and social_security_received and citizen:
            print('ward and social_security_received and citizen and flood')

            index = []
            wards_list = ast.literal_eval(ward)
            family = OwnerFamilyData.objects.filter(falling_under_social_security_criteria__icontains=citizen,
                                                    social_security_received__icontains=social_security_received)
            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)
            queryset = query.filter(flood_prone__icontains=flood, ward__in=wards_list, index__in=index)

        elif ward and flood and social_security_received and education_list:
            print('ward and social_security_received and education_list and flood')

            edu_list = ast.literal_eval(education_list)
            query = edu_matching(edu_list, query)
            index = []
            wards_list = ast.literal_eval(ward)
            family = OwnerFamilyData.objects.filter(social_security_received__icontains=social_security_received)
            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)
            queryset = query.filter(flood_prone__icontains=flood, ward__in=wards_list, index__in=index)

        elif ward and flood and citizen and education_list:
            print('ward and citizen and education_list and flood')

            edu_list = ast.literal_eval(education_list)
            query = edu_matching(edu_list, query)
            index = []
            wards_list = ast.literal_eval(ward)
            family = OwnerFamilyData.objects.filter(falling_under_social_security_criteria__icontains=citizen)
            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)
            queryset = query.filter(flood_prone__icontains=flood, ward__in=wards_list, index__in=index)

        elif flood and social_security_received and education_list and citizen:
            print('flood and social_security_received and education_list and citizen')
            edu_list = ast.literal_eval(education_list)
            query = edu_matching(edu_list, query)
            index = []

            family = OwnerFamilyData.objects.filter(falling_under_social_security_criteria__icontains=citizen,
                                                    social_security_received__icontains=social_security_received)

            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)

            queryset = query.filter(flood_prone__icontains=flood, index__in=index)

        elif ward and flood and social_security_received:
            print('ward and flood and social_security_received')
            index = []
            wards_list = ast.literal_eval(ward)
            family = OwnerFamilyData.objects.filter(social_security_received__icontains=social_security_received)
            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)
            queryset = query.filter(flood_prone__icontains=flood, ward__in=wards_list, index__in=index)

        elif ward and flood and citizen:
            print("ward and flood and citizen")
            index = []
            wards_list = ast.literal_eval(ward)
            family = OwnerFamilyData.objects.filter(falling_under_social_security_criteria__icontains=citizen)
            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)
            queryset = query.filter(index__in=index, flood_prone__icontains=flood, ward__in=wards_list)

        elif ward and flood and education_list:
            print("ward and flood and education_list")

            wards_list = ast.literal_eval(ward)
            edu_list = ast.literal_eval(education_list)
            query = edu_matching(edu_list, query)

            queryset = query.filter(ward__in=wards_list, flood_prone__icontains=flood)

        elif flood and social_security_received and citizen:
            print('flood and social_security_received and citizen')
            index = []
            family = OwnerFamilyData.objects.filter(falling_under_social_security_criteria__icontains=citizen,
                                                    social_security_received__icontains=social_security_received)
            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)
            queryset = query.filter(index__in=index, flood_prone__icontains=flood)

        elif flood and citizen and education_list:
            print('flood and education_list and citizen')

            edu_list = ast.literal_eval(education_list)
            query = edu_matching(edu_list, query)

            index = []
            family = OwnerFamilyData.objects.filter(falling_under_social_security_criteria__icontains=citizen)
            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)
            queryset = query.filter(index__in=index, flood_prone__icontains=flood)

        elif social_security_received and citizen and education_list:
            print('social_security_received and education_list and citizen')

            edu_list = ast.literal_eval(education_list)
            query = edu_matching(edu_list, query)
            index = []
            family = OwnerFamilyData.objects.filter(falling_under_social_security_criteria__icontains=citizen,
                                                    social_security_received__icontains=social_security_received)
            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)
            queryset = query.filter(index__in=index)

        elif ward and flood and social_security_received:
            print('ward and flood and social_security_received')
            index = []
            wards_list = ast.literal_eval(ward)
            family = OwnerFamilyData.objects.filter(social_security_received__icontains=social_security_received)
            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)
            queryset = query.filter(flood_prone__icontains=flood, ward__in=wards_list, index__in=index)

        elif ward and flood and citizen:
            print("ward and flood and citizen")
            index = []
            wards_list = ast.literal_eval(ward)
            family = OwnerFamilyData.objects.filter(falling_under_social_security_criteria__icontains=citizen)
            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)
            queryset = query.filter(index__in=index, flood_prone__icontains=flood, ward__in=wards_list)

        elif ward and flood and education_list:
            print("ward and flood and education_list")

            wards_list = ast.literal_eval(ward)
            edu_list = ast.literal_eval(education_list)
            query = edu_matching(edu_list, query)

            queryset = query.filter(ward__in=wards_list, flood_prone__icontains=flood)

        elif flood and social_security_received and citizen:
            print('flood and social_security_received and citizen')
            index = []
            family = OwnerFamilyData.objects.filter(falling_under_social_security_criteria__icontains=citizen,
                                                    social_security_received__icontains=social_security_received)
            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)
            queryset = query.filter(index__in=index, flood_prone__icontains=flood)

        elif flood and citizen and education_list:
            print('flood and education_list and citizen')

            edu_list = ast.literal_eval(education_list)
            query = edu_matching(edu_list, query)

            index = []
            family = OwnerFamilyData.objects.filter(falling_under_social_security_criteria__icontains=citizen)
            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)
            queryset = query.filter(index__in=index, flood_prone__icontains=flood)

        elif social_security_received and citizen and education_list:
            print('social_security_received and education_list and citizen')

            edu_list = ast.literal_eval(education_list)
            query = edu_matching(edu_list, query)
            index = []
            family = OwnerFamilyData.objects.filter(falling_under_social_security_criteria__icontains=citizen,
                                                    social_security_received__icontains=social_security_received)
            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)
            queryset = query.filter(index__in=index)

        elif ward and flood:
            print('ward and flood')
            print('ww ff')
            wards_list = ast.literal_eval(ward)
            queryset = query.filter(flood_prone__icontains=flood, ward__in=wards_list)

        elif ward and social_security_received:
            print('ward and social_security_received')
            wards_list = ast.literal_eval(ward)
            index = []
            family = OwnerFamilyData.objects.filter(social_security_received__icontains=social_security_received)
            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)
            queryset = query.filter(index__in=index, ward__in=wards_list)

        elif ward and citizen:
            print('ward and citizen')
            wards_list = ast.literal_eval(ward)
            index = []
            family = OwnerFamilyData.objects.filter(falling_under_social_security_criteria__icontains=citizen)
            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)
            queryset = query.filter(index__in=index, ward__in=wards_list)

        elif ward and education_list:
            print('ward and education_list')
            edu_list = ast.literal_eval(education_list)
            wards_list = ast.literal_eval(ward)
            query = edu_matching(edu_list, query)
            queryset = query.filter(ward__in=wards_list)

        elif flood and social_security_received:
            print('flood and social_security_received')
            index = []
            family = OwnerFamilyData.objects.filter(social_security_received__icontains=social_security_received)
            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)
            queryset = query.filter(index__in=index, flood_prone__icontains=flood)

        elif flood and citizen:
            print('flood and citizen')

            index = []
            family = OwnerFamilyData.objects.filter(falling_under_social_security_criteria__icontains=citizen)
            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)
            queryset = query.filter(index__in=index, flood_prone__icontains=flood)

        elif flood and education_list:
            print('flood and education_list')
            edu_list = ast.literal_eval(education_list)
            query = edu_matching(edu_list, query)
            queryset = query.filter(flood_prone__icontains=flood)


        elif social_security_received and citizen:
            print('social_security_received and citizen')

            index = []
            family = OwnerFamilyData.objects.filter(falling_under_social_security_criteria__icontains=citizen, social_security_received__icontains=social_security_received)
            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)
            queryset = query.filter(index__in=index)

        elif social_security_received and education_list:
            print('social_security_received and education_list')

            edu_list = ast.literal_eval(education_list)
            query = edu_matching(edu_list, query)

            # query = edu_matching(edu_list)
            index = []
            family = OwnerFamilyData.objects.filter(social_security_received__icontains=social_security_received)
            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)
            queryset = query.filter(index__in=index)

        elif citizen and education_list:
            print('citizen and education_list')

            edu_list = ast.literal_eval(education_list)
            query = edu_matching(edu_list, query)
            index = []
            family = OwnerFamilyData.objects.filter(falling_under_social_security_criteria__icontains=citizen)
            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)
            queryset = query.filter(index__in=index)


        elif ward:
            print('ward')
            wards_list = ast.literal_eval(ward)
            queryset = query.filter(ward__in=wards_list)


        elif flood:
            print(' flood')

            queryset = query.filter(flood_prone__icontains=flood)


        elif social_security_received:
            print('social_security_received')
            index = []
            family = OwnerFamilyData.objects.filter(social_security_received__icontains=social_security_received)
            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)
            queryset = query.filter(index__in=index)


        elif citizen:
            print('citizen')
            index = []
            family = OwnerFamilyData.objects.filter(falling_under_social_security_criteria__icontains=citizen)

            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)
            queryset = query.filter(index__in=index)
            print(queryset.count())


        elif education_list:
            print('edu')
            edu_list = ast.literal_eval(education_list)
            queryset = edu_matching(edu_list, query)


        else:
            queryset = query

        data = HouseHoldAlternativeSerializer(queryset, many=True).data

        return Response({'data': data})


class FamilyMemberFilterViewSet(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self,request):
        ward = self.request.data.get('ward')
        social_security_received = self.request.data.get('social_security_received')
        citizen = self.request.data.get('senior_citizen')
        education_list = self.request.data.get('education')
        flood = self.request.data.get('flood')
        user = self.request.user
        roles = user.role.all()
        user_ward = []
        user_municipality = []
        user_district = []
        user_province = []
        print(user_ward)
        for i in roles:
            if i.ward:
                user_ward.append(i.ward)
            if i.province:
                user_province.append(i.province.id)
            if i.municipality:
                user_municipality.append(i.municipality.id)
            if i.district:
                user_district.append(i.district.id)

        # creating dynamic q objects to query based on user ward, district and municipality and province
        q = Q()
        if user_ward:
            q &= Q(survey__ward__in=user_ward)

        if user_municipality:
            q &= Q(survey__municipality__in=user_municipality)

        if user_district:
            q &= Q(survey__district__in=user_district)

        if user_province:
            q &= Q(survey__province__in=user_province)

        query = OwnerFamilyData.objects.filter(q)

        if ward and flood and social_security_received and citizen and education_list:
            print('abc')
            edu_list = ast.literal_eval(education_list)
            wards_list = ast.literal_eval(ward)

            query = member_edu_matching(edu_list, query)
            queryset = query.filter(survey__ward__in=wards_list,
                                    social_security_received__icontains=social_security_received,
                                    survey__flood_prone__icontains=flood,
                                    falling_under_social_security_criteria__icontains=citizen
                                    )

        elif ward and flood and social_security_received and citizen:
            print('war flood social and citi')
            wards_list = ast.literal_eval(ward)
            queryset = query.filter(survey__ward__in=wards_list,
                                    social_security_received__icontains=social_security_received,
                                    survey__flood_prone__icontains=flood,
                                    falling_under_social_security_criteria__icontains=citizen
                                    )

        elif ward and flood and social_security_received and education_list:
            print('war floo soc edu')
            edu_list = ast.literal_eval(education_list)
            wards_list = ast.literal_eval(ward)
            query = member_edu_matching(edu_list, query)
            queryset = query.filter(survey__ward__in=wards_list,
                                    social_security_received__icontains=social_security_received,
                                    survey__flood_prone__icontains=flood,
                                    )

        elif ward and flood and citizen and education_list:
            print(' w f c e')
            edu_list = ast.literal_eval(education_list)
            wards_list = ast.literal_eval(ward)
            query = member_edu_matching(edu_list, query)
            queryset = query.filter(survey__ward__in=wards_list,
                                    survey__flood_prone__icontains=flood,
                                    falling_under_social_security_criteria__icontains=citizen
                                    )

        elif flood and social_security_received and education_list and citizen:
            print('f s e c')
            edu_list = ast.literal_eval(education_list)
            query = member_edu_matching(edu_list, query)
            queryset = query.filter(survey__flood_prone__icontains=flood,
                                    social_security_received__icontains=social_security_received,
                                    falling_under_social_security_criteria__icontains=citizen
                                    )

        elif ward and flood and social_security_received:
            print('w f s')
            wards_list = ast.literal_eval(ward)
            queryset = query.filter(survey__ward__in=wards_list,
                                    survey__flood_prone__icontains=flood,
                                    social_security_received__icontains=social_security_received
                                    )

        elif ward and flood and citizen:
            print('w f c')
            wards_list = ast.literal_eval(ward)
            queryset = query.filter(survey__ward__in=wards_list,
                                    survey__flood_prone__icontains=flood,
                                    falling_under_social_security_criteria__icontains=citizen
                                    )

        elif ward and flood and education_list:
            print(' w f  e')
            edu_list = ast.literal_eval(education_list)
            wards_list = ast.literal_eval(ward)
            query = member_edu_matching(edu_list, query)
            queryset = query.filter(survey__ward__in=wards_list,
                                    survey__flood_prone__icontains=flood,
                                    )

        elif flood and social_security_received and citizen:
            print('aaa')
            queryset = query.filter(
                                    social_security_received__icontains=social_security_received,
                                    survey__flood_prone__icontains=flood,
                                    falling_under_social_security_criteria__icontains=citizen
                                    )

        elif flood and citizen and education_list:
            print('f c e')
            edu_list = ast.literal_eval(education_list)
            query = member_edu_matching(edu_list, query)

            queryset = query.filter(
                survey__flood_prone__icontains=flood,
                falling_under_social_security_criteria__icontains=citizen
            )

        elif social_security_received and citizen and education_list:
            print('s c e')
            edu_list = ast.literal_eval(education_list)
            query = member_edu_matching(edu_list, query)

            queryset = query.filter(
                social_security_received__icontains=social_security_received,
                falling_under_social_security_criteria__icontains=citizen
            )

        elif ward and flood and social_security_received:
            print('w f s')
            wards_list = ast.literal_eval(ward)

            queryset = query.filter(
                survey__ward__in=wards_list,
                survey__flood_prone__icontains=flood,
                social_security_received__icontains=social_security_received,
            )

        elif ward and flood:
            print('ward and flood')
            wards_list = ast.literal_eval(ward)

            queryset = query.filter(
                survey__ward__in=wards_list,
                survey__flood_prone__icontains=flood,
            )

        elif ward and social_security_received:
            print('ward and social security')
            wards_list = ast.literal_eval(ward)

            queryset = query.filter(
                survey__ward__in=wards_list,
                social_security_received__icontains=social_security_received,
            )

        elif ward and citizen:
            print('ward and citizen')
            wards_list = ast.literal_eval(ward)

            queryset = query.filter(
                survey__ward__in=wards_list,
                falling_under_social_security_criteria__icontains=citizen
            )

        elif ward and education_list:
            print('ward and education list')
            wards_list = ast.literal_eval(ward)
            edu_list = ast.literal_eval(education_list)
            query = member_edu_matching(edu_list, query)

            queryset = query.filter(survey__ward__in=wards_list,)

        elif flood and social_security_received:
            print('flood and social scurity')
            queryset = query.filter(
                social_security_received__icontains=social_security_received,
                survey__flood_prone__icontains=flood
            )

        elif flood and citizen:
            print('flood and citizen')
            queryset = query.filter(
                survey__flood_prone__icontains=flood,
                falling_under_social_security_criteria__icontains=citizen
            )

        elif flood and education_list:
            print('flood education list')
            edu_list = ast.literal_eval(education_list)
            query = member_edu_matching(edu_list, query)

            queryset = query.filter(survey__flood_prone__icontains=flood)

        elif social_security_received and citizen:
            print('social_security and citizen')

            queryset = query.filter(
                social_security_received__icontains=social_security_received,
                falling_under_social_security_criteria__icontains=citizen
            )

        elif social_security_received and education_list:
            edu_list = ast.literal_eval(education_list)
            query = member_edu_matching(edu_list, query)
            queryset = query.filter(social_security_received__icontains=social_security_received)

        elif citizen and education_list:
            print('citizen and education list')
            edu_list = ast.literal_eval(education_list)
            query = member_edu_matching(edu_list, query)

            queryset = query.filter(falling_under_social_security_criteria__icontains=citizen)

        elif flood:
            print('flood')
            queryset = query.filter(survey__flood_prone__icontains=flood)

        elif social_security_received:
            print('social_security_received')
            queryset = query.filter(social_security_received__icontains=social_security_received)

        elif citizen:
            print('citizen')
            queryset = query.filter(falling_under_social_security_criteria__icontains=citizen)

        elif education_list:
            print('education list')
            edu_list = ast.literal_eval(education_list)
            queryset = member_edu_matching(edu_list, query)

        elif ward:
            print('ward')
            wards_list = ast.literal_eval(ward)
            queryset = query.filter(survey__ward__in=wards_list)

        else:
            print('bb')
            queryset = query

        data = OwnerFamilyDataSerializer(queryset, many=True).data

        return Response({'data': data})




class UniqueValuesViewSet(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        data = []

        flood = ['Yes','No']
        social_security_received = ['Yes', 'No']
        senior_citizen = ['Yes', 'No']
        edu_list = []
        education_list = HouseHoldData.objects.values('owner_education').distinct()
        ward = HouseHoldData.objects.values('ward').distinct()
        ward_list = []

        ward_count = ward.count()
        print(ward_count)
        for i in range(0, ward_count):
            ward_list.append(ward[i]['ward'])


        count= education_list.count()

        for i in range(0,count):
            if education_list[i]['owner_education'] != 'nan':
                edu_list.append(education_list[i]['owner_education'])

        # print(education_list[0]['education_level'])




        # for i in education_list:
        #     education_choice = education_list[i]['education_level']
        #     print(education_choice)
        #     # edu_list.append(education_choice)

        # print(edu_list)

        # for parent in parent_indexes:
        #     num = OwnerFamilyData.objects.filter(parent_index=parent['parent_index']).count()
        #     if num in num_of_family:
        #         pass
        #     else:
        #         num_of_family.append(num)
        #
        data.append({
            "ward": ward_list,
            "education": edu_list,
            "senior_citizen": senior_citizen,
            "social_security_received": social_security_received,
            "flood": flood,
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



class MoreViewSet(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        data = self.request.data

        # if field:
        #     queryset = HouseHoldData.objects.filter(field__icontains='Agriculture')
        #     data = HouseHoldDataSerializer(queryset, many=True).data
        user = self.request.user
        roles = user.role.all()
        user_ward = []
        user_municipality = []
        user_district = []
        user_province = []
        print(user_ward)
        for i in roles:
            if i.ward:
                user_ward.append(i.ward)
            if i.province:
                user_province.append(i.province.id)
            if i.municipality:
                user_municipality.append(i.municipality.id)
            if i.district:
                user_district.append(i.district.id)

        # creating dynamic q objects to query based on user ward, district and municipality and province
        q = Q()
        if user_ward:
            q &= Q(ward__in=user_ward)

        if user_municipality:
            q &= Q(municipality__in=user_municipality)

        if user_district:
            q &= Q(district__in=user_district)

        if user_province:
            q &= Q(province__in=user_province)

        query = HouseHoldData.objects.filter(q)

        if data['field'] == 'animals':
            index = []
            b = ast.literal_eval(data['value'])
            for i in b:
                animal_data = AnimalDetailData.objects.filter(animal_type__icontains=i)

            for i in animal_data:
                if i.parent_index not in index:
                    index.append(i.parent_index)

            household = query.objects.filter(id__in=index)

        else:
            b = ast.literal_eval(data['value'])
            datas = []
            for i in b:
                kwargs = {
                    '{0}__{1}'.format(data['field'], 'icontains'): i,
                }
                # household = household.filter(**kwargs)
                house = query.filter(**kwargs)
                print(house.count())
                for j in house:
                    if j not in datas:
                        datas.append(j)
            household = datas
        data = HouseHoldAlternativeSerializer(household, many=True).data

        return Response({'data': data})



class MoreDropDownViewSet(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        education_choice = []

        hazard_choices = HouseHoldData.objects.values('hazard_type').distinct()
        education_list = HouseHoldData.objects.values('owner_education').distinct()
        ethnicity = HouseHoldData.objects.values('owner_caste').distinct()
        mother_tongue_list = HouseHoldData.objects.values('mother_tongue').distinct()
        religion_list = HouseHoldData.objects.values('religion').distinct()
        main_occupation_list = HouseHoldData.objects.values('main_occupation').distinct()
        land_ownership_list = HouseHoldData.objects.values('owned_land_area').distinct()
        market_distance_list = HouseHoldData.objects.values('distance_to_nearest_market').distinct()
        # house_type_list = HouseHoldData.objects.values('house_type').distinct()

        distance_to_nearest_market_choice = []
        ethnicity_choice = []
        mother_tongue_choice = []
        religion_choice = []
        land_ownership_choice = []

        # education_choice = ['Literate / ', 'Illiterate', ]

        count = education_list.count()

        for i in range(0, count):
            if education_list[i]['owner_education'] != 'nan':
                education_choice.append(education_list[i]['owner_education'])

        e_count = ethnicity.count()
        for i in range(0, e_count):
            if ethnicity[i]['owner_caste'] != 'nan':
                ethnicity_choice.append(ethnicity[i]['owner_caste'])


        m_count = mother_tongue_list.count()
        for i in range(0, m_count):
            if mother_tongue_list[i]['mother_tongue'] != 'nan':
                mother_tongue_choice.append(mother_tongue_list[i]['mother_tongue'])


        r_count = religion_list.count()
        for i in range(0, r_count):
            if religion_list[i]['religion'] != 'nan':
                religion_choice.append(religion_list[i]['religion'])

        l_count = land_ownership_list.count()
        for i in range(0, l_count):
            if land_ownership_list[i]['owned_land_area'] != 'nan':
                land_ownership_choice.append(land_ownership_list[i]['owned_land_area'])

        m_count = market_distance_list.count()
        for i in range(0, m_count):
            if market_distance_list[i]['distance_to_nearest_market'] != 'nan':
                distance_to_nearest_market_choice.append(market_distance_list[i]['distance_to_nearest_market'])


        # h_count = house_type_list.count()
        # for i in range(0, h_count):
        #     if house_type_list[i]['house_type'] != 'nan':
        #         house_type_choice.append(house_type_list[i]['house_type'])

        disaster_information_medium_choice = ['Hoarding board', 'Local people', 'Radio/T.V', 'Newspaper', 'Related body',
                                              'Other', 'haven’t received any information'
                                              ]
        insurance_choice = ['Yes', 'No']
        food_choice = ['Pulses', 'Rice', 'Roti', 'Vegetable', 'Fish', 'Meat', 'Greens', 'Milk', 'oil', 'sag']
        animals = ['Buffalo', 'Cow', 'Goat', 'Dog', 'Duck', 'Fish', 'Hen', 'Male Buffalo', 'Ox', 'Pigeon', 'Pig', 'Fish']
        facility_choice = ['Radio', 'Television', 'Mobile/Telephone', 'Oven','Fridge', 'Washing Machine', 'Other']
        house_map_registered_choice = ['Yes', 'No', 'Don\'t know']
        water_source_choice = ['Public Tap-stand', 'Private Tap-stand', 'spring source', 'Tubewell', 'Well/Spout',
                               'River/Rivulet', 'Others']
        fuel_type_choice = ['Kerosene', 'Wood/Coal', 'LP Gas', 'Electrical', 'Bio-gas', 'Other']
        owner_sex_choice = ['Male', 'Female', 'Both']
        toilet_type_choice = ['Pit hole', 'Ring', 'Bio-gas attached', 'Septic tank', 'other']
        house_type_choice = ['Permanent house with CGI roof', 'Permanent house with slate roof',
                             'Permanent house with RCC structure', 'Semi-permanent house', 'Temporary house with CGI roof',
                             'Temporary house with thatched/mud roof']
        occupation_choice = ['Agriculture', 'Agricultural wages', 'Daily wages', 'Government service',
                             'Non-government service', 'Foreign employment', 'Entrepreneur', 'Business',
                             'Student', 'Other']
        hazard_choice = ['Flood', 'Landslide', 'Fire', 'Road', 'Snake', 'Animal', 'Lightening', 'Black', 'Cold wind']
        technical_choice = ['Doctor', 'Nurse', 'Engineer', 'carpenter', 'Knocker/carpenter', 'plumber', 'Sub-engineer',
                            'HA/Lab Asst', 'electrician']
        category = [{'hazard_type':hazard_choice ,'owner_education':education_choice, 'manpower_type':technical_choice,
                     'owner_caste':ethnicity_choice, 'mother_tongue':mother_tongue_choice, 'religion':religion_choice,
                     'main_occupation': occupation_choice, 'owner_sex': owner_sex_choice,
                     'house_type':house_type_choice, 'water_sources': water_source_choice,
                     'toilet_type':toilet_type_choice, 'fuel_type': fuel_type_choice,
                     'house_map_registered': house_map_registered_choice,
                     'owned_land_area': land_ownership_choice,
                     'facilities_type': facility_choice,
                    'distance_to_nearest_market': distance_to_nearest_market_choice,
                     'animals': animals, 'food_type':food_choice,
                     'disaster_information_medium':disaster_information_medium_choice,
                     'insurance': insurance_choice,
                     }]




        # all_fields = HouseHoldData._meta.get_fields()
        # for i in all_fields:
        #     print(i)

        return Response({'data':category})


class HighlightDataViewSet(APIView):
    permission_classes = []

    def get(self,request):
        data = []
        query = OwnerFamilyData.objects.all()
        house_hold_count = HouseHoldData.objects.all().count()
        num_of_people = query.count()
        q = Q()


        q = Q(age_group__icontains='less than 5 years') | Q(age_group__icontains='5-15 years')

        num_of_children = query.filter(q).count()

        senior_citizen = query.filter(falling_under_social_security_criteria__icontains='senior citizen').count()

        district = HouseHoldData.objects.values('district').distinct().count()

        data.append({
            'house_hold_count': house_hold_count,
            'num_of_people': num_of_people,
            'num_of_children': num_of_children,
            'senior_citizen': senior_citizen,
            'district': district
        })

        return Response({'data':data})


class CSVFileUploadHouseHold(APIView):
    # parser_classes = [FileUploadParser]

    def post(self, request):
        file = request.data['file']
        # print(file)
        # df = pd.read_csv(file)

        house = house_upload(file)

        return Response('Successfully uploaded file')

        # if file:
        #     house_upload_front(file)
        #     return Response('Successfully uploaded file')
        #
        # else:
        #     return Response('Please select the file ')





















