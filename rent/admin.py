from django.contrib import admin

# Register your models here.
from rent.models import RentCategory, Payment, Rent

admin.site.register(RentCategory)
admin.site.register(Payment)
admin.site.register(Rent)