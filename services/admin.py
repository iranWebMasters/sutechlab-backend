from django.contrib import admin
from .models import *

class LaboratoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name',)
    list_filter = ('location',)

class ParameterAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'laboratory', 'unit_amount', 'unit_price')
    search_fields = ('name', 'laboratory__name', 'unit_amount__amount', 'unit_price__unit_price')
    list_filter = ('unit', 'laboratory', 'unit_amount', 'unit_price')

class Unit_amountAdmin(admin.ModelAdmin):
    list_display = ('amount', 'unit')
    search_fields = ('amount', 'unit')
    list_filter = ('unit',)

class Unit_priceAdmin(admin.ModelAdmin):
    list_display = ('unit_price', 'currency')
    search_fields = ('unit_price', 'currency')
    list_filter = ('currency',)

class ExperimentSpecificationAdmin(admin.ModelAdmin):
    list_display = ('name_fa', 'name_en', 'unit_type', 'operating_range', 'description')
    search_fields = ('name_fa', 'name_en')
    list_filter = ('unit_type',)

class ExperimentAdmin(admin.ModelAdmin):
    list_display = (
        'laboratory', 
        'device', 
        'operator', 
        'status', 
        'iso_17025', 
        'created_date', 
        'updated_date'
    )
    search_fields = (
        'laboratory__name', 
        'faculty__name', 
        'device__name',  # Assuming there is a `name` field in `Device` model
        'operator__user__email', 
        'operator__first_name', 
        'operator__last_name'
    )
    list_filter = ('status', 'iso_17025', 'created_date', 'updated_date')
    date_hierarchy = 'created_date'
    autocomplete_fields = ('operator', 'device')  # Add search fields for autocomplete
    filter_horizontal = ('parameters',)  # Allow selecting multiple parameters in admin interface

admin.site.register(Laboratory, LaboratoryAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Parameter, ParameterAdmin)
admin.site.register(Unit_amount, Unit_amountAdmin)
admin.site.register(Unit_price, Unit_priceAdmin)
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(ExperimentSpecification, ExperimentSpecificationAdmin)
