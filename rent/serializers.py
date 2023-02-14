import datetime

import nepali_datetime
from rest_framework import serializers

from rent.models import RentCategory, RentPayment, RentCategoryPayment
from tenant.models import TenantRoom
from tenant.serializers import TenantRoomShowSerializer


class CategoryShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentCategory
        fields = '__all__'


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


class RentCategoryPaymentShowSerializer(serializers.ModelSerializer):
    category = CategoryShowSerializer()

    class Meta:
        model = RentCategoryPayment
        exclude = ['payment']


class RentPaymentShowSerializer(serializers.ModelSerializer):
    room = TenantRoomShowSerializer()
    rent_category = RentCategoryPaymentShowSerializer(many=True)

    class Meta:
        model = RentPayment
        fields = '__all__'


class CategoryCreateSerializer(serializers.Serializer):
    category = serializers.IntegerField()
    amount = serializers.DecimalField(decimal_places=2, max_digits=9, allow_null=True)


class RentPaymentSerializer(serializers.Serializer):
    category = CategoryCreateSerializer(many=True)
    total_paid = serializers.DecimalField(max_digits=9, decimal_places=2, allow_null=True)
    total_amount = serializers.DecimalField(max_digits=9, decimal_places=2)
    save = serializers.BooleanField()
    extra_charge = serializers.DecimalField(max_digits=9, decimal_places=2, allow_null=True, required=False)
    tenant = serializers.IntegerField()
    room = serializers.IntegerField()

    def create(self, validated_data):
        t_room = TenantRoom.objects.get(tenant__id=validated_data.get('tenant'), room__id=validated_data.get('room'))
        if validated_data.get('total_paid'):
            return_amt = validated_data.get('total_paid') - validated_data.get('total_amount')
        else:
            return_amt = None
        nep_date = nepali_datetime.date.from_datetime_date(datetime.date.today())
        month = '{0:%B}'.format(nep_date)
        year = '{0:%Y}'.format(nep_date)
        try:
            payment = RentPayment.objects.create(room=t_room, total_paid=validated_data.get('total_paid'), month=month, year=year,
                                                 total_amount=validated_data.get('total_amount'), return_amount=return_amt,
                                                 extra_charge=validated_data.get('extra_charge'), is_paid=validated_data.get('save'),
                                                 created_date=datetime.datetime.now())

        except:
            raise serializers.ValidationError('Something Went Wrong!')
        for category in validated_data['category']:
            cat = RentCategory.objects.get(id=category['category'])
            RentCategoryPayment.objects.create(payment=payment, category=cat, amount=category['amount'])
        return payment

    def update(self, instance, validated_data):
        return instance
