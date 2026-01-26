import pytest

from apps.Authentication.authentication.CookieJwtAuthScheme import CookieJwtAuthScheme


class DummyAutoSchema:
    pass


def test_get_security_definition():
    scheme = CookieJwtAuthScheme(target=None)
    result = scheme.get_security_definition(DummyAutoSchema())
    expected = {
        "type": "apiKey",
        "in": "cookie",
        "name": "access_token",
        "description": "JWT stored in HTTP-only cookie",
    }
    assert result == expected
