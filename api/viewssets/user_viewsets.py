from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from django.contrib.auth.models import Group, User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from api.serializers.user_serializers import UserSerializer
from rest_framework import viewsets


class Register(APIView):
    def post(self, request, *args, **kwargs):
        userParams = request.data

        self.email = userParams.get('email', None)
        self.username = userParams.get('user_name', None)
        self.password = userParams.get('password', None)
        self.first_name = userParams.get('first_name', None)
        self.last_name = userParams.get('last_name', None)
        # self.roles_id = userParams.pop('roles_id', None)

        # try:
        print('abc')
        # g = Group.objects.get(id=1)
        # except:
        # Response({
        #     'error': 'selected role was not found'
        # }, status.HTTP_403_FORBIDDEN)

        user = User(username=self.username, email=self.email,
                    first_name=self.first_name, last_name=self.last_name)
        # user.groups.add(g)
        user.set_password(self.password)
        user.save()

        return Response({
            'message': 'User has been successfully registered',
            'user': user.username,
            'id': user.id,
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
                return Response({
                    'message': 'Successfully logged in',
                    'status': status.HTTP_200_OK
                })
            else:
                return Response({
                    'status': status.HTTP_404_NOT_FOUND
                })
        else:
            return Response({
                'status': status.HTTP_401_UNAUTHORIZED
            })


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = []



