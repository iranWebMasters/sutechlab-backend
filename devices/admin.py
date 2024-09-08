from django.contrib import admin
from .models import Device

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('brand', 'usage')  # Remove created_date and updated_date
    list_filter = ('brand', )
    search_fields = ('brand', 'usage', 'services_description')

admin.site.register(Device, DeviceAdmin)
