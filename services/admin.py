from django.contrib import admin
from .models import *


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'published_date', 'created_date', 'updated_date')
    list_filter = ('status', )
    search_fields = ('title', 'content')
    date_hierarchy = 'published_date'
    readonly_fields = ('created_date', 'updated_date')
    exclude = ('published_date',) 
    
    

admin.site.register(Services, ServiceAdmin)
