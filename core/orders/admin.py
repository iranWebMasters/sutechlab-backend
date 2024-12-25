from django.contrib import admin
from .models import RequestInfo, Request, SampleInfo, DiscountInfo, TestInfo,LaboratoryRequest
from django.utils.html import format_html

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
    list_display = (
        'user',  # Assuming you want to display the user email
        'experiment',  # Assuming you want to display the experiment name
        'send_cost',
        'is_faculty_member',
        'is_student_or_staff',
        'is_affiliated_with_institution',
        'has_labs_net_grant',
        'has_research_grant',
        'research_grant_withdrawal_amount',
    )
    
    search_fields = (
        'user__email',  # Assuming you want to search by user email
        'experiment__test_name',  # Assuming you want to search by experiment name
        # Optional: Add new fields if necessary
    )
    
    list_filter = (
        'is_faculty_member',
        'is_student_or_staff',
        'is_affiliated_with_institution',
        'has_labs_net_grant',
        'has_research_grant',
    )


class TestInformationAdmin(admin.ModelAdmin):
    list_display = ('user', 'experiment', 'user_sample', 'test', 'repeat_count_test', 'created_at', 'updated_at')
    search_fields = ('user__email', 'experiment__name', 'user_sample__customer_sample_name', 'test__name')
    list_filter = ('experiment', 'test', 'created_at')
    ordering = ('-created_at',)

    def get_readonly_fields(self, request, obj=None):
        # اگر شیء وجود داشته باشد، فیلدهای فقط خواندنی را برمی‌گرداند
        if obj is not None:
            return super().get_readonly_fields(request, obj) + ('parameter_values_display',)
        return super().get_readonly_fields(request, obj)

    def parameter_values_display(self, obj):
        if obj:
            param_dict = obj.get_parameter_values_dict()  # فرض بر این است که متد get_parameter_values_dict در مدل وجود دارد
            return format_html('<br><br>'.join([f"<strong>{key}:</strong> {value}" for key, value in param_dict.items()]))  # نمایش به صورت HTML
        return "No parameter values available"
    
    parameter_values_display.short_description = 'Parameter Values'  # عنوان برای نمایش در پنل


class LaboratoryRequestAdmin(admin.ModelAdmin):
    ...


# Registering the models with their admin classes
admin.site.register(RequestInfo, RequestInfoAdmin)
admin.site.register(LaboratoryRequest, LaboratoryRequestAdmin)
admin.site.register(SampleInfo, SampleInfoAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(DiscountInfo, DiscountInfoAdmin)
admin.site.register(TestInfo, TestInformationAdmin)
