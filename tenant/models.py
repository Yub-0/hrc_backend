import datetime

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Tenant(models.Model):
    TENANT_STATUS = (
        ('Active', 'Active'),
        ('Left', 'Left'),
        ('Hold', 'Hold')
    )
    name = models.CharField(max_length=25)
    permanent_address = models.CharField(max_length=25, null=True)
    age = models.IntegerField(null=True)
    contact_no = PhoneNumberField(unique=True)
    status = models.CharField(max_length=25, choices=TENANT_STATUS, default='Active')
    entry_date = models.DateTimeField(default=datetime.datetime.now())
    leave_date = models.DateTimeField(auto_now=False, null=True)


class RoomChange(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    from_room = models.ForeignKey('house.Room', on_delete=models.CASCADE, related_name='from_room')
    to_room = models.ForeignKey('house.Room', on_delete=models.CASCADE, related_name='to_name')
    change_date = models.DateTimeField(auto_now=False, null=True)


class TenantRoom(models.Model):
    TENANT_STATUS = (
        ('Active', 'Active'),
        ('Left', 'Left'),
        ('Hold', 'Hold'),
        ('Changed', 'Changed')
    )
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    room = models.ForeignKey('house.Room', on_delete=models.CASCADE)
    status = models.CharField(max_length=25, choices=TENANT_STATUS, default='Active')
    entry_date = models.DateTimeField(default=datetime.datetime.now())
    leave_date = models.DateTimeField(auto_now=False, null=True)
