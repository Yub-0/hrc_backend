from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from user.token import MyTokenObtainPairSerializer
from user.models import MyUser
from house.models import Room


class UserRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['room', 'id', 'status']


class UserShowSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
        fields = ['id', 'phone', 'birthdate', 'name', 'gender', 'status', 'date_joined']
        depth = 1

    def get_status(self, obj):
        return obj.get_status_display()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['phone', 'birthdate', 'gender', 'password', 'name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = MyUser.objects.create(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    phone = PhoneNumberField(required=False)
    email = serializers.CharField(max_length=25)
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, data, *args):
        phone = '+9779849784723'
        password = data['password']
        user = authenticate(phone=phone, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid login credentials")
        refresh = MyTokenObtainPairSerializer.get_token(user)

        refresh_token = str(refresh)
        access_token = str(refresh.access_token)
        update_last_login(None, user)
        validation = {
            'access': access_token,
            'refresh': refresh_token,
        }
        return validation
