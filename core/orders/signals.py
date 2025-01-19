
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