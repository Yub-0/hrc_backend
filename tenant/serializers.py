from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from house.models import Room
from tenant.models import Tenant, TenantRoom


class TenantShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = '__all__'


class TenantRegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=25)
    address = serializers.CharField(max_length=25, allow_null=True)
    age = serializers.IntegerField(allow_null=True)
    phone = PhoneNumberField()
    room = serializers.IntegerField()

    def validate_room(self, obj):
        try:
            Room.objects.get(id=obj)
        except:
            raise serializers.ValidationError('Room not found')
        return obj

    def create(self, validated_data):
        try:
            tenant = Tenant.objects.create(name=validated_data.get('name'), address=validated_data.get('address'), age=validated_data.get('age'),
                                           contact_no=validated_data.get('phone'))
        except:
            raise serializers.ValidationError('Something Went WWrong!')

        room = Room.objects.get(id=validated_data.get('room'))
        TenantRoom.objects.create(tenatn=tenant, room=room)
        return tenant
