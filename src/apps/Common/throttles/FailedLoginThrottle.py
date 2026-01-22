import time

from django.core.cache import cache

from rest_framework.throttling import SimpleRateThrottle


class FailedLoginThrottle(SimpleRateThrottle):
    """
    Event-based throttle that activates after 3 failed login attempts.
    Once activated, the user is blocked for 30 minutes.
    Resets on successful login.

    Unlike standard throttles, this one doesn't count requests automatically.
    Instead, use record_failed_attempt() to record failures and reset() on success.
    """

    scope = "failed_login"
    cache_format = "throttle_%(scope)s_%(ident)s"

    # 3 attempts per 30 minutes
    THROTTLE_RATES = {"failed_login": "3/30m"}

    def __init__(self):
        # Bypass parent's rate lookup from settings
        self.rate = self.get_rate()
        self.num_requests, self.duration = self.parse_rate(self.rate)

    def get_rate(self):
        """Return the rate defined in THROTTLE_RATES."""
        return self.THROTTLE_RATES.get(self.scope)

    def parse_rate(self, rate):
        """Parse rate string like '3/30m' into (num_requests, duration_seconds)."""
        if rate is None:
            return (None, None)
        num, period = rate.split("/")
        num_requests = int(num)
        duration_unit = period[-1]
        duration_value = int(period[:-1]) if len(period) > 1 else 1
        duration_map = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        duration = duration_value * duration_map.get(duration_unit, 1)
        return (num_requests, duration)

    def get_cache_key(self, request, view=None):
        """Generate cache key based on client IP."""
        ident = self.get_ident(request)
        return self.cache_format % {"scope": self.scope, "ident": ident}

    def allow_request(self, request, view):
        """
        Check if the request should be allowed based on failed attempt history.
        This cleans up expired entries and checks if under the limit.
        Does NOT record the current request as an attempt.
        """
        self.key = self.get_cache_key(request, view)
        self.history = cache.get(self.key, [])
        self.now = time.time()

        # Remove expired timestamps (older than duration)
        while self.history and self.history[-1] <= self.now - self.duration:
            self.history.pop()

        if len(self.history) >= self.num_requests:
            return self.throttle_failure()
        return True

    def throttle_failure(self):
        """Called when throttle check fails."""
        return False

    def record_failed_attempt(self, request):
        """
        Record a failed login attempt.
        Call this method when a login attempt fails.
        """
        key = self.get_cache_key(request)
        now = time.time()
        history = cache.get(key, [])

        # Clean up expired entries
        while history and history[-1] <= now - self.duration:
            history.pop()

        # Add current timestamp at the beginning
        history.insert(0, now)
        cache.set(key, history, self.duration)

    def reset(self, request):
        """
        Reset the failed login counter.
        Call this method when a login is successful.
        """
        key = self.get_cache_key(request)
        cache.delete(key)
