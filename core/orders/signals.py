from django.db.models.signals import post_save
from django.dispatch import receiver
from .invoices import generate_invoice
from django.db import transaction
<<<<<<< HEAD
from .models import TemporaryRequestInfo, TemporarySampleInfo, TemporaryTestInfo, TemporaryDiscountInfo, TemporaryOrder, Order
=======
from .models import *
>>>>>>> parent of f4dc6a9 (✅ update in orders app and template)

@receiver(post_save, sender=TemporaryRequestInfo)
@receiver(post_save, sender=TemporarySampleInfo)
@receiver(post_save, sender=TemporaryTestInfo)
@receiver(post_save, sender=TemporaryDiscountInfo)
def create_request(sender, instance, **kwargs):
    # Check if the instance has a user and experiment
    if not instance.user or not instance.experiment:
        return  # Avoid processing if user or experiment is missing

    with transaction.atomic():
<<<<<<< HEAD
        # Get or create the request
        request, created = TemporaryOrder.objects.get_or_create(
            user=instance.user,
            experiment=instance.experiment,
        )
        
        # Update the request with the instance information
        if isinstance(instance, TemporaryRequestInfo):
=======
        # Create or retrieve the related Request
        request, created = Request.objects.get_or_create(
            user=instance.user,
            experiment=instance.experiment,
        )

        # Update fields based on instance type
        if isinstance(instance, RequestInfo):
>>>>>>> parent of f4dc6a9 (✅ update in orders app and template)
            request.request_info = instance
        elif isinstance(instance, TemporarySampleInfo):
            request.sample_info.add(instance)
        elif isinstance(instance, TemporaryTestInfo):
            request.test_info.add(instance)
        elif isinstance(instance, TemporaryDiscountInfo):
            request.discount_info = instance

        # Save the Request only if there are changes
        request.save()

<<<<<<< HEAD
        # Debugging logs (optional)
        print(f"TemporaryOrder ID: {request.id}, is_complete: {request.is_complete}")
=======
        # Check completeness and generate invoice if needed
  # Save changes to the request



@receiver(post_save, sender=Request)
def create_or_update_laboratory_request(sender, instance, created, **kwargs):
    print('Signal received for Request ID:', instance.id)

    try:
        with transaction.atomic():
            lab_request, created_lab_request = LaboratoryRequest.objects.get_or_create(
                user=instance.user,
                experiment=instance.experiment,
                defaults={
                    'submission_date': instance.request_info.submission_date if instance.request_info else None,
                    'description': instance.request_info.description if instance.request_info else None,
                    'order_code': instance.request_info.order_code if instance.request_info else None, 
                }
            )

            if created_lab_request:
                print(f'LaboratoryRequest created with ID: {lab_request.id}')
            else:
                print(f'LaboratoryRequest updated for Request ID: {instance.id}')

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

            if instance.test_info.exists():
                test = instance.test_info.first()
                lab_request.user_sample = str(test.user_sample.id) if test.user_sample else None
                lab_request.test = test.test
                lab_request.repeat_count_test = test.repeat_count_test
                lab_request.parameter = test.parameter
                lab_request.parameter_values = test.parameter_values
                print("Test information populated.")

            else:
                print(f"No test information found for Request ID: {instance.id}")

            if instance.discount_info:
                lab_request.is_faculty_member = instance.discount_info.is_faculty_member
                lab_request.is_student_or_staff = instance.discount_info.is_student_or_staff
                lab_request.is_affiliated_with_institution = instance.discount_info.is_affiliated_with_institution
                lab_request.discount_institution_name = instance.discount_info.discount_institution_name
                print("Discount information populated.")
            else:
                print(f"No discount information found for Request ID: {instance.id}")

            lab_request.status = instance.status
            lab_request.is_complete = instance.is_complete
            # lab_request.invoice_pdf = instance.invoice_pdf

            lab_request.save()
            print(f'LaboratoryRequest ID {lab_request.id} saved.')

    except Exception as e:
        print(f'Error occurred: {str(e)}')


@receiver(post_save, sender=LaboratoryRequest)
def update_or_create_invoice(sender, instance, created, **kwargs):
    # Only generate an invoice for newly created records
    if created:
        pdf_file_path = generate_invoice(instance)
        instance.invoice_pdf = pdf_file_path
        instance.save()
>>>>>>> parent of f4dc6a9 (✅ update in orders app and template)
