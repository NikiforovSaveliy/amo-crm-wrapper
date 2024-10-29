from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Union, Optional, TypeVar

from amopy.exceptions import DataclassValidationError
from amopy.objects.custom_fields import (
    TextCustomFieldObject,
    NumericCustomFieldObject,
    CheckboxCustomFieldObject,
    SelectCustomFieldObject,
    DateTimeCustomFieldObject,
)
from amopy.objects.embedded import EmbeddedContact, EmbeddedLead, EmbeddedCompany
from amopy.objects.mixins import TypeValidationMixin


# TODO: Добавить {{EntityName}}CreateObject
def cast_datetime(value: Union[str, datetime, int, float]) -> datetime:
    try:
        if isinstance(value, datetime):
            return value
        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(value)
        if isinstance(value, str):
            return datetime.fromisoformat(value)
    except ValueError as error:
        raise DataclassValidationError("Failed to cast datetime format: %s" % error)


@dataclass
class TagObject(TypeValidationMixin):
    id: int
    name: str
    color: Optional[str] = None
    request_id: Optional[str] = None


@dataclass
class EmbeddedObject(TypeValidationMixin):

    leads: List[EmbeddedLead] = field(default_factory=list)
    contacts: List[EmbeddedContact] = field(default_factory=list)
    # Теги всегда работают как самостоятельные сущности
    tags: List[TagObject] = field(default_factory=list)
    companies: List[EmbeddedCompany] = field(default_factory=list)


@dataclass
class BaseEntityObject(TypeValidationMixin):
    id: int
    created_by: int
    updated_by: int
    created_at: datetime
    updated_at: datetime
    custom_fields_values: List[
        Union[
            TextCustomFieldObject,
            NumericCustomFieldObject,
            CheckboxCustomFieldObject,
            SelectCustomFieldObject,
            DateTimeCustomFieldObject,
        ]
    ]
    account_id: int
    embedded: Optional[EmbeddedObject]

    def __post_init__(self) -> None:
        self.created_at = cast_datetime(self.created_at)
        self.updated_at = cast_datetime(self.updated_at)
        super().__post_init__()


ObjectType = TypeVar("ObjectType", bound=BaseEntityObject)


@dataclass
class LeadObject(BaseEntityObject):
    name: str
    price: int
    responsible_user_id: int
    group_id: int
    status_id: int
    pipeline_id: int
    loss_reason_id: int
    closed_at: datetime
    is_deleted: bool
    score: Union[int, None]
    is_price_modified_by_robot: bool
    embedded: EmbeddedObject
    source_id: Optional[int] = None
    labor_cost: Optional[int] = None
    closest_task_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        self.closed_at = cast_datetime(self.closed_at)
        self.closest_task_at = cast_datetime(self.closest_task_at)
        super().__post_init__()


@dataclass
class ContactObject(BaseEntityObject):
    # Контакт можно собрать пустым объектом
    name: str
    first_name: Optional[str]
    last_name: Optional[str]
    responsible_user_id: int
    group_id: int
    created_by: int
    updated_by: int
    created_at: datetime
    updated_at: Optional[datetime]
    closest_task_at: Optional[datetime]

    def __post_init__(self) -> None:
        self.closest_task_at = cast_datetime(self.closest_task_at)
        super().__post_init__()


@dataclass
class CatalogItem(BaseEntityObject):
    # name - обязательное полей
    catalog_id: int
    name: str


# TODO: Создать модель компании. При создании обязательных полей нет; Аналогичны контактам
