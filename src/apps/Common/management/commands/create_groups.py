from typing import Any

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from Authentication.models import UserProfile
from Common.models import CustomGroups

READ_PERMISSIONS = [
    "view",
]
WRITE_PERMISSIONS = [
    "add",
    "change",
]
FULL_PERMISSIONS = READ_PERMISSIONS + WRITE_PERMISSIONS

GROUPS_PERMISSIONS = {
    CustomGroups.MEMBER: {
        UserProfile: FULL_PERMISSIONS,
    },
    CustomGroups.MAINTAINER: {
        UserProfile: FULL_PERMISSIONS,
    },
    CustomGroups.ANALITICAL: {
        UserProfile: FULL_PERMISSIONS,
    },
    CustomGroups.ADMIN: {
        UserProfile: FULL_PERMISSIONS,
    },
}


class Command(BaseCommand):

    help = "Command for creating the default groups on the database"

    def handle(self, *args: Any, **options: Any) -> str | None:

        for group_name in GROUPS_PERMISSIONS:
            group, created = Group.objects.get_or_create(name=group_name)

            for model_cls, list_perms in GROUPS_PERMISSIONS[group_name].items():
                for perm in list_perms:

                    codename = perm + "_" + str(model_cls._meta.model_name)

                    try:
                        perm_obj = Permission.objects.get(codename=codename)
                        group.permissions.add(perm_obj)
                        self.stdout.write(
                            codename
                            + " added to the group "
                            + group_name
                            + " succesfully"
                        )

                    except:
                        self.stdout.write(codename + " not found")
