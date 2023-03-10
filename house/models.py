from django.db import models


class House(models.Model):
    plate_no = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=50)
    image = models.ImageField(null=True)
    floors = models.IntegerField(null=True)
    owner = models.ForeignKey('user.MyUser', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


class Floor(models.Model):
    floor = models.CharField(max_length=25)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


class Room(models.Model):
    ROOM_STATUS = (
        (1, 'Vacant'),
        (2, 'Occupied')
    )
    room = models.CharField(max_length=25, blank=True)
    location = models.CharField(max_length=25, blank=True)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    status = models.IntegerField(choices=ROOM_STATUS, default=1)
    room_rent = models.DecimalField(decimal_places=2, max_digits=9)
    is_active = models.BooleanField(default=True)
