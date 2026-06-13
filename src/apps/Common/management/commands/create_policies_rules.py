from typing import Any

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from apps.Authentication.models import UserProfile
from apps.Authorization.models import Policy, Rule
from apps.Common.models import EndpointOption, Operator, RuleType


class Command(BaseCommand):

    help = "Command for creating policies and rules"

    def handle(self, *args: Any, **options: Any) -> str | None:

        self.stdout.write("CREATING POLICIES")

        profile_content_type = ContentType.objects.get_for_model(UserProfile)

        profile_retrieve = Policy.objects.create(
            name="Profile policy retrieve",
            description="The profile policy of object retrieve",
            resource_type=profile_content_type,
            action=EndpointOption.VIEW,
        )
        profile_update = Policy.objects.create(
            name="Profile policy update",
            description="The profile policy of object update",
            resource_type=profile_content_type,
            action=EndpointOption.EDIT,
        )
        profile_delete = Policy.objects.create(
            name="Profile policy delete",
            description="The profile policy of object delete",
            resource_type=profile_content_type,
            action=EndpointOption.DELETE,
        )

        self.stdout.write("CREATING RULES")

        Rule.objects.create(
            policy=profile_retrieve,
            rule_type=RuleType.RELATIONSHIP,
            attribute_name="is_owner",
            operator=Operator.EQUALS,
            value="True",
        )
        Rule.objects.create(
            policy=profile_update,
            rule_type=RuleType.RELATIONSHIP,
            attribute_name="is_owner",
            operator=Operator.EQUALS,
            value="True",
        )
        Rule.objects.create(
            policy=profile_delete,
            rule_type=RuleType.RELATIONSHIP,
            attribute_name="is_owner",
            operator=Operator.EQUALS,
            value="True",
        )
