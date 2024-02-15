from django.contrib import admin
from properties.models import Property, Unit, Tenant, TenantAgreement
# Register your models here.
admin.site.register(Property)
admin.site.register(Unit)
admin.site.register(Tenant)
admin.site.register(TenantAgreement)