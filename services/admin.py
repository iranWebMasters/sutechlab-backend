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

class TestsAdmin(admin.ModelAdmin):  # Changed name from ExperimentSpecificationAdmin to TestSpecificationAdmin
    list_display = ('name_fa', 'name_en', 'unit_type', 'operating_range', 'description')
    search_fields = ('name_fa', 'name_en')
    list_filter = ('unit_type',)
    filter_horizontal = ('standards',)


class StandardsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    filter_horizontal = ('parameters',)


class SampleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_filter = ('name',)

class ExperimentAdmin(admin.ModelAdmin):
    list_display = (
        'device', 
        'operator', 
        'status', 
        'iso_17025', 
        'created_date', 
        'updated_date'
    )
    search_fields = (
        'laboratory__name', 
        'test_specifications__name_en',  # Updated field to match new model structure
        'device__name',  # Assuming there is a `name` field in `Device` model
        'operator__user__email', 
        'operator__first_name', 
        'operator__last_name'
    )
    list_filter = ('status', 'iso_17025', 'created_date', 'updated_date')
    date_hierarchy = 'created_date'
    autocomplete_fields = ('operator', 'device',)  # Add search fields for autocomplete
    filter_horizontal = ('samples','tests')  # Removed 'standards' if it doesn't exist

admin.site.register(Laboratory, LaboratoryAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Parameters, ParameterAdmin)
admin.site.register(Unit_amount, Unit_amountAdmin)
admin.site.register(Unit_price, Unit_priceAdmin)
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(Standards, StandardsAdmin)
admin.site.register(Tests, TestsAdmin)  # Updated model name registration
admin.site.register(Sample, SampleAdmin)
