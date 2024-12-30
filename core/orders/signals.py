from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import RequestInfo, SampleInfo, TestInfo, DiscountInfo, Request, LaboratoryRequest

@receiver(post_save, sender=RequestInfo)
@receiver(post_save, sender=SampleInfo)
@receiver(post_save, sender=TestInfo)
@receiver(post_save, sender=DiscountInfo)
def create_request(sender, instance, **kwargs):
    if not instance.user or not instance.experiment:
        return

    with transaction.atomic():
        # Get or create the request
        request, created = Request.objects.get_or_create(
            user=instance.user,
            experiment=instance.experiment,
        )
        
        # Update the request with the instance information
        if isinstance(instance, RequestInfo):
            request.request_info = instance
        elif isinstance(instance, SampleInfo):
            request.sample_info.add(instance)
        elif isinstance(instance, TestInfo):
            request.test_info.add(instance)
        elif isinstance(instance, DiscountInfo):
            request.discount_info = instance
            request.is_complete = True
        
        # Save the request
        request.save()

        # Debugging logs (optional)
        print(f"Request ID: {request.id}, is_complete: {request.is_complete}")

@receiver(post_save, sender=Request)
def create_laboratory_request(sender, instance, created, **kwargs):
    if instance.is_complete:
        # ایجاد یک شیء جدید از LaboratoryRequest
        laboratory_request = LaboratoryRequest.objects.create(
            user=instance.user,
            experiment=instance.experiment,
            order_code=instance.request_info.order_code,
            submission_date=instance.request_info.submission_date,
            description=instance.request_info.description,
            status='pending',  # یا هر وضعیت دیگری که بخواهید
            is_complete=instance.is_complete,
            invoice_pdf=None,
            final_price=0,
        )

        # کپی‌برداری از اطلاعات نمونه‌ها
        for sample_info in instance.sample_info.all():
            laboratory_request.sample_type = sample_info.sample_type
            laboratory_request.customer_sample_name = sample_info.customer_sample_name
            laboratory_request.sample_count = sample_info.sample_count
            laboratory_request.additional_info = sample_info.sample_description
            laboratory_request.is_perishable = sample_info.is_perishable
            laboratory_request.expiration_date = sample_info.expiration_date
            laboratory_request.sample_return = sample_info.sample_return
            laboratory_request.storage_duration = sample_info.storage_duration
            laboratory_request.storage_duration_unit = sample_info.storage_duration_unit
            laboratory_request.storage_conditions = sample_info.storage_conditions
            laboratory_request.file_upload = sample_info.file_upload

        # کپی‌برداری از اطلاعات آزمایش‌ها
        for test_info in instance.test_info.all():
            laboratory_request.user_sample = test_info.user_sample
            laboratory_request.test = test_info.test
            laboratory_request.repeat_count_test = test_info.repeat_count_test
            laboratory_request.parameter = test_info.parameter
            laboratory_request.parameter_values = test_info.parameter_values

        # کپی‌برداری از اطلاعات تخفیف
        if instance.discount_info:
            laboratory_request.send_cost = instance.discount_info.send_cost
            laboratory_request.is_faculty_member = instance.discount_info.is_faculty_member
            laboratory_request.is_student_or_staff = instance.discount_info.is_student_or_staff
            laboratory_request.is_affiliated_with_institution = instance.discount_info.is_affiliated_with_institution
            laboratory_request.contract_party_file = instance.discount_info.contract_party_file
            laboratory_request.has_labs_net_grant = instance.discount_info.has_labs_net_grant
            laboratory_request.labs_net_file = instance.discount_info.labs_net_file
            laboratory_request.has_research_grant = instance.discount_info.has_research_grant
            laboratory_request.research_grant_withdrawal_amount = instance.discount_info.research_grant_withdrawal_amount

        # ذخیره LaboratoryRequest
        laboratory_request.save()