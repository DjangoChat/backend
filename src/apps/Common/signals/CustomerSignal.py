from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.Chat.models import Participant
from apps.Billing.service import CreateCustomerService


@receiver(post_save, sender=Participant)
def create_stripe_customer(sender, instance, created, **kwargs):
    if created and instance.user is not None:
        custom_user = instance.user

        stripe_custom_user = CreateCustomerService().execute(
            name=f"{instance.first_name} {instance.last_name}",
            email=custom_user.email,
            phone=custom_user.phone,
        )
        custom_user.strip_customer_id = stripe_custom_user.id
        custom_user.save()
