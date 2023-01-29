from rest_framework import serializers
import inflect
from house.models import House, Room, Floor
from user.serializers import UserSerializer, UserShowSerializer


class HouseSerializer(serializers.Serializer):
    plate_no = serializers.CharField(allow_null=True)
    address = serializers.CharField()
    image = serializers.ImageField(required=False, allow_null=True, allow_empty_file=True)
    floors = serializers.IntegerField()

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            House.objects.get(plate_no=validated_data['plate_no'])
            raise serializers.ValidationError("Plate number already exist!!")
        except House.DoesNotExist:
            house = House.objects.create(plate_no=validated_data['plate_no'], image=validated_data['image'],
                                         floors=validated_data['floors'], address=validated_data['address'],
                                         owner=user)
        p = inflect.engine()
        for a in range(validated_data['floor']):
            Floor.objects.create(floor=p.ordinal(a), house=house)
        return house


class HouseShowSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=True)

    class Meta:
        model = House
        fields = '__all__'


class RoomShowSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    tenant = UserShowSerializer()

    class Meta:
        model = Room
        fields = '__all__'
        depth = 1

    def get_status(self, obj):
        return obj.get_status_display()


class RoomSerializer(serializers.Serializer):
    room = serializers.CharField(allow_blank=True)
    location = serializers.CharField(allow_blank=True)
    floor = serializers.IntegerField()
    room_rent = serializers.DecimalField(decimal_places=2, max_digits=9)

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            floor = Floor.objects.get(id=validated_data['floor'], house=user.house)
        except Floor.DoesNotExist:
            raise serializers.ValidationError("Floor doesnt exist")
        room = Room.objects.create(room=validated_data['room'], location=validated_data['location'],
                                   floor=floor, room_rent=validated_data['room_rent'])
        return room
