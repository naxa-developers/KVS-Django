from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from django.contrib.auth.models import Group, User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from api.serializers.user_serializers import UserSerializer
from rest_framework import viewsets
from core.models import UserRole, Province, District, Municipality, Ward


class Register(APIView):
    def post(self, request, *args, **kwargs):
        userParams = request.data

        self.email = userParams.get('email', None)
        self.username = userParams.get('user_name', None)
        self.password = userParams.get('password', None)
        self.first_name = userParams.get('first_name', None)
        self.last_name = userParams.get('last_name', None)

        print(self.username)
        user = User(username=self.username, email=self.email,
                    first_name=self.first_name, last_name=self.last_name)
        # user.groups.add(g)
        user.set_password(self.password)
        user.save()

        group = userParams.get('group', None)
        if group:
            group = Group.objects.get(name=group)
        else:
            return Response('Please select the type of user')

        if group.name == 'Province User':
            province_id = userParams.get('province', None)
            if province_id:
                province = Province.objects.get(id=province_id)
                user_role = UserRole.objects.create(user=user, province=province, group=group)
            else:
                return Response('Province must be selected')

        if group.name == 'District User':
            district_id = userParams.get('district', None)
            if district_id:
                district = District.objects.get(id=district_id)
                province = district.province
                user_role = UserRole.objects.create(user=user, district=district, province=province, group=group)
            else:
                return Response('District must be selected')

        if group.name == 'Municipality User':
            municipality_id = userParams.get('municipality', None)
            if municipality_id:
                municipality = Municipality.objects.get(id=municipality_id)
                district = municipality.district
                province = municipality.province
                user_role = UserRole.objects.create(user=user, district=district, province=province,
                                                    municipality=municipality, group=group)

            else:
                return Response('Municipality must be selected')

        if group.name == 'Ward User':
            ward_id = userParams.get('ward', None)
            if ward_id:
                ward = Ward.objects.get(id=ward_id)
                municipality = ward.municipality
                district = municipality.district
                province = district.province

                user_role = UserRole.objects.create(user=user, district=district, province=province,
                                                    municipality=municipality, ward=ward, group=group)

            else:
                return Response('Ward must be selected')


        return Response({
            'message': 'User has been successfully registered',
            'user': user.username,
            'id': user.id,
            'role': user_role.group.name
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



