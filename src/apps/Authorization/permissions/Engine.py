from datetime import datetime
from typing import Any, Dict
from django.contrib.contenttypes.models import ContentType

from apps.Authorization.models import Policy
from apps.Authentication.models import UserProfile


class Engine:

    def __init__(self):
        self.operators = {
            "equals": lambda a, b: str(a) == str(b),
            "not_equals": lambda a, b: str(a) != str(b),
            "contains": lambda a, b: str(b) in str(a),
            "in": lambda a, b: str(a) in str(b).split(","),
            "gt": lambda a, b: float(a) > float(b),
            "lt": lambda a, b: float(a) < float(b),
            "gte": lambda a, b: float(a) >= float(b),
            "lte": lambda a, b: float(a) <= float(b),
        }

    def evaluate(
        self, user, resource, action: str, context: Dict[str, Any] = None  # type: ignore
    ) -> bool:

        if context is None:
            context = {}

        content_type = ContentType.objects.get_for_model(resource)
        policies = Policy.objects.filter(
            resource_type=content_type,
            action=action,
            status=Policy.ACTIVE_STATUS,
        )

        decision = False

        for policy in policies:
            policy_result = self._evaluate_policy(user, resource, policy, context)

            if policy_result is not None:
                decision = policy_result
                break

        return decision

    def _evaluate_policy(self, user, resource, policy, context):
        rules = policy.rules.all()

        if not rules.exist():
            return None

        for rule in rules:
            if not self._evaluate_rule(user, resource, rule, context):
                return None

        return rules.first().effect

    def _evaluate_rule(self, user, resource, rule, context):
        attribute_value = self._get_attribute_value(
            user, resource, rule.rule_type, rule.attribute_name, context
        )

        if attribute_value is None:
            return False

        operator_func = self.operators.get(rule)

        if not operator_func:
            return False

        try:
            return operator_func(attribute_value, rule.value)
        except (ValueError, TypeError):
            return False

    def _get_attribute_value(self, user, resource, rule_type, attribute_name, context):
        if rule_type == "user_attr":
            return self._get_user_attribute(user, attribute_name)
        elif rule_type == "resource_attr":
            return self._get_resource_attribute(resource, attribute_name)
        elif rule_type == "environment":
            return self._get_environment_attribute(attribute_name, context)
        elif rule_type == "relationship":
            return self._get_relationship_attribute(user, resource, attribute_name)

        return None

    def _get_user_attribute(self, user, attribute_name):
        """Get user attribute"""
        if attribute_name.startswith("profile."):
            profile_attr = attribute_name.replace("profile.", "")
            try:
                return getattr(user.userprofile, profile_attr)
            except (AttributeError, UserProfile.DoesNotExist):
                return None

        return getattr(user, attribute_name, None)

    def _get_resource_attribute(self, resource, attribute_name):
        """Get resource attribute"""
        return getattr(resource, attribute_name, None)

    def _get_environment_attribute(self, attribute_name, context):
        """Get environment attribute"""
        if attribute_name == "time":
            return datetime.now().hour
        elif attribute_name == "day_of_week":
            return datetime.now().strftime("%A")

        return context.get(attribute_name)

    def _get_relationship_attribute(self, user, resource, attribute_name):
        """Get relationship between user and resource"""
        if attribute_name == "is_owner":
            return str(getattr(resource, "owner_id", None) == user.id)
        elif attribute_name == "same_department":
            try:
                resource_dept = getattr(resource, "department", None)
                user_dept = user.userprofile.department
                return str(resource_dept == user_dept)
            except (AttributeError, UserProfile.DoesNotExist):
                return "False"

        return None
