from dataclasses import dataclass
from datetime import datetime
from typing import (
    Optional,
    Union,
    Literal,
    Any,
)

from amopy.exceptions import DataclassValidationError, DataclassFieldRequiredError
from amopy.objects.mixins import TypeValidationMixin


class BaseValue:
    value: Any


@dataclass
class TextValue(BaseValue, TypeValidationMixin):
    value: str


@dataclass
class BooleanValue(BaseValue, TypeValidationMixin):
    value: bool


@dataclass
class DateTimeValue(BaseValue, TypeValidationMixin):
    value: datetime

    def __init__(self, value: Union[datetime, str, int, float]):
        try:
            if isinstance(value, datetime):
                self.value = value
            if isinstance(value, str):
                self.value = datetime.fromisoformat(value)
            if isinstance(value, (int, float)):
                self.value = datetime.fromtimestamp(value)
        except ValueError:
            raise DataclassValidationError("Can't parse datetime value: %s" % value)


@dataclass
class EnumValue(BaseValue, TypeValidationMixin):
    value: Union[str, None] = None
    enum_id: Union[int, None] = None
    enum_code: Union[str, None] = None

    def __post_init__(self):
        if not any([self.value, self.enum_id, self.enum_code]):
            raise DataclassFieldRequiredError(
                "`value` or `enum_id` or `enum_code` must be set"
            )
        super().__post_init__()


@dataclass
class LegalEntityValue(BaseValue, TypeValidationMixin):
    name: str
    entity_type: Optional[int] = None
    vat_id: Optional[str] = None
    tax_registration_reason_code: Optional[int] = None
    address: Optional[str] = None
    kpp: Optional[str] = None
    external_uid: Optional[str] = None

    def __post_init__(self):
        if self.name is None:
            raise DataclassFieldRequiredError("`name` should not be set")
        super().__post_init__()


@dataclass
class LinkedEntityValue(BaseValue, TypeValidationMixin):
    """
    Аналогично при привязке, только это поле.
    """

    name: str
    entity_id: int
    entity_type: Literal["catalog_elements", "contacts", "companies"]
    catalog_id: Optional[int] = None
