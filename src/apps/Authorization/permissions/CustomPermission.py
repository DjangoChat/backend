from rest_framework.permissions import BasePermission

from .Engine import Engine


class CustomPermission(BasePermission):

    def __init__(self):
        self.engine = Engine()

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        action_map = {
            "GET": "view",
            "POST": "create",
            "PUT": "edit",
            "PATCH": "edit",
            "DELETE": "delete",
        }

        action = action_map.get(request.method, "view")

        context = {
            "ip_address": self._get_client_ip(request),
            "user_agent": request.META.get("HTTP_USER_AGENT", ""),
        }

        return self.engine.evaluate(request.user, obj, action, context)

    def _get_client_ip(self, request):
        """Extract client IP from request"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
