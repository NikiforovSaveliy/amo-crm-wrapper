from typing import (
    TYPE_CHECKING,
    Dict,
    get_type_hints,
    get_args,
    TypeVar,
    Generic,
)

from amopy.body_fields import BodyField
from amopy.custom_fields import CustomField

if TYPE_CHECKING:
    from amopy.serializers import EntityType


def filter_dict_by_class(data: Dict, klass):
    return {key: value for key, value in data.items() if isinstance(value, klass)}


T = TypeVar("T")


def get_fields_for_entity(
    entity: "EntityType", field_klass: Generic[T]
) -> Dict[str, T]:
    type_hints = get_type_hints(entity, include_extras=True)

    attr_class_annotations = {}
    for attr, annotation in type_hints.items():
        actual_type, annotated_class = get_args(annotation)
        attr_class_annotations[attr] = annotated_class

    attr_class_annotations = filter_dict_by_class(attr_class_annotations, field_klass)
    return attr_class_annotations


def get_custom_field_for_entity(entity: "EntityType") -> Dict[str, CustomField]:
    return get_fields_for_entity(entity, CustomField)


def get_body_field_for_entity(entity: "EntityType") -> Dict[str, BodyField]:
    return get_fields_for_entity(entity, BodyField)
