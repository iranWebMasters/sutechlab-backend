from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .invoices import generate_invoice
from .models import RequestInfo, SampleInfo, TestInfo, DiscountInfo, Request

@receiver(post_save, sender=RequestInfo)
@receiver(post_save, sender=SampleInfo)
@receiver(post_save, sender=TestInfo)
@receiver(post_save, sender=DiscountInfo)
def create_request(sender, instance, **kwargs):
    # بررسی وجود رکورد قبلی برای همان کاربر و آزمایش
    request, created = Request.objects.get_or_create(
        user=instance.user,
        experiment=instance.experiment,
    )
    # به‌روزرسانی فیلدهای مرتبط با اطلاعات درخواست
    if isinstance(instance, RequestInfo):
        request.request_info = instance
    elif isinstance(instance, SampleInfo):
        request.sample_info.add(instance)
    elif isinstance(instance, TestInfo):
        request.test_info.add(instance)  # استفاده از add() برای ManyToManyField
    elif isinstance(instance, DiscountInfo):
        request.discount_info = instance

    request.save()  # ذخیره تغییرات

    # ایجاد PDF
    if created or request.invoice_pdf is None:  # فقط اگر درخواست جدید باشد یا PDF قبلاً ساخته نشده باشد
        pdf_file_path = generate_invoice(request)  # تابعی که PDF را ایجاد کرده و مسیر آن را برمی‌گرداند
        request.invoice_pdf = pdf_file_path
        request.save()


# @receiver(post_delete, sender=Request)
# def delete_related_objects(sender, instance, **kwargs):
#     if instance.request_info:
#         instance.request_info.delete()
#     if instance.test_info:
#         instance.test_info.delete()
#     instance.sample_info.clear()
#     if instance.discount_info:
#         instance.discount_info.delete()