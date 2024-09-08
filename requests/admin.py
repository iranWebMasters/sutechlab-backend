from django.contrib import admin
from .models import Request, Sample

class SampleInline(admin.TabularInline):
    model = Sample
    extra = 1  # تعداد فرم‌های اضافی برای اضافه کردن نمونه‌ها

class RequestAdmin(admin.ModelAdmin):
    list_display = ('request_type', 'submission_date', 'user')
    search_fields = ('request_type',)
    list_filter = ('request_type', 'submission_date')
    inlines = [SampleInline]  # اضافه کردن نمونه‌ها به فرم درخواست

admin.site.register(Request, RequestAdmin)
admin.site.register(Sample)