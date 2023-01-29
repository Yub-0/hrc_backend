from django.http import Http404
from rest_framework import serializers

from house.models import Room
from rent.models import RentCategory, Payment, Rent
from user.models import MyUser


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RentCategory
        fields = '__all__'


class PaymentShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        depth = 1


class PaymentSerializer(serializers.Serializer):
    cat = serializers.CharField()
    payment = serializers.FloatField()
    room = serializers.IntegerField()
    month = serializers.IntegerField()
    user = serializers.IntegerField()

    def create(self, validated_data):
        try:
            cat = Category.objects.get(category=validated_data['cat'])
        except Category.DoesNotExist:
            cat = Category.objects.create(category=validated_data['cat'])
        try:
            room = Room.objects.get(id=validated_data['room'])
        except Room.DoesNotExist:
            raise Http404
        payment = Payment.objects.create(cat=cat, month=validated_data['month'],
                                         room=room, payment=validated_data['payment'])
        rent = Rent.objects.get(room=room)
        rent.payment.add(payment)
        rent.save()
        return payment


class RentShowSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    tenant = serializers.SerializerMethodField()
    month = serializers.SerializerMethodField()

    class Meta:
        model = Rent
        fields = '__all__'
        depth = 1

    def get_month(self, obj):
        return obj.get_month_display()

    def get_status(self, obj):
        return obj.get_status_display()

    def get_tenant(self, obj):
        return obj.tenant.name


class RentSerializer(serializers.Serializer):
    room = serializers.IntegerField()
    tenant = serializers.IntegerField()
    month = serializers.IntegerField()
    date = serializers.DateField()

    def create(self, validated_data):
        try:
            user = MyUser.objects.get(id=validated_data['tenant'])
        except MyUser.DoesNotExist:
            raise Http404
        try:
            rom = Room.objects.get(id=validated_data['room'])
        except Room.DoesNotExist:
            raise Http404
        try:
            rent = Rent.objects.get(room=rom, tenant=user, date=validated_data['date'])
        except Rent.DoesNotExist:
            r = rom.room_rent
            rent = Rent.objects.create(room=rom, tenant=user, date=validated_data['date'],
                                       month=validated_data['month'], total_rent=r)
        return rent
