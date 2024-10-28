from abc import abstractmethod
from typing import TypeVar

from amopy.objects.custom_fields import BaseCustomFieldObject


class BaseEntity:

    @property
    @abstractmethod
    def entity_type(self):
        pass


EntityType = TypeVar("EntityType", bound=BaseEntity)


class LeadEntity(BaseCustomFieldObject):
    entity_type = "leads"
