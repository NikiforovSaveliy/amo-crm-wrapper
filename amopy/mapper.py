from typing import (
    Dict,
    Type,
    get_type_hints,
    Generic,
)

from amopy.types import EntityType
from amopy.utils import map_fields_from_dict


class BaseMapper:

    def __init__(self, entity_class: Type[EntityType]):
        self._entity = entity_class

    def from_dict(self, data: Dict) -> EntityType:
        """
        Создает экземпляр сущности на основании ответа от AMOCrm
        :param data:
        :return:
        """
        attrs = map_fields_from_dict(
            get_type_hints(self._entity, include_extras=True), data
        )
        entity_instance = self._entity(**attrs)
        return entity_instance

    def to_dict(self, entity: Generic[EntityType]) -> Dict:
        """
        Конвертирует экземпляр для отправки в AMOCrm
        :param entity:
        :return:
        """
        type_hints = get_type_hints(self._entity, include_extras=True)
        result = {}

        return result
