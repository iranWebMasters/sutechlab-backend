from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Profile
from devices.models import Device

class Laboratory(models.Model):
    LOCATION_CHOICES = [
        ('SD', 'صدرا'),
        ('SH', 'شیراز'),
    ]
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=2, choices=LOCATION_CHOICES)
    
    def __str__(self):
        return self.name

class Faculty(models.Model):
    LOCATION_CHOICES = [
        ('SD', 'صدرا'),
        ('SH', 'شیراز'),
    ]
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=2, choices=LOCATION_CHOICES)
    
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
    
    title = models.CharField(max_length=255)
    laboratory = models.ForeignKey('Laboratory', on_delete=models.CASCADE, related_name='tests')
    faculty = models.ForeignKey('Faculty', on_delete=models.CASCADE, related_name='tests')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='tests')
    operator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='institutes')
    iso_17025 = models.CharField(max_length=7, choices=ISO_CHOICES, default='has_not', verbose_name='ISO 17025')
    description = models.TextField()
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.title
