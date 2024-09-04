from django.db import models
from accounts.models import Profile
from devices.models import Device

class Unit_amount(models.Model):
    UNIT_CHOICES = [
        ('C', 'سانتی گراد'),
        ('F', 'فارنهایت'),
        ('K', 'کلوین'),
        ('H', 'ساعت'),
        ('MIN', 'دقیقه'),
        ('S', 'ثانیه'),
    ]
    
    amount = models.CharField(max_length=50, verbose_name='مقدار')
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES, verbose_name='واحد اندازه‌گیری')

    def __str__(self):
        return f"{self.amount} {self.get_unit_display()}"

class Unit_price(models.Model):
    CURRENCY_CHOICES = [
        ('IRR', 'ریال'),
        ('Toman', 'تومان'),
    ]

    unit_price = models.DecimalField(max_digits=15, decimal_places=0, verbose_name='مبلغ واحد')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='IRR', verbose_name='واحد پول')

    def __str__(self):
        return f"{self.unit_price} {self.get_currency_display()}"

class Parameter(models.Model):
    UNIT_CHOICES = [
        ('C', 'سانتی گراد'),
        ('F', 'فارنهایت'),
        ('K', 'کلوین'),
        ('H', 'ساعت'),
        ('MIN', 'دقیقه'),
        ('S', 'ثانیه'),
    ]

    name = models.CharField(max_length=255, verbose_name='نام پارامتر')
    unit = models.CharField(max_length=50, choices=UNIT_CHOICES, verbose_name='واحد اندازه‌گیری')
    laboratory = models.ForeignKey('Laboratory', on_delete=models.CASCADE, related_name='tests', verbose_name='آزمایشگاه')
    unit_amount = models.ForeignKey('Unit_amount', on_delete=models.CASCADE, related_name='parameters', verbose_name='مقدار واحد')
    unit_price = models.ForeignKey('Unit_price', on_delete=models.CASCADE, related_name='parameters', verbose_name='مبلغ واحد')

    def __str__(self):
        return f"{self.name} - {self.get_unit_display()} - {self.unit_amount} - {self.unit_price}"

class Laboratory(models.Model):
    LOCATION_CHOICES = [
        ('SD', 'صدرا'),
        ('SH', 'شیراز'),
    ]
    name = models.CharField(max_length=255, verbose_name='نام آزمایشگاه')
    location = models.CharField(max_length=2, choices=LOCATION_CHOICES, verbose_name='مکان')

    def __str__(self):
        return self.name

class Faculty(models.Model):
    LOCATION_CHOICES = [
        ('SD', 'صدرا'),
        ('SH', 'شیراز'),
    ]
    name = models.CharField(max_length=255, verbose_name='نام دانشکده')
    location = models.CharField(max_length=2, choices=LOCATION_CHOICES, verbose_name='مکان')

    def __str__(self):
        return self.name

class Experiment(models.Model):
    STATUS_CHOICES = [
        ('active', 'فعال'),
        ('inactive', 'غیرفعال'),
    ]
    ISO_CHOICES = [
        ('has', 'دارد'),
        ('has_not', 'ندارد'),
    ]
    
    title = models.CharField(max_length=255, verbose_name='عنوان آزمایش')
    laboratory = models.ForeignKey('Laboratory', on_delete=models.CASCADE, related_name='experiments', verbose_name='آزمایشگاه')
    faculty = models.ForeignKey('Faculty', on_delete=models.CASCADE, related_name='experiments', verbose_name='دانشکده')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='experiments', verbose_name='دستگاه')
    operator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experiments', verbose_name='اپراتور')
    iso_17025 = models.CharField(max_length=7, choices=ISO_CHOICES, default='has_not', verbose_name='ISO 17025')
    description = models.TextField(verbose_name='توضیحات')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active', verbose_name='وضعیت')
    created_date = models.DateField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_date = models.DateField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    def __str__(self):
        return self.title
