from dataclasses import dataclass, field
from typing import Union, List, Literal, Any, Optional

from amopy.exceptions import DataclassFieldRequiredError
from amopy.objects.values import TextValue, BooleanValue, EnumValue, DateTimeValue


@dataclass
class BaseCustomFieldObject:

    field_type: str
    values: List[Any] = field(default_factory=list)
    field_id: Union[int, None] = None
    field_code: Union[str, None] = None
    field_name: Optional[str] = None

    def __post_init__(self):
        if not any([self.field_id, self.field_code]):
            raise DataclassFieldRequiredError("`field_id` or `field_code` must be set`")


@dataclass
class TextCustomFieldObject(BaseCustomFieldObject):
    field_type: Literal["text"]
    values: List[TextValue] = field(default_factory=list)


@dataclass
class NumericCustomFieldObject(BaseCustomFieldObject):
    field_type: Literal["numeric"]
    values: List[TextValue] = field(default_factory=list)


@dataclass
class CheckboxCustomFieldObject(BaseCustomFieldObject):
    field_type: Literal["checkbox"]
    values: List[BooleanValue] = field(default_factory=list)


@dataclass
class SelectCustomFieldObject(BaseCustomFieldObject):
    field_type: Literal["select", "multiselect", "radiobutton", "multitext"]  # noqa
    values: List[EnumValue] = field(default_factory=list)


@dataclass
class DateTimeCustomFieldObject(BaseCustomFieldObject):
    field_type: Literal["data", "birthday", "date_time"]
    values: List[DateTimeValue] = field(default_factory=list)
