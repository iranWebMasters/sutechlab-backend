from django.conf import settings
from django.db import models
from accounts.models import User
from services.models import Experiment, Test, Parameters


class RequestInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    submission_date = models.DateField(auto_now_add=True, verbose_name='تاریخ ثبت درخواست')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')

    def __str__(self):
        return f"RequestInfo(ID: {self.id}, User: {self.user.email}, Experiment: {self.experiment.test_name}, Date: {self.submission_date})"


class SampleInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)

    # Required fields
    sample_type = models.CharField(max_length=50, verbose_name='نوع نمونه')  # Sample type
    customer_sample_name = models.CharField(max_length=255, verbose_name='نام نمونه مشتری')  # Customer sample name
    sample_count = models.PositiveIntegerField(verbose_name='تعداد نمونه')  # Sample count

    # Optional fields
    additional_info = models.TextField(blank=True, null=True, verbose_name='توضیحات اضافی')  # Additional info
    is_perishable = models.BooleanField(null=True, blank=True, default=False, verbose_name='نمونه فاسدشدنی است')  # Is perishable
    expiration_date = models.DateField(null=True, blank=True, verbose_name='تاریخ انقضا')  # Expiration date
    sample_return = models.BooleanField(null=True, blank=True, default=False, verbose_name='نمونه برگشت داده شده بشود')  # Sample return
    storage_duration = models.PositiveIntegerField(null=True, blank=True, verbose_name='مدت زمان نگهداری (به روز)')  # Storage duration in days
    storage_duration_unit = models.CharField(null=True, blank=True, max_length=32, verbose_name='واحد مدت زمان نگهداری')  # Storage duration unit

    # New fields to match the form
    storage_conditions = models.TextField(blank=True, null=True, verbose_name='شرایط نگهداری')  # Storage conditions
    sample_description = models.TextField(blank=True, null=True, verbose_name='توضیحات نمونه')  # Sample description
    file_upload = models.FileField(upload_to='sample_files/', blank=True, null=True, verbose_name='فایل تکمیلی نمونه')  # File upload

    def __str__(self):
        return f"SampleInfo(ID: {self.id}, Customer Sample: {self.customer_sample_name}, Type: {self.sample_type}, Count: {self.sample_count})"


class TestInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    user_sample = models.ForeignKey(SampleInfo, on_delete=models.CASCADE, verbose_name='شناسه نمونه آزمایش')
    test = models.ForeignKey(Test, blank=True, null=True, on_delete=models.CASCADE, verbose_name='عنوان آزمایش')

    repeat_count_test = models.PositiveIntegerField(verbose_name='تعداد تکرار آزمون')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    parameter = models.ForeignKey(Parameters, on_delete=models.CASCADE, verbose_name='پارامتر')
    parameter_value = models.CharField(max_length=255, verbose_name='مقدار پارامتر')

    def __str__(self):
        return f"TestInfo(ID: {self.id}, User: {self.user.email}, Experiment: {self.experiment.test_name}, Sample ID: {self.user_sample.id}, Test: {self.test.name_fa if self.test else 'N/A'})"


class DiscountInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    is_faculty_member = models.BooleanField(default=False)  # آیا کاربر عضو هیات علمی است؟
    is_student_or_staff = models.BooleanField(default=False)  # آیا کاربر دانشجو یا کارکنان دانشگاه است؟
    is_affiliated_with_institution = models.BooleanField(default=False)  # آیا کاربر متقاضی استفاده از تخفیف نهادهای طرف قرارداد است؟
    discount_institution_name = models.CharField(max_length=255, blank=True)  # نام نهاد تخفیف

    def __str__(self):
        return f"RequestInfo(ID: {self.id}, User: {self.user.email}, Experiment: {self.experiment.test_name},)"

class Request(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در حال بررسی'),        # در حال بررسی
        ('successful', 'پرداخت موفق'),     # پرداخت موفق
        ('failed', 'پرداخت ناموفق'),       # پرداخت ناموفق
        ('canceled', 'لغو شده'),           # لغو شده
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, verbose_name='آزمایش')
    
    request_info = models.OneToOneField('RequestInfo', on_delete=models.CASCADE, null=True, blank=True, verbose_name='اطلاعات درخواست')
    sample_info = models.ManyToManyField('SampleInfo', related_name='requests', verbose_name='اطلاعات نمونه')
    test_info = models.ManyToManyField('TestInfo', verbose_name='اطلاعات آزمایش')
    discount_info = models.OneToOneField('DiscountInfo', on_delete=models.CASCADE, null=True, blank=True, verbose_name='اطلاعات تخفیف')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='وضعیت')  # وضعیت پیش‌فرض "در حال بررسی"
    invoice_pdf = models.FileField(upload_to='invoices/', null=True, blank=True, verbose_name='پیش فاکتور')

    def __str__(self):
        return f"Request(ID: {self.id}, User: {self.user.email}, Experiment: {self.experiment.test_name})"

