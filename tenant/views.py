import datetime

import nepali_datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from tenant.models import Tenant, TenantRoom
from tenant.serializers import TenantRegisterSerializer, TenantShowSerializer, TenantRoomShowSerializer


class TenantView(APIView):

    def get(self, request):
        tenant = Tenant.objects.all()
        serializer = TenantShowSerializer(tenant, many=True).data
        return Response(serializer)

    def post(self, request):
        serializer = TenantRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            s = serializer.save()
            res = TenantShowSerializer(s).data
            return Response(res, status=status.HTTP_201_CREATED)
        return Response('Something Went Wrong', status=status.HTTP_400_BAD_REQUEST)


class TenantRoomView(APIView):

    def get(self, request):
        nep_date = nepali_datetime.date.from_datetime_date(datetime.date.today())
        month = '{0:%B}'.format(nep_date)
        year = '{0:%Y}'.format(nep_date)
        tenant_room = TenantRoom.objects.exclude(rent__month=month, rent__year=year)
        serializer = TenantRoomShowSerializer(tenant_room, many=True)
        return Response(serializer.data)

    def post(self, request):

        return Response()