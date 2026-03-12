from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomGroups(models.TextChoices):
    MEMBER = "MEMBER", ("Member")
    MAINTAINER = "MAINTAINER", ("Maintainer")
    ANALITICAL = "ANALITICAL", ("Analitical")
    ADMIN = "ADMIN", ("Admin")
