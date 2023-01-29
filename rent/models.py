from django.db import models
from datetime import datetime, date
from phonenumber_field.modelfields import PhoneNumberField

class Tenant(models.Model):
    TENANT_STATUS = (
        ('Active', 'Active'),
        ('Left', 'Left'),
        ('Hold', 'Hold')
    )
    name = models.CharField(max_length=25)
    permanent_address = models.CharField(max_length=25)
    age = models.IntegerField()
    contact_no = PhoneNumberField(unique=True)
    status = models.CharField(max_length=25, choices=TENANT_STATUS, default=1)
    entry_date = models.DateTimeField(default=datetime.now)
    leave_date = models.DateTimeField(auto_now=False)


class RoomTenant(models.Model):
    TENANT_STATUS = (
        ('Active', 'Active'),
        ('Left', 'Left'),
        ('Hold', 'Hold')
    )
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    room = models.ForeignKey('house.Room', on_delete=models.CASCADE)
    status = models.CharField(max_length=25, choices=TENANT_STATUS, default=1)
    entry_date = models.DateTimeField(default=datetime.now)
    leave_date = models.DateTimeField(auto_now=False)


class RentCategory(models.Model):
    category = models.CharField(max_length=25)


class Payment(models.Model):
    cat = models.ForeignKey(RentCategory, on_delete=models.CASCADE)
    payment = models.FloatField()
    date = models.DateTimeField(auto_now=False, default=datetime.now)


class Rent(models.Model):
    PAY_STATUS = (
        (1, 'Fully Payed'),
        (2, 'Partially Payed'),
        (3, 'Not Payed')
    )
    NEPALI_MON = (
        (0, 'बैशाख'),
        (1, 'जेठ'),
        (2, 'असार'),
        (3, 'श्रावण'),
        (4, 'भाद्र'),
        (5, 'आश्विन'),
        (6, 'कार्तिक'),
        (7, 'मंसिर'),
        (8, 'पौष'),
        (9, 'माघ'),
        (10, 'फाल्गुण'),
        (11, 'चैत्र')
    )
    total_rent = models.FloatField()
    paid_rent = models.FloatField(null=True, blank=True)
    payment = models.ManyToManyField(Payment)
    tenant_room = models.ForeignKey(RoomTenant, on_delete=models.CASCADE)
    status = models.IntegerField(choices=PAY_STATUS, default=3)
    date = models.DateTimeField(auto_now=False, null=True, blank=True)


