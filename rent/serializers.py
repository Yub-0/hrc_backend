import datetime

from rest_framework import serializers

from rent.models import RentCategory, RentPayment
from tenant.models import TenantRoom

# class RentPaymentShow
class CategorySerializer(serializers.Serializer):
    category = serializers.CharField(max_length=25)
    per = serializers.DecimalField(decimal_places=2, max_digits=9, allow_null=True)
    amount = serializers.DecimalField(decimal_places=2, max_digits=9, allow_null=True)
    unit = serializers.CharField(max_length=25, allow_null=True)
    mandetory = serializers.BooleanField(required=False)

    def create(self, validated_data):
        try:
            category = RentCategory.objects.create(category=validated_data.get('category'), per=validated_data.get('per'),
                                                   amount=validated_data.get('amount'), unit=validated_data.get('unit'),
                                                   mandetory=validated_data.get('mandetory'))
        except:
            raise serializers.ValidationError('lwal')
        return category


class RentPaymentSerializer(serializers.Serializer):
    category = CategorySerializer(many=True)
    total_paid = serializers.DecimalField(max_digits=9, decimal_places=2)
    return_amount = serializers.DecimalField(max_digits=9, decimal_places=2)
    total_amount = serializers.DecimalField(max_digits=9, decimal_places=2)
    save = serializers.BooleanField(default=False)
    extra_charge = serializers.DecimalField(max_digits=9, decimal_places=2, allow_null=True)
    tenant = serializers.IntegerField()
    room = serializers.IntegerField()

    def create(self, validated_data):
        t_room = TenantRoom.objects.get(tenant__id=validated_data.get('tenant'), room__id=validated_data.get('room'))
        try:
            if validated_data.get('save'):
                payment = RentPayment.objects.create(room=t_room, total_paid=validated_data.get('total_paid'),
                                                     return_amount=validated_data.get('return_amount'), total_amount=validated_data.get('total_amount'),
                                                     extra_charge=validated_data.get('extra_charge'), is_paid=False, created_date=datetime.datetime.now())
            else:
                payment = RentPayment.objects.create(room=t_room, total_paid=validated_data.get('total_paid'),
                                                     return_amount=validated_data.get('return_amount'), total_amount=validated_data.get('total_amount'),
                                                     extra_charge=validated_data.get('extra_charge'), is_paid=True, created_date=datetime.datetime.now(),
                                                     payment_date=datetime.datetime.now())
        except:
            raise serializers.ValidationError('Something Went Wrong!')
        for category in validated_data.get('category'):
            payment.category.add(category)
        return payment

    def update(self, instance, validated_data):
        return instance
