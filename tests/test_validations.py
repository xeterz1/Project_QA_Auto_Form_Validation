# tests/test_validations.py
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from logic.validations import Age_validation, Name_validation, Email_validation

@pytest.mark.parametrize("age", [-5, -1, 121, 300])
def test_age_out_of_range_raises(age):
    with pytest.raises(ValueError):
        Age_validation(age)


@pytest.mark.parametrize("age", [0, 1, 25, 120])
def test_age_in_range_ok(age):
    Age_validation(age)  # should not raise


@pytest.mark.parametrize("name", ["", "A", "A"*51, "Akram1", "123", "Akram B@", " "])
def test_name_invalid(name):
    with pytest.raises(ValueError):
        Name_validation(name)


@pytest.mark.parametrize("name", ["Akram", "Akram Berjaoui", "Jean Pierre"])
def test_name_valid(name):
    Name_validation(name)


@pytest.mark.parametrize("email", ["a123@.com", "no-at.com", "akram@domain", "akram@domain.", "akram@domain.c"])
def test_email_invalid(email):
    with pytest.raises(ValueError):
        Email_validation(email)


@pytest.mark.parametrize("email", ["akram@test.com", "akram.name.tag@domain.org"])
def test_email_valid(email):
    Email_validation(email)


def test_email_type_error():
    with pytest.raises(TypeError):
        Email_validation(123)
