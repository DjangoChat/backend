"""
Tests for the CustomUserSerializer.

This module tests the CustomUserSerializer validation functionality including:
- Email format validation
"""

import pytest
from rest_framework.exceptions import ValidationError

from apps.Authentication.api.v1.serializers.CustomUserSerializer import (
    CustomUserSerializer,
)

pytestmark = pytest.mark.django_db


# =============================================================================
# Email Validation Tests
# =============================================================================


def test_validate_email_invalid_format():
    """
    Test email validation with invalid format.

    Verifies that the validate_email method raises a ValidationError
    when the email lacks the '@' symbol.
    """
    serializer = CustomUserSerializer()
    invalid_email = "invalidemail.com"

    with pytest.raises(ValidationError):
        serializer.validate_email(invalid_email)
