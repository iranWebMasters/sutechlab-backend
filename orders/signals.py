from django.db.models.signals import post_save
from django.dispatch import receiver
from .invoices import generate_invoice
from .models import RequestInfo, SampleInfo, TestInfo, DiscountInfo, Request

@receiver(post_save, sender=RequestInfo)
@receiver(post_save, sender=SampleInfo)
@receiver(post_save, sender=TestInfo)
@receiver(post_save, sender=DiscountInfo)
def create_request(sender, instance, **kwargs):
    print(f"Signal received for {sender.__name__}")
    
    # بررسی وجود رکورد قبلی برای همان کاربر و آزمایش
    request, created = Request.objects.get_or_create(
        user=instance.user,
        experiment=instance.experiment,
    )
    print(f"Request {'created' if created else 'retrieved'}: {request.id}")

    # به‌روزرسانی فیلدهای مرتبط با اطلاعات درخواست
    if isinstance(instance, RequestInfo):
        request.request_info = instance
        print(f"RequestInfo updated for request {request.id}")
    elif isinstance(instance, SampleInfo):
        request.sample_info.add(instance)
        print(f"SampleInfo added for request {request.id}")
    elif isinstance(instance, TestInfo):
        request.test_info.add(instance)
        print(f"TestInfo added for request {request.id}")
    elif isinstance(instance, DiscountInfo):
        request.discount_info = instance
        print(f"DiscountInfo updated for request {request.id}")

    request.save()  # ذخیره تغییرات
    print(f"Request {request.id} saved.")

    # بررسی اینکه آیا همه فیلدهای مورد نیاز پر شده‌اند
    if request.discount_info:
        print(f"Request {request.id} is complete.")
        request.is_complete = True  # مشخص کردن تکمیل درخواست
        request.save()
        print(f"Request {request.id} marked as complete.")

        # ایجاد PDF تنها زمانی که همه فیلدها پر شده باشند
        if created or not request.invoice_pdf:  # فقط اگر درخواست جدید باشد یا PDF قبلاً ساخته نشده باشد
            print(f"Generating invoice for request {request.id}.")
            pdf_file_path = generate_invoice(request)  # تابعی که PDF را ایجاد کرده و مسیر آن را برمی‌گرداند
            request.invoice_pdf = pdf_file_path
            request.save()  # ذخیره فایل PDF
            print(f"PDF saved for request {request.id}: {pdf_file_path}")
    else:
        print(f"Request {request.id} is incomplete.")
