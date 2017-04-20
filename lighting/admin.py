from django.contrib import admin
from lighting.models import Zone

class ZoneAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('device.name', 'name')}


admin.site.register(Zone)
