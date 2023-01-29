from django.contrib import admin

# Register your models here.
from house.models import House, Floor, Room

admin.site.register(House)
admin.site.register(Room)
admin.site.register(Floor)
