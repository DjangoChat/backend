from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.Authentication.models import UserProfile
from apps.Chat.models import Participant
from apps.Billing.service import CreateCustomerService
from apps.Common.models import ParticipantType


@receiver(post_save, sender=UserProfile)
def create_stripe_customer(sender, instance, created, **kwargs):
    if created:
        custom_user = instance.user

        stripe_custom_user = CreateCustomerService().execute(
            name=f"{instance.first_name} {instance.last_name}",
            email=custom_user.email,
            phone=custom_user.phone,
        )
        custom_user.strip_customer_id = stripe_custom_user.id
        custom_user.save()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_participant(sender, instance, created, **kwargs):
    if created:
        custom_user = instance

        Participant.objects.get_or_create(
            participaty_type=ParticipantType.USER,
            user=custom_user,
        )
