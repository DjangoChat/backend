import re

from django.core.exceptions import ValidationError


def has_number(s):
    if not bool(re.search(r"\d", s)):
        raise ValidationError("A number must be provided.", code="must_contain_number")


def has_uppercase(s):
    if not bool(re.search(r"[A-Z]", s)):
        raise ValidationError(
            "An uppercase character must be provided.", code="must_contain_uppercase"
        )


def has_special_character(s):
    if not bool(re.compile(r"^(?=.*[^a-zA-Z0-9\s])\S+$")):
        raise ValidationError(
            "A special character must be provided.",
            code="must_contain_special_character",
        )
