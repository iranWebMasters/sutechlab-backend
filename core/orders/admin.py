from django.contrib import admin
from .models import Order, SampleInfo, TestInfo, DiscountInfo

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'experiment', 'status', 'is_complete', 'created_at')
    search_fields = ('order_code', 'user__email', 'experiment__test_name')
    list_filter = ('status', 'is_complete')
    ordering = ('-created_at',)

@admin.register(SampleInfo)
class SampleInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'sample_type', 'customer_sample_name', 'sample_count')
    search_fields = ('customer_sample_name', 'sample_type')
    list_filter = ('is_perishable',)
    ordering = ('-order',)

@admin.register(TestInfo)
class TestInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'user_sample', 'test', 'repeat_count_test', 'created_at')
    search_fields = ('order__order_code', 'user_sample__customer_sample_name', 'test__name_fa')
    list_filter = ('test',)
    ordering = ('-created_at',)

@admin.register(DiscountInfo)
class DiscountInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'is_faculty_member', 'is_student_or_staff', 'has_labs_net_grant')
    search_fields = ('order__order_code', 'order__user__email')
    list_filter = ('is_faculty_member', 'is_student_or_staff', 'has_labs_net_grant')
    ordering = ('-order',)