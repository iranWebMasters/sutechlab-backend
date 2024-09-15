from django.contrib import admin
from .models import *

class LaboratoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty', 'technical_manager')
    search_fields = ('name', 'faculty__name', 'technical_manager__user__email')
    list_filter = ('faculty',)

class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name',)
    list_filter = ('location',)

class ParameterAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'laboratory', 'unit_amount', 'unit_price')
    search_fields = ('name', 'laboratory__name', 'unit_amount__amount', 'unit_price__unit_price')
    list_filter = ('unit', 'laboratory', 'unit_amount', 'unit_price')

class UnitAmountAdmin(admin.ModelAdmin):
    list_display = ('amount', 'unit')
    search_fields = ('amount', 'unit')
    list_filter = ('unit',)

class UnitPriceAdmin(admin.ModelAdmin):
    list_display = ('unit_price', 'currency')
    search_fields = ('unit_price', 'currency')
    list_filter = ('currency',)

class TestsAdmin(admin.ModelAdmin):
    list_display = ('name_fa', 'name_en', 'unit_type', 'operating_range', 'description')
    search_fields = ('name_fa', 'name_en')
    list_filter = ('unit_type',)
    filter_horizontal = ('standards',)

class StandardsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('parameters',)

class SampleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_filter = ('name',)
    filter_horizontal = ('tests',)


class ExperimentAdmin(admin.ModelAdmin):
    list_display = (
        'test_name',
        'laboratory',
        'device',
        'operator',
        'status',
        'iso_17025',
        'created_date',
        'updated_date'
    )
    search_fields = (
        'test_name',
        'laboratory__name',
        'device__name',
        'operator__user__email',
        'operator__first_name',
        'operator__last_name'
    )
    list_filter = ('status', 'iso_17025', 'created_date', 'updated_date')
    date_hierarchy = 'created_date'
    autocomplete_fields = ('operator', 'device',)
    filter_horizontal = ('samples',)

admin.site.register(Laboratory, LaboratoryAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Parameters, ParameterAdmin)
admin.site.register(UnitAmount, UnitAmountAdmin)
admin.site.register(UnitPrice, UnitPriceAdmin)
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(Standards, StandardsAdmin)
admin.site.register(Test, TestsAdmin)
admin.site.register(Sample, SampleAdmin)
