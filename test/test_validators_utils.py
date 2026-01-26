from django.core.exceptions import ValidationError

import pytest

from apps.Common.validators import utils


@pytest.mark.parametrize(
    "func,input_str",
    [
        (utils.has_number, "abc"),
        (utils.has_uppercase, "abc"),
        (utils.has_special_character, "abcABC123"),
        (utils.has_lowercase, "ABC123!@#"),
    ],
)
def test_validators_raise(func, input_str):
    with pytest.raises(ValidationError):
        func(input_str)


@pytest.mark.parametrize(
    "func,input_str",
    [
        (utils.has_number, "abc1"),
        (utils.has_uppercase, "abcA"),
        (utils.has_special_character, "abc!"),
        (utils.has_lowercase, "ABCd"),
    ],
)
def test_validators_pass(func, input_str):
    # Should not raise
    func(input_str)
