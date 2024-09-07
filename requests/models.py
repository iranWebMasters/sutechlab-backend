from django.db import models
from accounts.models import Profile

class Request(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='کاربر')
    request_type = models.CharField(max_length=50, verbose_name='نوع درخواست')
    submission_date = models.DateField(auto_now_add=True, verbose_name='تاریخ ثبت درخواست') 
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')


class Sample(models.Model):
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

    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='samples', verbose_name='درخواست')  # ForeignKey به مدل Request
    sample_type = models.CharField(max_length=50, choices=SAMPLE_TYPE_CHOICES, verbose_name='نوع نمونه')
    sample_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='مقدار نمونه')
    sample_unit = models.CharField(max_length=50, choices=WEIGHT_CHOICES, verbose_name='واحد اندازه‌گیری')
    additional_info = models.TextField(blank=True, null=True, verbose_name='توضیحات اضافی')
    is_perishable = models.BooleanField(default=False, verbose_name='نمونه فاسدشدنی است')
    expiration_date = models.DateField(null=True, blank=True, verbose_name='تاریخ انقضا')
    storage_duration = models.IntegerField(null=True, blank=True, verbose_name='مدت زمان نگهداری (به روز)')
    storage_unit = models.CharField(max_length=10, choices=[('D', 'روز'), ('W', 'هفته'), ('M', 'ماه')], verbose_name='واحد مدت زمان نگهداری')

    def __str__(self):
        return f"Sample of {self.get_sample_type_display()} for Request {self.request.id}"