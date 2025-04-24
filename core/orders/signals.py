from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.services import (
    send_email_notification,
    send_sms_notification,
    create_panel_notification,
)
from .invoices import generate_invoice
from .models import Order

# @receiver(post_save, sender=Order)
# def create_invoice(sender, instance, created, **kwargs):
#     if not created and instance.is_complete and not instance.invoice_pdf:
#         pdf_file_path = generate_invoice(instance)
#         instance.invoice_pdf = pdf_file_path
#         instance.save()

# @receiver(post_save, sender=Order)
# def update_invoice(sender, instance, created, **kwargs):
#     if not created and instance.is_complete:
#         if not instance.invoice_pdf:
#             pdf_file_path = generate_invoice(instance)
#             instance.invoice_pdf = pdf_file_path
#             instance.save(update_fields=['invoice_pdf'])


@receiver(post_save, sender=Order)
def handle_order_notifications(sender, instance, created, **kwargs):
    if created:
        subject = "سفارش جدید شما ثبت شد"
        message = f"سفارش شما با کد {instance.order_code} با موفقیت ثبت شد."
        send_email_notification(instance.user, subject, message)
        send_sms_notification(instance.user, message)
        create_panel_notification(instance.user, "سفارش جدید", message)
    else:
        if instance.status == "ready_for_payment":
            subject = "سفارش شما آماده پرداخت است"
            message = f"سفارش شما با کد {instance.order_code} اکنون آماده پرداخت است."
            send_email_notification(instance.user, subject, message)
            send_sms_notification(instance.user, message)
            create_panel_notification(instance.user, "سفارش آماده پرداخت", message)
