from django.contrib import admin
from .models import RequestInfo, Request, SampleInfo, DiscountInfo, TestInfo,LaboratoryRequest


class RequestInfoAdmin(admin.ModelAdmin):   
    list_display = ('user', 'experiment', 'submission_date', 'description')
    search_fields = ('user__email', 'experiment__name', 'description')
    list_filter = ('submission_date', 'experiment')
    ordering = ('-submission_date',)


class SampleInfoAdmin(admin.ModelAdmin):
    list_display = ('customer_sample_name', 'sample_type', 'sample_count', 'is_perishable', 'expiration_date')
    search_fields = ('customer_sample_name', 'sample_type')
    list_filter = ('is_perishable', 'expiration_date')
    ordering = ('-expiration_date',)


class RequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'request_info','discount_info')
    search_fields = ('user__email',)
    ordering = ('user',)
    filter_horizontal = ('sample_info','test_info',)


class DiscountInfoAdmin(admin.ModelAdmin):
    list_display = ('is_faculty_member', 'is_student_or_staff', 'is_affiliated_with_institution', 'discount_institution_name')
    search_fields = ('discount_institution_name',)
    list_filter = ('is_faculty_member', 'is_student_or_staff', 'is_affiliated_with_institution')


class TestInformationAdmin(admin.ModelAdmin):
    list_display = ('user', 'experiment', 'user_sample', 'test', 'repeat_count_test', 'created_at', 'updated_at')
    search_fields = ('user__email', 'experiment__name', 'user_sample__customer_sample_name', 'test__name')
    list_filter = ('experiment', 'test', 'created_at')
    ordering = ('-created_at',)

class LaboratoryRequestAdmin(admin.ModelAdmin):
    ...


# Registering the models with their admin classes
admin.site.register(RequestInfo, RequestInfoAdmin)
admin.site.register(LaboratoryRequest, LaboratoryRequestAdmin)
admin.site.register(SampleInfo, SampleInfoAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(DiscountInfo, DiscountInfoAdmin)
admin.site.register(TestInfo, TestInformationAdmin)
