from django.contrib import admin
from .models import Organization, Works

class WorksAdmin(admin.ModelAdmin):
    list_display = ['title']
admin.site.register(Organization)
admin.site.register(Works,WorksAdmin)

