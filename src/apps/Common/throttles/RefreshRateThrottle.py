from rest_framework.throttling import AnonRateThrottle


class RefreshRateThrottle(AnonRateThrottle):
    scope = "refresh"
