from django.db import models
from accounts.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.title}"
    
class NotificationLog(models.Model):
    TYPE_CHOICES = [
        ('email', 'ایمیل'),
        ('sms', 'پیامک'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_logs')
    notification_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=[
        ('sent', 'ارسال شده'),
        ('failed', 'ارسال ناموفق'),
    ])
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.notification_type} - {self.status}"
