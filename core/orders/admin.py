from django.contrib import admin
from .models import Order, SampleInfo, TestInfo, DiscountInfo


class SampleInfoInline(admin.TabularInline):
    model = SampleInfo
    extra = 0
    fields = [
        "sample_type",
        "customer_sample_name",
        "sample_count",
        "storage_conditions",
        "sample_description",
        "file_upload",
    ]
    readonly_fields = ["file_upload"]
    help_texts = {
        "sample_type": "نوع نمونه را وارد کنید.",
        "customer_sample_name": "نام نمونه مشتری را وارد کنید.",
        "sample_count": "تعداد نمونه‌ها را وارد کنید.",
        "storage_conditions": "شرایط نگهداری نمونه را وارد کنید.",
        "sample_description": "توضیحات اضافی در مورد نمونه را وارد کنید.",
    }


class TestInfoInline(admin.TabularInline):
    model = TestInfo
    extra = 0
    fields = [
        "user_sample",
        "test",
        "repeat_count_test",
        "parameter",
        "parameter_values",
    ]
    readonly_fields = ["parameter_values"]
    help_texts = {
        "user_sample": "انتخاب نمونه آزمایش.",
        "test": "عنوان آزمایش را انتخاب کنید.",
        "repeat_count_test": "تعداد تکرار آزمایش را وارد کنید.",
        "parameter": "پارامترهای مربوط به آزمایش را انتخاب کنید.",
        "parameter_values": "مقادیر پارامترها را وارد کنید.",
    }


class DiscountInfoInline(admin.TabularInline):
    model = DiscountInfo
    extra = 0
    fields = [
        "send_cost",
        "is_faculty_member",
        "is_student_or_staff",
        "is_affiliated_with_institution",
        "contract_party_file",
        "has_labs_net_grant",
        "labs_net_file",
        "has_research_grant",
        "research_grant_withdrawal_amount",
    ]
    readonly_fields = ["contract_party_file", "labs_net_file"]
    help_texts = {
        "send_cost": "آیا مایل به پرداخت هزینه ارسال هستید؟",
        "is_faculty_member": "آیا کاربر عضو هیات علمی است؟",
        "is_student_or_staff": "آیا کاربر دانشجو یا کارکنان دانشگاه است؟",
        "is_affiliated_with_institution": "آیا کاربر متقاضی استفاده از تخفیف نهادهای طرف قرارداد است؟",
        "has_labs_net_grant": "آیا کاربر دارای گرنت شبکه آزمایشگاهی است؟",
        "has_research_grant": "آیا کاربر دارای گرنت پژوهشی است؟",
    }


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "experiment",
        "status",
        "current_step",
        "is_complete",
        "order_code",
        "created_at",
        "final_price",
        "tracking_code",
    ]
    list_filter = ["status", "is_complete", "created_at", "experiment"]
    search_fields = ["order_code", "user__email", "experiment__test_name"]
    inlines = [SampleInfoInline, TestInfoInline, DiscountInfoInline]

    fieldsets = (
        (
            "اطلاعات سفارش",
            {
                "fields": (
                    "user",
                    "experiment",
                    "description",
                    "status",
                    "current_step",
                    "is_complete",
                    "order_code",
                    "invoice_pdf",
                    "final_price",
                    "tracking_code",
                )
            },
        ),
        (
            "تاریخ‌ها",
            {
                "fields": ("created_at",),
            },
        ),
    )
    readonly_fields = ["order_code", "created_at", "invoice_pdf"]

    # Adding custom styling for the admin panel
    class Media:
        css = {
            "all": (
                "admin/css/custom_admin.css",
            )  # Ensure to create this CSS file for custom styles
        }
        js = (
            "admin/js/custom_admin.js",
        )  # Ensure to create this JS file for custom scripts

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            "user", "experiment"
        )  # Optimize queries by using select_related


# Registering the OrderAdmin class with the Order model
admin.site.register(Order, OrderAdmin)
