import string

import pytest
from pydantic import ValidationError

from main import PasswordOptions, create_password


def test_generated_password_has_requested_length_and_character_groups():
    options = PasswordOptions(
        length=24,
        uppercase=True,
        lowercase=True,
        numbers=True,
        symbols=True,
    )

    password, entropy, strength = create_password(options)

    assert len(password) == 24
    assert any(char in string.ascii_uppercase for char in password)
    assert any(char in string.ascii_lowercase for char in password)
    assert any(char in string.digits for char in password)
    assert any(char in "!@#$%^&*()-_=+[]{};:,.?" for char in password)
    assert entropy > 0
    assert strength == "Excelente"


def test_excluding_similar_characters_applies_to_the_entire_password():
    options = PasswordOptions(length=64, exclude_similar=True)

    password, _, _ = create_password(options)

    assert not set(password).intersection("Il1O0")


@pytest.mark.parametrize("length", [7, 65])
def test_password_length_must_be_between_8_and_64(length):
    with pytest.raises(ValidationError):
        PasswordOptions(length=length)


def test_at_least_one_character_group_is_required():
    with pytest.raises(ValidationError, match="Selecciona al menos un tipo"):
        PasswordOptions(uppercase=False, lowercase=False, numbers=False, symbols=False)
