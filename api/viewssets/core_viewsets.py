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
from core.generals import edu_matching

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
    filterset_fields = ['index','owner_age', 'ward', 'owner_age']


    # def get_queryset(self, request):
    #     user = self.request.user
    #     return super(self).get_queryset()

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


        edu_level_illiterate = HouseHoldData.objects.filter(owner_education__icontains='Illiterate').count()
        edu_level_literate = HouseHoldData.objects.filter(owner_education__icontains='Literate / ordinary').count()
        edu_level_seconday = HouseHoldData.objects.filter(owner_education__icontains='Secondary level').count()
        edu_level_basic_level_1 = HouseHoldData.objects.filter(owner_education__icontains='Basic Level 1').count()

        #mother tongue
        mother_tongue_tharu = HouseHoldData.objects.filter(mother_tongue__icontains='Tharu').count()
        mother_tongue_tamang = HouseHoldData.objects.filter(mother_tongue__icontains='Tamang').count()
        mother_tongue_other = HouseHoldData.objects.filter(mother_tongue__icontains='Other').count()
        mother_tongue_newari = HouseHoldData.objects.filter(mother_tongue__icontains='Newari').count()
        mother_tongue_limbu = HouseHoldData.objects.filter(mother_tongue__icontains='Limbu').count()
        mother_tongue_rajbanshi = HouseHoldData.objects.filter(mother_tongue__icontains='Rajbanshi').count()
        mother_tongue_maithi = HouseHoldData.objects.filter(mother_tongue__icontains='Maithi').count()


        #main occupation
        occupation_agriculture = HouseHoldData.objects.filter(main_occupation__icontains='Agriculture').count()
        occupation_agriculture_wages = HouseHoldData.objects.filter(main_occupation__icontains='(Agricultural wages').count()
        occupation_daily_wages = HouseHoldData.objects.filter(main_occupation__icontains='Daily wages').count()
        occupation_government_service = HouseHoldData.objects.filter(main_occupation__icontains='Government service').count()
        occupation_non_government_service = HouseHoldData.objects.filter(main_occupation__icontains='Non-government service').count()
        occupation_foreign_employment = HouseHoldData.objects.filter(main_occupation__icontains='Foreign employment').count()
        occupation_foreign_entrepreneur = HouseHoldData.objects.filter(main_occupation__icontains='Entrepreneur').count()
        occupation_foreign_business = HouseHoldData.objects.filter(main_occupation__icontains='Business').count()
        occupation_foreign_labour_india = HouseHoldData.objects.filter(main_occupation__icontains='Seasonal labor, India').count()
        occupation_foreign_labour_nepal = HouseHoldData.objects.filter(main_occupation__icontains='Seasonal labor, Nepal').count()
        occupation_foreign_student = HouseHoldData.objects.filter(main_occupation__icontains='Student').count()
        occupation_foreign_other = HouseHoldData.objects.filter(main_occupation__icontains='Other').count()

        #num of family_member
        # member_2_to_4 =


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

#front filter api

class FddViewSet(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        ward = self.request.data.get('ward')
        social_security_received = self.request.data.get('social_security_received')
        citizen = self.request.data.get('senior_citizen')
        education_list = self.request.data.get('education')
        flood = self.request.data.get('flood')
        query = HouseHoldData.objects.all()

        if ward:
            wards_list = ast.literal_eval(ward)
            queryset = query.filter(ward__in=wards_list)


        if flood:
            queryset = query.filter(flood_prone__icontains=flood)


        if social_security_received:
            index = []
            family = OwnerFamilyData.objects.filter(social_security_received__icontains=social_security_received)
            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)
            queryset = query.filter(index__in=index)


        if citizen:
            index = []
            family = OwnerFamilyData.objects.filter(falling_under_social_security_criteria__icontains=citizen)
            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)
            queryset = query.filter(index__in=index)


        if education_list:
            print('edu')
            edu_list = ast.literal_eval(education_list)
            print(edu_list)
            queryset = edu_matching(edu_list)


        if ward and flood:
            wards_list = ast.literal_eval(ward)
            queryset = query.filter(flood_prone__icontains=flood, ward__in=wards_list)

        if ward and social_security_received:
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

        if ward and citizen:
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

        if ward and education_list:
            edu_list = ast.literal_eval(education_list)
            wards_list = ast.literal_eval(ward)
            query = edu_matching(edu_list)
            queryset = query.filter(ward__in=wards_list)

        if flood and social_security_received:
            index = []
            family = OwnerFamilyData.objects.filter(social_security_received__icontains=social_security_received)
            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)
            queryset = query.filter(index__in=index, flood_prone__icontains=flood)

        if flood and citizen:
            index = []
            family = OwnerFamilyData.objects.filter(falling_under_social_security_criteria__icontains=citizen)
            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)
            queryset = query.filter(index__in=index, flood_prone__icontains=flood)

        if flood and education_list:
            edu_list = ast.literal_eval(education_list)
            query = edu_matching(edu_list)
            queryset = query.filter(flood_prone__icontains=flood)


        if social_security_received and citizen:
            index = []
            family = OwnerFamilyData.objects.filter(falling_under_social_security_criteria__icontains=citizen, social_security_received__icontains=social_security_received)
            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)
            queryset = query.filter(index__in=index)

        if social_security_received and education_list:
            edu_list = ast.literal_eval(education_list)
            query = edu_matching(edu_list)

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

        if citizen and education_list:
            edu_list = ast.literal_eval(education_list)
            query = edu_matching(edu_list)
            index = []
            family = OwnerFamilyData.objects.filter(falling_under_social_security_criteria__icontains=citizen)
            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)
            queryset = query.filter(index__in=index)

        if ward and flood and social_security_received:
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

        if ward and flood and citizen:
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

        if ward and flood and education_list:
            wards_list = ast.literal_eval(ward)
            edu_list = ast.literal_eval(education_list)
            query = edu_matching(edu_list)


            queryset = query.filter(ward__in=wards_list, flood_prone__icontains=flood)

        if flood and social_security_received and citizen:
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

        if flood and citizen and education_list:
            edu_list = ast.literal_eval(education_list)
            query = edu_matching(edu_list)

            index = []
            family = OwnerFamilyData.objects.filter(falling_under_social_security_criteria__icontains=citizen)
            for i in family:
                parent_index = i.parent_index
                if parent_index in index:
                    pass
                else:
                    index.append(parent_index)
            queryset = query.filter(index__in=index, flood_prone__icontains=flood)

        if social_security_received and citizen and education_list:
            edu_list = ast.literal_eval(education_list)
            query = edu_matching(edu_list)
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

        if ward and flood and social_security_received and citizen:
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


        if ward and flood and social_security_received and education_list:
            edu_list = ast.literal_eval(education_list)
            query = edu_matching(edu_list)
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

        if ward and flood and citizen and education_list:
            edu_list = ast.literal_eval(education_list)
            query = edu_matching(edu_list)
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

        if ward and flood and social_security_received and citizen and education_list:
            edu_list = ast.literal_eval(education_list)
            query = edu_matching(edu_list)
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



        data = HouseHoldDataSerializer(queryset, many=True).data

        return Response({'data':data})




class UniqueValuesViewSet(APIView):
    authentication_classes = []
    permission_classes = []

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


class HDDViewSet(APIView):
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
            print(f_list)
            query = HouseHoldData.objects.all()
            app_data = []
            for house in query:
                coun = house.house_hold_data.all().count()
                print(coun)
                print(f_list)

                if coun in f_list:
                    id = house.index
                    queryset = HouseHoldData.objects.filter(index=id)
                    data = HouseHoldDataSerializer(queryset, many=True).data
                    for i in data:
                        app_data.append(i)

        if age_group_list:
            age_list = ast.literal_eval(age_group_list)
            # print(age_list)
            age_m = []
            for i in age_list:
                age = i.split('-')
                age_m.append(age)

            # print(age_m[0][0])
            app_data = []
            for age_value in age_m:
                # print (age_value[0])
                queryset = HouseHoldData.objects.filter(Q(owner_age__range=[age_value[0], age_value[1]]))
                data = HouseHoldDataSerializer(queryset, many=True).data
                for i in data:
                    app_data.append(i)


        if wards and education_lists:
            wards_list = ast.literal_eval(wards)
            edu_list = ast.literal_eval(education_lists)
            queryset = HouseHoldData.objects.filter(ward__in=wards_list, owner_education__in=edu_list)
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
            app_data = []
            for age_value in age_m:
                # print (age_value[0])
                queryset = query.filter(Q(owner_age__range=[age_value[0], age_value[1]]))
                data = HouseHoldDataSerializer(queryset, many=True).data
                for i in data:
                    app_data.append(i)


        if wards and family_members_list:
            wards_list = ast.literal_eval(wards)
            f_list = ast.literal_eval(family_members_list)
            query = HouseHoldData.objects.filter(ward__in=wards_list)
            app_data = []
            for house in query:
                coun = house.house_hold_data.all().count()
                print(coun)
                print(f_list)

                if coun in f_list:
                    id = house.index
                    queryset = HouseHoldData.objects.filter(index=id)
                    data = HouseHoldDataSerializer(queryset, many=True).data
                    for i in data:
                        app_data.append(i)


        if education_lists and age_group_list:
            edu_list = ast.literal_eval(education_lists)
            age_list = ast.literal_eval(age_group_list)
            query = HouseHoldData.objects.filter(owner_education__in=edu_list)
            age_m = []
            for i in age_list:
                age = i.split('-')
                age_m.append(age)

            # print(age_m[0][0])
            app_data = []
            for age_value in age_m:
                # print (age_value[0])
                queryset = query.filter(Q(owner_age__range=[age_value[0], age_value[1]]))
                data = HouseHoldDataSerializer(queryset, many=True).data
                for i in data:
                    app_data.append(i)


        if education_lists and family_members_list:
            edu_list = ast.literal_eval(education_lists)
            f_list = ast.literal_eval(family_members_list)
            query = HouseHoldData.objects.filter(owner_education__in=edu_list)
            app_data = []
            for house in query:
                coun = house.house_hold_data.all().count()
                print(coun)
                print(f_list)

                if coun in f_list:
                    id = house.index
                    queryset = HouseHoldData.objects.filter(index=id)
                    data = HouseHoldDataSerializer(queryset, many=True).data
                    for i in data:
                        app_data.append(i)


        if age_group_list and family_members_list:
            f_list = ast.literal_eval(family_members_list)
            age_list = ast.literal_eval(age_group_list)

            age_m = []
            for i in age_list:
                age = i.split('-')
                age_m.append(age)

            # print(age_m[0][0])
            app_data = []

            for age_value in age_m:
                query = HouseHoldData.objects.filter(Q(owner_age__range=[age_value[0], age_value[1]]))

                for house in query:
                    coun = house.house_hold_data.all().count()
                    print(coun)
                    print(f_list)

                    if coun in f_list:
                        id = house.index
                        queryset = HouseHoldData.objects.filter(index=id)
                        data = HouseHoldDataSerializer(queryset, many=True).data
                        for i in data:
                            app_data.append(i)


        if wards and education_lists and family_members_list:
            print('abc')
            wards_list = ast.literal_eval(wards)
            edu_list = ast.literal_eval(education_lists)
            f_list = ast.literal_eval(family_members_list)
            query = HouseHoldData.objects.filter(ward__in=wards_list, owner_education__in=edu_list)
            app_data = []
            for house in query:
                coun = house.house_hold_data.all().count()
                print(coun)
                print(f_list)

                if coun in f_list:
                    id = house.index
                    queryset = HouseHoldData.objects.filter(index=id)
                    data = HouseHoldDataSerializer(queryset, many=True).data
                    for i in data:
                        app_data.append(i)


        if wards and education_lists and age_group_list:
            wards_list = ast.literal_eval(wards)
            edu_list = ast.literal_eval(education_lists)
            age_list = ast.literal_eval(age_group_list)
            query = HouseHoldData.objects.filter(ward__in=wards_list, owner_education__in=edu_list)
            age_m = []
            for i in age_list:
                age = i.split('-')
                age_m.append(age)

            # print(age_m[0][0])
            app_data = []
            for age_value in age_m:
                # print (age_value[0])
                queryset = query.filter(Q(owner_age__range=[age_value[0], age_value[1]]))
                data = HouseHoldDataSerializer(queryset, many=True).data
                for i in data:
                    app_data.append(i)


        if wards and family_members_list and age_group_list:
            wards_list = ast.literal_eval(wards)
            f_list = ast.literal_eval(family_members_list)
            age_list = ast.literal_eval(age_group_list)

            age_m = []
            for i in age_list:
                age = i.split('-')
                age_m.append(age)

            # print(age_m[0][0])
            app_data = []

            for age_value in age_m:
                query = HouseHoldData.objects.filter(Q(owner_age__range=[age_value[0], age_value[1]]) & Q(ward__in=wards_list))

                for house in query:
                    coun = house.house_hold_data.all().count()
                    print(coun)
                    print(f_list)

                    if coun in f_list:
                        id = house.index
                        queryset = HouseHoldData.objects.filter(index=id)
                        data = HouseHoldDataSerializer(queryset, many=True).data
                        for i in data:
                            app_data.append(i)


        if education_lists and family_members_list and age_group_list:
            edu_list = ast.literal_eval(education_lists)
            f_list = ast.literal_eval(family_members_list)
            age_list = ast.literal_eval(age_group_list)

            age_m = []
            for i in age_list:
                age = i.split('-')
                age_m.append(age)

            # print(age_m[0][0])
            app_data = []

            for age_value in age_m:
                query = HouseHoldData.objects.filter(Q(owner_age__range=[age_value[0], age_value[1]]) & Q(owner_education__in=edu_list))

                for house in query:
                    coun = house.house_hold_data.all().count()
                    print(coun)
                    print(f_list)

                    if coun in f_list:
                        id = house.index
                        queryset = HouseHoldData.objects.filter(index=id)
                        data = HouseHoldDataSerializer(queryset, many=True).data
                        for i in data:
                            app_data.append(i)


        if wards and education_lists and family_members_list and age_group_list:
            wards_list = ast.literal_eval(wards)
            edu_list = ast.literal_eval(education_lists)
            f_list = ast.literal_eval(family_members_list)
            age_list = ast.literal_eval(age_group_list)
            abc = HouseHoldData.objects.filter(ward__in=wards_list, owner_education__in=edu_list)

            age_m = []
            for i in age_list:
                age = i.split('-')
                age_m.append(age)

            # print(age_m[0][0])
            app_data = []

            for age_value in age_m:
                query = abc.filter(Q(owner_age__range=[age_value[0], age_value[1]]))

                for house in query:
                    coun = house.house_hold_data.all().count()
                    print(coun)
                    print(f_list)

                    if coun in f_list:
                        id = house.index
                        queryset = HouseHoldData.objects.filter(index=id)
                        data = HouseHoldDataSerializer(queryset, many=True).data
                        for i in data:
                            app_data.append(i)



        # if coun in count:
            #     pass
            # else:
            #     count.append(coun)
            #
            #
            # house_hold = HouseHoldData.objects.annotate(count=HouseHoldData.house_hold_data.count())
            # print(house_hold)

            # print(count)


        return Response({'data': app_data})


class MoreViewSet(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        pass












