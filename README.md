# cli-input-validator

[![CI](https://github.com/VanPaitin/cli-input-validator/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/VanPaitin/cli-input-validator/actions/workflows/pylint.yml)
[![Downloads](https://static.pepy.tech/badge/cli-input-validator)](https://pepy.tech/project/cli-input-validator)

Small, reusable helpers for validating interactive command-line input in Python.
The package repeatedly prompts until the user enters a valid value, while
letting you control the validation rules, error messages, and input function.

## Installation

Add it to a project managed by `uv`:

```bash
uv add cli-input-validator
```

Or install it with `pip`:

```bash
python -m pip install cli-input-validator
```

## Quick start

Prompt until a user enters one of the allowed choices:

```python
from cli_input_validator import get_valid_choice

answer = get_valid_choice(["yes", "no"], "Continue? ")
```

`get_valid_choice()` is case-insensitive by default, so `YES`, `Yes`, and
`yes` are all accepted. It returns the value exactly as the user entered it.

## Custom validators

A validator receives the user's input and returns a tuple containing:

- A Boolean indicating whether the input is valid.
- An error message to use as the next prompt when the input is invalid.

Use the exported `VALID` result for successful validation:

```python
from cli_input_validator import VALID, get_validated_input


def positive_number(value):
    if value.isdigit() and int(value) > 0:
        return VALID
    return False, "Enter a positive whole number: "


get_positive_number = get_validated_input(positive_number)
number = get_positive_number("Number: ")
```

If the user enters `zero`, the validator's error message becomes the next
prompt. Validation continues until the validator returns `(True, None)`.
The accepted value is returned as a string.

Each validator controls its own error message, so different rules can provide
specific guidance:

```python
def username_validator(value):
    if len(value) < 3:
        return False, "Username must contain at least 3 characters: "
    if not value.isalnum():
        return False, "Username must contain only letters and numbers: "
    return True, None
```

## Custom input functions

By default, prompts are read with Python's built-in `input()`. You can pass any
callable that accepts a prompt and returns a string. For example, use
`getpass.getpass` when the entered value should not be displayed:

```python
from getpass import getpass

from cli_input_validator import VALID, get_validated_input


def password_validator(value):
    if len(value) >= 8:
        return VALID
    return False, "Password must contain at least 8 characters: "


password = get_validated_input(
    password_validator,
    input_function=getpass,
)("Password: ")
```

Third-party prompt functions work the same way. For example, after installing
`maskpass`, its masked `askpass()` function can be supplied directly:

```python
from maskpass import askpass

from cli_input_validator import get_validated_input

password = get_validated_input(
    password_validator,
    input_function=askpass,
)("Password: ")
```

`maskpass` is optional and is not installed with `cli-input-validator`.

## Valid choices

`get_valid_choice()` accepts any iterable of strings and generates its own
error prompt from the available choices:

```python
from cli_input_validator import get_valid_choice

difficulty = get_valid_choice(
    ["easy", "medium", "hard"],
    "Difficulty: ",
)
```

Matching is case-insensitive by default. Set `case_sensitive=True` when letter
case is significant:

```python
confirmation = get_valid_choice(
    ["YES", "NO"],
    "Type YES or NO: ",
    case_sensitive=True,
)
```

A custom input function can also be supplied:

```python
answer = get_valid_choice(
    ["yes", "no"],
    "Continue? ",
    input_function=my_prompt_function,
)
```

Passing an empty collection of choices raises `ValueError`.

## Valid names

`get_valid_name()` prompts until the user enters a non-empty name containing
only letters, spaces, or hyphens:

```python
from cli_input_validator import get_valid_name

name = get_valid_name("Name: ")
```

It also accepts a custom input function:

```python
name = get_valid_name("Name: ", input_function=my_prompt_function)
```

Use `name_validator()` directly when you need to validate a value without
prompting:

```python
from cli_input_validator import name_validator

valid, error = name_validator("Anne-Marie")
```

To use different name rules or a custom error message, create your own
validator and pass it to `get_validated_input()`.

## API overview

- `get_validated_input(is_valid=None, input_function=None)` creates a reusable
  prompting function from a validator.
- `get_valid_choice(choices, prompt="", case_sensitive=False,
input_function=None)` prompts for one of a collection of values.
- `get_valid_name(prompt, input_function=None)` prompts for a supported name.
- `name_validator(name)` validates a name without prompting.
- `VALID` is the convenience result `(True, None)`.

## Development

```bash
python -m pip install -e ".[test]"
pytest
```
