from typing import List, Union, Dict, Iterable, Tuple, Any, get_args, get_origin

from amopy.fields import BodyField, CustomField
from amopy.objects.factories import init_list_custom_field_object
from amopy.objects.types import CustomFieldType


def get_custom_fields_reverse_index(
    data: List[CustomFieldType],
) -> Dict[Union[str, int], CustomFieldType]:
    by_field_id = {obj.field_id: obj for obj in data}
    by_field_code = {obj.field_code: obj for obj in data}
    by_field_id.update(by_field_code)
    return by_field_id


def map_body_fields_from_dict(body_fields: Iterable[Tuple[str, Any]], data: Dict):
    result = {}

    for attr, annotation in body_fields:
        actual_type, metadata = get_args(annotation)
        result[attr] = actual_type(data.get(metadata.alias))

    return result


def map_custom_fields_from_dict(custom_fields: Iterable[Tuple[str, Any]], data: Dict):
    result = {}

    custom_fields_values = data.get("custom_fields_values", [])
    custom_fields_values = custom_fields_values or []
    custom_field_objects = init_list_custom_field_object(custom_fields_values)
    reversed_index_custom_fields = get_custom_fields_reverse_index(custom_field_objects)

    for attr, annotation in custom_fields:
        actual_type, metadata = get_args(annotation)

        ident = metadata.field_id or metadata.field_code
        custom_field_object = reversed_index_custom_fields.get(ident, None)
        origin = get_origin(actual_type)

        if custom_field_object is None:
            result[attr] = [] if origin is list else None
            continue

        value = custom_field_object.values[0]
        if origin is list:
            value = custom_field_object.values

        result[attr] = value.value
        if metadata.use_object:
            result[attr] = value
    return result


def is_body_field(annotation: Tuple[str, Any]) -> bool:
    return is_annotated_subclasses(annotation, BodyField)


def is_annotated_subclasses(annotation, metadata_class):
    attr_name, annotated = annotation
    actual_type, metadata = get_args(annotated)
    return issubclass(type(metadata), metadata_class)


def is_custom_field(annotation: Tuple[str, Any]) -> bool:
    return is_annotated_subclasses(annotation, CustomField)


def map_fields_from_dict(annotations: Dict[str, Any], data: Dict) -> Dict[str, Any]:
    body_fields = list(filter(is_body_field, annotations.items()))
    custom_fields = list(
        filter(
            is_custom_field,
            annotations.items(),
        )
    )

    result = {}
    result.update(map_body_fields_from_dict(body_fields, data))
    result.update(map_custom_fields_from_dict(custom_fields, data))

    return result
