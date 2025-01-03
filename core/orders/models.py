from django.conf import settings
from django.db import models
from accounts.models import User
from services.models import Experiment, Test, Parameters
from .utils import generate_order_code
import json


class RequestInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, verbose_name='آزمایش')
    submission_date = models.DateField(auto_now_add=True, verbose_name='تاریخ ثبت درخواست')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    order_code = models.CharField(max_length=255, blank=True, unique=True, verbose_name='کد سفارش')

    def save(self, *args, **kwargs):
        if not self.order_code:
            self.order_code = generate_order_code(self.user.customer_code)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"RequestInfo(ID: {self.id}, User: {self.user.email}, Experiment: {self.experiment.test_name}, Date: {self.submission_date}, Order Code: {self.order_code})"



class SampleInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, verbose_name='آزمایش')

    sample_type = models.CharField(max_length=50, verbose_name='نوع نمونه')
    customer_sample_name = models.CharField(max_length=255, verbose_name='نام نمونه مشتری')
    sample_count = models.PositiveIntegerField(verbose_name='تعداد نمونه')

    # additional_info = models.TextField(blank=True, null=True, verbose_name='توضیحات اضافی')
    # is_perishable = models.BooleanField(null=True, blank=True, default=False, verbose_name='نمونه فاسدشدنی است')
    # expiration_date = models.DateField(null=True, blank=True, verbose_name='تاریخ انقضا')
    # sample_return = models.BooleanField(null=True, blank=True, default=False, verbose_name='نمونه برگشت داده شده بشود')
    # storage_duration = models.PositiveIntegerField(null=True, blank=True, verbose_name='مدت زمان نگهداری (به روز)')
    # storage_duration_unit = models.CharField(null=True, blank=True, max_length=32, verbose_name='واحد مدت زمان نگهداری')

    storage_conditions = models.TextField(blank=True, null=True, verbose_name='شرایط نگهداری')
    sample_description = models.TextField(blank=True, null=True, verbose_name='توضیحات نمونه')
    file_upload = models.FileField(upload_to='sample_files/', blank=True, null=True, verbose_name='فایل تکمیلی نمونه')

    def __str__(self):
        return f"{self.customer_sample_name} , تعداد: {self.sample_count}"

class TestInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, verbose_name='آزمایش')
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
        return f"TestInfo(ID: {self.id}, User: {self.user.email}, Experiment: {self.experiment.test_name}, Sample ID: {self.user_sample.id}, Test: {self.test.name_fa if self.test else 'N/A'})"

class DiscountInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, verbose_name='آزمایش')
    
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
        return f"DiscountInfo(ID: {self.id}, User: {self.user.email}, Experiment: {self.experiment.test_name,})"

class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, verbose_name='آزمایش')
    
    request_info = models.OneToOneField('RequestInfo', on_delete=models.CASCADE, null=True, blank=True, verbose_name='اطلاعات درخواست')
    sample_info = models.ManyToManyField('SampleInfo', related_name='requests', verbose_name='اطلاعات نمونه')
    test_info = models.ManyToManyField('TestInfo', verbose_name='اطلاعات آزمایش')
    discount_info = models.OneToOneField('DiscountInfo', on_delete=models.CASCADE, null=True, blank=True, verbose_name='اطلاعات تخفیف')
    is_complete = models.BooleanField(default=False, verbose_name='تکمیل شده')

    def __str__(self):
        return f"Request(ID: {self.id}, User: {self.user.email}, Experiment: {self.experiment.test_name})"
class LaboratoryRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در حال بررسی'),
        ('successful', 'پرداخت موفق'),
        ('failed', 'پرداخت ناموفق'),
        ('canceled', 'لغو شده'),
        ('ready_for_payment', 'آماده پرداخت'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر', null=True, blank=True)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, verbose_name='آزمایش', null=True, blank=True)
    order_code = models.CharField(max_length=255, blank=True, null=True, unique=True, verbose_name='کد سفارش')
    submission_date = models.DateField(auto_now_add=True, verbose_name='تاریخ ثبت درخواست', null=True, blank=True)
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')

    sample_type = models.CharField(max_length=50, verbose_name='نوع نمونه', null=True, blank=True)
    customer_sample_name = models.CharField(max_length=255, verbose_name='نام نمونه مشتری', null=True, blank=True)
    sample_count = models.PositiveIntegerField(null=True, verbose_name='تعداد نمونه', blank=True)
    additional_info = models.TextField(blank=True, null=True, verbose_name='توضیحات اضافی')
    is_perishable = models.BooleanField(null=True, blank=True, default=False, verbose_name='نمونه فاسدشدنی است')
    expiration_date = models.DateField(null=True, blank=True, verbose_name='تاریخ انقضا')
    sample_return = models.BooleanField(null=True, blank=True, default=False, verbose_name='نمونه برگشت داده شده بشود')
    storage_duration = models.PositiveIntegerField(null=True, blank=True, verbose_name='مدت زمان نگهداری (به روز)')
    storage_duration_unit = models.CharField(null=True, blank=True, max_length=32, verbose_name='واحد مدت زمان نگهداری')
    storage_conditions = models.TextField(blank=True, null=True, verbose_name='شرایط نگهداری')
    sample_description = models.TextField(blank=True, null=True, verbose_name='توضیحات نمونه')
    file_upload = models.FileField(upload_to='sample_files/', blank=True, null=True, verbose_name='فایل تکمیلی نمونه')

    user_sample = models.CharField(max_length=255, verbose_name='شناسه نمونه آزمایش', blank=True, null=True)
    test = models.ForeignKey(Test, blank=True, null=True, on_delete=models.CASCADE, verbose_name='عنوان آزمایش')
    repeat_count_test = models.PositiveIntegerField(verbose_name='تعداد تکرار آزمون', null=True, blank=True)
    parameter = models.ForeignKey(Parameters, on_delete=models.CASCADE, verbose_name='پارامتر', null=True, blank=True)
    parameter_values = models.JSONField(verbose_name='مقادیر پارامتر', null=True, blank=True)

    send_cost = models.BooleanField(default=False, verbose_name='تمایل به پرداخت هزینه ارسال')
    is_faculty_member = models.BooleanField(default=False, verbose_name='آیا کاربر عضو هیات علمی است؟')
    is_student_or_staff = models.BooleanField(default=False, verbose_name='آیا کاربر دانشجو یا کارکنان دانشگاه است؟')
    is_affiliated_with_institution = models.BooleanField(default=False, verbose_name='آیا کاربر متقاضی استفاده از تخفیف نهادهای طرف قرارداد است؟')
    contract_party_file = models.FileField(upload_to='contract_party_files/', blank=True, null=True, verbose_name='فایل نهاد تخفیف')
    
    has_labs_net_grant = models.BooleanField(default=False, verbose_name='آیا کاربر دارای گرنت شبکه آزمایشگاهی است؟')
    labs_net_file = models.FileField(upload_to='labs_net_files/', blank=True, null=True, verbose_name='فایل گرنت شبکه آزمایشگاهی')
    has_research_grant = models.BooleanField(default=False, verbose_name='آیا کاربر دارای گرنت پژوهشی است؟')
    research_grant_withdrawal_amount = models.PositiveIntegerField(blank=True, null=True, verbose_name='میزان استفاده از گرنت پژوهشی')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='وضعیت', null=True, blank=True)
    is_complete = models.BooleanField(default=False, verbose_name='تکمیل شده', null=True, blank=True)
    invoice_pdf = models.FileField(upload_to='invoices/', null=True, blank=True, verbose_name='پیش فاکتور')

    final_price = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name='قیمت نهایی', null=True, blank=True)
    tracking_code = models.CharField(max_length=255, null=False, blank=False, verbose_name='کد پیگیری')

    def __str__(self):
        return f"LaboratoryRequest(ID: {self.id}, User: {self.user.email if self.user else 'N/A'}, Experiment: {self.experiment.test_name if self.experiment else 'N/A'})"
