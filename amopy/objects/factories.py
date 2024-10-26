from typing import get_args, Dict, Type, List

from amopy.exceptions import DataclassValidationError
from amopy.objects.custom_fields import (
    BaseCustomFieldObject,
    TextCustomFieldObject,
    NumericCustomFieldObject,
    CheckboxCustomFieldObject,
    SelectCustomFieldObject,
    DateTimeCustomFieldObject,
)
from amopy.objects.embedded import EmbeddedLead, EmbeddedContact, EmbeddedCompany
from amopy.objects.entities import LeadObject, EmbeddedObject, TagObject, ContactObject
from amopy.objects.types import CustomFieldType

custom_field_type_registry: Dict[str, Type[BaseCustomFieldObject]] = {
    "text": TextCustomFieldObject,
    "numeric": NumericCustomFieldObject,
    "checkbox": CheckboxCustomFieldObject,
    "select": SelectCustomFieldObject,
    "multiselect": SelectCustomFieldObject,
    "radiobutton": SelectCustomFieldObject,
    "data": DateTimeCustomFieldObject,
    "birthday": DateTimeCustomFieldObject,
    "date_time": DateTimeCustomFieldObject,
    "multitext": SelectCustomFieldObject,
}


def init_custom_field_object(data: dict) -> CustomFieldType:
    """
    Создает объект и инициализирует вложенные типы полей
    :param data: элемент из списка custom_fields_values
    :return:
    """

    if "field_type" not in data:
        raise DataclassValidationError("field_type is required")
    field_type = data.get("field_type")

    if field_type not in custom_field_type_registry:
        raise DataclassValidationError("%s Field type is not supported" % field_type)

    field_class = custom_field_type_registry.get(field_type)
    field_class_annotations = field_class.__annotations__
    value_type_annotation = field_class_annotations.get("values")
    value_class = get_args(value_type_annotation)[0]

    value_instances = [value_class(**obj) for obj in data.pop("values")]

    return field_class(values=value_instances, **data)  # noqa


def init_list_custom_field_object(data: list[dict]) -> List[CustomFieldType]:
    return [init_custom_field_object(data) for data in data]


def init_embedded_object(data: dict) -> EmbeddedObject:
    embedded_contacts = [
        EmbeddedContact(id=obj["id"], is_main=obj["is_main"])
        for obj in data.get("contacts", [])
    ]
    embedded_companies = [
        EmbeddedCompany(obj["id"]) for obj in data.get("companies", [])
    ]
    tags = [TagObject(**obj) for obj in data.get("tags", [])]
    embedded_leads = [EmbeddedLead(obj["id"]) for obj in data.get("leads", [])]
    return EmbeddedObject(
        leads=embedded_leads,
        contacts=embedded_contacts,
        companies=embedded_companies,
        tags=tags,
    )


def init_lead_object(data: dict):
    embedded_data = data.pop("_embedded", {})
    custom_fields_data = data.pop("custom_fields_values", [])
    custom_fields_data = custom_fields_data if custom_fields_data else []

    embedded = init_embedded_object(embedded_data)
    custom_fields_values = init_list_custom_field_object(custom_fields_data)

    return LeadObject(
        **data, custom_fields_values=custom_fields_values, embedded=embedded
    )


def init_contact_object(data: dict) -> ContactObject:
    embedded_data = data.pop("_embedded", {})
    custom_fields_data = data.pop("custom_fields_values", [])
    custom_fields_data = custom_fields_data if custom_fields_data else []

    embedded = init_embedded_object(embedded_data)
    custom_fields_values = init_list_custom_field_object(custom_fields_data)

    return ContactObject(
        **data, custom_fields_values=custom_fields_values, embedded=embedded
    )
