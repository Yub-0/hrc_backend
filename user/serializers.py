from django.contrib.auth import authenticate
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
        password = make_password('Nepal123')
        user = MyUser.objects.create(**validated_data)
        return user


# class OwnerSerializer(serializers.Serializer):
#     phone = PhoneNumberField()
#     birthdate = serializers.DateField()
#     gender = serializers.IntegerField()
#     name = serializers.CharField()
#     permanent_address = serializers.CharField(allow_blank=True)
#     role = serializers.IntegerField()
#     password = serializers.CharField()
#     date_joined = serializers.DateField(required=False)
#
#     plate = serializers.CharField()
#     address = serializers.CharField()
#     image = serializers.ImageField(required=False)
#     floor = serializers.IntegerField()
#
#     def create(self, validated_data):
#         try:
#             MyUser.objects.get(phone=validated_data['phone'])
#             raise serializers.ValidationError("User with this number already exist!!")
#         except MyUser.DoesNotExist:
#             try:
#                 House.objects.get(plate_no=validated_data['plate'])
#                 raise serializers.ValidationError("Plate number already exist!!")
#             except House.DoesNotExist:
#                 house = House.objects.create(plate_no=validated_data['plate'], address=validated_data['address'])
#                 if 'image' in validated_data:
#                     if validated_data['image'] is None or validated_data['image'] == '':
#                         pass
#                     else:
#                         house.image = validated_data['image']
#                         house.save()
#             f = validated_data['floor']
#             if f:
#                 p = inflect.engine()
#                 for a in range(f):
#                     Floor.objects.create(floor=p.ordinal(a+1), house=house)
#             password = make_password(validated_data['password'])
#             user = MyUser.objects.create(phone=validated_data['phone'], password=password, house=house,
#                                          gender=validated_data['gender'], role=validated_data['role'],
#                                          birthdate=validated_data['birthdate'], name=validated_data['name'])
#             return user


class LoginSerializer(serializers.Serializer):
    phone = PhoneNumberField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, data, *args):
        phone = data['phone']
        password = data['password']
        user = authenticate(phone=phone, password=password)
        if user is None:
            print('lol')
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