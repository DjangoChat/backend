from django.contrib.auth import get_user_model
from django.core.validators import validate_email as django_validate_email
from django.core.exceptions import ValidationError as DjangoValidationError

from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.Common.validators import (
    has_lowercase,
    has_number,
    has_special_character,
    has_uppercase,
)


class CustomUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    phone = PhoneNumberField()
    password1 = serializers.CharField(
        write_only=True,
        min_length=10,
        max_length=25,
        validators=[
            has_uppercase,
            has_number,
            has_special_character,
            has_lowercase,
        ],
    )
    password2 = serializers.CharField(
        write_only=True,
        min_length=10,
        max_length=25,
    )

    def validate_email(self, email):
        try:
            django_validate_email(email)
        except DjangoValidationError as e:
            raise ValidationError(str(e), code="invalid_email_format")

        email_name, domain_part = email.strip().rsplit("@", 1)
        email = email_name + "@" + domain_part.lower()

        if get_user_model()._default_manager.filter(email=email).exists():
            raise ValidationError(
                "A user with this email address already exists.",
                code="email_already_exists",
            )

        # TODO: add aws ses check if exists
        return email

    def validate_phone(self, phone):
        if get_user_model()._default_manager.filter(phone=phone).exists():
            raise ValidationError(
                "A user with this phone number already exists.",
                code="phone_already_exists",
            )
        return phone

    def validate(self, data):
        password1 = data.get("password1")
        password2 = data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError(
                "The two password fields do not match.",
                code="different_passwords",
            )
        return data

    def save(self, **kwargs):
        user_model = get_user_model()
        validated_data = self.validated_data

        user = user_model._default_manager.create_user(  # type: ignore
            email=validated_data["email"],  # type: ignore
            password=validated_data["password1"],  # type: ignore
            phone=validated_data["phone"],  # type: ignore
        )

        self.instance = user
        return self.instance
