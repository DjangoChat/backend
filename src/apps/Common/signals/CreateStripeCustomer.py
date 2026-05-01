from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.Common.utils import create_stripe_customuser

from apps.Authentication.models import CustomUser, UserProfile


@receiver(post_save, sender=UserProfile)
def create_stripe_customer(sender, instance, created, **kwargs):
    if created:
        custom_user = CustomUser.objects.get(id=instance.user)

        stripe_custom_user = create_stripe_customuser(
            name=f"{instance.first_name} {instance.last_name}",
            email=custom_user.email,
            phone=custom_user.phone,
        )

        custom_user.strip_customer_id = stripe_custom_user.id
        custom_user.save()
