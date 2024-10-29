from dataclasses import dataclass
from typing import Union, TYPE_CHECKING

from amopy.objects.types import ValueType

if TYPE_CHECKING:
    from amopy.types import EntityType


@dataclass(frozen=True)
class BodyField:
    """
    :ivar alias: Название поля, которое располагается НЕ в custom_fields_valuesi
    :ivar changeable: Можно ли изменять значение поля
    """

    alias: str
    changeable: bool = False


class FieldDeclarationError(Exception):
    pass


@dataclass(frozen=True)
class CustomField:
    """
    :ivar target_object: Объект, который используется для хранения значения.
    :ivar field_id: ID поля
    :ivar field_code: Буквенный идентификатор поля
    :ivar use_object: Использовать исходный объект, вместо преобразования
    """

    target_object: ValueType
    field_id: Union[int, None] = None
    field_code: Union[str, None] = None
    use_object = True

    def __post_init__(self):
        if self.field_id is None and self.field_code is None:
            raise FieldDeclarationError("field_id or field_code must be set")


@dataclass(frozen=True)
class EmbeddedField:

    entity_type: str
    to_entity: "EntityType"

    def __post_init__(self):
        if self.entity_type != self.to_entity.entities:
            raise FieldDeclarationError(
                "entity_type and attr 'entity_type' of to_entity should be the same"
            )
