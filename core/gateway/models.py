from django.db import models
from django.conf import settings
from orders.models import LaboratoryRequest

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در حال انتظار'),
        ('completed', 'تکمیل شده'),
        ('failed', 'ناموفق'),
    ]

    laboratory_request = models.ForeignKey(LaboratoryRequest, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    
    tracking_code = models.CharField(max_length=255,null=False, blank=False, verbose_name='Tracking Code')
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment {self.id} - {self.amount} - {self.status}'