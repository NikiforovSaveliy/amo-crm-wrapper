from typing_extensions import TypeVar

from amopy.objects.custom_fields import BaseCustomFieldObject
from amopy.objects.values import BaseValue

ValueType = TypeVar("ValueType", bound=BaseValue)
CustomFieldType = TypeVar("CustomFieldType", bound=BaseCustomFieldObject)
