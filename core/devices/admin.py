from django.contrib import admin
from .models import Device

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'english_name', 'model','status', 'manufacturer', 'country', 'display_option')
    list_filter = ('status', 'manufacturer', 'country', 'display_option')
    search_fields = ('name', 'english_name', 'model', 'usage', 'description')
    list_editable = ('status', 'display_option')  # Make these fields editable in the list view

admin.site.register(Device, DeviceAdmin)