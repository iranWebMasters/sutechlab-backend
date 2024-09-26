from django.db import models
from accounts.models import Profile
from services.models import Experiment


class RequestInfo(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='کاربر')
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    submission_date = models.DateField(auto_now_add=True, verbose_name='تاریخ ثبت درخواست')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    
    class Meta:
        unique_together = ('user', 'experiment')

class Request(models.Model):
    RequestInfo = models.OneToOneField('RequestInfo', on_delete=models.CASCADE, null=True, blank=True, verbose_name='اطلاعات درخواست')
    SampleInfo = models.OneToOneField('SampleInfo', on_delete=models.CASCADE, null=True, blank=True, verbose_name='اطلاعات نمونه')
    ExperimentInfo = models.OneToOneField('ExperimentInfo', on_delete=models.CASCADE, null=True, blank=True, verbose_name='اطلاعات آزمایش')
    AdditionalInfo = models.OneToOneField('AdditionalInfo', on_delete=models.CASCADE, null=True, blank=True, verbose_name='اطلاعات تکمیلی')
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


class TemporaryRequest(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='کاربر')
    step = models.IntegerField(default=0, verbose_name='مرحله فعلی')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    sample_info = models.JSONField(default=dict, verbose_name='اطلاعات نمونه')
    experiment_info = models.JSONField(default=dict, verbose_name='اطلاعات آزمایش')
    additional_info = models.JSONField(default=dict, verbose_name='اطلاعات تکمیلی')
    finalized = models.BooleanField(default=False, verbose_name='درخواست نهایی شده است؟')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Temporary Request - User: {self.user}, Step: {self.step}"