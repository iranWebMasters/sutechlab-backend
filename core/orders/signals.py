from django.db.models.signals import post_save
from django.dispatch import receiver
from .invoices import generate_invoice
from django.db import transaction
from .models import RequestInfo, SampleInfo, TestInfo, DiscountInfo, Order, Order

@receiver(post_save, sender=RequestInfo)
@receiver(post_save, sender=SampleInfo)
@receiver(post_save, sender=TestInfo)
@receiver(post_save, sender=DiscountInfo)
def create_request(sender, instance, **kwargs):
    # Check if the instance has a user and experiment
    if not instance.user or not instance.experiment:
        return  # Avoid processing if user or experiment is missing

    with transaction.atomic():
        # Get or create the request
        request, created = Order.objects.get_or_create(
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

        # Save the Request only if there are changes
        request.save()

        # Debugging logs (optional)
        print(f"Order ID: {request.id}, is_complete: {request.is_complete}")
        # Check completeness and generate invoice if needed
  # Save changes to the request


