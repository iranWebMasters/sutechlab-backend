from django.contrib import admin
from .models import RequestInfo, Request, SampleInfo, ExperimentInfo, AdditionalInfo, DiscountInfo

class RequestInfoAdmin(admin.ModelAdmin):
    list_display = ('submission_date', 'description')

class RequestAdmin(admin.ModelAdmin):
    ...
class SampleInfoAdmin(admin.ModelAdmin):
    list_display = ('sample_type', 'sample_count', 'sample_unit', 'is_perishable', 'expiration_date')
    search_fields = ('sample_type', 'additional_info')

class ExperimentInfoAdmin(admin.ModelAdmin):
    list_display = ()
    search_fields = ('additional_info__additional_info', 'cost__sample_return')

class AdditionalInfoAdmin(admin.ModelAdmin):
    list_display = ()
    search_fields = ('cost__sample_return',)

class CostAdmin(admin.ModelAdmin):
    list_display = ('sample_return',)
    search_fields = ('sample_return',)

class DiscountInfoAdmin(admin.ModelAdmin):
    list_display = ('is_faculty_member', 'is_student_or_staff', 'is_affiliated_with_institution', 'discount_institution_name')
    search_fields = ('discount_institution_name',)

admin.site.register(RequestInfo, RequestInfoAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(SampleInfo, SampleInfoAdmin)
admin.site.register(ExperimentInfo, ExperimentInfoAdmin)
admin.site.register(AdditionalInfo, AdditionalInfoAdmin)
admin.site.register(DiscountInfo, DiscountInfoAdmin)
