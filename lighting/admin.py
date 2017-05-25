from django.contrib import admin
from lighting.models import Zone
from lighting.models import LightHistory

class ZoneAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('device.name', 'name')}


admin.site.register(Zone)
admin.site.register(LightHistory, list_display=["id", "timestamp", "status", "config"],)
