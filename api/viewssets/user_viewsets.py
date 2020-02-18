from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from django.contrib.auth.models import Group, User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from api.serializers.user_serializers import UserSerializer
from rest_framework import viewsets
from core.models import UserRole, Province, District, Municipality, Ward, HouseHoldData
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


class Register(APIView):
    def post(self, request, *args, **kwargs):
        userParams = request.data

        self.email = userParams.get('email', None)
        self.username = userParams.get('user_name', None)
        self.password = userParams.get('password', None)
        # self.first_name = userParams.get('first_name', None)
        # self.last_name = userParams.get('last_name', None)

        # print(self.username)
        # user = User(username=self.username, email=self.email,
        #             first_name=self.first_name, last_name=self.last_name)
        user = User(username=self.username, email=self.email)
        # user.groups.add(g)
        user.set_password(self.password)
        deactive = userParams.get('deactive', None)

        if deactive is not None:
            if deactive:
                user.is_active = False
            else:
                user.is_active = True

        else:
            return Response(' Select user is active or deactive user')

        user.save()

        group = userParams.get('group', None)
        if group:
            group = Group.objects.get(name=group)
        else:
            return Response('Please select the type of user')

        if group.name == 'Province User':
            province_name = userParams.get('province', None)
            if province_name:
                province = Province.objects.get(name=province_name)
                user_role = UserRole.objects.create(user=user, province=province, group=group)
            else:
                return Response('Province must be selected')

        if group.name == 'District User':
            district_name = userParams.get('district', None)
            if district_name:
                district = District.objects.get(name=district_name)
                province = district.province
                user_role = UserRole.objects.create(user=user, district=district, province=province, group=group)
            else:
                return Response('District must be selected')

        if group.name == 'Municipality User':
            municipality_name = userParams.get('municipality', None)
            if municipality_name:
                municipality = Municipality.objects.get(name=municipality_name)
                district = municipality.district
                province = municipality.province
                user_role = UserRole.objects.create(user=user, district=district, province=province,
                                                    municipality=municipality, group=group)

            else:
                return Response('Municipality must be selected')

        if group.name == 'Ward User':
            ward_id = userParams.get('ward', None)
            municipality_name = userParams.get('municipality', None)
            if ward_id and municipality_name:
                municipality = Municipality.objects.get(name=municipality_name)
                district = municipality.district
                province = district.province

                user_role = UserRole.objects.create(user=user, district=district, province=province,
                                                    municipality=municipality, ward=ward_id, group=group)

            else:
                return Response('Ward  and Municipality must be selected')
                print('abc')


        return Response({
            'message': 'User has been successfully registered',
            'user': user.username,
            'id': user.id,
            'role': user_role.group.name,
            'active': user.is_active
        })


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class UserLogIn(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'message': 'Successfully logged in',
                    'status': status.HTTP_200_OK,
                    'token': token.key
                })
            else:
                return Response({
                    'status': status.HTTP_404_NOT_FOUND
                })
        else:
            return Response({
                'status': status.HTTP_401_UNAUTHORIZED
            })


class UserLogOut(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        return Response({
            'message': 'User logged out successfully',
            'status': status.HTTP_200_OK
        })


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = []


class RoleViewSet(viewsets.ModelViewSet):
    serializer_class = UserRole
    queryset = UserRole.objects.all()
    permission_classes = []


class UserListViewSet(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        data = []
        logged_user = self.request.user

        logged_user_role = logged_user.role.all()

        province = logged_user_role[0].province
        district = logged_user_role[0].district
        municipality = logged_user_role[0].municipality
        ward = logged_user_role[0].ward

        print(province,district,municipality,ward)

        q = Q()

        if province:
            q &= Q(role__province=province)

        if district:
            q &= Q(role__district=district)

        if municipality:
            q &= Q(role__municipality=municipality)

        if ward:
            q &= Q(role__ward=ward)

        users = User.objects.filter(q)

        print(users)

        for user in users:
            group = None
            place = None
            for role in user.role.all():
                if role.group.name == 'Province User':
                    group = role.group.name
                    place = role.province.name
                elif role.group.name == 'District User':
                    group = role.group.name
                    place = role.district.name
                elif role.group.name == 'Municipality User':
                    group = role.group.name
                    place = role.municipality.name
                elif role.group.name == 'Ward User':
                    group = role.group.name
                    place = role.municipality.name + ' ' + role.ward

                elif role.group.name == 'Super User':
                    group = role.group.name
                    place = None

                else:
                    group = None
                    place = None

            data.append({
                'name': user.username,
                'email': user.email,
                'group': group,
                'place': place,
                'status': user.is_active,
                'action': ''

            })
        return Response({'data': data})


class CreateUserDropDownViewSet(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):

        logged_user = self.request.user
        roles = logged_user.role.all()
        level = []
        district_list = []
        municipality_list = []
        ward_list = []

        for role in roles:

            if role.group.name == 'Province User':
                level = ['District User', 'Municipality User', 'Ward User']
                districts = District.objects.filter(province__name=role.province.name).values('name')
                municipalities = Municipality.objects.filter(province__name=role.province.name).values('name', 'hlcit_code')

                for district in districts:
                    district_list.append(district['name'])

                for municipality in municipalities:
                    municipality_list.append({municipality['name']: municipality['hlcit_code']})

            if role.group.name == 'District User':
                level = ['Municipality User', 'Ward User']
                municipalities = Municipality.objects.filter(district__name=role.district.name).values('name', 'hlcit_code')
                for municipality in municipalities:
                    municipality_list.append({municipality['name']: municipality['hlcit_code']})

            if role.group.name == 'Municipality User':
                level = ['Ward User']

            if role.group.name == 'Ward User':
                pass

        return Response({
            'level': level,
            'district': district_list,
            'municipality': municipality_list,
            'ward': ward_list
        })




