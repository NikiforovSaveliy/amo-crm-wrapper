from dataclasses import is_dataclass, asdict
from typing import Dict, Generic, Type, MutableMapping, List, Union, TypedDict, Any

from typing_extensions import TypeVar

from amopy.custom_fields import CustomField
from amopy.enities.base import BaseEntity
from amopy.utils import get_custom_field_for_entity, get_body_field_for_entity

EntityType = TypeVar("EntityType", bound=Type[BaseEntity])


class CustomFieldDict(TypedDict):
    field_id: Union[int, None]
    values: List[Dict]


class NotDeclaredEntityFieldError(Exception):

    def __init__(self, entity: EntityType, field_name: str):
        super().__init__("%s is not declared as entity field" % field_name, entity)


class AmoRequestCustomFieldsMutableMapping(MutableMapping):
    """
    Позволяет получить значение полей по ID
    """

    def __init__(
        self,
        custom_fields_values=None,
    ):
        if custom_fields_values is None:
            custom_fields_values = []
        self._custom_fields_values_by_field_id = {
            custom_field["field_id"]: custom_field
            for custom_field in custom_fields_values
        }

    def __setitem__(self, field_id: int, values: List[Dict]) -> None:
        self._custom_fields_values_by_field_id[field_id] = CustomFieldDict(
            field_id=field_id, values=values
        )

    def __delitem__(self, field_id: int):
        del self._custom_fields_values_by_field_id[field_id]

    def __getitem__(self, field_id: int) -> List[Dict]:
        return self._custom_fields_values_by_field_id[field_id]["values"]

    def __len__(self):
        return len(self._custom_fields_values_by_field_id)

    def __iter__(self):
        return iter(self._custom_fields_values_by_field_id)

    @property
    def data(self):
        return list(self._custom_fields_values_by_field_id.values())


def build_value_object(data: List[Dict], field: CustomField):
    values = data
    value_objects = [field.value_object(**value) for value in values]
    return value_objects if field.many else value_objects[0]


def serialize_custom_field(value, field: CustomField) -> List[Dict]:
    values = [value]
    if isinstance(value, list):
        values = value

    result = []
    for value in values:
        if is_dataclass(value):
            result.append(asdict(value))
        else:
            # Плохо пиздец
            result.append(asdict(field.value_object(value)))
    return result


class EntitySerializer:

    def __init__(self, entity_type: Generic[EntityType]):
        self._entity_type = entity_type
        self._entity_custom_fields = get_custom_field_for_entity(entity_type)
        self._entity_body_fields = get_body_field_for_entity(entity_type)

    def from_response(self, data: Dict) -> EntityType:
        """
        Де-сериализация из представления АМО
        :param data: словарь сущности в представлении АМО
        :return:
        """
        initial_state = {}
        initial_state.update(self.get_custom_fields_for_initial_state(data))
        initial_state.update(self.get_body_fields_for_initial_state(data))
        return self._entity_type(**initial_state)

    def get_custom_fields_for_initial_state(self, data: Dict) -> Dict[str, Any]:
        custom_fields_values_mapping = AmoRequestCustomFieldsMutableMapping(
            data.get("custom_fields_values")
        )
        result = {}

        for attr, field in self._entity_custom_fields.items():
            values = custom_fields_values_mapping.get(field.field_id)
            value_object = build_value_object(data=values, field=field)
            result[attr] = value_object.get_value()

        return result

    def get_body_fields_for_initial_state(self, data: Dict) -> Dict[str, Any]:
        return {
            attr: data.get(field.source)
            for attr, field in self._entity_body_fields.items()
        }

    def to_response(self, entity_instance: Generic[EntityType]) -> Dict:
        """
        Сериализация в представление АМО
        :param entity_instance: экземпляр Сущности
        :return:
        """
        serialized = dict(
            custom_fields_values=self.serialize_custom_fields(entity_instance)
        )
        serialized.update(self.serialize_body_fields(entity_instance))
        return serialized

    def serialize_body_fields(self, entity: EntityType):
        return {
            field.source: getattr(entity, attr, None)
            for attr, field in self._entity_body_fields.items()
        }

    def serialize_custom_fields(self, entity: EntityType):
        custom_fields_mapping = AmoRequestCustomFieldsMutableMapping()

        for attr, field in self._entity_custom_fields.items():
            value = getattr(entity, attr, None)
            custom_fields_mapping[field.field_id] = serialize_custom_field(value, field)

        return custom_fields_mapping.data
