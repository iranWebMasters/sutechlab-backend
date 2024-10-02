from django.db import models
from accounts.models import User
from services.models import Experiment,Sample,Test
from django.conf import settings


class RequestInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    submission_date = models.DateField(auto_now_add=True, verbose_name='تاریخ ثبت درخواست')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')

class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    requestinfo = models.OneToOneField('RequestInfo', on_delete=models.CASCADE, null=True, blank=True, verbose_name='اطلاعات درخواست')
    sample_info = models.ManyToManyField('SampleInfo', related_name='requests', verbose_name='اطلاعات نمونه')
    experimentinfo = models.OneToOneField('ExperimentInfo', on_delete=models.CASCADE, null=True, blank=True, verbose_name='اطلاعات آزمایش')
    additional_info = models.OneToOneField('AdditionalInfo', on_delete=models.CASCADE, null=True, blank=True, verbose_name='اطلاعات تکمیلی')
# -------------------------------

class SampleInfo(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    
    # Required fields
    sample_type = models.CharField(max_length=50,verbose_name='نوع نمونه')  # Sample type
    customer_sample_name = models.CharField(max_length=255, verbose_name='نام نمونه مشتری')  # Customer sample name
    sample_count = models.PositiveIntegerField(verbose_name='تعداد نمونه')  # Sample count

    # Optional fields
    sample_unit = models.CharField(null=True, blank=True,max_length=50, verbose_name='واحد اندازه‌گیری')  # Measurement unit
    additional_info = models.TextField(blank=True, null=True, verbose_name='توضیحات اضافی')  # Additional info
    is_perishable = models.BooleanField(null=True, blank=True,default=False, verbose_name='نمونه فاسدشدنی است')  # Is perishable
    expiration_date = models.DateField(null=True, blank=True, verbose_name='تاریخ انقضا')  # Expiration date
    sample_return = models.BooleanField(null=True, blank=True,default=False, verbose_name='نمونه برگشت داده شده بشود')  # Sample return
    storage_duration = models.PositiveIntegerField(null=True, blank=True, verbose_name='مدت زمان نگهداری (به روز)')  # Storage duration in days
    storage_duration_unit = models.CharField(null=True, blank=True,max_length=32,verbose_name='واحد مدت زمان نگهداری')  # Storage duration unit

    # New fields to match the form
    storage_conditions = models.TextField(blank=True, null=True, verbose_name='شرایط نگهداری')  # Storage conditions
    sample_description = models.TextField(blank=True, null=True, verbose_name='توضیحات نمونه')  # Sample description
    file_upload = models.FileField(upload_to='sample_files/', blank=True, null=True, verbose_name='فایل تکمیلی نمونه')  # File upload

    def __str__(self):
        return f"{self.customer_sample_name} - {self.sample_type} ({self.sample_count})"
    
class ExperimentInfo(models.Model):
    ...
class AdditionalInfo(models.Model):
    ...

class DiscountInfo(models.Model):
    is_faculty_member = models.BooleanField(default=False)  # آیا کاربر عضو هیات علمی است؟
    is_student_or_staff = models.BooleanField(default=False)  # آیا کاربر دانشجو یا کارکنان دانشگاه است؟
    is_affiliated_with_institution = models.BooleanField(default=False)  # آیا کاربر متقاضی استفاده از تخفیف نهادهای طرف قرارداد است؟
    discount_institution_name = models.CharField(max_length=255, blank=True)  # نام نهاد تخفیف


class TestInformation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, verbose_name='شناسه نمونه آزمایش')  # کلید خارجی به مدل Sample
    test = models.ForeignKey(Test, blank=True, null=True, on_delete=models.CASCADE, verbose_name='عنوان آزمایش')  # کلید خارجی به مدل Test

    repeat_count_test = models.PositiveIntegerField(verbose_name='تعداد تکرار آزمون')  # تعداد تکرار آزمون
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')  # تاریخ ایجاد
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')  # تاریخ به‌روزرسانی

    def __str__(self):
        return f"Request ID: {self.id} - Sample ID: {self.sample.id}"