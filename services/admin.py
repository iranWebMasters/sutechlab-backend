from django.contrib import admin
from .models import *

class LaboratoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name',)
    list_filter = ('location',)

class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name',)
    list_filter = ('location',)

class ExperimentAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'laboratory', 
        'faculty', 
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
admin.site.register(Faculty,FacultyAdmin)
admin.site.register(Experiment, ExperimentAdmin)
