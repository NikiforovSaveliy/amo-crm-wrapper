from dataclasses import dataclass, fields
from typing import get_origin, Literal, get_args, List, Any, Union

from amopy.exceptions import DataclassValidationError


def validate_literal(value: Any, expected_type):
    if value not in get_args(expected_type):
        raise DataclassValidationError(
            "Value should be a literal type: %s, but got %s"
            % (value, get_args(expected_type))
        )


def validate_union(value, expected_type):
    expected_types = get_args(expected_type)
    if not isinstance(value, expected_types):
        raise DataclassValidationError(
            "Expected %s type, but got %s instead with value %s"
            % (expected_types, type(value), value)
        )


def validate_list(value: List[Any], expected_type):
    expected_types = get_args(expected_type)
    for val in value:
        if not isinstance(val, expected_types):
            raise DataclassValidationError(
                "Expected %s types, but got %s instead with value %s"
                % (expected_types, type(value), value)
            )


def validate_type_of_value(value, expected_type):
    if get_origin(expected_type) is Literal:
        validate_literal(value, expected_type)
        return

    if get_origin(expected_type) is list:
        validate_list(value, expected_type)

    if get_origin(expected_type) is Union:
        validate_union(value, expected_type)

    if isinstance(expected_type, type):
        if not isinstance(value, expected_type):
            raise DataclassValidationError(
                "Expected %s type, but got %s instead with value %s"
                % (expected_type, type(value), value)
            )


@dataclass
class TypeValidationMixin:
    """
    Глупый миксин, который проверяет только builtin типы
    """

    def __post_init__(self, *args, **kwargs):

        for field in fields(self):
            validate_type_of_value(getattr(self, field.name), field.type)
