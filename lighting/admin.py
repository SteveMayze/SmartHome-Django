from django.contrib import admin
from lighting.models import Zone
from lighting.models import LightingState

class ZoneAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('device.name', 'name')}


admin.site.register(Zone)
admin.site.register(LightingState, list_display=["id", "device", "status", "config"],)
