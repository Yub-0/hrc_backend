from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import MyUser
from user.serializers import UserShowSerializer, UserSerializer, LoginSerializer\
    # , OwnerSerializer


class OwnerView(generics.GenericAPIView):
    def get(self, request):
        user = MyUser.objects.all()
        serializer = UserShowSerializer(user, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)
#
#     def post(self, request):
#         serializer = OwnerSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             s = serializer.save()
#             res = {
#                 'user': UserShowSerializer(s).data
#             }
#             return Response(res, status=status.HTTP_201_CREATED)


class UserView(generics.GenericAPIView):

    def get(self, request):
        user = MyUser.objects.exclude(id=1)
        serializer = UserShowSerializer(user, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

    def post(self, request):
        print(request.data)
        # return Response("lol")
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            s = serializer.save()
            res = {
                'user': UserShowSerializer(s).data
            }
            return Response(res, status=status.HTTP_201_CREATED)

    def put(self, request, pk):
        user = MyUser.objects.get(id=pk)
        serializer = UserSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        print(request.data)
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            response = {
                'access': serializer.validated_data['access'],
                'refresh': serializer.validated_data['refresh']
            }
            return Response(response, status=status.HTTP_200_OK)
