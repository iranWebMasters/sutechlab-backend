from django.contrib import admin
from .models import *


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'status','created_date', 'updated_date')
    list_filter = ('status', )
    search_fields = ('title', 'content')
    readonly_fields = ('created_date', 'updated_date')    
    
admin.site.register(Device, ServiceAdmin)
