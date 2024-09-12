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
    currency = models.CharField(max_length=5, choices=CURRENCY_CHOICES, default='IRR', verbose_name='واحد پول')

    def __str__(self):
        return f"{self.unit_price} {self.get_currency_display()}"

class Parameters(models.Model):
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
        return f"{self.name} ({self.get_unit_display()}) - {self.unit_amount} - {self.unit_price}"

class Laboratory(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام آزمایشگاه')
    faculty = models.ForeignKey('Faculty', on_delete=models.CASCADE, related_name='experiments', verbose_name='دانشکده')
    technical_manager = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='managed_laboratories', verbose_name='مدیر فنی')
    
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
        return f"{self.name} ({self.get_location_display()})"

class ExperimentSpecification(models.Model):
    UNIT_TYPE_CHOICES = [
        ('EQ', 'دستگاه'),
        ('CM', 'کامپیوتر'),
        ('MA', 'ماشین'),
    ]
    
    name_fa = models.CharField(max_length=255, verbose_name='نام فارسی آزمون')
    name_en = models.CharField(max_length=255, verbose_name='نام انگلیسی آزمون')
    unit_type = models.CharField(max_length=2, choices=UNIT_TYPE_CHOICES, verbose_name='نوع واحد آزمون')
    operating_range = models.TextField(verbose_name='گستره کاری')
    description = models.TextField(verbose_name='توصیف آزمون')

    def __str__(self):
        return f"{self.name_fa} / {self.name_en}"

class Standards(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام استاندارد')
    description = models.TextField(verbose_name='توصیف استاندارد')

    def __str__(self):
        return self.name

class Sample(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام نمونه')
    description = models.TextField(verbose_name='توصیف نمونه')

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
    
    laboratory = models.ForeignKey('Laboratory', on_delete=models.CASCADE, related_name='experiments', verbose_name='آزمایشگاه')
    samples = models.ManyToManyField(Sample, related_name='experiments', verbose_name='نمونه‌ها') 
    experiment = models.ForeignKey(ExperimentSpecification, on_delete=models.CASCADE, related_name='experiments', verbose_name='مشخصات آزمایش')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='experiments', verbose_name='دستگاه')
    standards = models.ManyToManyField(Standards, related_name='experiments', verbose_name='استانداردها')  # Updated line for many-to-many relationship
    operator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experiments', verbose_name='اپراتور')
    parameters = models.ManyToManyField(Parameters, related_name='experiments', verbose_name='پارامتر ها')
    iso_17025 = models.CharField(max_length=7, choices=ISO_CHOICES, default='has_not', verbose_name='ISO 17025')
    request_type = models.CharField(max_length=50, verbose_name='نوع درخواست')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active', verbose_name='وضعیت')
    created_date = models.DateField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_date = models.DateField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    def __str__(self):
        return f"Experiment in {self.laboratory.name} - {self.experiment.name_en} ({self.status})"