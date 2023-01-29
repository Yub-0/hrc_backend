from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import MyUser
from user.serializers import UserShowSerializer, UserSerializer, LoginSerializer


class UserView(generics.GenericAPIView):

    def get(self, request, pk=None):
        try:
            user = MyUser.objects.get(id=pk)
        except MyUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserShowSerializer(user).data
        return Response(serializer, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            s = serializer.save()
            res = UserShowSerializer(s).data
            return Response(res, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        user = MyUser.objects.get(id=pk)
        serializer = UserSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_205_RESET_CONTENT)


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            response = {
                'access': serializer.validated_data['access'],
                'refresh': serializer.validated_data['refresh']
            }
            return Response(response, status=status.HTTP_200_OK)
