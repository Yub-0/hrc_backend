from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tenant.serializers import TenantRegisterSerializer, TenantShowSerializer


class TenantView(APIView):

    def get(self):
        return Response()

    def post(self, request):
        serializer = TenantRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            s = serializer.save()
            res = TenantShowSerializer(s).data
            return Response(res, status=status.HTTP_201_CREATED)
        return Response('Something Went Wrong', status=status.HTTP_400_BAD_REQUEST)