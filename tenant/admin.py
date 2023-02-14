from django.contrib import admin

from .models import Tenant, TenantRoom

admin.site.register(Tenant)
admin.site.register(TenantRoom)
