from django.contrib.auth.models import User, Group, Permission
from rest_framework import serializers
from core.models import UserRole


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    group = serializers.CharField(source='group.name')
    province = serializers.CharField(source='province.name')
    district = serializers.CharField(source='district.name')
    municipality = serializers.CharField(source='municipality.name')

    class Meta:
        model = UserRole
        fields = '__all__'
        # depth = 1


class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(source='role', many=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'groups', 'is_active', 'is_staff',
                  'is_superuser', 'roles')
        write_only_fields = ('password',)
        read_only_fields = ('id',)


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'
