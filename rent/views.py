import datetime

import nepali_datetime
from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response

from rent.models import RentCategory, RentPayment
from rent.serializers import CategorySerializer, RentPaymentSerializer, RentPaymentShowSerializer, CategoryShowSerializer


class CategoryView(generics.GenericAPIView):
    def get(self, request):
        cat = RentCategory.objects.all()
        serializer = CategoryShowSerializer(cat, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)


class RentView(generics.GenericAPIView):
    def get(self, request):
        paid = request.GET.get('paid')
        rent = RentPayment.objects.all()
        if paid:
            nep_date = nepali_datetime.date.from_datetime_date(datetime.date.today())
            month = '{0:%B}'.format(nep_date)
            year = '{0:%Y}'.format(nep_date)
            rent = rent.filter(month=month, year=year)
        serializer = RentPaymentShowSerializer(rent, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RentPaymentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status)