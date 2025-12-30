from rest_framework.throttling import BaseThrottle
from django.core.cache import cache
from django.conf import settings
import time


class FailedLoginThrottle(BaseThrottle):
    RATE = 5
    TIMEOUT = 1800

    def get_ident(self, request):
        return request.META.get("REMOTE_ADDR")

    def get_cache_key(self, request):
        ident = self.get_ident(request)
        return f"failed_login_{ident}"

    def allowed_request(self, request, view):
        key = self.get_cache_key(request)
        attempts = cache.get(key, 0)

        if attempts >= self.RATE:
            return False
        return True

    def throttle_failure(self, request):
        key = self.get_cache_key(request)
        attempts = cache.get(key, 0)
        cache.set(key, attempts + 1, timeout=self.TIMEOUT)

    def reset(self, request):
        key = self.get_cache_key(request)
        cache.delete(key)
