from django.db.models.signals import post_save
from django.dispatch import receiver
from .invoices import generate_invoice
from django.db import transaction
from .models import *

@receiver(post_save, sender=RequestInfo)
@receiver(post_save, sender=SampleInfo)
@receiver(post_save, sender=TestInfo)
@receiver(post_save, sender=DiscountInfo)
def create_request(sender, instance, **kwargs):
    # Check if the instance has a user and experiment
    if not instance.user or not instance.experiment:
        return  # Avoid processing if user or experiment is missing

    with transaction.atomic():
        # Create or retrieve the related Request
        request, created = Request.objects.get_or_create(
            user=instance.user,
            experiment=instance.experiment,
        )

        # Update fields based on instance type
        if isinstance(instance, RequestInfo):
            request.request_info = instance
        elif isinstance(instance, SampleInfo):
            request.sample_info.add(instance)
        elif isinstance(instance, TestInfo):
            request.test_info.add(instance)
        elif isinstance(instance, DiscountInfo):
            request.discount_info = instance

        # Save the Request only if there are changes
        request.save()

        # Check completeness and generate invoice if needed
        if request.discount_info:
            request.is_complete = True
            # Generate invoice only if it's a new request or the invoice hasn't been generated yet
            if created or not request.invoice_pdf:
                pdf_file_path = generate_invoice(request)  # Call the function to generate the invoice
                request.invoice_pdf = pdf_file_path

            request.save()  # Save changes to the request

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Request, LaboratoryRequest

@receiver(post_save, sender=Request)
def create_or_update_laboratory_request(sender, instance, created, **kwargs):
    print('Signal received for Request ID:', instance.id)

    try:
        with transaction.atomic():
            # ایجاد یا به‌روزرسانی LaboratoryRequest بر اساس وضعیت ایجاد Request
            lab_request, created_lab_request = LaboratoryRequest.objects.get_or_create(
                user=instance.user,
                experiment=instance.experiment,
                defaults={
                    'submission_date': instance.request_info.submission_date if instance.request_info else None,
                    'description': instance.request_info.description if instance.request_info else None,
                }
            )

            if created_lab_request:
                print(f'LaboratoryRequest created with ID: {lab_request.id}')
            else:
                print(f'LaboratoryRequest updated for Request ID: {instance.id}')

            # پر کردن اطلاعات نمونه
            if instance.sample_info.exists():
                sample = instance.sample_info.first()
                lab_request.sample_type = sample.sample_type
                lab_request.customer_sample_name = sample.customer_sample_name
                lab_request.sample_count = sample.sample_count
                lab_request.additional_info = sample.additional_info
                lab_request.is_perishable = sample.is_perishable
                lab_request.expiration_date = sample.expiration_date
                lab_request.sample_return = sample.sample_return
                lab_request.storage_duration = sample.storage_duration
                lab_request.storage_duration_unit = sample.storage_duration_unit
                lab_request.storage_conditions = sample.storage_conditions
                lab_request.sample_description = sample.sample_description
                lab_request.file_upload = sample.file_upload
                print("Sample information populated.")

            else:
                print(f"No sample information found for Request ID: {instance.id}")

            # پر کردن اطلاعات تست
            if instance.test_info.exists():
                test = instance.test_info.first()
                lab_request.user_sample = str(test.user_sample.id) if test.user_sample else None
                lab_request.test = test.test
                lab_request.repeat_count_test = test.repeat_count_test
                lab_request.parameter = test.parameter
                lab_request.parameter_value = test.parameter_value
                print("Test information populated.")

            else:
                print(f"No test information found for Request ID: {instance.id}")

            # پر کردن اطلاعات تخفیف
            if instance.discount_info:
                lab_request.is_faculty_member = instance.discount_info.is_faculty_member
                lab_request.is_student_or_staff = instance.discount_info.is_student_or_staff
                lab_request.is_affiliated_with_institution = instance.discount_info.is_affiliated_with_institution
                lab_request.discount_institution_name = instance.discount_info.discount_institution_name
                print("Discount information populated.")
            else:
                print(f"No discount information found for Request ID: {instance.id}")

            # مقداردهی وضعیت، تکمیل و فاکتور PDF
            lab_request.status = instance.status
            lab_request.is_complete = instance.is_complete
            lab_request.invoice_pdf = instance.invoice_pdf

            lab_request.save()  # ذخیره نمونه LaboratoryRequest
            print(f'LaboratoryRequest ID {lab_request.id} saved.')

    except Exception as e:
        print(f'Error occurred: {str(e)}')
