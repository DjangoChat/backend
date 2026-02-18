from django.core.management.base import BaseCommand

from apps.Authentication.models import Gender, Role, UserProfile
from apps.Authorization.models import Operator, Policy, Rule, RuleType


class Command(BaseCommand):

    help = "Command for creating the policies and roles of each model"

    def handle(self, *args, **kwargs):
        profile_policy_get = Policy.objects.create(
            name="UserProfile Policy Get",
            description="A policy to get a UserProfile",
            resource_type=UserProfile,
            action="view",
            priority=1,
        )
        Rule.objects.create(
            policy=profile_policy_get,
            rule_type=RuleType.USER_ATTR,
            attribute_name="profile.role",
            operator=Operator.EQUALS,
            value=Role.BASIC,
        )
        Rule.objects.create(
            policy=profile_policy_get,
            rule_type=RuleType.RELATIONSHIP,
            attribute_name="is_owner",
            operator=Operator.EQUALS,
            value="True",
        )
