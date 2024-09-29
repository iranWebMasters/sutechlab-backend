from django.db import models
from accounts.models import User
from services.models import Experiment
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
    SAMPLE_TYPE_CHOICES = [
        ('vacuum_oven', 'Vacuum Oven'),
        ('oven', 'Oven'),
        ('sieve_sample', 'نمونه دانه بندی (الک)'),
    ]

    WEIGHT_CHOICES = [
        ('KG', 'کیلوگرم'),
        ('G', 'گرم'),
        ('MG', 'میلی‌گرم'),
        ('LB', 'پوند'),
        ('OZ', 'اونس'),
    ]
    request = models.ForeignKey('Request', on_delete=models.CASCADE, related_name='sample_infos', verbose_name='درخواست')
    sample_type = models.CharField(max_length=50, choices=SAMPLE_TYPE_CHOICES, verbose_name='نوع نمونه')
    sample_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='مقدار نمونه')
    sample_unit = models.CharField(max_length=50, choices=WEIGHT_CHOICES, verbose_name='واحد اندازه‌گیری')
    additional_info = models.TextField(blank=True, null=True, verbose_name='توضیحات اضافی')
    is_perishable = models.BooleanField(default=False, verbose_name='نمونه فاسدشدنی است')
    expiration_date = models.DateField(null=True, blank=True, verbose_name='تاریخ انقضا')
    sample_return = models.BooleanField(default=False, verbose_name='نمونه برگشت داده شده بشود')
    storage_duration = models.IntegerField(null=True, blank=True, verbose_name='مدت زمان نگهداری (به روز)')
    storage_unit = models.CharField(max_length=10, choices=[('D', 'روز'), ('W', 'هفته'), ('M', 'ماه')], verbose_name='واحد مدت زمان نگهداری')
    
class ExperimentInfo(models.Model):
    ...
class AdditionalInfo(models.Model):
    ...

class DiscountInfo(models.Model):
    is_faculty_member = models.BooleanField(default=False)  # آیا کاربر عضو هیات علمی است؟
    is_student_or_staff = models.BooleanField(default=False)  # آیا کاربر دانشجو یا کارکنان دانشگاه است؟
    is_affiliated_with_institution = models.BooleanField(default=False)  # آیا کاربر متقاضی استفاده از تخفیف نهادهای طرف قرارداد است؟
    discount_institution_name = models.CharField(max_length=255, blank=True)  # نام نهاد تخفیف
