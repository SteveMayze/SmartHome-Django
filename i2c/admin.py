from django.contrib import admin
from i2c.models import Device

class DeviceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('address',)}

admin.site.register(Device)
