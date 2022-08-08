from rest_framework import serializers
from apps.users.models import User
from apps.companies.api.serializers import CompanySerializer

class UserListSerializer(serializers.ModelSerializer):

    company = CompanySerializer()
    class Meta:
        model = User
        fields = ['id','email', 'name', 'last_name', 'last_login', 'company']

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'last_name', 'password', 'company']

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'name', 'last_name', 'company']

class UserChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']


