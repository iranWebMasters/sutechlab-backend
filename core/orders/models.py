from django.conf import settings
from django.db import models
from accounts.models import User
from services.models import Experiment, Test, Parameters
from .utils import generate_order_code
import json

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در حال بررسی'),
        ('successful', 'پرداخت موفق'),
        ('failed', 'پرداخت ناموفق'),
        ('canceled', 'لغو شده'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, verbose_name='آزمایش')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='وضعیت')
    is_complete = models.BooleanField(default=False, verbose_name='تکمیل شده')
    order_code = models.CharField(max_length=255, blank=True, unique=True, verbose_name='کد سفارش')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    def save(self, *args, **kwargs):
        if not self.order_code:
            self.order_code = generate_order_code(self.user.customer_code)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Request(ID: {self.id}, User: {self.user.email}, Experiment: {self.experiment.test_name})"

    class Meta:
        verbose_name = 'درخواست'
        verbose_name_plural = 'درخواست‌ها'

class SampleInfo(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='sample_info')
    sample_type = models.CharField(max_length=50, verbose_name='نوع نمونه')
    customer_sample_name = models.CharField(max_length=255, verbose_name='نام نمونه مشتری')
    sample_count = models.PositiveIntegerField(verbose_name='تعداد نمونه')

    additional_info = models.TextField(blank=True, null=True, verbose_name='توضیحات اضافی')
    is_perishable = models.BooleanField(null=True, blank=True, default=False, verbose_name='نمونه فاسدشدنی است')
    expiration_date = models.DateField(null=True, blank=True, verbose_name='تاریخ انقضا')
    sample_return = models.BooleanField(null=True, blank=True, default=False, verbose_name='نمونه برگشت داده شده بشود')
    storage_duration = models.PositiveIntegerField(null=True, blank=True, verbose_name='مدت زمان نگهداری (به روز)')
    storage_duration_unit = models.CharField(null=True, blank=True, max_length=32, verbose_name='واحد مدت زمان نگهداری')

    storage_conditions = models.TextField(blank=True, null=True, verbose_name='شرایط نگهداری')
    sample_description = models.TextField(blank=True, null=True, verbose_name='توضیحات نمونه')
    file_upload = models.FileField(upload_to='sample_files/', blank=True, null=True, verbose_name='فایل تکمیلی نمونه')

    def __str__(self):
        return f"SampleInfo(ID: {self.id}, Customer Sample: {self.customer_sample_name}, Type: {self.sample_type}, Count: {self.sample_count})"

    class Meta:
        verbose_name = 'اطلاعات نمونه'
        verbose_name_plural = 'اطلاعات نمونه‌ها'


class TestInfo(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='test_info')
    user_sample = models.ForeignKey(SampleInfo, on_delete=models.CASCADE, verbose_name='شناسه نمونه آزمایش')
    test = models.ForeignKey(Test, blank=True, null=True, on_delete=models.CASCADE, verbose_name='عنوان آزمایش')

    repeat_count_test = models.PositiveIntegerField(verbose_name='تعداد تکرار آزمون')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    parameter = models.ForeignKey(Parameters, on_delete=models.CASCADE, verbose_name='پارامتر')
    parameter_values = models.JSONField(verbose_name='مقادیر پارامتر') 

    def get_parameter_values_dict(self):
        try:
            return json.loads(self.parameter_values)
        except json.JSONDecodeError:
            return {}

    def __str__(self):
        return f"TemporaryTestInfo(ID: {self.id}, User: {self.user.email}, Experiment: {self.experiment.test_name}, Sample ID: {self.user_sample.id}, Test: {self.test.name_fa if self.test else 'N/A'})"

    class Meta:
        verbose_name = 'اطلاعات آزمایش'
        verbose_name_plural = 'اطلاعات آزمایش‌ها'


class DiscountInfo(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='discount_info')
    
    send_cost = models.BooleanField(default=False, verbose_name='تمایل به پرداخت هزینه ارسال')
    is_faculty_member = models.BooleanField(default=False, verbose_name='آیا کاربر عضو هیات علمی است؟')
    is_student_or_staff = models.BooleanField(default=False, verbose_name='آیا کاربر دانشجو یا کارکنان دانشگاه است؟')
    is_affiliated_with_institution = models.BooleanField(default=False, verbose_name='آیا کاربر متقاضی استفاده از تخفیف نهادهای طرف قرارداد است؟')
    contract_party_file = models.FileField(upload_to='contract_party_files/', blank=True, null=True, verbose_name='فایل نهاد تخفیف')
    
    has_labs_net_grant = models.BooleanField(default=False, verbose_name='آیا کاربر دارای گرنت شبکه آزمایشگاهی است؟')
    labs_net_file = models.FileField(upload_to='labs_net_files/', blank=True, null=True, verbose_name='فایل گرنت شبکه آزمایشگاهی')
    has_research_grant = models.BooleanField(default=False, verbose_name='آیا کاربر دارای گرنت پژوهشی است؟')
    research_grant_withdrawal_amount = models.PositiveIntegerField(blank=True, null=True, verbose_name='میزان استفاده از گرنت پژوهشی')

    def __str__(self):
        return f"TemporaryDiscountInfo(ID: {self.id}, User: {self.user.email}, Experiment: {self.experiment.test_name,})"

    class Meta:
        verbose_name = 'اطلاعات تخفیف'
        verbose_name_plural = 'اطلاعات تخفیف‌ها'
