import pytest

from cli_input_validator import (
    DEFAULT_NAME_ERROR,
    VALID,
    get_valid_choice,
    get_valid_name,
    get_validated_input,
    name_validator,
)


def input_from(entries, prompts=None):
    values = iter(entries)

    def read(prompt):
        if prompts is not None:
            prompts.append(prompt)
        return next(values)

    return read


def test_get_validated_input_returns_first_valid_entry():
    read = input_from(["valid"])

    result = get_validated_input(input_function=read)("Enter value: ")

    assert result == "valid"


def test_get_validated_input_reprompts_with_error_message():
    prompts = []
    read = input_from(["", "accepted"], prompts)
    validator = lambda value: VALID if value else (False, "Try again: ")

    result = get_validated_input(validator, read)("Enter value: ")

    assert result == "accepted"
    assert prompts == ["Enter value: ", "Try again: "]


@pytest.mark.parametrize("name", ["Mayowa", "Mary Jane", "Anne-Marie"])
def test_name_validator_accepts_supported_names(name):
    assert name_validator(name) == VALID


@pytest.mark.parametrize("name", ["", "   ", "Mayowa2", "Mayowa!"])
def test_name_validator_rejects_invalid_names(name):
    assert name_validator(name) == (False, DEFAULT_NAME_ERROR)


def test_get_valid_name_accepts_a_custom_input_function():
    read = input_from(["123", "Mayowa"])

    assert get_valid_name("Name: ", input_function=read) == "Mayowa"


def test_get_valid_choice_is_case_insensitive_by_default():
    read = input_from(["MAYBE", "YES"])

    assert get_valid_choice(["yes", "no"], input_function=read) == "YES"


def test_get_valid_choice_can_be_case_sensitive():
    read = input_from(["yes", "Yes"])

    result = get_valid_choice(
        ["Yes", "No"],
        case_sensitive=True,
        input_function=read,
    )

    assert result == "Yes"


def test_get_valid_choice_rejects_empty_choices():
    with pytest.raises(ValueError, match="choices must not be empty"):
        get_valid_choice([])


def test_get_valid_choice_accepts_generators():
    choices = (choice for choice in ["left", "right"])

    assert get_valid_choice(choices, input_function=input_from(["left"])) == "left"
