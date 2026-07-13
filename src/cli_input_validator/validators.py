"""Functions for validating interactive command-line input."""

import re
from collections.abc import Callable, Iterable

ValidationResult = tuple[bool, str | None]
Validator = Callable[[str], ValidationResult]
InputFunction = Callable[[str], str]

VALID: ValidationResult = (True, None)
DEFAULT_NAME_ERROR = (
    "Please enter a name containing only letters, spaces, or hyphens: "
)


def get_validated_input(
    is_valid: Validator | None = None,
    input_function: InputFunction | None = None,
) -> Callable[[str], str]:
    """Return a prompt function that repeats until its input is valid.

    A validator returns ``(True, None)`` for valid input or
    ``(False, error_message)`` for invalid input. The error message becomes
    the next prompt.
    """
    validator = is_valid or (lambda _: VALID)
    read_input = input_function or input

    def validate(prompt: str = " ") -> str:
        while True:
            user_entry = read_input(prompt)
            valid, error = validator(user_entry)
            if valid:
                return user_entry
            prompt = error or ""

    return validate


def name_validator(
    name: str,
    error_message: str = DEFAULT_NAME_ERROR,
) -> ValidationResult:
    """Validate a non-empty name containing letters, spaces, or hyphens."""
    is_valid = bool(name.strip()) and re.fullmatch(r"[A-Za-z\s-]+", name) is not None
    return VALID if is_valid else (False, error_message)


def verify_name_integrity(
    prompt: str,
    *,
    input_function: InputFunction | None = None,
    error_message: str = DEFAULT_NAME_ERROR,
) -> str:
    """Prompt repeatedly until the user enters a valid name."""

    def validator(name: str) -> ValidationResult:
        return name_validator(name, error_message)

    return get_validated_input(validator, input_function)(prompt)


def get_valid_choice(
    choices: Iterable[str],
    prompt: str = "",
    case_sensitive: bool = False,
    *,
    input_function: InputFunction | None = None,
) -> str:
    """Prompt until the user enters one of the supplied choices."""
    options = tuple(choices)
    if not options:
        raise ValueError("choices must not be empty")

    normalized = set(options) if case_sensitive else {choice.casefold() for choice in options}
    error_message = f"Please enter {_join_choices(options)}: "

    def validator(choice: str) -> ValidationResult:
        entry = choice if case_sensitive else choice.casefold()
        return VALID if entry in normalized else (False, error_message)

    return get_validated_input(validator, input_function)(prompt)


def _join_choices(choices: tuple[str, ...]) -> str:
    if len(choices) == 1:
        return choices[0]
    if len(choices) == 2:
        return f"{choices[0]} or {choices[1]}"
    return f"{', '.join(choices[:-1])}, or {choices[-1]}"
