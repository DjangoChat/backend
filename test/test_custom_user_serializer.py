import pytest
from rest_framework.exceptions import ValidationError
from apps.Authentication.api.v1.serializers.CustomUserSerializer import CustomUserSerializer

pytestmark = pytest.mark.django_db

def test_validate_email_invalid_format():
    """
    Test that the validate_email method raises a ValidationError for invalid email formats.
    """
    serializer = CustomUserSerializer()

    # Invalid email without '@'
    invalid_email = "invalidemail.com"

    with pytest.raises(ValidationError):
        serializer.validate_email(invalid_email)
