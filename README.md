# cli-input-validator

Small, reusable helpers for validating interactive command-line input in Python.

## Installation

```bash
pip install cli-input-validator
```

## Usage

Prompt until a user enters one of the allowed choices:

```python
from cli_input_validator import get_valid_choice

answer = get_valid_choice(["yes", "no"], "Continue? ")
```

Build a custom validator:

```python
from cli_input_validator import VALID, get_validated_input


def positive_number(value):
    if value.isdigit() and int(value) > 0:
        return VALID
    return False, "Enter a positive whole number: "


number = get_validated_input(positive_number)("Number: ")
```

Validate a name containing letters, spaces, or hyphens:

```python
from cli_input_validator import verify_name_integrity

name = verify_name_integrity("Name: ")
```

## Development

```bash
python -m pip install -e ".[test]"
pytest
```
