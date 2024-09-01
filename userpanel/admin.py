from django.contrib import admin
from .models import Laboratory, Institute, Test

class LaboratoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name',)
    list_filter = ('location',)

class InstituteAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name',)
    list_filter = ('location',)

class TestAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'laboratory', 
        'institute', 
        'operator', 
        'status', 
        'iso_17025', 
        'created_date', 
        'updated_date'
    )
    search_fields = (
        'title', 
        'laboratory__name', 
        'institute__name', 
        'institute__national_id', 
        'operator__user__email', 
        'operator__first_name', 
        'operator__last_name'
    )
    list_filter = ('status', 'iso_17025', 'created_date', 'updated_date')
    date_hierarchy = 'created_date'
    autocomplete_fields = ('operator',)  # Add search fields for autocomplete



admin.site.register(Laboratory, LaboratoryAdmin)
admin.site.register(Institute, InstituteAdmin)
admin.site.register(Test, TestAdmin)
