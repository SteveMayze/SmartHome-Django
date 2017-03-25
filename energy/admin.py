from django.contrib import admin
from energy.models import Resource, ResourceValueFactor, ResourceEntry


class ResourceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name', )}

admin.site.register(Resource, ResourceAdmin)
admin.site.register(ResourceValueFactor)
admin.site.register(ResourceEntry)
