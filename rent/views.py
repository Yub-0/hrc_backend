from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response

from rent.models import RentCategory
from rent.serializers import CategorySerializer


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
