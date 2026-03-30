from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import stripe

from apps.Authentication.models import UserProfile, CustomUser

stripe.api_key = settings.STRIPE_API_KEY


@receiver(post_save, sender=UserProfile)
def create_stripe_customer(sender, instance, created, **kwargs):
    if created:
        custom_user = CustomUser.objects.get(id=instance.user)

        stripe.Customer.create(
            name=f"{instance.first_name} {instance.last_name}",
            email=custom_user.email,
            phone=custom_user.phone,
        )
