from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import TemporaryRequestInfo, TemporarySampleInfo, TemporaryTestInfo, TemporaryDiscountInfo, TemporaryOrder, Order

@receiver(post_save, sender=TemporaryRequestInfo)
@receiver(post_save, sender=TemporarySampleInfo)
@receiver(post_save, sender=TemporaryTestInfo)
@receiver(post_save, sender=TemporaryDiscountInfo)
def create_request(sender, instance, **kwargs):
    if not instance.user or not instance.experiment:
        return

    with transaction.atomic():
        # Get or create the request
        request, created = TemporaryOrder.objects.get_or_create(
            user=instance.user,
            experiment=instance.experiment,
        )
        
        # Update the request with the instance information
        if isinstance(instance, TemporaryRequestInfo):
            request.request_info = instance
        elif isinstance(instance, TemporarySampleInfo):
            request.sample_info.add(instance)
        elif isinstance(instance, TemporaryTestInfo):
            request.test_info.add(instance)
        elif isinstance(instance, TemporaryDiscountInfo):
            request.discount_info = instance
            request.is_complete = True
        
        # Save the request
        request.save()

        # Debugging logs (optional)
        print(f"TemporaryOrder ID: {request.id}, is_complete: {request.is_complete}")
