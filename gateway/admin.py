from django.contrib import admin
from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'tracking_code', 'amount', 'status', 'created_at')  # فیلدهایی که در لیست نمایش داده شوند
    list_filter = ('status', 'created_at')  # فیلتر کردن بر اساس این فیلدها
    search_fields = ('tracking_code', 'user__email')  # امکان جستجو در این فیلدها
    ordering = ('-created_at',)  # ترتیب نمایش بر اساس تاریخ ایجاد

# ثبت مدل Payment در ادمین
admin.site.register(Payment, PaymentAdmin)
