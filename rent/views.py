from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response

from rent.models import RentCategory, Payment, Rent
from rent.serializers import CategorySerializer, PaymentShowSerializer, RentShowSerializer, PaymentSerializer,\
                             RentSerializer


class CategoryView(generics.GenericAPIView):
    def get(self, request):
        cat = RentCategory.objects.all()
        serializer = CategorySerializer(cat, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class PaymentView(generics.GenericAPIView):
    def get(self, request):
        payment = Payment.objects.all()
        serializer = PaymentShowSerializer(payment, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PaymentSerializer(data=request)
        if serializer.is_valid(raise_exceptions=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class RentView(generics.GenericAPIView):
    def get_object(self, pk):
        try:
            rent = Rent.objects.get(id=pk)
            return rent
        except Rent.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        if pk:
            rent = self.get_object(pk)
            serializer = RentShowSerializer(rent).data
        else:
            r = request.GET.get('rent')
            d = request.GET.get('date')
            if r:
                rent = Rent.objects.get(room__id=r, date=d)
                serializer = RentShowSerializer(rent).data
            else:
                rent = Rent.objects.all()
                serializer = RentShowSerializer(rent, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            s = serializer.save()
            res = RentShowSerializer(s).data
            return Response(res, status=status.HTTP_201_CREATED)