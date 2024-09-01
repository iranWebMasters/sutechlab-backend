from django.db import models
from django.contrib.auth import get_user_model

class Laboratory(models.Model):
    LOCATION_CHOICES = [
        ('SD', 'صدر'),
        ('SH', 'شیراز'),
    ]
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=2, choices=LOCATION_CHOICES)
    
    def __str__(self):
        return self.name

class Institute(models.Model):
    LOCATION_CHOICES = [
        ('SD', 'صدر'),
        ('SH', 'شیراز'),
    ]
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=2, choices=LOCATION_CHOICES)
    
    def __str__(self):
        return self.name

class Test(models.Model):
    STATUS_CHOICES = [
        ('active', 'فعال'),
        ('inactive', 'غیرفعال'),
    ]
    ISO_CHOICES = [
        ('has', 'دارد'),
        ('has_not', 'ندارد'),
    ]
    
    title = models.CharField(max_length=255)
    laboratory = models.ForeignKey('Laboratory', on_delete=models.CASCADE, related_name='tests')
    institute = models.ForeignKey('Institute', on_delete=models.CASCADE, related_name='tests')
    operator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='institutes')
    iso_17025 = models.CharField(max_length=7, choices=ISO_CHOICES, default='has_not', verbose_name='ISO 17025')
    description = models.TextField()
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.title
