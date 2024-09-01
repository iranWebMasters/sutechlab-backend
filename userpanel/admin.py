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
    list_display = ('title', 'laboratory', 'institute', 'operator', 'status', 'iso_17025', 'created_date', 'updated_date')
    search_fields = ('title', 'laboratory__name', 'institute__name', 'operator__username')
    list_filter = ('status', 'iso_17025', 'created_date', 'updated_date')
    date_hierarchy = 'created_date'

admin.site.register(Laboratory, LaboratoryAdmin)
admin.site.register(Institute, InstituteAdmin)
admin.site.register(Test, TestAdmin)
