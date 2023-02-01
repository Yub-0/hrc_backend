from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from house.models import House, Room
from house.serializers import HouseSerializer, RoomSerializer, RoomShowSerializer, HouseShowSerializer


class HouseView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        try:
            house = House.objects.filter(owner=user)
        except House.DoesNotExist:
            return Response("owner has no house registered")
        serializer = HouseShowSerializer(house, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = HouseSerializer(context={'request': request}, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class RoomView(generics.GenericAPIView):
    def get(self, request):
        room = Room.objects.all()
        serializer = RoomShowSerializer(room, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RoomSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            s = serializer.save()
            res = {
                'room': RoomShowSerializer(s).data
            }
            return Response(res, status=status.HTTP_201_CREATED)
