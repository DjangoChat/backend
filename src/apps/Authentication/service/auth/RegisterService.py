from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from apps.Common.models import CustomGroups


class RegisterService:
    def execute(self, email, password, phone):
        user_model = get_user_model()

        user = user_model._default_manager.create_user(  # type: ignore
            email=email,
            password=password,
            phone=phone,
        )

        group = Group.objects.get(name=CustomGroups.MEMBER)
        self.instance = user.groups.add(group)

        return user
