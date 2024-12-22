from django.contrib import admin
from .models import *


class LaboratoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty', 'technical_manager')
    search_fields = ('name', 'faculty__name', 'technical_manager__user__email')
    list_filter = ('faculty',)
    autocomplete_fields = ('faculty', 'technical_manager')
    ordering = ('name',)
    list_per_page = 20


class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name',)
    list_filter = ('location',)
    ordering = ('name',)
    list_per_page = 20


class ParameterAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'unit_amount', 'unit_price')
    search_fields = ('name','unit_amount__amount', 'unit_price__unit_price')
    list_filter = ('unit','unit_amount', 'unit_price')
    autocomplete_fields = ('unit_amount', 'unit_price')
    ordering = ('name',)
    list_per_page = 20
    filter_horizontal = ('values',)


class UnitAmountAdmin(admin.ModelAdmin):
    list_display = ('amount', 'unit')
    search_fields = ('amount', 'unit')
    list_filter = ('unit',)
    ordering = ('amount',)
    list_per_page = 20


class UnitPriceAdmin(admin.ModelAdmin):
    list_display = ('unit_price', 'currency')
    search_fields = ('unit_price', 'currency')
    list_filter = ('currency',)
    ordering = ('unit_price',)
    list_per_page = 20


class TestsAdmin(admin.ModelAdmin):
    list_display = ('name_fa', 'name_en', 'operating_range', 'description')
    search_fields = ('name_fa', 'name_en')
    filter_horizontal = ('parameters',)
    ordering = ('name_fa',)
    list_per_page = 20


class SampleAdmin(admin.ModelAdmin):
    list_display = ('type', 'description', 'is_returnable')
    search_fields = ('type',)
    list_filter = ('is_returnable',)
    ordering = ('type',)
    list_per_page = 20

class ParameterValueAdmin(admin.ModelAdmin):
    list_display = ('name', 'default_value', 'min_value', 'max_value')
    list_editable = ('default_value', 'min_value', 'max_value')
    search_fields = ('name', 'default_value')
    list_filter = ('min_value', 'max_value')
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'default_value', 'min_value', 'max_value')
        }),
    )
class ExperimentAdmin(admin.ModelAdmin):
    list_display = (
        'test_name',
        'laboratory',
        'device',
        'operator',
        'status',
        'iso_17025',
        'updated_date',
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
    filter_horizontal = ('samples', 'tests')
    readonly_fields = ('created_date', 'updated_date')
    ordering = ('-created_date',)
    list_per_page = 20
    actions = ['duplicate_experiments']
    list_editable = ('status','iso_17025',)

    def duplicate_experiments(self, request, queryset):
        for experiment in queryset:
            experiment.duplicate_experiments()
        self.message_user(request, "تعداد آزمایش‌های انتخابی دو برابر شد.")
    
    duplicate_experiments.short_description = "دو برابر کردن آزمایش‌های انتخاب شده"


admin.site.register(Laboratory, LaboratoryAdmin)
admin.site.register(ParameterValue, ParameterValueAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Parameters, ParameterAdmin)
admin.site.register(UnitAmount, UnitAmountAdmin)
admin.site.register(UnitPrice, UnitPriceAdmin)
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(Test, TestsAdmin)
admin.site.register(Sample, SampleAdmin)
