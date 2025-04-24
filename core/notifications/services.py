from django.core.mail import send_mail
from notifications.models import Notification, NotificationLog

from django.db import transaction


def send_email_notification(user, subject, message):
    """ارسال ایمیل به کاربر"""
    try:
        send_mail(subject, message, "noreply@example.com", [user.email])

        # ذخیره لاگ در یک بلاک اتمیک جداگانه
        with transaction.atomic():
            NotificationLog.objects.create(
                user=user, notification_type="email", status="sent", message=message
            )
    except Exception as e:
        with transaction.atomic():
            NotificationLog.objects.create(
                user=user, notification_type="email", status="failed", message=str(e)
            )


def send_sms_notification(user, message):
    """ارسال پیامک به کاربر (فرض: شما از یک API پیامک استفاده می‌کنید)"""
    try:
        # کد ارسال پیامک با API مربوطه
        NotificationLog.objects.create(
            user=user, notification_type="sms", status="sent", message=message
        )
    except Exception as e:
        NotificationLog.objects.create(
            user=user, notification_type="sms", status="failed", message=str(e)
        )


def create_panel_notification(user, title, message):
    """ایجاد اعلان در پنل کاربری"""
    Notification.objects.create(user=user, title=title, message=message)
