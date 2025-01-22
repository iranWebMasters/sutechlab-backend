
from django.db.models.signals import post_save
from django.dispatch import receiver
from .invoices import generate_invoice
from .models import Order

@receiver(post_save, sender=Order)
def create_invoice(sender, instance, created, **kwargs):
    if not created and instance.is_complete and not instance.invoice_pdf:
        pdf_file_path = generate_invoice(instance)
        instance.invoice_pdf = pdf_file_path
        instance.save()

@receiver(post_save, sender=Order)
def update_invoice(sender, instance, created, **kwargs):
    # فقط در صورتی که سفارش به‌روزرسانی شده باشد و کامل باشد، پیش‌فاکتور را به‌روزرسانی کنید
    if not created and instance.is_complete:
        # بررسی اینکه آیا پیش‌فاکتور قبلاً تولید شده است
        if not instance.invoice_pdf:  # اگر پیش‌فاکتور وجود ندارد
            pdf_file_path = generate_invoice(instance)
            instance.invoice_pdf = pdf_file_path
            instance.save(update_fields=['invoice_pdf'])  # فقط فیلد پیش‌فاکتور را به‌روزرسانی کنید
