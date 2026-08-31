from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.Common.models import CustomModel
from apps.Chat.models import Participant


class Contact(CustomModel):
    owner = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        related_name="owned_contacts",
    )
    contact = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        related_name="contact_of",
    )

    class Meta:
        db_table = "CHAT_CONTACT"
        verbose_name = _("Contacts")
        verbose_name_plural = _("Contacts")
        app_label = "Chat"
